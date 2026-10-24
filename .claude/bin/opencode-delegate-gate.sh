#!/bin/bash
# PreToolUse gate: opencode-delegate スキルを読まずに opencode へ実装を投げるのを止める。
# cursor-delegate-gate.sh と同型。opencode が既定の実装経路になったので、既定側にも同じ
# enforcement を置く（CLAUDE.md は context であって enforcement ではない）。
input=$(cat)
cmd=$(printf '%s' "$input" | jq -r '.tool_input.command // ""')
transcript=$(printf '%s' "$input" | jq -r '.transcript_path // ""')

skill_loaded() {
  [ -n "$transcript" ] && [ -f "$transcript" ] || return 0
  grep -Eq "\"name\":\"Skill\",\"input\":\{\"skill\":\"$1\"[,}]" "$transcript"
}

# dispatch (`opencode run`) だけを対象。models / auth / session list / agent list /
# debug skill は素通し — セッション id の取得や疎通確認を妨げないため。
# 実行されない部分（heredoc の本文、引用符の中）を消してから、残りに opencode run が語として
# 現れるかを見る。文字列として触れているだけのコミットメッセージや grep まで止めていたため。
# ponytail: 簡易な字句処理で、シェルの構文解析はしない。見逃すのは、引用符の中の dispatch
# （bash -c '…'、"$(…)"）と、引用符やコメントの中の <<WORD に続く行。引用符なしで書いた語
# （echo opencode run、# opencode run）は止める。どれも実際の dispatch の形では起きない。
code=$(printf '%s\n' "$cmd" | awk '
  skip { if ($0 ~ "^\t*" delim "$") skip = 0; next }
  match($0, /<<-?[ \t]*["\047]?[A-Za-z_][A-Za-z0-9_]*/) {
    delim = substr($0, RSTART, RLENGTH); sub(/^<<-?[ \t]*["\047]?/, "", delim); skip = 1
  }
  { print }' | tr '\n' ' ' | sed -E "s/'[^']*'|\"([^\"\\\\]|\\\\.)*\"/ /g")
printf '%s' "$code" | grep -Eq '(^|[^[:alnum:]_.-])opencode([[:space:]]|\\)+run([[:space:]]|$)' || exit 0

skill_loaded "opencode-delegate" && exit 0

printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":%s}}' \
  "$(printf '%s' "opencode に実装を投げる前に Skill(opencode-delegate) をロードすること（このセッションで未ロード）。headless の external_directory 自動拒否（プラグインskillが読めず無言で0件終了する罠）・モデルの可用性ゲート・セッション id の取り方はスキル側にある。記憶で組み立てたコマンドは高確率で古い。ロードしてから再送して。" | jq -Rs .)"
exit 0
