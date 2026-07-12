#!/bin/bash
# PreToolUse guard: codex exec はフォアグラウンド + stdin 閉鎖を強制する
# 根拠: 2026-07-09 実測 — バックグラウンド化された codex exec は stdin パイプ待ちで永久ハング
input=$(cat)
cmd=$(printf '%s' "$input" | jq -r '.tool_input.command // ""')
bg=$(printf '%s' "$input" | jq -r '.tool_input.run_in_background // false')

case "$cmd" in
  *"codex exec"*) ;;
  *) exit 0 ;;
esac

deny() {
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":%s}}' \
    "$(printf '%s' "$1" | jq -Rs .)"
  exit 0
}

if [ "$bg" = "true" ]; then
  deny "codex exec は run_in_background 禁止（バックグラウンドでは stdin パイプ待ちで永久ハングする）。フォアグラウンドで、'< /dev/null' 付きで再実行して。"
fi

case "$cmd" in
  *"< /dev/null"*|*"</dev/null"*) ;;
  *) deny "codex exec には stdin 閉鎖 '< /dev/null' が必須（ハーネスに途中でバックグラウンド変換されてもハングしないように）。コマンド末尾に付けて再送して。" ;;
esac

exit 0
