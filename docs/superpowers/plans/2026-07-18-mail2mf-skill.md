# mail2mf skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
> **This repo's CLAUDE.md overrides the implementer**: each task is dispatched to Cursor (`cursor-grok-4.5-medium-fast`) with the TDD skill content embedded. Claude Code does not write implementation code.

**Goal:** `/mail2mf` skill — Mail.app の決済系メールから PDF 証憑を抽出し、マネーフォワード クラウドBox にアップロードし、決済明細との突合レポートを出す。

**Architecture:** 2つの stdlib-only Python スクリプト(`scan_mail.py` = Mail.app スキャン/抽出/状態管理、`mf_api.py` = OAuth リフレッシュ/Box アップロード/MCP 明細取得)+ SKILL.md(Claude のオーケストレーション手順)。判定・突合は Claude が行い、機械的な処理はスクリプトが行う。

**Tech Stack:** Python 3 標準ライブラリのみ / osascript(JXA + AppleScript)/ macOS Keychain(`security`)/ unittest

**Spec:** `docs/superpowers/specs/2026-07-18-mail2mf-skill-design.md`(必読。state 遷移・添付キー・エラー処理の正はこちら)

## Global Constraints

- Python 3 標準ライブラリのみ。pip 依存追加禁止。テストは unittest(pytest 不可)。
- 秘匿情報(client_secret / refresh_token / access_token)をディスク・stdout・ログに出さない。Keychain service は `mail2mf-mfc`、PKCE 一時保存は `mail2mf-mfc-pkce`。
- 対象ブランチ: `feat/mail2mf-skill`(dotfiles リポジトリ)。main 直接コミット禁止。
- ファイル配置: `~/dotfiles/.claude/skills/mail2mf/`(リポジトリ内パス `.claude/skills/mail2mf/`)。
- state ファイル: `~/.local/state/mail2mf/state.json`。書き込みは tmp + `os.replace` のアトミック置換。
- テスト実行はすべて: `cd ~/dotfiles/.claude/skills/mail2mf && python3 -m unittest discover -s tests -v`
- 添付キー = `<message_id>/<添付順位>-<添付名>`(順位は全添付中の 1 始まり)。
- コミットメッセージ末尾に `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`。
- **タスク完了順序(SDD・全タスク共通)**: 実装 → テスト green → **Task Review
  (superpowers:subagent-driven-development の task-reviewer で ✅ Approved)→ その後で
  commit**。レビュー前にコミットしない。レビュー ❌ は修正を Cursor に差し戻して再レビュー。
- 各タスク開始時にブランチを確認する(Task 1 Step 0 参照。以降のタスクも
  `git branch --show-current` が `feat/mail2mf-skill` であることを確認してから着手)。

**API 定数(全タスク共通、実測で動作確認済み):**

| 名前 | 値 |
|---|---|
| TOKEN_URL | `https://api.biz.moneyforward.com/token` |
| AUTHORIZE_URL | `https://api.biz.moneyforward.com/authorize` |
| BOX_URL | `https://api.box.moneyforward.com/v1/files` |
| MCP_URL | `https://beta.mcp.developers.biz.moneyforward.com/mcp/ca/v3` |
| REDIRECT_URI | `http://localhost:3118/callback` |

---

### Task 1: リポジトリ足場 + mf_api.py の Keychain / トークンリフレッシュ

**Files:**
- Create: `.claude/skills/mail2mf/scripts/mf_api.py`
- Create: `.claude/skills/mail2mf/tests/test_mf_api.py`

**Interfaces:**
- Produces: `keychain_read(service) -> dict` / `keychain_write(service, data: dict) -> None` / `keychain_delete(service) -> None` / `http(method, url, headers: dict, data: bytes|None) -> (status:int, headers:dict, body:bytes)` / `get_access_token() -> str`。以降のタスクはこれらをそのまま使う。

- [ ] **Step 0: ブランチ確認**

Run: `cd ~/dotfiles && (git switch feat/mail2mf-skill 2>/dev/null || git switch -c feat/mail2mf-skill) && git branch --show-current`
Expected: `feat/mail2mf-skill`

- [ ] **Step 1: Write the failing tests**

`.claude/skills/mail2mf/tests/test_mf_api.py`:

```python
import json
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import mf_api


class TestGetAccessToken(unittest.TestCase):
    def setUp(self):
        self.creds = {"client_id": "cid", "client_secret": "sec", "refresh_token": "rt1"}

    def test_refresh_returns_access_token(self):
        resp = json.dumps({"access_token": "at", "refresh_token": "rt1"}).encode()
        with mock.patch.object(mf_api, "keychain_read", return_value=dict(self.creds)), \
             mock.patch.object(mf_api, "keychain_write") as kw, \
             mock.patch.object(mf_api, "http", return_value=(200, {}, resp)):
            self.assertEqual(mf_api.get_access_token(), "at")
            kw.assert_not_called()  # ローテーションなしなら書き戻さない

    def test_refresh_rotation_updates_keychain(self):
        resp = json.dumps({"access_token": "at", "refresh_token": "rt2"}).encode()
        with mock.patch.object(mf_api, "keychain_read", return_value=dict(self.creds)), \
             mock.patch.object(mf_api, "keychain_write") as kw, \
             mock.patch.object(mf_api, "http", return_value=(200, {}, resp)):
            mf_api.get_access_token()
            kw.assert_called_once()
            service, data = kw.call_args[0]
            self.assertEqual(service, mf_api.KEYCHAIN_SERVICE)
            self.assertEqual(data["refresh_token"], "rt2")

    def test_refresh_invalid_grant_exits_with_guidance(self):
        resp = json.dumps({"error": "invalid_grant"}).encode()
        with mock.patch.object(mf_api, "keychain_read", return_value=dict(self.creds)), \
             mock.patch.object(mf_api, "http", return_value=(400, {}, resp)):
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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd ~/dotfiles/.claude/skills/mail2mf && python3 -m unittest discover -s tests -v`
Expected: ERROR — `ModuleNotFoundError: No module named 'mf_api'`

- [ ] **Step 3: Write minimal implementation**

`.claude/skills/mail2mf/scripts/mf_api.py`:

```python
#!/usr/bin/env python3
"""mail2mf: マネーフォワード クラウド API クライアント。

サブコマンド:
  upload <file>...              PDF をクラウドBox へアップロード
  list-box [--limit N]          Box ファイル一覧(重複チェック用)
  transactions --from D --to D  決済明細を MCP 経由で取得
  auth-url                      再認可用 authorize URL 生成(PKCE)
  auth-exchange <callback_url>  コールバック URL をトークンに交換

秘匿情報は macOS Keychain のみ。アクセストークンはプロセス内でだけ保持する。
"""
import argparse
import base64
import getpass
import hashlib
import json
import secrets
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

KEYCHAIN_SERVICE = "mail2mf-mfc"
PKCE_SERVICE = "mail2mf-mfc-pkce"
TOKEN_URL = "https://api.biz.moneyforward.com/token"
AUTHORIZE_URL = "https://api.biz.moneyforward.com/authorize"
BOX_URL = "https://api.box.moneyforward.com/v1/files"
MCP_URL = "https://beta.mcp.developers.biz.moneyforward.com/mcp/ca/v3"
REDIRECT_URI = "http://localhost:3118/callback"
SCOPES = " ".join(
    ["mfc/accounting/%s" % s for s in [
        "offices.read", "accounts.read", "departments.read", "journal.read",
        "journal.write", "report.read", "taxes.read", "trade_partners.read",
        "trade_partners.write", "connected_account.read",
        "transaction.read", "transaction.write"]]
    + ["mfc/box/files.read", "mfc/box/files.write"])


def keychain_read(service):
    cp = subprocess.run(
        ["security", "find-generic-password", "-s", service, "-w"],
        capture_output=True, text=True)
    if cp.returncode != 0:
        raise SystemExit("keychain read failed (%s): %s" % (service, cp.stderr.strip()))
    return json.loads(cp.stdout)


def keychain_write(service, data):
    cp = subprocess.run(
        ["security", "add-generic-password", "-a", getpass.getuser(),
         "-s", service, "-w", json.dumps(data), "-U"],
        capture_output=True, text=True)
    if cp.returncode != 0:
        raise SystemExit("keychain write failed (%s): %s" % (service, cp.stderr.strip()))


def keychain_delete(service):
    subprocess.run(["security", "delete-generic-password", "-s", service],
                   capture_output=True, text=True)


def http(method, url, headers, data):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read()


def get_access_token():
    creds = keychain_read(KEYCHAIN_SERVICE)
    body = urllib.parse.urlencode({
        "grant_type": "refresh_token",
        "refresh_token": creds["refresh_token"],
        "client_id": creds["client_id"],
        "client_secret": creds["client_secret"],
    }).encode()
    status, _, resp = http("POST", TOKEN_URL,
                           {"Content-Type": "application/x-www-form-urlencoded"}, body)
    try:
        tok = json.loads(resp)
    except ValueError:
        raise SystemExit("token endpoint returned non-JSON (HTTP %d)" % status)
    if status != 200:
        if tok.get("error") == "invalid_grant":
            raise SystemExit(
                "refresh token expired. Run 'mf_api.py auth-url' to re-authorize.")
        raise SystemExit("token refresh failed: HTTP %d %s" % (status, tok.get("error", "")))
    if tok.get("refresh_token") and tok["refresh_token"] != creds["refresh_token"]:
        creds["refresh_token"] = tok["refresh_token"]
        keychain_write(KEYCHAIN_SERVICE, creds)
    return tok["access_token"]


def main(argv=None):
    parser = argparse.ArgumentParser(prog="mf_api.py")
    parser.add_subparsers(dest="cmd")
    parser.parse_args(argv)
    parser.error("no command")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd ~/dotfiles/.claude/skills/mail2mf && python3 -m unittest discover -s tests -v`
Expected: `OK` (6 tests)

- [ ] **Step 5: Task Review(✅必須)→ Commit**

task-reviewer の ✅ Approved を得てからコミットする(Global Constraints 参照):

```bash
cd ~/dotfiles
git add .claude/skills/mail2mf
git commit -m "feat(mail2mf): mf_api keychain + token refresh

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 2: mf_api.py — Box アップロード / 一覧

**Files:**
- Modify: `.claude/skills/mail2mf/scripts/mf_api.py`(Task 1 の `main` を置き換え、関数追加)
- Modify: `.claude/skills/mail2mf/tests/test_mf_api.py`(テストクラス追加)

**Interfaces:**
- Consumes: `get_access_token()`, `http()`(Task 1)
- Produces: CLI `upload <file>...`(stdout: `{"<basename>": {"file_id": ...}|{"error": ..., "permanent": bool}}`、全成功なら exit 0)/ CLI `list-box [--limit N]`(stdout: Box API の files JSON)。内部関数 `build_multipart(fields) -> (bytes, content_type)`・`upload_one(token, path) -> dict`。

- [ ] **Step 1: Write the failing tests**

`test_mf_api.py` に追加:

```python
class TestMultipart(unittest.TestCase):
    def test_build_multipart_format(self):
        body, ctype = mf_api.build_multipart([
            ("file", "a.pdf", "application/pdf", b"%PDF-1.4"),
            ("metadata", None, "application/json", b'{"file_name": "a.pdf"}'),
        ])
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
        responses = [(s, {"Retry-After": "0"}, json.dumps({"file_id": "F1"}).encode())
                     for s in statuses]
        with mock.patch.object(mf_api, "http", side_effect=responses) as h, \
             mock.patch.object(mf_api.time, "sleep"):
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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd ~/dotfiles/.claude/skills/mail2mf && python3 -m unittest discover -s tests -v`
Expected: ERROR — `AttributeError: module 'mf_api' has no attribute 'build_multipart'`

- [ ] **Step 3: Write implementation**

`mf_api.py` に追加し、`main` を argparse サブコマンド化:

```python
import os


def build_multipart(fields):
    """fields: [(name, filename|None, content_type, payload_bytes)]"""
    boundary = "----mail2mf" + secrets.token_hex(8)
    out = bytearray()
    for name, filename, ctype, payload in fields:
        out += ("--%s\r\nContent-Disposition: form-data; name=\"%s\"" % (boundary, name)).encode()
        if filename:
            out += ('; filename="%s"' % filename).encode()
        out += ("\r\nContent-Type: %s\r\n\r\n" % ctype).encode()
        out += payload + b"\r\n"
    out += ("--%s--\r\n" % boundary).encode()
    return bytes(out), "multipart/form-data; boundary=%s" % boundary


def upload_one(token, path):
    name = os.path.basename(path)
    with open(path, "rb") as f:
        payload = f.read()
    body, ctype = build_multipart([
        ("file", name, "application/pdf", payload),
        ("metadata", None, "application/json",
         json.dumps({"file_name": name}, ensure_ascii=False).encode()),
    ])
    headers = {"Authorization": "Bearer " + token, "Content-Type": ctype}
    status, rh, resp = http("POST", BOX_URL, headers, body)
    if status == 429:
        time.sleep(min(int(rh.get("Retry-After", "5") or "5"), 60))
        status, rh, resp = http("POST", BOX_URL, headers, body)
    if status == 201:
        parsed = json.loads(resp)
        file_id = parsed.get("file_id") or parsed.get("file", {}).get("file_id", "")
        return {"file_id": file_id}
    if status in (402, 413):
        return {"error": "HTTP %d" % status, "permanent": True}
    return {"error": "HTTP %d: %s" % (status, resp[:200].decode("utf-8", "replace"))}


def cmd_upload(args):
    token = get_access_token()
    results, ok = {}, True
    for path in args.files:
        results[os.path.basename(path)] = r = upload_one(token, path)
        if "error" in r:
            ok = False
    print(json.dumps(results, ensure_ascii=False))
    return 0 if ok else 1


def cmd_list_box(args):
    token = get_access_token()
    status, _, resp = http(
        "GET", BOX_URL + "?" + urllib.parse.urlencode({"limit": args.limit}),
        {"Authorization": "Bearer " + token, "Accept": "application/json"}, None)
    if status != 200:
        raise SystemExit("list-box failed: HTTP %d" % status)
    print(resp.decode())
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(prog="mf_api.py")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("upload")
    p.add_argument("files", nargs="+")
    p.set_defaults(fn=cmd_upload)
    p = sub.add_parser("list-box")
    p.add_argument("--limit", type=int, default=100)
    p.set_defaults(fn=cmd_list_box)
    args = parser.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd ~/dotfiles/.claude/skills/mail2mf && python3 -m unittest discover -s tests -v`
Expected: `OK` (11 tests)

- [ ] **Step 5: Task Review(✅必須)→ Commit**

task-reviewer の ✅ Approved を得てからコミットする(Global Constraints 参照):

```bash
cd ~/dotfiles
git add .claude/skills/mail2mf
git commit -m "feat(mail2mf): Box upload / list-box

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 3: mf_api.py — MCP 経由の決済明細取得

**Files:**
- Modify: `.claude/skills/mail2mf/scripts/mf_api.py`
- Modify: `.claude/skills/mail2mf/tests/test_mf_api.py`

**Interfaces:**
- Consumes: `get_access_token()`, `http()`
- Produces: CLI `transactions --from YYYY-MM-DD --to YYYY-MM-DD`(stdout: `mfc_ca_getTransactions` の結果 JSON)。内部関数 `parse_sse(text) -> dict`(最後の `data:` 行の JSON)・`mcp_call(tool: str, arguments: dict) -> object`。

- [ ] **Step 1: Write the failing tests**

`test_mf_api.py` に追加:

```python
class TestMcp(unittest.TestCase):
    def test_parse_sse_takes_last_data_line(self):
        text = 'event: message\ndata: {"a": 1}\n\ndata: {"b": 2}\n'
        self.assertEqual(mf_api.parse_sse(text), {"b": 2})

    def test_parse_sse_plain_json_fallback(self):
        self.assertEqual(mf_api.parse_sse('{"x": 1}'), {"x": 1})

    def test_mcp_call_flow(self):
        init = 'data: {"jsonrpc":"2.0","id":1,"result":{}}\n'
        result = {"jsonrpc": "2.0", "id": 2, "result": {
            "content": [{"type": "text", "text": '{"transactions": []}'}]}}
        responses = [
            (200, {"Mcp-Session-Id": "S1"}, init.encode()),
            (202, {}, b""),
            (200, {}, ("data: " + json.dumps(result) + "\n").encode()),
        ]
        with mock.patch.object(mf_api, "get_access_token", return_value="tok"), \
             mock.patch.object(mf_api, "http", side_effect=responses) as h:
            out = mf_api.mcp_call("mfc_ca_getTransactions",
                                  {"start_date": "2026-04-01", "end_date": "2026-07-18"})
        self.assertEqual(out, {"transactions": []})
        # 2回目以降はセッション ID を送っている
        self.assertEqual(h.call_args_list[2][0][2].get("Mcp-Session-Id"), "S1")

    def test_mcp_call_error_result_exits(self):
        init = 'data: {"jsonrpc":"2.0","id":1,"result":{}}\n'
        err = 'data: {"jsonrpc":"2.0","id":2,"error":{"code":-1,"message":"boom"}}\n'
        responses = [(200, {"Mcp-Session-Id": "S1"}, init.encode()),
                     (202, {}, b""), (200, {}, err.encode())]
        with mock.patch.object(mf_api, "get_access_token", return_value="tok"), \
             mock.patch.object(mf_api, "http", side_effect=responses):
            with self.assertRaises(SystemExit):
                mf_api.mcp_call("mfc_ca_getTransactions", {})
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd ~/dotfiles/.claude/skills/mail2mf && python3 -m unittest discover -s tests -v`
Expected: ERROR — `AttributeError: module 'mf_api' has no attribute 'parse_sse'`

- [ ] **Step 3: Write implementation**

`mf_api.py` に追加。`main()` のサブコマンド登録にも追記:

```python
def parse_sse(text):
    last = None
    for line in text.splitlines():
        if line.startswith("data: "):
            last = json.loads(line[6:])
    if last is None:
        last = json.loads(text)
    return last


def mcp_call(tool, arguments):
    token = get_access_token()
    base = {"Authorization": "Bearer " + token, "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"}

    def post(payload, sid=None):
        h = dict(base)
        if sid:
            h["Mcp-Session-Id"] = sid
        status, rh, body = http("POST", MCP_URL, h, json.dumps(payload).encode())
        if status >= 400:
            raise SystemExit("MCP HTTP %d: %s" % (status, body[:200].decode("utf-8", "replace")))
        return rh.get("Mcp-Session-Id"), body.decode("utf-8", "replace")

    sid, _ = post({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
        "protocolVersion": "2025-03-26", "capabilities": {},
        "clientInfo": {"name": "mail2mf", "version": "1.0"}}})
    post({"jsonrpc": "2.0", "method": "notifications/initialized"}, sid)
    _, body = post({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                    "params": {"name": tool, "arguments": arguments}}, sid)
    msg = parse_sse(body)
    if "error" in msg:
        raise SystemExit("MCP tool error: %s" % json.dumps(msg["error"], ensure_ascii=False))
    content = msg.get("result", {}).get("content", [])
    text = content[0].get("text", "") if content else ""
    try:
        return json.loads(text)
    except ValueError:
        return text


def cmd_transactions(args):
    out = mcp_call("mfc_ca_getTransactions",
                   {"start_date": getattr(args, "from"), "end_date": args.to})
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0
```

`main()` に追加:

```python
    p = sub.add_parser("transactions")
    p.add_argument("--from", required=True)
    p.add_argument("--to", dest="to", required=True)
    p.set_defaults(fn=cmd_transactions)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd ~/dotfiles/.claude/skills/mail2mf && python3 -m unittest discover -s tests -v`
Expected: `OK` (15 tests)

- [ ] **Step 5: Task Review(✅必須)→ Commit**

task-reviewer の ✅ Approved を得てからコミットする(Global Constraints 参照):

```bash
cd ~/dotfiles
git add .claude/skills/mail2mf
git commit -m "feat(mail2mf): transactions via MCP JSON-RPC

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 4: mf_api.py — PKCE 再認可(auth-url / auth-exchange)

**Files:**
- Modify: `.claude/skills/mail2mf/scripts/mf_api.py`
- Modify: `.claude/skills/mail2mf/tests/test_mf_api.py`

**Interfaces:**
- Consumes: `keychain_read/write/delete`, `http()`
- Produces: CLI `auth-url`(stdout: authorize URL 1行。verifier/state は `mail2mf-mfc-pkce` に保存)/ CLI `auth-exchange <callback_url>`(state 検証 → トークン交換 → `mail2mf-mfc` 更新 → PKCE エントリ削除)。

- [ ] **Step 1: Write the failing tests**

`test_mf_api.py` に追加:

```python
class TestAuth(unittest.TestCase):
    def test_auth_url_persists_pkce_and_prints_url(self):
        stored = {}
        with mock.patch.object(mf_api, "keychain_read",
                               return_value={"client_id": "cid", "client_secret": "sec",
                                             "refresh_token": "rt"}), \
             mock.patch.object(mf_api, "keychain_write",
                               side_effect=lambda s, d: stored.update({s: d})), \
             mock.patch("sys.stdout") as out:
            mf_api.cmd_auth_url(None)
        pk = stored[mf_api.PKCE_SERVICE]
        self.assertIn("verifier", pk)
        self.assertIn("state", pk)
        printed = "".join(c[0][0] for c in out.write.call_args_list)
        self.assertIn(mf_api.AUTHORIZE_URL, printed)
        self.assertIn("code_challenge=", printed)
        self.assertIn(pk["state"], printed)

    def test_auth_exchange_state_mismatch_aborts_and_deletes(self):
        with mock.patch.object(mf_api, "keychain_read",
                               return_value={"verifier": "v", "state": "GOOD"}), \
             mock.patch.object(mf_api, "keychain_delete") as kd:
            args = mock.Mock(callback_url="http://localhost:3118/callback?code=c&state=BAD")
            with self.assertRaises(SystemExit) as cm:
                mf_api.cmd_auth_exchange(args)
            self.assertIn("state", str(cm.exception))
            kd.assert_called_once_with(mf_api.PKCE_SERVICE)

    def test_auth_exchange_success_updates_refresh_token(self):
        def kread(service):
            if service == mf_api.PKCE_SERVICE:
                return {"verifier": "v", "state": "S"}
            return {"client_id": "cid", "client_secret": "sec", "refresh_token": "old"}
        resp = json.dumps({"access_token": "at", "refresh_token": "new",
                           "scope": "mfc/box/files.write"}).encode()
        written = {}
        with mock.patch.object(mf_api, "keychain_read", side_effect=kread), \
             mock.patch.object(mf_api, "keychain_write",
                               side_effect=lambda s, d: written.update({s: d})), \
             mock.patch.object(mf_api, "keychain_delete") as kd, \
             mock.patch.object(mf_api, "http", return_value=(200, {}, resp)) as h:
            args = mock.Mock(callback_url="http://localhost:3118/callback?code=c&state=S")
            mf_api.cmd_auth_exchange(args)
        self.assertEqual(written[mf_api.KEYCHAIN_SERVICE]["refresh_token"], "new")
        kd.assert_called_once_with(mf_api.PKCE_SERVICE)
        sent = urllib.parse.parse_qs(h.call_args[0][3].decode())
        self.assertEqual(sent["code_verifier"], ["v"])
        self.assertEqual(sent["code"], ["c"])
```

先頭の import に `import urllib.parse` を追加。

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd ~/dotfiles/.claude/skills/mail2mf && python3 -m unittest discover -s tests -v`
Expected: ERROR — `AttributeError: module 'mf_api' has no attribute 'cmd_auth_url'`

- [ ] **Step 3: Write implementation**

`mf_api.py` に追加。`main()` にサブコマンド登録:

```python
def cmd_auth_url(args):
    creds = keychain_read(KEYCHAIN_SERVICE)
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(48)).decode().rstrip("=")
    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode()).digest()).decode().rstrip("=")
    state = base64.urlsafe_b64encode(secrets.token_bytes(24)).decode().rstrip("=")
    keychain_write(PKCE_SERVICE, {"verifier": verifier, "state": state})
    url = AUTHORIZE_URL + "?" + urllib.parse.urlencode({
        "response_type": "code",
        "client_id": creds["client_id"],
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    })
    print(url)
    return 0


def cmd_auth_exchange(args):
    q = urllib.parse.parse_qs(urllib.parse.urlparse(args.callback_url).query)
    pk = keychain_read(PKCE_SERVICE)
    if q.get("state", [None])[0] != pk.get("state"):
        keychain_delete(PKCE_SERVICE)
        raise SystemExit("OAuth state mismatch — aborted (PKCE entry discarded)")
    creds = keychain_read(KEYCHAIN_SERVICE)
    body = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "code": q["code"][0],
        "redirect_uri": REDIRECT_URI,
        "client_id": creds["client_id"],
        "client_secret": creds["client_secret"],
        "code_verifier": pk["verifier"],
    }).encode()
    status, _, resp = http("POST", TOKEN_URL,
                           {"Content-Type": "application/x-www-form-urlencoded"}, body)
    if status != 200:
        raise SystemExit("token exchange failed: HTTP %d" % status)
    tok = json.loads(resp)
    creds["refresh_token"] = tok["refresh_token"]
    keychain_write(KEYCHAIN_SERVICE, creds)
    keychain_delete(PKCE_SERVICE)
    print("re-authorized OK. granted scopes: %s" % tok.get("scope", ""))
    return 0
```

`main()` に追加:

```python
    p = sub.add_parser("auth-url")
    p.set_defaults(fn=cmd_auth_url)
    p = sub.add_parser("auth-exchange")
    p.add_argument("callback_url")
    p.set_defaults(fn=cmd_auth_exchange)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd ~/dotfiles/.claude/skills/mail2mf && python3 -m unittest discover -s tests -v`
Expected: `OK` (18 tests)

- [ ] **Step 5: Task Review(✅必須)→ Commit**

task-reviewer の ✅ Approved を得てからコミットする(Global Constraints 参照):

```bash
cd ~/dotfiles
git add .claude/skills/mail2mf
git commit -m "feat(mail2mf): PKCE re-authorization flow

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 5: scan_mail.py — state 管理・金額抽出・候補構築(純粋ロジック)

**Files:**
- Create: `.claude/skills/mail2mf/scripts/scan_mail.py`
- Create: `.claude/skills/mail2mf/tests/test_scan_mail.py`

**Interfaces:**
- Produces:
  - `extract_amounts(text: str) -> list[int]`
  - `load_state(path) -> dict` / `save_state(state, path)`(tmp + `os.replace`)
  - `attachment_key(message_id, index, name) -> str`
  - `hash8(key) -> str` / `sender_domain(sender) -> str` / `final_name(key, date_iso, sender, orig_name) -> str`
  - `build_candidates(state, messages) -> (new_pending: dict, candidates: list[dict])`
    - `messages` の要素: `{"message_id", "date", "sender", "subject", "body_preview", "pdf_attachments": [{"index": int, "name": str}]}`
    - candidate: `{"key", "status": "new"|"pending_retry"|"failed_retry", "subject", "sender", "date", "amounts"}`
  - CLI `mark --key K (--uploaded FILE_ID | --failed MSG [--permanent])` / CLI `discard <key>...`
- Task 6 がこれらをそのまま使う。

- [ ] **Step 1: Write the failing tests**

`.claude/skills/mail2mf/tests/test_scan_mail.py`:

```python
import json
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
            self.assertEqual(st, {"last_scan": None, "pending": {},
                                  "uploaded": {}, "failed": {}, "discarded": {}})
            st["pending"]["k"] = {"subject": "s"}
            scan_mail.save_state(st, p)
            self.assertEqual(scan_mail.load_state(p)["pending"]["k"]["subject"], "s")
            self.assertFalse(os.path.exists(p + ".tmp"))


class TestNaming(unittest.TestCase):
    def test_attachment_key_includes_index(self):
        self.assertEqual(scan_mail.attachment_key("<m@x>", 2, "a.pdf"), "<m@x>/2-a.pdf")

    def test_final_name_unique_per_key(self):
        n1 = scan_mail.final_name("<m@x>/1-a.pdf", "2026-07-01T10:00:00+09:00",
                                  "Shop <no-reply@shop.jp>", "a.pdf")
        n2 = scan_mail.final_name("<m@x>/2-a.pdf", "2026-07-01T10:00:00+09:00",
                                  "Shop <no-reply@shop.jp>", "a.pdf")
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
        return {"message_id": mid, "date": "2026-07-01T10:00:00+09:00",
                "sender": "Shop <no-reply@shop.jp>", "subject": "領収書 ¥1,000",
                "body_preview": "合計 1,000円",
                "pdf_attachments": atts or [{"index": 1, "name": "r.pdf"}]}

    def test_new_message_becomes_pending_candidate(self):
        st = scan_mail.load_state("/nonexistent/state.json")
        pending, cands = scan_mail.build_candidates(st, [self._msg()])
        self.assertEqual(list(pending), ["<m@x>/1-r.pdf"])
        self.assertEqual(cands[0]["status"], "new")
        self.assertEqual(cands[0]["amounts"], [1000])

    def test_uploaded_and_permanent_failed_are_skipped(self):
        st = {"last_scan": None,
              "pending": {},
              "uploaded": {"<m@x>/1-r.pdf": {"file_id": "F"}},
              "failed": {"<old>/1-x.pdf": {"error": "HTTP 413", "permanent": True}}}
        pending, cands = scan_mail.build_candidates(st, [self._msg()])
        self.assertEqual(pending, {})
        self.assertEqual(cands, [])

    def test_discarded_keys_are_not_rediscovered(self):
        st = {"last_scan": None, "pending": {}, "uploaded": {}, "failed": {},
              "discarded": {"<m@x>/1-r.pdf": {"at": "t"}}}
        pending, cands = scan_mail.build_candidates(st, [self._msg()])
        self.assertEqual(pending, {})
        self.assertEqual(cands, [])

    def test_pending_and_failed_are_relisted(self):
        st = {"last_scan": None,
              "pending": {"<p>/1-a.pdf": {"subject": "s", "sender": "x@y.jp",
                                          "date": "d", "amounts": []}},
              "uploaded": {},
              "failed": {"<f>/1-b.pdf": {"error": "HTTP 500", "at": "t"}}}
        _, cands = scan_mail.build_candidates(st, [])
        statuses = {c["key"]: c["status"] for c in cands}
        self.assertEqual(statuses, {"<p>/1-a.pdf": "pending_retry",
                                    "<f>/1-b.pdf": "failed_retry"})


class TestMarkDiscard(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.dir.name, "state.json")
        st = scan_mail.load_state(self.path)
        st["pending"]["k1"] = {"subject": "s", "sender": "x", "date": "d", "amounts": []}
        scan_mail.save_state(st, self.path)

    def tearDown(self):
        self.dir.cleanup()

    def test_mark_uploaded_moves_entry(self):
        scan_mail.main(["mark", "--state", self.path, "--key", "k1",
                        "--uploaded", "FILE9"])
        st = scan_mail.load_state(self.path)
        self.assertNotIn("k1", st["pending"])
        self.assertEqual(st["uploaded"]["k1"]["file_id"], "FILE9")

    def test_mark_failed_permanent(self):
        scan_mail.main(["mark", "--state", self.path, "--key", "k1",
                        "--failed", "HTTP 413", "--permanent"])
        st = scan_mail.load_state(self.path)
        self.assertTrue(st["failed"]["k1"]["permanent"])

    def test_discard_removes_pending_and_leaves_tombstone(self):
        scan_mail.main(["discard", "--state", self.path, "k1"])
        st = scan_mail.load_state(self.path)
        self.assertNotIn("k1", st["pending"])
        self.assertNotIn("k1", st["failed"])
        self.assertIn("k1", st["discarded"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd ~/dotfiles/.claude/skills/mail2mf && python3 -m unittest discover -s tests -v`
Expected: ERROR — `ModuleNotFoundError: No module named 'scan_mail'`

- [ ] **Step 3: Write implementation**

`.claude/skills/mail2mf/scripts/scan_mail.py`:

```python
#!/usr/bin/env python3
"""mail2mf: Mail.app スキャン・添付抽出・state 管理。

サブコマンド:
  scan [--since YYYY-MM-DD] [--state PATH]   PDF 付きメールを走査し候補 JSON を出力
  extract --out DIR [--state PATH] <message_id>...   承認済みメールの PDF を保存
  mark --key K (--uploaded FILE_ID | --failed MSG [--permanent]) [--state PATH]
  discard [--state PATH] <key>...            非決済と判定された候補を pending から除去
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys

STATE_PATH = os.path.expanduser("~/.local/state/mail2mf/state.json")

AMOUNT_RE = re.compile(r"(?:[¥￥]\s*([0-9][0-9,]*)|([0-9][0-9,]*)\s*円)")


def extract_amounts(text):
    vals = []
    for m in AMOUNT_RE.finditer(text or ""):
        raw = (m.group(1) or m.group(2)).replace(",", "")
        try:
            v = int(raw)
        except ValueError:
            continue
        if 10 <= v <= 100_000_000 and v not in vals:
            vals.append(v)
    return vals[:20]


def load_state(path=STATE_PATH):
    try:
        with open(path) as f:
            state = json.load(f)
    except (FileNotFoundError, NotADirectoryError):
        state = {}
    state.setdefault("last_scan", None)
    for k in ("pending", "uploaded", "failed", "discarded"):
        state.setdefault(k, {})
    return state


def save_state(state, path=STATE_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def attachment_key(message_id, index, name):
    return "%s/%d-%s" % (message_id, index, name)


def hash8(key):
    return hashlib.sha256(key.encode()).hexdigest()[:8]


def sender_domain(sender):
    m = re.search(r"@([A-Za-z0-9.\-]+)", sender or "")
    return m.group(1).lower().rstrip(".>") if m else "unknown"


def _sanitize(s):
    return re.sub(r"[^\w.\-]+", "_", s, flags=re.UNICODE).strip("_") or "unknown"


def final_name(key, date_iso, sender, orig_name):
    d = (date_iso or "")[:10].replace("-", "") or "00000000"
    stem, ext = os.path.splitext(orig_name)
    if ext.lower() != ".pdf":
        ext = ".pdf"
    return "%s_%s_%s_%s%s" % (d, sender_domain(sender), _sanitize(stem),
                              hash8(key), ext.lower())


def build_candidates(state, messages):
    pending = dict(state["pending"])
    candidates = []
    for msg in messages:
        amounts = extract_amounts(
            (msg.get("subject") or "") + "\n" + (msg.get("body_preview") or ""))
        for att in msg["pdf_attachments"]:
            key = attachment_key(msg["message_id"], att["index"], att["name"])
            if (key in state["uploaded"] or key in state["failed"]
                    or key in state.get("discarded", {}) or key in pending):
                continue
            meta = {"subject": msg.get("subject", ""), "sender": msg.get("sender", ""),
                    "date": msg.get("date", ""), "amounts": amounts}
            pending[key] = meta
            candidates.append(dict(meta, key=key, status="new"))
    for key, meta in state["pending"].items():
        candidates.append(dict(meta, key=key, status="pending_retry"))
    for key, meta in state["failed"].items():
        if not meta.get("permanent"):
            candidates.append(dict(meta, key=key, status="failed_retry"))
    return pending, candidates


def cmd_mark(args):
    state = load_state(args.state)
    meta = state["pending"].pop(args.key, None) or state["failed"].pop(args.key, None) or {}
    now = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    if args.uploaded:
        state["uploaded"][args.key] = {"file_id": args.uploaded, "at": now}
    else:
        entry = {"error": args.failed, "at": now}
        entry.update({k: v for k, v in meta.items() if k in ("subject", "sender", "date")})
        if args.permanent:
            entry["permanent"] = True
        state["failed"][args.key] = entry
    save_state(state, args.state)
    return 0


def cmd_discard(args):
    state = load_state(args.state)
    now = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    for key in args.keys:
        state["pending"].pop(key, None)
        state["failed"].pop(key, None)
        # 墓標: 期間が重なる再スキャンでも再発見させない
        state["discarded"][key] = {"at": now}
    save_state(state, args.state)
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(prog="scan_mail.py")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("mark")
    p.add_argument("--state", default=STATE_PATH)
    p.add_argument("--key", required=True)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--uploaded")
    g.add_argument("--failed")
    p.add_argument("--permanent", action="store_true")
    p.set_defaults(fn=cmd_mark)
    p = sub.add_parser("discard")
    p.add_argument("--state", default=STATE_PATH)
    p.add_argument("keys", nargs="+")
    p.set_defaults(fn=cmd_discard)
    args = parser.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd ~/dotfiles/.claude/skills/mail2mf && python3 -m unittest discover -s tests -v`
Expected: `OK` (31 tests)

- [ ] **Step 5: Task Review(✅必須)→ Commit**

task-reviewer の ✅ Approved を得てからコミットする(Global Constraints 参照):

```bash
cd ~/dotfiles
git add .claude/skills/mail2mf
git commit -m "feat(mail2mf): scan_mail state/amount/candidate logic

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 6: scan_mail.py — Mail.app 連携(scan / extract)

**Files:**
- Modify: `.claude/skills/mail2mf/scripts/scan_mail.py`
- Modify: `.claude/skills/mail2mf/tests/test_scan_mail.py`

**Interfaces:**
- Consumes: Task 5 の全関数
- Produces: CLI `scan [--since YYYY-MM-DD] [--state PATH]`(stdout: `{"since": ..., "candidates": [...]}`)/ CLI `extract --out DIR [--state PATH] <message_id>...`(stdout: `{"<key>": "<saved_path>"}`)。内部関数 `run_jxa_scan(since_iso) -> list[dict]`・`parse_jxa_output(text) -> list[dict]`。

- [ ] **Step 1: Write the failing tests**

`test_scan_mail.py` に追加:

```python
from unittest import mock


class TestScanCmd(unittest.TestCase):
    def test_scan_checkpoints_pending_before_last_scan(self):
        """pending 書き出し → last_scan 前進の順序(spec の要)を save 呼び出し順で検証。"""
        msg = {"message_id": "<m@x>", "date": "2026-07-01T10:00:00+09:00",
               "sender": "a@b.jp", "subject": "領収書", "body_preview": "",
               "pdf_attachments": [{"index": 1, "name": "r.pdf"}]}
        saves = []
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "state.json")
            real_save = scan_mail.save_state

            def spy(state, path=p):
                saves.append(json.loads(json.dumps(state)))
                real_save(state, path)

            with mock.patch.object(scan_mail, "run_jxa_scan", return_value=[msg]), \
                 mock.patch.object(scan_mail, "save_state", side_effect=spy), \
                 mock.patch("sys.stdout"):
                scan_mail.main(["scan", "--state", p, "--since", "2026-07-01"])
            self.assertEqual(len(saves), 2)
            self.assertIn("<m@x>/1-r.pdf", saves[0]["pending"])
            self.assertIsNone(saves[0]["last_scan"])   # 1回目は cursor 未前進
            self.assertIsNotNone(saves[1]["last_scan"])

    def test_scan_default_since_is_90_days_when_no_state(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "state.json")
            with mock.patch.object(scan_mail, "run_jxa_scan", return_value=[]) as rj, \
                 mock.patch("sys.stdout"):
                scan_mail.main(["scan", "--state", p])
            since = rj.call_args[0][0]
            dt = datetime.datetime.fromisoformat(since)
            age = datetime.datetime.now().astimezone() - dt
            self.assertAlmostEqual(age.days, 90, delta=1)


class TestJxaParse(unittest.TestCase):
    def test_parse_jxa_output(self):
        raw = json.dumps([{"message_id": "<m@x>", "date": "2026-07-01T01:00:00.000Z",
                           "sender": "s", "subject": "t", "body_preview": "b",
                           "pdf_attachments": [{"index": 2, "name": "a.pdf"}]}])
        msgs = scan_mail.parse_jxa_output(raw)
        self.assertEqual(msgs[0]["pdf_attachments"][0]["index"], 2)

    def test_parse_jxa_output_rejects_garbage(self):
        with self.assertRaises(SystemExit):
            scan_mail.parse_jxa_output("execution error: Mail got an error (-1712)")


class TestExtractNamePlan(unittest.TestCase):
    def test_plan_extract_targets_reads_pending(self):
        state = {"last_scan": None,
                 "pending": {"<m@x>/1-r.pdf": {"subject": "s", "sender": "a@shop.jp",
                                               "date": "2026-07-01T10:00:00+09:00",
                                               "amounts": [100]},
                             "<other>/1-z.pdf": {"subject": "", "sender": "",
                                                 "date": "", "amounts": []}},
                 "uploaded": {}, "failed": {}}
        targets = scan_mail.plan_extract_targets(state, "<m@x>")
        self.assertEqual(len(targets), 1)
        idx, name, fname = targets[0]
        self.assertEqual((idx, name), (1, "r.pdf"))
        self.assertTrue(fname.startswith("20260701_shop.jp_r_"))

    def test_plan_extract_targets_includes_retryable_failed(self):
        state = {"last_scan": None, "pending": {}, "uploaded": {}, "discarded": {},
                 "failed": {"<m@x>/1-r.pdf": {"error": "HTTP 500",
                                              "sender": "a@shop.jp",
                                              "date": "2026-07-01T10:00:00+09:00"},
                            "<m@x>/2-big.pdf": {"error": "HTTP 413",
                                                "permanent": True}}}
        targets = scan_mail.plan_extract_targets(state, "<m@x>")
        self.assertEqual([(t[0], t[1]) for t in targets], [(1, "r.pdf")])
```

`test_scan_mail.py` 先頭の import に `import datetime` を追加。

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd ~/dotfiles/.claude/skills/mail2mf && python3 -m unittest discover -s tests -v`
Expected: ERROR — `AttributeError: module 'scan_mail' has no attribute 'run_jxa_scan'`(ほか同種)

- [ ] **Step 3: Write implementation**

`scan_mail.py` に追加。`main()` にサブコマンド登録:

```python
# JXA: whose で日付フィルタし、プロパティは配列一括取得(1メッセージ毎の
# Apple Event 往復を避ける)。本文は PDF 付きメールのみ個別取得。
# ponytail: 大量ヒット時は content() 取得が支配的。遅すぎる場合の改善路は
# Envelope Index (SQLite) 直読みだが、フルディスクアクセスが要るため v1 では見送り。
JXA_SCAN = r"""
function run(argv) {
  const since = new Date(argv[0]);
  const Mail = Application("Mail");
  const msgs = Mail.inbox.messages.whose({dateReceived: {_greaterThan: since}});
  const ids = msgs.messageId();
  const dates = msgs.dateReceived();
  const senders = msgs.sender();
  const subjects = msgs.subject();
  const out = [];
  for (let i = 0; i < ids.length; i++) {
    let names = [], mimes = [];
    try {
      names = msgs[i].mailAttachments.name();
      mimes = msgs[i].mailAttachments.mimeType();
    } catch (e) { continue; }
    const pdfs = [];
    for (let j = 0; j < names.length; j++) {
      const n = names[j] || "";
      const mt = (mimes[j] || "").toLowerCase();
      if (n.toLowerCase().endsWith(".pdf") || mt === "application/pdf") {
        pdfs.push({index: j + 1, name: n});
      }
    }
    if (!pdfs.length) continue;
    let body = "";
    try { body = (msgs[i].content() || "").slice(0, 1000); } catch (e) {}
    out.push({message_id: ids[i], date: dates[i].toISOString(),
              sender: senders[i], subject: subjects[i],
              body_preview: body, pdf_attachments: pdfs});
  }
  return JSON.stringify(out);
}
"""

APPLESCRIPT_EXTRACT = '''
set AppleScript's text item delimiters to linefeed
tell application "Mail"
  set theMsgs to (messages of inbox whose message id is "%s")
  if (count of theMsgs) = 0 then error "message not found"
  set m to item 1 of theMsgs
  set i to 0
  repeat with a in mail attachments of m
    set i to i + 1
    save a in POSIX file ("%s/att-" & i)
  end repeat
  return i as string
end tell
'''


def parse_jxa_output(text):
    try:
        msgs = json.loads(text)
    except ValueError:
        raise SystemExit("JXA scan failed: %s" % text[:300])
    if not isinstance(msgs, list):
        raise SystemExit("JXA scan returned unexpected JSON")
    return msgs


def run_jxa_scan(since_iso):
    cp = subprocess.run(
        ["osascript", "-l", "JavaScript", "-e", JXA_SCAN, since_iso],
        capture_output=True, text=True, timeout=1800)
    if cp.returncode != 0:
        raise SystemExit(
            "osascript failed (Mail のオートメーション権限を確認: システム設定 > "
            "プライバシーとセキュリティ > オートメーション): %s" % cp.stderr.strip()[:300])
    return parse_jxa_output(cp.stdout.strip())


def cmd_scan(args):
    state = load_state(args.state)
    if args.since:
        since = args.since
    elif state.get("last_scan"):
        since = state["last_scan"]
    else:
        since = (datetime.datetime.now().astimezone()
                 - datetime.timedelta(days=90)).isoformat(timespec="seconds")
    scan_started = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    messages = run_jxa_scan(since)
    pending, candidates = build_candidates(state, messages)
    state["pending"] = pending
    save_state(state, args.state)          # 候補を先に永続化(取りこぼし防止)
    state["last_scan"] = scan_started
    save_state(state, args.state)          # その後で cursor を前進
    print(json.dumps({"since": since, "candidates": candidates},
                     ensure_ascii=False, indent=1))
    return 0


def plan_extract_targets(state, message_id):
    """pending と再試行可能な failed から (添付順位, 添付名, 保存ファイル名) を得る。"""
    prefix = message_id + "/"
    sources = list(state["pending"].items()) + [
        (k, v) for k, v in state["failed"].items() if not v.get("permanent")]
    targets, seen = [], set()
    for key, meta in sources:
        if not key.startswith(prefix) or key in seen:
            continue
        m = re.match(r"^(\d+)-(.*)$", key[len(prefix):])
        if not m:
            continue
        seen.add(key)
        idx, name = int(m.group(1)), m.group(2)
        targets.append((idx, name,
                        final_name(key, meta.get("date", ""),
                                   meta.get("sender", ""), name)))
    return sorted(targets)


def cmd_extract(args):
    state = load_state(args.state)
    os.makedirs(args.out, exist_ok=True)
    results = {}
    ok = True
    for mid in args.message_ids:
        targets = plan_extract_targets(state, mid)
        if not targets:
            print("no pending attachments for %s" % mid, file=sys.stderr)
            ok = False
            continue
        script = APPLESCRIPT_EXTRACT % (mid.replace('"', '\\"'), args.out)
        cp = subprocess.run(["osascript", "-e", script],
                            capture_output=True, text=True, timeout=600)
        if cp.returncode != 0:
            print("extract failed for %s: %s" % (mid, cp.stderr.strip()[:200]),
                  file=sys.stderr)
            ok = False
            continue
        saved = {i: os.path.join(args.out, "att-%d" % i)
                 for i in range(1, int(cp.stdout.strip() or "0") + 1)}
        wanted = set()
        for idx, name, fname in targets:
            src = saved.get(idx)
            key = attachment_key(mid, idx, name)
            if src and os.path.exists(src):
                dst = os.path.join(args.out, fname)
                os.replace(src, dst)
                results[key] = dst
                wanted.add(idx)
            else:
                print("attachment %d missing for %s" % (idx, mid), file=sys.stderr)
                ok = False
        for idx, path in saved.items():   # 非 PDF 添付の残骸を削除
            if idx not in wanted and os.path.exists(path):
                os.remove(path)
    print(json.dumps(results, ensure_ascii=False))
    return 0 if ok else 1
```

`main()` に追加:

```python
    p = sub.add_parser("scan")
    p.add_argument("--state", default=STATE_PATH)
    p.add_argument("--since")
    p.set_defaults(fn=cmd_scan)
    p = sub.add_parser("extract")
    p.add_argument("--state", default=STATE_PATH)
    p.add_argument("--out", required=True)
    p.add_argument("message_ids", nargs="+")
    p.set_defaults(fn=cmd_extract)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd ~/dotfiles/.claude/skills/mail2mf && python3 -m unittest discover -s tests -v`
Expected: `OK` (37 tests)

- [ ] **Step 5: Manual smoke test (read-only)**

Run: `cd ~/dotfiles/.claude/skills/mail2mf && python3 scripts/scan_mail.py scan --since 2026-07-15 --state /tmp/mail2mf-smoke.json | head -40`
Expected: 直近3日の PDF 付きメールが `candidates` に JSON で出る(0件でも `{"since": ..., "candidates": []}` が正常)。実行後 `rm /tmp/mail2mf-smoke.json`。

- [ ] **Step 6: Task Review(✅必須)→ Commit**

task-reviewer の ✅ Approved を得てからコミットする(Global Constraints 参照):

```bash
cd ~/dotfiles
git add .claude/skills/mail2mf
git commit -m "feat(mail2mf): Mail.app scan (JXA) and attachment extract

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 7: SKILL.md + E2E スモーク

**Files:**
- Create: `.claude/skills/mail2mf/SKILL.md`

**Interfaces:**
- Consumes: Task 1-6 の全 CLI。
- Produces: `/mail2mf` skill 本体。

- [ ] **Step 1: Write SKILL.md**

`.claude/skills/mail2mf/SKILL.md`(以下の内容そのまま):

````markdown
---
name: mail2mf
description: Mail.app の決済系メール(PDF 証憑付き)をマネーフォワード クラウドBox へアップロードし、決済明細との突合レポートを出す。「決済メールをマネフォに」「証憑アップロード」「mail2mf」等で起動。
---

# mail2mf — 決済メール証憑 → クラウドBox 連携

スクリプト: このファイルと同じディレクトリの `scripts/scan_mail.py` と `scripts/mf_api.py`。
以降 `SKILL_DIR` = このファイルのあるディレクトリ。

## 手順

### 1. スキャン

```bash
python3 "$SKILL_DIR/scripts/scan_mail.py" scan
```

- ユーザーが期間を指定した場合のみ `--since YYYY-MM-DD` を付ける。
- 出力 JSON の `candidates` が空なら「新しい候補なし」と報告して手順 4 へ。

### 2. 判定と承認(必須ゲート)

candidates の各件を**意味的に**分類する: 決済系(領収書・請求書・利用明細・
注文確認に伴う適格請求書など)か、非決済(広告・物件情報・ニュースレター等)か。
金額候補(`amounts`)・件名・差出人を根拠に判断する。

- 結果を表で提示: | 判定 | 件名 | 差出人 | 日付 | 金額候補 | status |
- `status` が `failed_retry` の行は失敗理由も表示する。
- **ユーザーの承認を得るまでアップロードしない。**
- 非決済と判定されユーザーが同意した候補は pending から除去:
  `python3 "$SKILL_DIR/scripts/scan_mail.py" discard <key>...`

### 3. 抽出とアップロード

承認された候補について message_id ごとに:

```bash
python3 "$SKILL_DIR/scripts/scan_mail.py" extract --out ~/.local/state/mail2mf/downloads "<message_id>" ...
python3 "$SKILL_DIR/scripts/mf_api.py" upload <保存されたファイル>...
```

- upload の結果 JSON を見て 1 件ずつ state を確定する:
  - 成功: `scan_mail.py mark --key "<key>" --uploaded <file_id>`
  - 失敗: `scan_mail.py mark --key "<key>" --failed "<error>"`(402/413 は `--permanent` 付き)
- アップロード前に必要なら `mf_api.py list-box --limit 200` で同名ファイルの有無を確認し、
  既に存在するものはアップロードせず mark --uploaded で消し込む(file_id は一覧のもの)。

### 4. 突合レポート

```bash
python3 "$SKILL_DIR/scripts/mf_api.py" transactions --from <期間開始> --to <今日>
```

明細(決済)とアップロード済み証憑(メール由来の金額・日付・差出人)を突合し、
Markdown レポートを出す:

- **対応あり**: 明細と証憑が金額±0・日付±3日で一致(取引内容と差出人の意味一致も加味)
- **証憑なし決済**: 対応する証憑が見つからない明細(`journalizing_statuses` が
  `none` のものは「未仕訳」と明記)
- **明細なし証憑**: どの明細とも一致しない証憑

レポート末尾に必ず添える案内:
「仕訳の確定はマネーフォワード クラウド会計の [自動で仕訳 > 連携サービスから入力] と
[クラウドBox の仕訳候補] 画面で承認してください。証憑の添付はこのルートでのみ行われます。」

### 5. エラー対応

- `refresh token expired` → `mf_api.py auth-url` で URL を生成しユーザーに提示 →
  ブラウザで許可後、`localhost:3118` のエラーページの URL を貼ってもらい
  `mf_api.py auth-exchange "<callback_url>"`。
- osascript 権限エラー → システム設定 > プライバシーとセキュリティ > オートメーション で
  ターミナルに Mail の許可を付与するよう案内。
- MCP/明細取得の失敗 → アップロードまでで完了とし、レポートは「突合スキップ」と明記。

## 注意

- 秘匿情報は Keychain(`mail2mf-mfc`)。トークンや client_secret を表示・保存しない。
- Box への削除操作は存在しない(アップロードのみ)。誤アップは MF 画面から削除してもらう。
````

- [ ] **Step 2: E2E スモークテスト**

実データのアップロードは行わない(承認ゲートは E2E でも適用)。

1. `python3 scripts/mf_api.py list-box --limit 3` → 既存ファイルの JSON が返る(認証・Keychain 動作確認)
2. `python3 scripts/scan_mail.py scan --since <3日前> --state /tmp/e2e-state.json` → candidates 取得
3. candidates から 1 件選び `extract --out /tmp/e2e-dl --state /tmp/e2e-state.json "<message_id>"` → リネーム済み PDF がローカルに保存される(**アップロードはしない**)
4. アップロード経路は合成テスト PDF で確認する。**実行前にユーザーへ「テスト PDF を 1 件 Box にアップします。削除は Box の UI からになります」と確認し、明示的な承認を得ること。承認がなければこのステップはスキップし、その旨を報告する**:
   `printf '%%PDF-1.4\n%%%%EOF\n' > /tmp/mail2mf_e2e_test.pdf && python3 scripts/mf_api.py upload /tmp/mail2mf_e2e_test.pdf` → `file_id` が返り、`list-box` に `mail2mf_e2e_test.pdf` が現れる。完了後、Box UI からの削除手順をユーザーに案内
5. `python3 scripts/mf_api.py transactions --from <月初> --to <今日>` → 明細 JSON が返る
6. 後片付け: `rm -rf /tmp/e2e-state.json /tmp/e2e-dl /tmp/mail2mf_e2e_test.pdf`

Expected: 全ステップ成功(4 は承認時のみ)。state 遷移(mark)は単体テストで担保済みのため実データでは行わない。

- [ ] **Step 3: Task Review(✅必須)→ Commit**

task-reviewer の ✅ Approved を得てからコミットする(Global Constraints 参照):

```bash
cd ~/dotfiles
git add .claude/skills/mail2mf
git commit -m "feat(mail2mf): SKILL.md orchestration

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

## Self-Review チェック済み事項

- spec の全要件(scan/判定ゲート/extract/upload/突合/state 遷移/PKCE/エラー処理)に対応タスクあり
- 型・シグネチャ整合: `build_candidates(state, messages)` は Task 5 定義・Task 6 使用で一致。`attachment_key` / `final_name` / `mark` / `discard` の引数は全タスクで同一
- プレースホルダなし(全ステップに実コード)
- 実装後の Branch Review(superpowers:requesting-code-review)を PR 前に実施
