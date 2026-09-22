# RTK - Rust Token Killer (Codex CLI)

**Usage**: Token-optimized CLI proxy for shell commands.

## Rule

Always prefix shell commands with `rtk`.

Examples:

```bash
rtk git status
rtk cargo test
rtk npm run build
rtk pytest -q
```

## Meta Commands

```bash
rtk gain            # Token savings analytics
rtk gain --history  # Recent command savings history
rtk proxy <cmd>     # Run raw command without filtering
```

## Verification

```bash
rtk --version
rtk gain
which rtk
```

## Exception: reviewing code

コードレビューやデバッグで差分・ログを精読するときは圧縮しないこと。
`rtk proxy git diff` / `rtk proxy git show` を使い、`rtk git diff` は使わない。
情報の欠落がレビューの誤判定に直結するため。
