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
