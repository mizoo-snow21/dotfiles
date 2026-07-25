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
is_issue_create() {
  case "$cmd" in
    *"gh issue create"*) return 0 ;;
  esac
  case "$cmd" in
    *"gh api"*) ;;
    *) return 1 ;;
  esac
  # GraphQL 経路
  case "$cmd" in
    *createIssue*) return 0 ;;
  esac
  # 明示 GET は読み取り。GET はクエリパラメータも -f で渡すため、先に除外しないと誤爆する。
  case "$cmd" in
    *"-X GET"*|*"-XGET"*|*"--method GET"*) return 1 ;;
  esac
  # REST の作成先は POST /repos/{owner}/{repo}/issues だけ。
  # search/issues（検索）や /issues/<n>/... （コメント・編集・ラベル）は対象外。
  printf '%s' "$cmd" \
    | grep -Eq 'repos/[^/[:space:]]+/[^/[:space:]]+/issues([^/[:alnum:]]|$)' || return 1
  # gh api は -f / -F / --input があれば -X なしでも POST になる。
  case "$cmd" in
    *"-X POST"*|*"-XPOST"*|*"--method POST"*|*" -f "*|*" -F "*|*"--input"*) return 0 ;;
  esac
  return 1
}

is_issue_create || exit 0

skill_loaded "github-issues" && exit 0

printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":%s}}' \
  "$(printf '%s' "issue を作る前に Skill(github-issues) をロードすること（このセッションで未ロード）。作成は閲覧・コメントとは別種の行動で、手順が違う。ロードしてから再送して。" | jq -Rs .)"
exit 0
