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

# 作成だけを対象にする。閲覧・コメント（/issues/<n>/comments）・編集（/issues/<n> -X PATCH）は素通し。
# gh api は -f / -F を付けると -X 無しでも POST になるので、明示 POST だけ見ると漏れる。
# スキル本体が「MCP は issue 作成に未対応なので gh api を使え」と指示しているため、
# gh issue create だけ見ていると推奨経路そのものが素通りする。
# 文字列として触れているだけのレポートの heredoc・コミットメッセージ・grep まで止めていたため、
# 実行されない部分を消し、コマンドごとに判定する。heredoc の本文を消したあと、引用符の外の
# ; & | と改行で分けて 1 行 1 コマンドにする（行継続と、引用符の中の改行はつなぐ）。
# args はその 1 コマンド、code はさらに引用符の中を消したもの。
# ponytail: 簡易な字句処理で、シェルの構文解析はしない。見逃すのは、引用符の中の実行
# （bash -c '…'、"$(…)"）、引用符で囲んだコマンド語（"gh" issue create）、引用符の中の
# <<WORD に続く行。どれも実際の作成の形では起きない。
commands=$(printf '%s\n' "$cmd" | awk '
  skip { if ($0 ~ "^\t*" delim "$") skip = 0; next }
  match($0, /<<-?[ \t]*["\047]?[A-Za-z_][A-Za-z0-9_.-]*/) {
    delim = substr($0, RSTART, RLENGTH); sub(/^<<-?[ \t]*["\047]?/, "", delim); skip = 1
  }
  { s = s $0 "\n" }
  END {
    for (i = 1; i <= length(s); i++) {
      ch = substr(s, i, 1)
      if (q != "") {
        if (q == "\"" && ch == "\\") { out = out ch substr(s, ++i, 1); continue }
        if (ch == q) q = ""
        out = out (ch == "\n" ? " " : ch); continue
      }
      if (ch == "\\" && substr(s, i + 1, 1) == "\n") { i++; out = out " "; continue }
      if (ch == "\047" || ch == "\"") q = ch
      out = out (ch ~ /[;&|\n]/ ? "\n" : ch)
    }
    printf "%s", out
  }')

is_issue_create() {  # $1: 1 コマンド
  local args=$1 code
  code=$(printf '%s' "$args" | sed -E "s/'[^']*'|\"([^\"\\\\]|\\\\.)*\"/ /g")
  printf '%s' "$code" | grep -Eq '(^|[^[:alnum:]_.-])gh[[:space:]]+issue[[:space:]]+create([[:space:]]|$)' && return 0
  printf '%s' "$code" | grep -Eq '(^|[^[:alnum:]_.-])gh[[:space:]]+api([[:space:]]|$)' || return 1
  # ここから先は gh api が実際に走るときだけ。作成だと決める根拠（エンドポイント、GraphQL の
  # query、-f）は引用符に入るのが普通なので args で見る。作成ではないと決める根拠（-X GET）は
  # code で見る — 本文に書いた例文の -X GET で、本物の POST を素通しさせないため。
  # GraphQL 経路
  case "$args" in
    *createIssue*) return 0 ;;
  esac
  # 明示 GET は読み取り。GET はクエリパラメータも -f で渡すため、先に除外しないと誤爆する。
  case "$code" in
    *"-X GET"*|*"-XGET"*|*"--method GET"*) return 1 ;;
  esac
  # REST の作成先は POST /repos/{owner}/{repo}/issues だけ。
  # search/issues（検索）や /issues/<n>/... （コメント・編集・ラベル）は対象外。
  printf '%s' "$args" \
    | grep -Eq 'repos/[^/[:space:]]+/[^/[:space:]]+/issues([^/[:alnum:]]|$)' || return 1
  # gh api は -f / -F / --input があれば -X なしでも POST になる。
  case "$args" in
    *"-X POST"*|*"-XPOST"*|*"--method POST"*|*" -f "*|*" -F "*|*"--input"*) return 0 ;;
  esac
  return 1
}

creates=no
while IFS= read -r c; do is_issue_create "$c" && { creates=yes; break; }; done <<< "$commands"
[ "$creates" = yes ] || exit 0

skill_loaded "github-issues" && exit 0

printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":%s}}' \
  "$(printf '%s' "issue を作る前に Skill(github-issues) をロードすること（このセッションで未ロード）。作成は閲覧・コメントとは別種の行動で、手順が違う。ロードしてから再送して。" | jq -Rs .)"
exit 0
