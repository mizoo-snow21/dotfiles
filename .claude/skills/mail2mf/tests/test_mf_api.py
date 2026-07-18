import json
import os
import sys
import unittest
import urllib.parse
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import mf_api


class TestGetAccessToken(unittest.TestCase):
    def setUp(self):
        self.creds = {
            "client_id": "cid",
            "client_secret": "sec",
            "refresh_token": "rt1",
        }

    def test_refresh_returns_access_token(self):
        resp = json.dumps({"access_token": "at", "refresh_token": "rt1"}).encode()
        with (
            mock.patch.object(mf_api, "keychain_read", return_value=dict(self.creds)),
            mock.patch.object(mf_api, "keychain_write") as kw,
            mock.patch.object(mf_api, "http", return_value=(200, {}, resp)),
        ):
            self.assertEqual(mf_api.get_access_token(), "at")
            kw.assert_not_called()  # ローテーションなしなら書き戻さない

    def test_refresh_rotation_updates_keychain(self):
        resp = json.dumps({"access_token": "at", "refresh_token": "rt2"}).encode()
        with (
            mock.patch.object(mf_api, "keychain_read", return_value=dict(self.creds)),
            mock.patch.object(mf_api, "keychain_write") as kw,
            mock.patch.object(mf_api, "http", return_value=(200, {}, resp)),
        ):
            mf_api.get_access_token()
            kw.assert_called_once()
            service, data = kw.call_args[0]
            self.assertEqual(service, mf_api.KEYCHAIN_SERVICE)
            self.assertEqual(data["refresh_token"], "rt2")

    def test_refresh_invalid_grant_exits_with_guidance(self):
        resp = json.dumps({"error": "invalid_grant"}).encode()
        with (
            mock.patch.object(mf_api, "keychain_read", return_value=dict(self.creds)),
            mock.patch.object(mf_api, "http", return_value=(400, {}, resp)),
        ):
            with self.assertRaises(SystemExit) as cm:
                mf_api.get_access_token()
            self.assertIn("auth-url", str(cm.exception))


class TestKeychain(unittest.TestCase):
    def test_read_parses_json(self):
        cp = mock.Mock(returncode=0, stdout='{"a": 1}\n', stderr="")
        with mock.patch.object(mf_api.subprocess, "run", return_value=cp) as r:
            self.assertEqual(mf_api.keychain_read("svc"), {"a": 1})
            args = r.call_args[0][0]
            self.assertEqual(args[:2], ["security", "find-generic-password"])

    def test_read_failure_exits(self):
        cp = mock.Mock(returncode=44, stdout="", stderr="not found")
        with mock.patch.object(mf_api.subprocess, "run", return_value=cp):
            with self.assertRaises(SystemExit):
                mf_api.keychain_read("svc")


class TestMultipart(unittest.TestCase):
    def test_build_multipart_format(self):
        body, ctype = mf_api.build_multipart(
            [
                ("file", "a.pdf", "application/pdf", b"%PDF-1.4"),
                ("metadata", None, "application/json", b'{"file_name": "a.pdf"}'),
            ]
        )
        self.assertIn("multipart/form-data; boundary=", ctype)
        boundary = ctype.split("boundary=")[1]
        self.assertIn(b"--" + boundary.encode(), body)
        self.assertIn(b'name="file"; filename="a.pdf"', body)
        self.assertIn(b"%PDF-1.4", body)
        self.assertIn(b'name="metadata"', body)
        self.assertTrue(body.endswith(b"--" + boundary.encode() + b"--\r\n"))


class TestUpload(unittest.TestCase):
    def _run(self, statuses, tmpdir):
        path = os.path.join(tmpdir, "x.pdf")
        with open(path, "wb") as f:
            f.write(b"%PDF-1.4")
        responses = [
            (s, {"Retry-After": "0"}, json.dumps({"file_id": "F1"}).encode())
            for s in statuses
        ]
        with (
            mock.patch.object(mf_api, "http", side_effect=responses) as h,
            mock.patch.object(mf_api.time, "sleep"),
        ):
            result = mf_api.upload_one("tok", path)
        return result, h

    def test_upload_success_returns_file_id(self):
        import tempfile

        with tempfile.TemporaryDirectory() as d:
            result, h = self._run([201], d)
            self.assertEqual(result, {"file_id": "F1"})
            self.assertEqual(h.call_count, 1)

    def test_upload_retries_once_on_429(self):
        import tempfile

        with tempfile.TemporaryDirectory() as d:
            result, h = self._run([429, 201], d)
            self.assertEqual(result, {"file_id": "F1"})
            self.assertEqual(h.call_count, 2)

    def test_upload_413_is_permanent(self):
        import tempfile

        with tempfile.TemporaryDirectory() as d:
            result, _ = self._run([413], d)
            self.assertTrue(result["permanent"])
            self.assertIn("413", result["error"])

    def test_upload_500_is_transient(self):
        import tempfile

        with tempfile.TemporaryDirectory() as d:
            result, _ = self._run([500], d)
            self.assertNotIn("permanent", result)
            self.assertIn("500", result["error"])

    def test_upload_retries_on_http_date_retry_after(self):
        import tempfile

        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "x.pdf")
            with open(path, "wb") as f:
                f.write(b"%PDF-1.4")
            responses = [
                (429, {"Retry-After": "Fri, 31 Dec 1999 23:59:59 GMT"}, b""),
                (201, {}, json.dumps({"file_id": "F1"}).encode()),
            ]
            with (
                mock.patch.object(mf_api, "http", side_effect=responses) as h,
                mock.patch.object(mf_api.time, "sleep") as sleep,
            ):
                result = mf_api.upload_one("tok", path)
            self.assertEqual(result, {"file_id": "F1"})
            self.assertEqual(h.call_count, 2)
            sleep.assert_called_once_with(5)

    def test_upload_missing_file_returns_error(self):
        result = mf_api.upload_one("tok", "/nonexistent/path/x.pdf")
        self.assertIn("error", result)
        self.assertNotIn("file_id", result)

    def test_upload_201_non_json_returns_error(self):
        import tempfile

        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "x.pdf")
            with open(path, "wb") as f:
                f.write(b"%PDF-1.4")
            with (
                mock.patch.object(mf_api, "http", return_value=(201, {}, b"not-json")),
                mock.patch.object(mf_api.time, "sleep"),
            ):
                result = mf_api.upload_one("tok", path)
            self.assertIn("error", result)
            self.assertNotIn("file_id", result)


class TestCmdUpload(unittest.TestCase):
    def test_mixed_success_and_error_returns_1_with_full_json(self):
        import io
        import tempfile

        with tempfile.TemporaryDirectory() as d:
            ok_path = os.path.join(d, "ok.pdf")
            with open(ok_path, "wb") as f:
                f.write(b"%PDF-1.4")
            bad_path = os.path.join(d, "missing.pdf")  # never created
            args = mock.Mock(files=[ok_path, bad_path])
            with (
                mock.patch.object(mf_api, "get_access_token", return_value="tok"),
                mock.patch.object(
                    mf_api,
                    "http",
                    return_value=(201, {}, json.dumps({"file_id": "F1"}).encode()),
                ),
                mock.patch("sys.stdout", new_callable=io.StringIO) as out,
            ):
                code = mf_api.cmd_upload(args)
            self.assertEqual(code, 1)
            payload = json.loads(out.getvalue())
            self.assertEqual(payload["ok.pdf"], {"file_id": "F1"})
            self.assertIn("error", payload["missing.pdf"])


class TestListBox(unittest.TestCase):
    def test_list_box_retries_once_on_429(self):
        import io
        from types import SimpleNamespace

        args = SimpleNamespace(limit=10, name=None)
        responses = [
            (429, {"Retry-After": "0"}, b""),
            (200, {}, b'{"files":[]}'),
        ]
        with (
            mock.patch.object(mf_api, "get_access_token", return_value="tok"),
            mock.patch.object(mf_api, "http", side_effect=responses) as h,
            mock.patch.object(mf_api.time, "sleep"),
            mock.patch("sys.stdout", new_callable=io.StringIO) as out,
        ):
            code = mf_api.cmd_list_box(args)
        self.assertEqual(code, 0)
        self.assertEqual(h.call_count, 2)
        self.assertEqual(out.getvalue(), '{"files":[]}\n')

    def test_list_box_name_adds_file_name_query(self):
        import io
        import urllib.parse
        from types import SimpleNamespace

        args = SimpleNamespace(limit=50, name="20260701_x.jp_r_abc.pdf")
        with (
            mock.patch.object(mf_api, "get_access_token", return_value="tok"),
            mock.patch.object(
                mf_api, "http", return_value=(200, {}, b'{"files":[]}')
            ) as h,
            mock.patch("sys.stdout", new_callable=io.StringIO),
        ):
            self.assertEqual(mf_api.cmd_list_box(args), 0)
        url = h.call_args[0][1]
        q = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
        self.assertEqual(q["file_name"], ["20260701_x.jp_r_abc.pdf"])
        self.assertEqual(q["limit"], ["50"])

    def test_list_box_without_name_omits_file_name(self):
        import io
        import urllib.parse
        from types import SimpleNamespace

        args = SimpleNamespace(limit=10, name=None)
        with (
            mock.patch.object(mf_api, "get_access_token", return_value="tok"),
            mock.patch.object(
                mf_api, "http", return_value=(200, {}, b'{"files":[]}')
            ) as h,
            mock.patch("sys.stdout", new_callable=io.StringIO),
        ):
            mf_api.cmd_list_box(args)
        url = h.call_args[0][1]
        q = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
        self.assertNotIn("file_name", q)
        self.assertEqual(q["limit"], ["10"])


class TestMcp(unittest.TestCase):
    def test_parse_sse_takes_last_data_line(self):
        text = 'event: message\ndata: {"a": 1}\n\ndata: {"b": 2}\n'
        self.assertEqual(mf_api.parse_sse(text), {"b": 2})

    def test_parse_sse_plain_json_fallback(self):
        self.assertEqual(mf_api.parse_sse('{"x": 1}'), {"x": 1})

    def test_mcp_call_flow(self):
        init = 'data: {"jsonrpc":"2.0","id":1,"result":{}}\n'
        result = {
            "jsonrpc": "2.0",
            "id": 2,
            "result": {"content": [{"type": "text", "text": '{"transactions": []}'}]},
        }
        responses = [
            (200, {"Mcp-Session-Id": "S1"}, init.encode()),
            (202, {}, b""),
            (200, {}, ("data: " + json.dumps(result) + "\n").encode()),
        ]
        with (
            mock.patch.object(mf_api, "get_access_token", return_value="tok"),
            mock.patch.object(mf_api, "http", side_effect=responses) as h,
        ):
            out = mf_api.mcp_call(
                "mfc_ca_getTransactions",
                {"start_date": "2026-04-01", "end_date": "2026-07-18"},
            )
        self.assertEqual(out, {"transactions": []})
        # 2回目以降はセッション ID を送っている
        self.assertEqual(h.call_args_list[2][0][2].get("Mcp-Session-Id"), "S1")

    def test_mcp_call_error_result_exits(self):
        init = 'data: {"jsonrpc":"2.0","id":1,"result":{}}\n'
        err = 'data: {"jsonrpc":"2.0","id":2,"error":{"code":-1,"message":"boom"}}\n'
        responses = [
            (200, {"Mcp-Session-Id": "S1"}, init.encode()),
            (202, {}, b""),
            (200, {}, err.encode()),
        ]
        with (
            mock.patch.object(mf_api, "get_access_token", return_value="tok"),
            mock.patch.object(mf_api, "http", side_effect=responses),
        ):
            with self.assertRaises(SystemExit):
                mf_api.mcp_call("mfc_ca_getTransactions", {})

    def test_parse_sse_unparseable_exits(self):
        for bad in ("", "<html>oops</html>"):
            with self.subTest(bad=bad):
                with self.assertRaises(SystemExit) as cm:
                    mf_api.parse_sse(bad)
                self.assertIn("unparseable", str(cm.exception).lower())

    def test_mcp_call_initialize_error_stops_early(self):
        init = (
            'data: {"jsonrpc":"2.0","id":1,"error":{"code":-1,"message":"init fail"}}\n'
        )
        responses = [(200, {"Mcp-Session-Id": "S1"}, init.encode())]
        with (
            mock.patch.object(mf_api, "get_access_token", return_value="tok"),
            mock.patch.object(mf_api, "http", side_effect=responses) as h,
        ):
            with self.assertRaises(SystemExit) as cm:
                mf_api.mcp_call("mfc_ca_getTransactions", {})
        self.assertEqual(h.call_count, 1)
        self.assertIn("init fail", str(cm.exception))

    def test_mcp_call_session_id_case_insensitive(self):
        init = 'data: {"jsonrpc":"2.0","id":1,"result":{}}\n'
        result = {
            "jsonrpc": "2.0",
            "id": 2,
            "result": {"content": [{"type": "text", "text": '{"transactions": []}'}]},
        }
        responses = [
            (200, {"mcp-session-id": "S1"}, init.encode()),
            (202, {}, b""),
            (200, {}, ("data: " + json.dumps(result) + "\n").encode()),
        ]
        with (
            mock.patch.object(mf_api, "get_access_token", return_value="tok"),
            mock.patch.object(mf_api, "http", side_effect=responses) as h,
        ):
            out = mf_api.mcp_call("mfc_ca_getTransactions", {})
        self.assertEqual(out, {"transactions": []})
        self.assertEqual(h.call_args_list[2][0][2].get("Mcp-Session-Id"), "S1")


class TestAuth(unittest.TestCase):
    def test_auth_url_persists_pkce_and_prints_url(self):
        stored = {}
        with (
            mock.patch.object(
                mf_api,
                "keychain_read",
                return_value={
                    "client_id": "cid",
                    "client_secret": "sec",
                    "refresh_token": "rt",
                },
            ),
            mock.patch.object(
                mf_api, "keychain_write", side_effect=lambda s, d: stored.update({s: d})
            ),
            mock.patch("sys.stdout") as out,
        ):
            mf_api.cmd_auth_url(None)
        pk = stored[mf_api.PKCE_SERVICE]
        self.assertIn("verifier", pk)
        self.assertIn("state", pk)
        printed = "".join(c[0][0] for c in out.write.call_args_list)
        self.assertIn(mf_api.AUTHORIZE_URL, printed)
        self.assertIn("code_challenge=", printed)
        self.assertIn(pk["state"], printed)

    def test_auth_exchange_state_mismatch_aborts_and_deletes(self):
        with (
            mock.patch.object(
                mf_api, "keychain_read", return_value={"verifier": "v", "state": "GOOD"}
            ),
            mock.patch.object(mf_api, "keychain_delete") as kd,
        ):
            args = mock.Mock(
                callback_url="http://localhost:3118/callback?code=c&state=BAD"
            )
            with self.assertRaises(SystemExit) as cm:
                mf_api.cmd_auth_exchange(args)
            self.assertIn("state", str(cm.exception))
            kd.assert_called_once_with(mf_api.PKCE_SERVICE)

    def test_auth_exchange_success_updates_refresh_token(self):
        def kread(service):
            if service == mf_api.PKCE_SERVICE:
                return {"verifier": "v", "state": "S"}
            return {"client_id": "cid", "client_secret": "sec", "refresh_token": "old"}

        resp = json.dumps(
            {
                "access_token": "at",
                "refresh_token": "new",
                "scope": "mfc/box/files.write",
            }
        ).encode()
        written = {}
        with (
            mock.patch.object(mf_api, "keychain_read", side_effect=kread),
            mock.patch.object(
                mf_api,
                "keychain_write",
                side_effect=lambda s, d: written.update({s: d}),
            ),
            mock.patch.object(mf_api, "keychain_delete") as kd,
            mock.patch.object(mf_api, "http", return_value=(200, {}, resp)) as h,
        ):
            args = mock.Mock(
                callback_url="http://localhost:3118/callback?code=c&state=S"
            )
            mf_api.cmd_auth_exchange(args)
        self.assertEqual(written[mf_api.KEYCHAIN_SERVICE]["refresh_token"], "new")
        kd.assert_called_once_with(mf_api.PKCE_SERVICE)
        sent = urllib.parse.parse_qs(h.call_args[0][3].decode())
        self.assertEqual(sent["code_verifier"], ["v"])
        self.assertEqual(sent["code"], ["c"])

    def test_auth_exchange_oauth_error_exits_and_deletes_pkce(self):
        with (
            mock.patch.object(
                mf_api, "keychain_read", return_value={"verifier": "v", "state": "S"}
            ),
            mock.patch.object(mf_api, "keychain_delete") as kd,
            mock.patch.object(mf_api, "keychain_write") as kw,
        ):
            args = mock.Mock(
                callback_url="http://localhost:3118/callback?error=access_denied&state=S"
            )
            with self.assertRaises(SystemExit) as cm:
                mf_api.cmd_auth_exchange(args)
            self.assertIn("access_denied", str(cm.exception))
            kd.assert_called_once_with(mf_api.PKCE_SERVICE)
            kw.assert_not_called()

    def test_auth_exchange_missing_refresh_token_exits_without_write(self):
        def kread(service):
            if service == mf_api.PKCE_SERVICE:
                return {"verifier": "v", "state": "S"}
            return {"client_id": "cid", "client_secret": "sec", "refresh_token": "old"}

        resp = json.dumps({"access_token": "at", "scope": "x"}).encode()
        with (
            mock.patch.object(mf_api, "keychain_read", side_effect=kread),
            mock.patch.object(mf_api, "keychain_write") as kw,
            mock.patch.object(mf_api, "keychain_delete"),
            mock.patch.object(mf_api, "http", return_value=(200, {}, resp)),
        ):
            args = mock.Mock(
                callback_url="http://localhost:3118/callback?code=c&state=S"
            )
            with self.assertRaises(SystemExit) as cm:
                mf_api.cmd_auth_exchange(args)
            self.assertIn("refresh_token", str(cm.exception))
            kw.assert_not_called()


if __name__ == "__main__":
    unittest.main()
