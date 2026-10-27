#!/bin/bash
# PreToolUse gate: cursor-delegate スキルを読まずに Cursor へ実装を投げるのを止める。
#
# なぜフックか: CLAUDE.md やスキル一覧は context であって enforcement ではない
# （公式: "Claude treats them as context, not enforced configuration. To block an action
# regardless of what Claude decides, use a PreToolUse hook instead."）。散文はロード確率を
# 上げるだけで確実性には届かない。
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

# 実際の dispatch (-p / --print) だけを対象にする。
# create-chat / ls / models / status / --help は素通し: chatId の発行を妨げないため。
# 実行されない部分（heredoc の本文、引用符の中）を消してから判定する。文字列として触れている
# だけのコミットメッセージやレポートの heredoc まで止めていたため。消し方と見逃す形
# （bash -c '…' の中の dispatch など）は opencode-delegate-gate.sh と同じ。
code=$(printf '%s\n' "$cmd" | awk '
  skip { line = $0; sub(/^\t+/, "", line); if (line == delim) skip = 0; next }
  match($0, /<<-?[ \t]*["\047]?[A-Za-z_][A-Za-z0-9_.-]*/) {
    delim = substr($0, RSTART, RLENGTH); sub(/^<<-?[ \t]*["\047]?/, "", delim); skip = 1
  }
  { print }' | tr '\n' ' ' | sed -E "s/'[^']*'|\"([^\"\\\\]|\\\\.)*\"/ /g")
printf '%s' "$code" | grep -Eq '(^|[^[:alnum:]_.-])cursor([[:space:]]+|-)agent([[:space:]]|$)' || exit 0
printf '%s' "$code" | grep -Eq '[[:space:]](-p|--print)([[:space:]]|$)' || exit 0

skill_loaded "cursor-delegate" && exit 0

printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":%s}}' \
  "$(printf '%s' "Cursor に実装を投げる前に Skill(cursor-delegate) をロードすること（このセッションで未ロード）。モデル id・chatId の取り方（cursor agent create-chat）・quota fallback・プロンプトに貼るべき制約はスキル側にある。記憶で組み立てたコマンドは高確率で古い。ロードしてから再送して。" | jq -Rs .)"
exit 0
