import json
import os
import sys
import unittest
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


if __name__ == "__main__":
    unittest.main()
