#!/bin/bash
# PreToolUse gate: github-issues スキルを読まずに issue を作るのを止める。
# view / comment / edit は素通し — 作成だけが別種の行動で、手順が違う。
#
# なぜフックか: CLAUDE.md やスキル一覧は context であって enforcement ではない
# （公式: "Claude treats them as context, not enforced configuration. To block an action
# regardless of what Claude decides, use a PreToolUse hook instead."）。
input=$(cat)
cmd=$(printf '%s' "$input" | jq -r '.tool_input.command // ""')
transcript=$(printf '%s' "$input" | jq -r '.transcript_path // ""')

# ponytail: セッション全体を1回 grep するだけ。時間窓なし（1セッション1ロードが意図）。
# 読めなければ fail-open — 判定できないことを理由に実作業を止めない。
skill_loaded() {
  [ -n "$transcript" ] && [ -f "$transcript" ] || return 0
  # [,}] : args 付きロード {"skill":"X","args":"..."} と args 無し {"skill":"X"} の両方を拾う
  grep -Eq "\"name\":\"Skill\",\"input\":\{\"skill\":\"$1\"[,}]" "$transcript"
}

case "$cmd" in
  *"gh issue create"*) ;;
  *) exit 0 ;;
esac

skill_loaded "github-issues" && exit 0

printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":%s}}' \
  "$(printf '%s' "issue を作る前に Skill(github-issues) をロードすること（このセッションで未ロード）。作成は閲覧・コメントとは別種の行動で、手順が違う。ロードしてから再送して。" | jq -Rs .)"
exit 0
