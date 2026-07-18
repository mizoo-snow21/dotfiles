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
import email
import hashlib
import json
import os
import re
import sqlite3
import sys

STATE_PATH = os.path.expanduser("~/.local/state/mail2mf/state.json")
MAIL_ROOT = os.path.expanduser("~/Library/Mail/V10")
ENVELOPE_INDEX = os.path.join(MAIL_ROOT, "MailData", "Envelope Index")

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
    for k in ("pending", "uploaded", "failed", "discarded", "sources", "skipped"):
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
    return "%s_%s_%s_%s%s" % (
        d,
        sender_domain(sender),
        _sanitize(stem),
        hash8(key),
        ext.lower(),
    )


def build_candidates(state, messages):
    pending = dict(state["pending"])
    candidates = []
    for msg in messages:
        amounts = extract_amounts(
            (msg.get("subject") or "") + "\n" + (msg.get("body_preview") or "")
        )
        for att in msg["pdf_attachments"]:
            key = attachment_key(msg["message_id"], att["index"], att["name"])
            if (
                key in state["uploaded"]
                or key in state["failed"]
                or key in state.get("discarded", {})
                or key in pending
            ):
                continue
            meta = {
                "subject": msg.get("subject", ""),
                "sender": msg.get("sender", ""),
                "date": msg.get("date", ""),
                "amounts": amounts,
            }
            pending[key] = meta
            candidates.append(dict(meta, key=key, status="new"))
    for key, meta in state["pending"].items():
        candidates.append(dict(meta, key=key, status="pending_retry"))
    for key, meta in state["failed"].items():
        if not meta.get("permanent"):
            candidates.append(dict(meta, key=key, status="failed_retry"))
    return pending, candidates


def open_envelope_index(path=ENVELOPE_INDEX):
    if not os.path.exists(path):
        raise SystemExit(
            "Envelope Index が見つからない/読めません。システム設定 > プライバシーと"
            "セキュリティ > フルディスクアクセス で端末アプリに許可してください: %s" % path)
    try:
        return sqlite3.connect("file:%s?mode=ro" % path, uri=True)
    except sqlite3.Error as e:
        raise SystemExit(
            "Envelope Index を開けません(フルディスクアクセスを確認してください): %s" % e)


def query_attachment_messages(conn, cutoff_epoch):
    # 添付を持つメッセージを引く(PDF 判定は名前ではなく .emlx の MIME で行うため、
    # 拡張子 .pdf でなく application/pdf でも取りこぼさない)。DISTINCT で1メッセージ1行。
    cur = conn.execute(
        "SELECT DISTINCT m.ROWID, m.date_received, ad.address, s.subject "
        "FROM messages m JOIN attachments a ON a.message=m.ROWID "
        "LEFT JOIN addresses ad ON ad.ROWID=m.sender "
        "LEFT JOIN subjects s ON s.ROWID=m.subject "
        "WHERE m.date_received>=? AND m.deleted=0 "
        "ORDER BY m.date_received DESC, m.ROWID", (cutoff_epoch,))
    return [{"rowid": rowid, "date_received": dr, "sender": addr or "", "subject": subj or ""}
            for rowid, dr, addr, subj in cur.fetchall()]


def query_messages_by_rowids(conn, rowids):
    """ROWID 群から messages 行を引く(skipped 再解決用。cutoff と無関係)。"""
    ids = [int(r) for r in rowids]
    if not ids:
        return []
    placeholders = ",".join("?" * len(ids))
    cur = conn.execute(
        "SELECT m.ROWID, m.date_received, ad.address, s.subject "
        "FROM messages m "
        "LEFT JOIN addresses ad ON ad.ROWID=m.sender "
        "LEFT JOIN subjects s ON s.ROWID=m.subject "
        "WHERE m.ROWID IN (%s) AND m.deleted=0" % placeholders, ids)
    return [{"rowid": rowid, "date_received": dr, "sender": addr or "", "subject": subj or ""}
            for rowid, dr, addr, subj in cur.fetchall()]


def build_emlx_index(mail_root=MAIL_ROOT):
    idx = {}
    for dp, _, fns in os.walk(mail_root):
        for fn in fns:
            if fn.endswith(".emlx"):
                rowid = fn.split(".")[0]
                full = fn.endswith(".emlx") and not fn.endswith(".partial.emlx")
                cur = idx.get(rowid)
                # full を優先。未登録 or 既存が partial かつ今回 full なら差し替え
                if cur is None or (full and cur.endswith(".partial.emlx")):
                    idx[rowid] = os.path.join(dp, fn)
    return idx


def read_emlx(path):
    with open(path, "rb") as f:
        raw = f.read()
    nl = raw.index(b"\n")
    count = int(raw[:nl].strip())
    body = raw[nl + 1:nl + 1 + count]
    return email.message_from_bytes(body)


def emlx_message_id(msg):
    mid = msg.get("Message-ID")
    return mid.strip() if mid else ""


def pdf_parts(msg):
    out = []
    i = 0
    for part in msg.walk():
        fn = part.get_filename()
        if not fn:
            continue
        i += 1
        if fn.lower().endswith(".pdf") or part.get_content_type() == "application/pdf":
            try:
                payload = part.get_payload(decode=True)
            except Exception:
                payload = None
            # 未 DL(partial)は None または空 b'' になり得る。実PDFは0バイトにならないので
            # 空はすべて「未ダウンロード」に正規化する(空PDFを誤って抽出しない)。
            if not payload:
                payload = None
            out.append((i, fn, payload))
    return out


def _body_preview(msg):
    for part in msg.walk():
        if part.get_content_type() == "text/plain" and not part.get_filename():
            try:
                txt = part.get_payload(decode=True)
                return (txt.decode(part.get_content_charset() or "utf-8", "replace")
                        if txt else "")[:1000]
            except Exception:
                return ""
    return ""


def cmd_scan(args):
    # 注: この Mail V10 の Envelope Index では messages.date_received は Unix epoch。
    # 実測で確認済み(raw 1784382632 → 2026-07-18、`datetime(...,'unixepoch')` が正しい年月日を返す)。
    # 旧 macOS の Cocoa epoch(2001基準)ではないため、Unix epoch の cutoff をそのまま比較する。
    state = load_state(args.state)
    if args.since:
        since = args.since
        cutoff = int(datetime.datetime.fromisoformat(args.since).timestamp())
    elif state.get("last_scan"):
        since = state["last_scan"]
        cutoff = int(datetime.datetime.fromisoformat(since).timestamp())
    else:
        ys = datetime.datetime(datetime.datetime.now().year, 1, 1)
        since = ys.isoformat(timespec="seconds")
        cutoff = int(ys.timestamp())
    scan_started = datetime.datetime.now().astimezone().isoformat(timespec="seconds")

    conn = open_envelope_index(ENVELOPE_INDEX)
    try:
        rows = query_attachment_messages(conn, cutoff)
        # skipped の ROWID は cutoff と無関係に毎回再解決対象へ加える
        by_id = {r["rowid"]: r for r in rows}
        for r in query_messages_by_rowids(conn, state["skipped"]):
            by_id.setdefault(r["rowid"], r)
        rows = sorted(by_id.values(),
                      key=lambda r: (-r["date_received"], -r["rowid"]))
    finally:
        conn.close()
    emlx = build_emlx_index(MAIL_ROOT)

    # 添付順位(index)は .emlx の MIME パート位置が唯一の正。DB の attachments.name は
    # 順序保証がないため、index の生成には使わない。.emlx 未在/解析不可は skipped に
    # 明示追跡し、次回スキャンで再試行する(cursor はピン留めしない)。
    messages, seen = [], set()
    new_skipped = {}
    for r in rows:
        path = emlx.get(str(r["rowid"]))
        msg = None
        if path and os.path.exists(path):
            try:
                msg = read_emlx(path)
            except Exception:
                msg = None
        if msg is None:
            print("skip rowid %d: .emlx 未在/解析不可(次回再スキャン)" % r["rowid"],
                  file=sys.stderr)
            new_skipped[str(r["rowid"])] = {
                "date": r["date_received"], "at": scan_started}
            continue
        parts = pdf_parts(msg)
        if not parts:
            continue
        mid = emlx_message_id(msg) or ("rowid:%d" % r["rowid"])
        if mid in seen:
            continue
        seen.add(mid)
        state["sources"][mid] = r["rowid"]
        messages.append({
            "message_id": mid,
            "date": datetime.datetime.fromtimestamp(r["date_received"]).astimezone()
                    .isoformat(timespec="seconds"),
            "sender": r["sender"], "subject": r["subject"],
            "body_preview": _body_preview(msg),
            "pdf_attachments": [{"index": i, "name": n} for i, n, _ in parts]})

    pending, candidates = build_candidates(state, messages)
    state["pending"] = pending
    state["skipped"] = new_skipped
    save_state(state, args.state)      # 候補 + sources + skipped を先に永続化
    # cursor は常に scan_started へ前進(未解決は skipped で再試行するため巻き戻さない)
    state["last_scan"] = scan_started
    save_state(state, args.state)
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
    emlx = build_emlx_index(MAIL_ROOT)
    results, ok = {}, True
    for mid in args.message_ids:
        targets = plan_extract_targets(state, mid)
        if not targets:
            print("no pending attachments for %s" % mid, file=sys.stderr); ok = False; continue
        rowid = state.get("sources", {}).get(mid)
        path = emlx.get(str(rowid)) if rowid is not None else None
        if not path or not os.path.exists(path):
            print("emlx not found for %s (再スキャンしてください)" % mid, file=sys.stderr)
            ok = False; continue
        try:
            parts = {(i, n): p for i, n, p in pdf_parts(read_emlx(path))}
        except Exception as e:
            print("emlx parse failed for %s: %s" % (mid, e), file=sys.stderr); ok = False; continue
        for idx, name, fname in targets:
            key = attachment_key(mid, idx, name)
            payload = parts.get((idx, name))
            if payload is None:
                print("attachment %d of %s は未ダウンロード。Mail で対象メールを開いて"
                      "添付を DL してから再実行してください。" % (idx, mid), file=sys.stderr)
                ok = False; continue
            dst = os.path.join(args.out, fname)
            with open(dst, "wb") as f:
                f.write(payload)
            results[key] = dst
    print(json.dumps(results, ensure_ascii=False))
    return 0 if ok else 1


def cmd_mark(args):
    state = load_state(args.state)
    meta = (
        state["pending"].pop(args.key, None)
        or state["failed"].pop(args.key, None)
        or {}
    )
    now = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    if args.uploaded:
        state["uploaded"][args.key] = {"file_id": args.uploaded, "at": now}
    else:
        entry = {"error": args.failed, "at": now}
        entry.update(
            {
                k: v
                for k, v in meta.items()
                if k in ("subject", "sender", "date", "amounts")
            }
        )
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
    p = sub.add_parser("scan")
    p.add_argument("--state", default=STATE_PATH)
    p.add_argument("--since")
    p.set_defaults(fn=cmd_scan)
    p = sub.add_parser("extract")
    p.add_argument("--state", default=STATE_PATH)
    p.add_argument("--out", required=True)
    p.add_argument("message_ids", nargs="+")
    p.set_defaults(fn=cmd_extract)
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
