#!/bin/bash
# cursor-delegate-gate.sh の判定テスト。実行: bash .claude/bin/cursor-delegate-gate.test.sh
gate="$(dirname "$0")/cursor-delegate-gate.sh"
transcript=$(mktemp)  # スキル未ロードのセッション
trap 'rm -f "$transcript"' EXIT
fail=0

check() {  # check <deny|allow> <command>
  out=$(jq -n --arg c "$2" --arg t "$transcript" '{tool_input:{command:$c},transcript_path:$t}' | "$gate")
  got=allow; [[ $out == *'"deny"'* ]] && got=deny
  [ "$got" = "$1" ] || { echo "FAIL: want $1, got $got: $2"; fail=1; }
}

check deny  'cursor agent -p --model x "do it"'
check deny  'cd /r && cursor-agent --print --model x "do it"'
check deny  $'cursor agent -p --resume "$CHAT" "$(cat <<\'EOF\'\ndo it\nEOF\n)"'
check deny  $'cat > r.md <<\'END-REPORT\'\nnotes\nEND-REPORT\ncursor agent -p "do it"'
check allow 'git commit -m "gate: stop denying cursor agent -p mentions"'
check allow $'cat > r.md <<\'EOF\'\nrun cursor agent -p to dispatch\nEOF'
check allow "grep -n 'cursor agent -p' SKILL.md"
check allow $'cat <<\'END.REPORT\'\nENDxREPORT\ncursor agent -p\nEND.REPORT'
check allow 'cursor agent create-chat'

[ $fail = 0 ] && echo PASS
exit $fail
