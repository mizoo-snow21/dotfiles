#!/usr/bin/env python3
"""mail2mf: マネーフォワード クラウド API クライアント。

サブコマンド:
  upload <file>...              PDF をクラウドBox へアップロード
  list-box [--limit N] [--name FILE]  Box ファイル一覧(重複チェック用)
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
import os
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
    [
        "mfc/accounting/%s" % s
        for s in [
            "offices.read",
            "accounts.read",
            "departments.read",
            "journal.read",
            "journal.write",
            "report.read",
            "taxes.read",
            "trade_partners.read",
            "trade_partners.write",
            "connected_account.read",
            "transaction.read",
            "transaction.write",
        ]
    ]
    + ["mfc/box/files.read", "mfc/box/files.write"]
)


def keychain_read(service):
    cp = subprocess.run(
        ["security", "find-generic-password", "-s", service, "-w"],
        capture_output=True,
        text=True,
    )
    if cp.returncode != 0:
        raise SystemExit("keychain read failed (%s): %s" % (service, cp.stderr.strip()))
    return json.loads(cp.stdout)


def keychain_write(service, data):
    cp = subprocess.run(
        [
            "security",
            "add-generic-password",
            "-a",
            getpass.getuser(),
            "-s",
            service,
            "-w",
            json.dumps(data),
            "-U",
        ],
        capture_output=True,
        text=True,
    )
    if cp.returncode != 0:
        raise SystemExit(
            "keychain write failed (%s): %s" % (service, cp.stderr.strip())
        )


def keychain_delete(service):
    subprocess.run(
        ["security", "delete-generic-password", "-s", service],
        capture_output=True,
        text=True,
    )


def http(method, url, headers, data):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read()


def get_access_token():
    creds = keychain_read(KEYCHAIN_SERVICE)
    body = urllib.parse.urlencode(
        {
            "grant_type": "refresh_token",
            "refresh_token": creds["refresh_token"],
            "client_id": creds["client_id"],
            "client_secret": creds["client_secret"],
        }
    ).encode()
    status, _, resp = http(
        "POST", TOKEN_URL, {"Content-Type": "application/x-www-form-urlencoded"}, body
    )
    try:
        tok = json.loads(resp)
    except ValueError:
        raise SystemExit("token endpoint returned non-JSON (HTTP %d)" % status)
    if status != 200:
        if tok.get("error") == "invalid_grant":
            raise SystemExit(
                "refresh token expired. Run 'mf_api.py auth-url' to re-authorize."
            )
        raise SystemExit(
            "token refresh failed: HTTP %d %s" % (status, tok.get("error", ""))
        )
    if tok.get("refresh_token") and tok["refresh_token"] != creds["refresh_token"]:
        creds["refresh_token"] = tok["refresh_token"]
        keychain_write(KEYCHAIN_SERVICE, creds)
    return tok["access_token"]


def retry_after_seconds(headers, default=5, cap=60):
    """Retry-After を秒数に。非数値・負値・空は default、上限 cap。"""
    raw = (headers or {}).get("Retry-After", "")
    if raw is None or str(raw).strip() == "":
        return default
    try:
        n = int(str(raw).strip())
    except (TypeError, ValueError):
        return default
    if n < 0:
        return default
    return min(n, cap)


def build_multipart(fields):
    """fields: [(name, filename|None, content_type, payload_bytes)]"""
    boundary = "----mail2mf" + secrets.token_hex(8)
    out = bytearray()
    for name, filename, ctype, payload in fields:
        out += (
            '--%s\r\nContent-Disposition: form-data; name="%s"' % (boundary, name)
        ).encode()
        if filename:
            out += ('; filename="%s"' % filename).encode()
        out += ("\r\nContent-Type: %s\r\n\r\n" % ctype).encode()
        out += payload + b"\r\n"
    out += ("--%s--\r\n" % boundary).encode()
    return bytes(out), "multipart/form-data; boundary=%s" % boundary


def upload_one(token, path):
    name = os.path.basename(path)
    try:
        with open(path, "rb") as f:
            payload = f.read()
    except OSError as e:
        return {"error": str(e)}
    body, ctype = build_multipart(
        [
            ("file", name, "application/pdf", payload),
            (
                "metadata",
                None,
                "application/json",
                json.dumps({"file_name": name}, ensure_ascii=False).encode(),
            ),
        ]
    )
    headers = {"Authorization": "Bearer " + token, "Content-Type": ctype}
    status, rh, resp = http("POST", BOX_URL, headers, body)
    if status == 429:
        time.sleep(retry_after_seconds(rh))
        status, rh, resp = http("POST", BOX_URL, headers, body)
    if status == 201:
        try:
            parsed = json.loads(resp)
        except ValueError:
            return {"error": "invalid JSON: %s" % resp[:200].decode("utf-8", "replace")}
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
    # Box一覧APIは limit の上限が100で、オフセット/ページ指定が無い。
    # 101件以上を一度に見る手段が無いので、全件棚卸しでの重複チェックは
    # 原理的に不可能。重複判定は必ず --name のサーバー側完全一致で行う。
    if args.limit > 100:
        raise SystemExit(
            "list-box: --limit の上限は100です(APIがページングに非対応)。"
            "重複チェックは --name でファイル名を指定してください。")
    token = get_access_token()
    headers = {"Authorization": "Bearer " + token, "Accept": "application/json"}
    q = {"limit": args.limit}
    if args.name:
        q["file_name"] = args.name
    url = BOX_URL + "?" + urllib.parse.urlencode(q)
    status, rh, resp = http("GET", url, headers, None)
    if status == 429:
        time.sleep(retry_after_seconds(rh))
        status, rh, resp = http("GET", url, headers, None)
    if status != 200:
        raise SystemExit("list-box failed: HTTP %d" % status)
    print(resp.decode())
    return 0


def parse_sse(text):
    last = None
    try:
        for line in text.splitlines():
            if line.startswith("data: "):
                last = json.loads(line[6:])
        if last is None:
            last = json.loads(text)
    except (TypeError, ValueError):
        raise SystemExit("MCP: unparseable response: %s" % (text or "")[:200])
    return last


def _header_ci(headers, name):
    """応答ヘッダーを case-insensitive に取得。"""
    want = name.lower()
    for k, v in (headers or {}).items():
        if str(k).lower() == want:
            return v
    return None


def mcp_call(tool, arguments):
    token = get_access_token()
    base = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }

    def post(payload, sid=None):
        h = dict(base)
        if sid:
            h["Mcp-Session-Id"] = sid
        status, rh, body = http("POST", MCP_URL, h, json.dumps(payload).encode())
        if status >= 400:
            raise SystemExit(
                "MCP HTTP %d: %s" % (status, body[:200].decode("utf-8", "replace"))
            )
        return _header_ci(rh, "mcp-session-id"), body.decode("utf-8", "replace")

    sid, init_body = post(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "mail2mf", "version": "1.0"},
            },
        }
    )
    init_msg = parse_sse(init_body) if init_body.strip() else {}
    if "error" in init_msg:
        raise SystemExit(
            "MCP initialize error: %s"
            % json.dumps(init_msg["error"], ensure_ascii=False)
        )
    post({"jsonrpc": "2.0", "method": "notifications/initialized"}, sid)
    _, body = post(
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {"name": tool, "arguments": arguments},
        },
        sid,
    )
    msg = parse_sse(body)
    if "error" in msg:
        raise SystemExit(
            "MCP tool error: %s" % json.dumps(msg["error"], ensure_ascii=False)
        )
    content = msg.get("result", {}).get("content", [])
    text = content[0].get("text", "") if content else ""
    try:
        return json.loads(text)
    except ValueError:
        return text


def cmd_transactions(args):
    """全ページを取得して1つのJSONにまとめて返す。

    getTransactions は既定 per_page=50 で、指定期間の件数が多いと
    total_pages > 1 になる。1ページ目だけを見て突合すると明細を静かに
    取りこぼし「証憑に対応する決済がない」と誤判定するため、必ず
    メタデータの total_pages 分だけ回して結合する。
    """
    base = {
        "start_date": getattr(args, "from"),
        "end_date": args.to,
        "per_page": args.per_page,
        "order": "asc",
    }
    if args.account:
        base["connected_account_id"] = args.account

    merged, seen, page, total_pages = [], set(), 1, 1
    while page <= total_pages:
        q = dict(base, page=page)
        out = mcp_call("mfc_ca_getTransactions", q)
        if not isinstance(out, dict):
            raise SystemExit("transactions: 想定外の応答: %r" % (out,)[:200])
        meta = out.get("metadata") or {}
        total_pages = meta.get("total_pages") or 1
        for t in out.get("transactions") or []:
            if t.get("id") in seen:
                continue
            seen.add(t.get("id"))
            merged.append(t)
        page += 1

    print(json.dumps(
        {"metadata": {"total_count": len(merged), "pages_fetched": total_pages},
         "transactions": merged},
        ensure_ascii=False, indent=1))
    return 0


def cmd_auth_url(args):
    creds = keychain_read(KEYCHAIN_SERVICE)
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(48)).decode().rstrip("=")
    challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest())
        .decode()
        .rstrip("=")
    )
    state = base64.urlsafe_b64encode(secrets.token_bytes(24)).decode().rstrip("=")
    keychain_write(PKCE_SERVICE, {"verifier": verifier, "state": state})
    url = (
        AUTHORIZE_URL
        + "?"
        + urllib.parse.urlencode(
            {
                "response_type": "code",
                "client_id": creds["client_id"],
                "redirect_uri": REDIRECT_URI,
                "scope": SCOPES,
                "state": state,
                "code_challenge": challenge,
                "code_challenge_method": "S256",
            }
        )
    )
    print(url)
    return 0


def cmd_auth_exchange(args):
    q = urllib.parse.parse_qs(urllib.parse.urlparse(args.callback_url).query)
    pk = keychain_read(PKCE_SERVICE)
    if q.get("state", [None])[0] != pk.get("state"):
        keychain_delete(PKCE_SERVICE)
        raise SystemExit("OAuth state mismatch — aborted (PKCE entry discarded)")
    code = q.get("code", [None])[0]
    if not code:
        keychain_delete(PKCE_SERVICE)
        err = q.get("error", [None])[0]
        raise SystemExit(
            "OAuth authorization failed: %s" % err
            if err
            else "OAuth callback missing code parameter"
        )
    creds = keychain_read(KEYCHAIN_SERVICE)
    body = urllib.parse.urlencode(
        {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": creds["client_id"],
            "client_secret": creds["client_secret"],
            "code_verifier": pk["verifier"],
        }
    ).encode()
    status, _, resp = http(
        "POST", TOKEN_URL, {"Content-Type": "application/x-www-form-urlencoded"}, body
    )
    try:
        tok = json.loads(resp)
    except ValueError:
        raise SystemExit("token exchange returned non-JSON (HTTP %d)" % status)
    if status != 200:
        raise SystemExit("token exchange failed: HTTP %d" % status)
    if "refresh_token" not in tok:
        raise SystemExit("token exchange response missing refresh_token")
    creds["refresh_token"] = tok["refresh_token"]
    keychain_write(KEYCHAIN_SERVICE, creds)
    keychain_delete(PKCE_SERVICE)
    print("re-authorized OK. granted scopes: %s" % tok.get("scope", ""))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(prog="mf_api.py")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("upload")
    p.add_argument("files", nargs="+")
    p.set_defaults(fn=cmd_upload)
    p = sub.add_parser("list-box")
    p.add_argument("--limit", type=int, default=100)
    p.add_argument("--name")
    p.set_defaults(fn=cmd_list_box)
    p = sub.add_parser("transactions")
    p.add_argument("--from", required=True)
    p.add_argument("--to", dest="to", required=True)
    p.add_argument("--per-page", dest="per_page", type=int, default=500,
                   help="1ページあたり件数(最大500)。全ページ自動取得するので通常は既定のままでよい")
    p.add_argument("--account", help="connected_account_id で絞り込む(任意)")
    p.set_defaults(fn=cmd_transactions)
    p = sub.add_parser("auth-url")
    p.set_defaults(fn=cmd_auth_url)
    p = sub.add_parser("auth-exchange")
    p.add_argument("callback_url")
    p.set_defaults(fn=cmd_auth_exchange)
    args = parser.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
