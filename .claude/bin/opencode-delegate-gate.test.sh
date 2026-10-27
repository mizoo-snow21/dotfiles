#!/bin/bash
# opencode-delegate-gate.sh の判定テスト。実行: bash .claude/bin/opencode-delegate-gate.test.sh
gate="$(dirname "$0")/opencode-delegate-gate.sh"
transcript=$(mktemp)  # スキル未ロードのセッション
trap 'rm -f "$transcript"' EXIT
fail=0

check() {  # check <deny|allow> <command>
  out=$(jq -n --arg c "$2" --arg t "$transcript" '{tool_input:{command:$c},transcript_path:$t}' | "$gate")
  got=allow; [[ $out == *'"deny"'* ]] && got=deny
  [ "$got" = "$1" ] || { echo "FAIL: want $1, got $got: $2"; fail=1; }
}

check deny  'opencode run --standalone -m x "do it"'
check deny  'cd /tmp/p && opencode run -m x "do it"'
check deny  'env OPENCODE_X=1 ~/.local/bin/opencode run -m x "do it"'
check deny  $'opencode \\\n  run -m x "do it"'
check deny  $'opencode run -s "$SID" -m x "$(cat <<\'EOF\'\ndo it\nEOF\n)"'
check deny  $'cat > r.md <<\'END-REPORT\'\nnotes\nEND-REPORT\nopencode run -m x "do it"'
check allow 'git commit -m "fix; opencode run gate"'
check allow $'git commit -F - <<\'EOF\'\nopencode run gate\nEOF'
check allow "grep -n 'opencode run' SKILL.md"
check allow 'opencode session list'

[ $fail = 0 ] && echo PASS
exit $fail
