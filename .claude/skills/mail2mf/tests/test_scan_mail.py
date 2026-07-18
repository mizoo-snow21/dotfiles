import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import scan_mail


class TestAmounts(unittest.TestCase):
    def test_yen_symbol_and_suffix(self):
        text = "ご請求額 ¥12,345 (税込)。前回 5000円 でした。¥12,345"
        self.assertEqual(scan_mail.extract_amounts(text), [12345, 5000])

    def test_bounds_and_noise(self):
        self.assertEqual(scan_mail.extract_amounts("3円 999999999999円 no amounts"), [])


class TestState(unittest.TestCase):
    def test_roundtrip_and_default(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "state.json")
            st = scan_mail.load_state(p)
            self.assertEqual(
                st,
                {
                    "last_scan": None,
                    "pending": {},
                    "uploaded": {},
                    "failed": {},
                    "discarded": {},
                },
            )
            st["pending"]["k"] = {"subject": "s"}
            scan_mail.save_state(st, p)
            self.assertEqual(scan_mail.load_state(p)["pending"]["k"]["subject"], "s")
            self.assertFalse(os.path.exists(p + ".tmp"))


class TestNaming(unittest.TestCase):
    def test_attachment_key_includes_index(self):
        self.assertEqual(scan_mail.attachment_key("<m@x>", 2, "a.pdf"), "<m@x>/2-a.pdf")

    def test_final_name_unique_per_key(self):
        n1 = scan_mail.final_name(
            "<m@x>/1-a.pdf",
            "2026-07-01T10:00:00+09:00",
            "Shop <no-reply@shop.jp>",
            "a.pdf",
        )
        n2 = scan_mail.final_name(
            "<m@x>/2-a.pdf",
            "2026-07-01T10:00:00+09:00",
            "Shop <no-reply@shop.jp>",
            "a.pdf",
        )
        self.assertNotEqual(n1, n2)
        self.assertTrue(n1.startswith("20260701_shop.jp_a_"))
        self.assertTrue(n1.endswith(".pdf"))

    def test_final_name_sanitizes(self):
        n = scan_mail.final_name("k", "", "??", "領収書 (7月)?.PDF")
        self.assertNotIn(" ", n)
        self.assertNotIn("?", n)
        self.assertTrue(n.endswith(".pdf"))


class TestBuildCandidates(unittest.TestCase):
    def _msg(self, mid="<m@x>", atts=None):
        return {
            "message_id": mid,
            "date": "2026-07-01T10:00:00+09:00",
            "sender": "Shop <no-reply@shop.jp>",
            "subject": "領収書 ¥1,000",
            "body_preview": "合計 1,000円",
            "pdf_attachments": atts or [{"index": 1, "name": "r.pdf"}],
        }

    def test_new_message_becomes_pending_candidate(self):
        st = scan_mail.load_state("/nonexistent/state.json")
        pending, cands = scan_mail.build_candidates(st, [self._msg()])
        self.assertEqual(list(pending), ["<m@x>/1-r.pdf"])
        self.assertEqual(cands[0]["status"], "new")
        self.assertEqual(cands[0]["amounts"], [1000])

    def test_uploaded_and_permanent_failed_are_skipped(self):
        st = {
            "last_scan": None,
            "pending": {},
            "uploaded": {"<m@x>/1-r.pdf": {"file_id": "F"}},
            "failed": {"<old>/1-x.pdf": {"error": "HTTP 413", "permanent": True}},
        }
        pending, cands = scan_mail.build_candidates(st, [self._msg()])
        self.assertEqual(pending, {})
        self.assertEqual(cands, [])

    def test_discarded_keys_are_not_rediscovered(self):
        st = {
            "last_scan": None,
            "pending": {},
            "uploaded": {},
            "failed": {},
            "discarded": {"<m@x>/1-r.pdf": {"at": "t"}},
        }
        pending, cands = scan_mail.build_candidates(st, [self._msg()])
        self.assertEqual(pending, {})
        self.assertEqual(cands, [])

    def test_pending_and_failed_are_relisted(self):
        st = {
            "last_scan": None,
            "pending": {
                "<p>/1-a.pdf": {
                    "subject": "s",
                    "sender": "x@y.jp",
                    "date": "d",
                    "amounts": [],
                }
            },
            "uploaded": {},
            "failed": {"<f>/1-b.pdf": {"error": "HTTP 500", "at": "t"}},
        }
        _, cands = scan_mail.build_candidates(st, [])
        statuses = {c["key"]: c["status"] for c in cands}
        self.assertEqual(
            statuses, {"<p>/1-a.pdf": "pending_retry", "<f>/1-b.pdf": "failed_retry"}
        )


class TestMarkDiscard(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.dir.name, "state.json")
        st = scan_mail.load_state(self.path)
        st["pending"]["k1"] = {
            "subject": "s",
            "sender": "x",
            "date": "d",
            "amounts": [],
        }
        scan_mail.save_state(st, self.path)

    def tearDown(self):
        self.dir.cleanup()

    def test_mark_uploaded_moves_entry(self):
        scan_mail.main(
            ["mark", "--state", self.path, "--key", "k1", "--uploaded", "FILE9"]
        )
        st = scan_mail.load_state(self.path)
        self.assertNotIn("k1", st["pending"])
        self.assertEqual(st["uploaded"]["k1"]["file_id"], "FILE9")

    def test_mark_failed_permanent(self):
        scan_mail.main(
            [
                "mark",
                "--state",
                self.path,
                "--key",
                "k1",
                "--failed",
                "HTTP 413",
                "--permanent",
            ]
        )
        st = scan_mail.load_state(self.path)
        self.assertTrue(st["failed"]["k1"]["permanent"])

    def test_discard_removes_pending_and_leaves_tombstone(self):
        scan_mail.main(["discard", "--state", self.path, "k1"])
        st = scan_mail.load_state(self.path)
        self.assertNotIn("k1", st["pending"])
        self.assertNotIn("k1", st["failed"])
        self.assertIn("k1", st["discarded"])

    def test_mark_failed_preserves_amounts_for_retry(self):
        st = scan_mail.load_state(self.path)
        st["pending"]["k1"]["amounts"] = [1000]
        scan_mail.save_state(st, self.path)
        scan_mail.main(
            ["mark", "--state", self.path, "--key", "k1", "--failed", "HTTP 500"]
        )
        st = scan_mail.load_state(self.path)
        _, cands = scan_mail.build_candidates(st, [])
        retry = next(c for c in cands if c["key"] == "k1")
        self.assertEqual(retry["status"], "failed_retry")
        self.assertEqual(retry["amounts"], [1000])


if __name__ == "__main__":
    unittest.main()
