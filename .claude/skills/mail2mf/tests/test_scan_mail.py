import datetime
import json
import os
import sqlite3
import sys
import tempfile
import unittest
from unittest import mock

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
            self.assertEqual(st, {"last_scan": None, "pending": {}, "uploaded": {},
                                  "failed": {}, "discarded": {}, "sources": {},
                                  "skipped": {}})
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


def _make_emlx(path, headers, parts):
    """parts: [(content_type, filename|None, payload_bytes|None, extra_headers_str)]"""
    lines = []
    boundary = "BOUNDARY123"
    lines.append("From: %s" % headers.get("From", "a@b.jp"))
    lines.append("Subject: %s" % headers.get("Subject", "sub"))
    if headers.get("Message-ID"):
        lines.append("Message-ID: %s" % headers["Message-ID"])
    lines.append('Content-Type: multipart/mixed; boundary="%s"' % boundary)
    lines.append("")
    for ct, fn, payload, extra in parts:
        lines.append("--%s" % boundary)
        disp = ('; name="%s"' % fn) if fn else ""
        lines.append("Content-Type: %s%s" % (ct, disp))
        if fn:
            lines.append('Content-Disposition: attachment; filename="%s"' % fn)
        if payload is not None:
            import base64
            lines.append("Content-Transfer-Encoding: base64")
            lines.append("")
            lines.append(base64.b64encode(payload).decode())
        else:
            if extra:
                lines.append(extra)
            lines.append("")
        lines.append("")
    lines.append("--%s--" % boundary)
    body = ("\r\n".join(lines)).encode()
    blob = ("%d\n" % len(body)).encode() + body
    with open(path, "wb") as f:
        f.write(blob)


class TestEnvelopeIndex(unittest.TestCase):
    def _db(self, d):
        p = os.path.join(d, "Envelope Index")
        c = sqlite3.connect(p)
        c.executescript("""
          CREATE TABLE messages(ROWID INTEGER PRIMARY KEY, sender INTEGER, subject INTEGER,
                                date_received INTEGER, deleted INTEGER DEFAULT 0);
          CREATE TABLE attachments(ROWID INTEGER PRIMARY KEY, message INTEGER, name TEXT);
          CREATE TABLE addresses(ROWID INTEGER PRIMARY KEY, address TEXT, comment TEXT DEFAULT '');
          CREATE TABLE subjects(ROWID INTEGER PRIMARY KEY, subject TEXT);
        """)
        c.execute("INSERT INTO addresses VALUES(1,'shop@x.jp','')")
        c.execute("INSERT INTO subjects VALUES(1,'領収書 ¥1,000')")
        # in range + pdf
        c.execute("INSERT INTO messages VALUES(10,1,1,2000,0)")
        c.execute("INSERT INTO attachments VALUES(1,10,'r.pdf')")
        # in range, non-pdf only -> excluded
        c.execute("INSERT INTO messages VALUES(11,1,1,2000,0)")
        c.execute("INSERT INTO attachments VALUES(2,11,'note.txt')")
        # out of range -> excluded
        c.execute("INSERT INTO messages VALUES(12,1,1,500,0)")
        c.execute("INSERT INTO attachments VALUES(3,12,'old.pdf')")
        # deleted -> excluded
        c.execute("INSERT INTO messages VALUES(13,1,1,2000,1)")
        c.execute("INSERT INTO attachments VALUES(4,13,'del.pdf')")
        c.commit(); c.close()
        return p

    def test_query_returns_attachment_messages_in_range(self):
        with tempfile.TemporaryDirectory() as d:
            p = self._db(d)
            conn = scan_mail.open_envelope_index(p)
            rows = scan_mail.query_attachment_messages(conn, 1000)
            conn.close()
            # 添付ありで in-range・非 deleted の 10(r.pdf)と 11(note.txt)を返す。
            # PDF かどうかの判定は後段の pdf_parts(.emlx の MIME)で行うためここでは絞らない。
            # 12(範囲外)・13(deleted)は除外。
            self.assertEqual(sorted(r["rowid"] for r in rows), [10, 11])
            by_id = {r["rowid"]: r for r in rows}
            self.assertEqual(by_id[10]["sender"], "shop@x.jp")
            self.assertEqual(by_id[10]["subject"], "領収書 ¥1,000")
            self.assertNotIn("pdf_names", by_id[10])

    def test_open_missing_db_exits_with_fda_hint(self):
        with self.assertRaises(SystemExit) as cm:
            scan_mail.open_envelope_index("/nonexistent/Envelope Index")
        self.assertIn("フルディスクアクセス", str(cm.exception))


class TestEmlx(unittest.TestCase):
    def test_build_index_prefers_full(self):
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "A/Messages"))
            os.makedirs(os.path.join(d, "B/Messages"))
            open(os.path.join(d, "A/Messages/10.partial.emlx"), "w").close()
            open(os.path.join(d, "B/Messages/10.emlx"), "w").close()
            open(os.path.join(d, "A/Messages/11.partial.emlx"), "w").close()
            idx = scan_mail.build_emlx_index(d)
            self.assertTrue(idx["10"].endswith("10.emlx"))          # full 優先
            self.assertTrue(idx["11"].endswith("11.partial.emlx"))  # partial のみ

    def test_read_parse_and_pdf_parts(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "10.emlx")
            _make_emlx(p, {"Message-ID": "<abc@x>", "Subject": "領収書"},
                       [("text/plain", None, b"body 1,000\xef\xbc\x91", ""),
                        ("application/pdf", "r.pdf", b"%PDF-1.4 data", "")])
            msg = scan_mail.read_emlx(p)
            self.assertEqual(scan_mail.emlx_message_id(msg), "<abc@x>")
            parts = scan_mail.pdf_parts(msg)
            self.assertEqual(len(parts), 1)
            idx, name, payload = parts[0]
            self.assertEqual((idx, name), (1, "r.pdf"))
            self.assertTrue(payload.startswith(b"%PDF"))

    def test_pdf_parts_detects_partial(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "10.partial.emlx")
            _make_emlx(p, {"Message-ID": "<abc@x>"},
                       [("application/pdf", "big.pdf", None, "X-Apple-Content-Length: 999")])
            parts = scan_mail.pdf_parts(scan_mail.read_emlx(p))
            self.assertEqual(parts[0][2], None)   # payload 未 DL

    def test_message_id_fallback(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "10.emlx")
            _make_emlx(p, {}, [("application/pdf", "r.pdf", b"%PDF", "")])
            msg = scan_mail.read_emlx(p)
            self.assertTrue(scan_mail.emlx_message_id(msg).startswith("<") or
                            scan_mail.emlx_message_id(msg) == "")


class TestScanCmd(unittest.TestCase):
    def _setup(self, d):
        # 一時 Envelope Index + emlx を作り、scan_mail 定数をパッチ
        mail_root = os.path.join(d, "V10")
        os.makedirs(os.path.join(mail_root, "acct/Messages"))
        ei_dir = os.path.join(mail_root, "MailData"); os.makedirs(ei_dir)
        ei = os.path.join(ei_dir, "Envelope Index")
        c = sqlite3.connect(ei)
        c.executescript("""
          CREATE TABLE messages(ROWID INTEGER PRIMARY KEY, sender INTEGER, subject INTEGER,
                                date_received INTEGER, deleted INTEGER DEFAULT 0);
          CREATE TABLE attachments(ROWID INTEGER PRIMARY KEY, message INTEGER, name TEXT);
          CREATE TABLE addresses(ROWID INTEGER PRIMARY KEY, address TEXT, comment TEXT DEFAULT '');
          CREATE TABLE subjects(ROWID INTEGER PRIMARY KEY, subject TEXT);""")
        c.execute("INSERT INTO addresses VALUES(1,'shop@x.jp','')")
        c.execute("INSERT INTO subjects VALUES(1,'領収書 ¥1,000')")
        c.execute("INSERT INTO messages VALUES(10,1,1,2000000000,0)")
        c.execute("INSERT INTO attachments VALUES(1,10,'r.pdf')")
        c.commit(); c.close()
        _make_emlx(os.path.join(mail_root, "acct/Messages/10.emlx"),
                   {"Message-ID": "<abc@x>", "Subject": "領収書 ¥1,000"},
                   [("text/plain", None, b"body", ""),
                    ("application/pdf", "r.pdf", b"%PDF-1.4", "")])
        return mail_root, ei

    def test_scan_checkpoints_and_records_sources(self):
        with tempfile.TemporaryDirectory() as d:
            mail_root, ei = self._setup(d)
            statep = os.path.join(d, "state.json")
            saves = []
            real_save = scan_mail.save_state

            def spy(state, path=statep):
                saves.append(json.loads(json.dumps(state))); real_save(state, path)

            with mock.patch.object(scan_mail, "MAIL_ROOT", mail_root), \
                 mock.patch.object(scan_mail, "ENVELOPE_INDEX", ei), \
                 mock.patch.object(scan_mail, "save_state", side_effect=spy), \
                 mock.patch("sys.stdout"):
                scan_mail.main(["scan", "--state", statep, "--since", "2000-01-01"])
            self.assertEqual(len(saves), 2)
            self.assertIn("<abc@x>/1-r.pdf", saves[0]["pending"])
            self.assertEqual(saves[0]["sources"]["<abc@x>"], 10)
            self.assertIsNone(saves[0]["last_scan"])       # 1回目は cursor 未前進
            self.assertIsNotNone(saves[1]["last_scan"])    # 2回目で前進

    def test_scan_default_since_is_year_start(self):
        with tempfile.TemporaryDirectory() as d:
            mail_root, ei = self._setup(d)
            statep = os.path.join(d, "state.json")
            captured = {}
            real_q = scan_mail.query_attachment_messages

            def spy_q(conn, cutoff):
                captured["cutoff"] = cutoff; return real_q(conn, cutoff)

            with mock.patch.object(scan_mail, "MAIL_ROOT", mail_root), \
                 mock.patch.object(scan_mail, "ENVELOPE_INDEX", ei), \
                 mock.patch.object(scan_mail, "query_attachment_messages", side_effect=spy_q), \
                 mock.patch("sys.stdout"):
                scan_mail.main(["scan", "--state", statep])
            year_start = datetime.datetime(datetime.datetime.now().year, 1, 1)
            self.assertEqual(captured["cutoff"], int(year_start.timestamp()))

    def test_scan_missing_emlx_records_skipped_and_advances_cursor(self):
        with tempfile.TemporaryDirectory() as d:
            mail_root, ei = self._setup(d)
            # DB にだけある(添付あり)が .emlx 不在の候補。date は cutoff(2000-01-01)内
            ghost_date = 1_000_000_000  # 2001-09-09
            c = sqlite3.connect(ei)
            c.execute("INSERT INTO messages VALUES(20,1,1,?,0)", (ghost_date,))
            c.execute("INSERT INTO attachments VALUES(2,20,'ghost.pdf')")
            c.commit(); c.close()
            statep = os.path.join(d, "state.json")
            with mock.patch.object(scan_mail, "MAIL_ROOT", mail_root), \
                 mock.patch.object(scan_mail, "ENVELOPE_INDEX", ei), \
                 mock.patch("sys.stdout"), mock.patch("sys.stderr"):
                scan_mail.main(["scan", "--state", statep, "--since", "2000-01-01"])
            st = scan_mail.load_state(statep)
            self.assertIn("20", st["skipped"])
            self.assertEqual(st["skipped"]["20"]["date"], ghost_date)
            self.assertIsNotNone(st["skipped"]["20"].get("at"))
            # cursor は巻き戻さず scan_started 相当へ前進(ghost_date にピン留めされない)
            last = datetime.datetime.fromisoformat(st["last_scan"])
            self.assertGreater(last.timestamp(), ghost_date + 100_000_000)
            # 未解決は candidates/pending に出ない(解決済み 10 のみ)
            self.assertIn("<abc@x>/1-r.pdf", st["pending"])
            self.assertFalse(any("ghost" in k or k.startswith("rowid:20")
                                 for k in st["pending"]))

    def test_scan_retries_skipped_even_before_cutoff(self):
        with tempfile.TemporaryDirectory() as d:
            mail_root = os.path.join(d, "V10")
            os.makedirs(os.path.join(mail_root, "acct/Messages"))
            ei_dir = os.path.join(mail_root, "MailData"); os.makedirs(ei_dir)
            ei = os.path.join(ei_dir, "Envelope Index")
            c = sqlite3.connect(ei)
            c.executescript("""
              CREATE TABLE messages(ROWID INTEGER PRIMARY KEY, sender INTEGER, subject INTEGER,
                                    date_received INTEGER, deleted INTEGER DEFAULT 0);
              CREATE TABLE attachments(ROWID INTEGER PRIMARY KEY, message INTEGER, name TEXT);
              CREATE TABLE addresses(ROWID INTEGER PRIMARY KEY, address TEXT, comment TEXT DEFAULT '');
              CREATE TABLE subjects(ROWID INTEGER PRIMARY KEY, subject TEXT);""")
            c.execute("INSERT INTO addresses VALUES(1,'shop@x.jp','')")
            c.execute("INSERT INTO subjects VALUES(1,'旧領収書 ¥500')")
            # cutoff より古い(since=2020-01-01 では通常クエリに出ない)
            c.execute("INSERT INTO messages VALUES(20,1,1,1000,0)")
            c.execute("INSERT INTO attachments VALUES(1,20,'old.pdf')")
            c.commit(); c.close()
            _make_emlx(os.path.join(mail_root, "acct/Messages/20.emlx"),
                       {"Message-ID": "<old@x>", "Subject": "旧領収書 ¥500"},
                       [("application/pdf", "old.pdf", b"%PDF-1.4", "")])
            statep = os.path.join(d, "state.json")
            st = scan_mail.load_state(statep)
            st["skipped"]["20"] = {"date": 1000, "at": "2020-01-01T00:00:00+09:00"}
            st["last_scan"] = "2020-01-01T00:00:00+09:00"
            scan_mail.save_state(st, statep)
            with mock.patch.object(scan_mail, "MAIL_ROOT", mail_root), \
                 mock.patch.object(scan_mail, "ENVELOPE_INDEX", ei), \
                 mock.patch("sys.stdout"), mock.patch("sys.stderr"):
                scan_mail.main(["scan", "--state", statep, "--since", "2020-01-01"])
            st = scan_mail.load_state(statep)
            self.assertNotIn("20", st["skipped"])
            self.assertIn("<old@x>/1-old.pdf", st["pending"])


class TestExtractCmd(unittest.TestCase):
    def _state(self, statep, rowid=10, mid="<abc@x>"):
        st = scan_mail.load_state(statep)
        key = "%s/1-r.pdf" % mid
        st["pending"][key] = {"subject": "領収書", "sender": "shop@x.jp",
                              "date": "2026-07-01T10:00:00+09:00", "amounts": [1000]}
        st["sources"][mid] = rowid
        scan_mail.save_state(st, statep)

    def test_extract_full_saves_file(self):
        with tempfile.TemporaryDirectory() as d:
            mail_root = os.path.join(d, "V10"); os.makedirs(os.path.join(mail_root, "acct/Messages"))
            _make_emlx(os.path.join(mail_root, "acct/Messages/10.emlx"),
                       {"Message-ID": "<abc@x>"}, [("application/pdf", "r.pdf", b"%PDF-1.4 X", "")])
            statep = os.path.join(d, "state.json"); self._state(statep)
            outd = os.path.join(d, "out")
            with mock.patch.object(scan_mail, "MAIL_ROOT", mail_root), mock.patch("sys.stdout"):
                rc = scan_mail.main(["extract", "--out", outd, "--state", statep, "<abc@x>"])
            self.assertEqual(rc, 0)
            saved = [f for f in os.listdir(outd) if f.endswith(".pdf")]
            self.assertEqual(len(saved), 1)
            self.assertTrue(saved[0].startswith("20260701_x.jp_r_"))
            with open(os.path.join(outd, saved[0]), "rb") as f:
                self.assertTrue(f.read().startswith(b"%PDF"))

    def test_extract_partial_skips_with_error(self):
        with tempfile.TemporaryDirectory() as d:
            mail_root = os.path.join(d, "V10"); os.makedirs(os.path.join(mail_root, "acct/Messages"))
            _make_emlx(os.path.join(mail_root, "acct/Messages/10.partial.emlx"),
                       {"Message-ID": "<abc@x>"},
                       [("application/pdf", "r.pdf", None, "X-Apple-Content-Length: 999")])
            statep = os.path.join(d, "state.json"); self._state(statep)
            outd = os.path.join(d, "out")
            with mock.patch.object(scan_mail, "MAIL_ROOT", mail_root), \
                 mock.patch("sys.stdout"), mock.patch("sys.stderr"):
                rc = scan_mail.main(["extract", "--out", outd, "--state", statep, "<abc@x>"])
            self.assertEqual(rc, 1)
            self.assertFalse(os.path.isdir(outd) and any(f.endswith(".pdf") for f in os.listdir(outd)))

    def test_extract_missing_source_exits_nonzero(self):
        with tempfile.TemporaryDirectory() as d:
            mail_root = os.path.join(d, "V10"); os.makedirs(mail_root)
            statep = os.path.join(d, "state.json")
            st = scan_mail.load_state(statep)
            st["pending"]["<zzz@x>/1-r.pdf"] = {"subject": "", "sender": "", "date": "", "amounts": []}
            scan_mail.save_state(st, statep)   # sources に <zzz@x> なし
            with mock.patch.object(scan_mail, "MAIL_ROOT", mail_root), \
                 mock.patch("sys.stdout"), mock.patch("sys.stderr"):
                rc = scan_mail.main(["extract", "--out", os.path.join(d, "out"),
                                     "--state", statep, "<zzz@x>"])
            self.assertEqual(rc, 1)


if __name__ == "__main__":
    unittest.main()
