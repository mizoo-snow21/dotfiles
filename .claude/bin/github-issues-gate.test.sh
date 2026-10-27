#!/bin/bash
# github-issues-gate.sh の判定テスト。実行: bash .claude/bin/github-issues-gate.test.sh
gate="$(dirname "$0")/github-issues-gate.sh"
transcript=$(mktemp)  # スキル未ロードのセッション
trap 'rm -f "$transcript"' EXIT
fail=0

check() {  # check <deny|allow> <command>
  out=$(jq -n --arg c "$2" --arg t "$transcript" '{tool_input:{command:$c},transcript_path:$t}' | "$gate")
  got=allow; [[ $out == *'"deny"'* ]] && got=deny
  [ "$got" = "$1" ] || { echo "FAIL: want $1, got $got: $2"; fail=1; }
}

check deny  'gh issue create --title x --body y'
check deny  'cd /r && gh issue create -t x -b y'
check deny  $'gh issue create -t x --body "$(cat <<\'EOF\'\nbody\nEOF\n)"'
check deny  'gh api repos/o/r/issues -f title=x'
check deny  'gh api "repos/o/r/issues" -f title=x'
check deny  "gh api graphql -f query='mutation { createIssue(input:{}) { issue { id } } }'"
check deny  $'cat > r.md <<\'END-REPORT\'\nnotes\nEND-REPORT\ngh issue create -t x -b y'
check deny  'gh api repos/o/r/issues -f title=x -f body="Example: gh api user -X GET"'
check deny  $'gh api repos/o/r/issues -X GET\ngh api repos/o/r/issues -X POST -f title=x'
check deny  $'gh api repos/o/r/issues \\\n  -X POST \\\n  -f title=x'
check deny  $'gh api repos/o/r/issues -X GET && \\\ngh api repos/o/r/issues -X POST -f title=x'
check deny  'gh api -f title="Fix A; fix B" repos/o/r/issues'
check allow 'git commit -m "Document gate; gh issue create --title x"'
check allow $'gh api user\ncat > r.md <<\'EOF\'\nmutation { createIssue }\nEOF'
check allow "gh api user && printf '%s' 'Example: createIssue'"
check allow $'cat > report.md <<\'EOF\'\nthe gate fired on gh issue create\nEOF'
check allow 'git commit -m "gate: stop denying gh issue create mentions"'
check allow "grep -n 'gh issue create' SKILL.md"
check allow 'gh api repos/o/r/issues/5/comments -f body=x'

[ $fail = 0 ] && echo PASS
exit $fail
