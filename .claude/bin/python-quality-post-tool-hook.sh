#!/usr/bin/env bash
set -euo pipefail

INPUT=$(cat)
FILE_PATH=$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // empty')
case "$FILE_PATH" in
  *.py | *.pyi) ;;
  *) exit 0 ;;
esac
[ -f "$FILE_PATH" ] || exit 0

run_and_capture() {
  local output
  if output=$("$@" 2>&1); then
    printf '%s' "$output"
    return 0
  fi
  printf '%s' "$output"
  return 1
}

messages=""
ruff_check_output=$(run_and_capture uvx -q --no-progress ruff check --fix --quiet "$FILE_PATH")
ruff_check_status=$?
if [ -n "$ruff_check_output" ] || [ "$ruff_check_status" -ne 0 ]; then
  messages="${messages}ruff check --fix:\n${ruff_check_output}\n\n"
fi

ruff_format_output=$(run_and_capture uvx -q --no-progress ruff format --quiet "$FILE_PATH")
ruff_format_status=$?
if [ -n "$ruff_format_output" ] || [ "$ruff_format_status" -ne 0 ]; then
  messages="${messages}ruff format:\n${ruff_format_output}\n\n"
fi

ty_output=$(run_and_capture uvx -q --no-progress ty check --output-format concise --no-progress "$FILE_PATH")
ty_status=$?
if [ "$ty_output" = "All checks passed!" ]; then
  ty_output=""
fi
if [ -n "$ty_output" ] || [ "$ty_status" -ne 0 ]; then
  messages="${messages}ty check:\n${ty_output}\n"
fi

[ -z "$messages" ] && exit 0

jq -Rn --arg message "$messages" \
  '{hookSpecificOutput:{hookEventName:"PostToolUse",additionalContext:("Python quality hook result for the edited file.\n"+$message)}}'
