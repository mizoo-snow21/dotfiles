#!/usr/bin/env bash
set -euo pipefail

INPUT=$(cat)
FILE_PATH=$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // empty')

command -v codex >/dev/null 2>&1 || exit 0
[ -n "$FILE_PATH" ] || exit 0

BASENAME=$(basename "$FILE_PATH")
case "$BASENAME" in
  *[Tt][Oo][Dd][Oo]*.md | *[Pp][Ll][Aa][Nn]*.md | *[Ss][Pp][Ee][Cc]*.md) ;;
  *) exit 0 ;;
esac
[ -f "$FILE_PATH" ] || exit 0

CWD=$(printf '%s' "$INPUT" | jq -r '.cwd // empty')

CLAUDE_MD=""
for candidate in "$CWD/CLAUDE.md" "$CWD/.claude/CLAUDE.md"; do
  if [ -n "$candidate" ] && [ -f "$candidate" ]; then
    CLAUDE_MD="$candidate"
    break
  fi
done

REF_ARG=""
if [ -n "$CLAUDE_MD" ]; then
  REF_ARG=" (ref: $CLAUDE_MD)"
fi

MODELS=("gpt-5.4" "gpt-5.3-codex" "gpt-5.2-codex" "gpt-5.2" "gpt-5.1-codex-max")

STATE_DIR="${TMPDIR:-/tmp}/codex-review-plan-state"
mkdir -p "$STATE_DIR"
FILE_HASH=$(printf '%s' "$FILE_PATH" | shasum -a 256 | awk '{print $1}')
STATE_FILE="$STATE_DIR/$FILE_HASH"

OUTPUT_FILE=$(mktemp)
JSONL_FILE=$(mktemp)
SCHEMA_FILE=$(mktemp)
REVIEW_OK=false
trap 'rm -f "$OUTPUT_FILE" "$JSONL_FILE" "$SCHEMA_FILE"' EXIT

cat > "$SCHEMA_FILE" <<'EOF'
{
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "status": {
      "type": "string",
      "enum": ["no_findings", "needs_changes"]
    },
    "summary": {
      "type": "string"
    }
  },
  "required": ["status", "summary"]
}
EOF

run_review() {
  local mode="$1"
  local prompt="$2"
  local model
  : > "$JSONL_FILE"
  : > "$OUTPUT_FILE"

  for model in "${MODELS[@]}"; do
    if [ "$mode" = "resume" ]; then
      if codex exec resume -m "$model" --json -o "$OUTPUT_FILE" "$SESSION_ID" "$prompt" > "$JSONL_FILE" 2>/dev/null && normalize_review_output; then
        USED_MODEL="$model"
        return 0
      fi
    elif codex exec -m "$model" --json --output-schema "$SCHEMA_FILE" -o "$OUTPUT_FILE" "$prompt" > "$JSONL_FILE" 2>/dev/null && normalize_review_output; then
      USED_MODEL="$model"
      return 0
    fi
  done

  return 1
}

normalize_review_output() {
  python3 - "$OUTPUT_FILE" <<'PY'
import json
import pathlib
import re
import sys

path = pathlib.Path(sys.argv[1])
text = path.read_text(encoding='utf-8').strip()
candidates = [text]

if text.startswith("```"):
    stripped = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.S)
    candidates.append(stripped.strip())

for candidate in candidates:
    if not candidate:
        continue
    try:
        obj = json.loads(candidate)
    except Exception:
        continue
    if obj.get("status") in {"no_findings", "needs_changes"} and isinstance(obj.get("summary"), str):
        path.write_text(json.dumps(obj), encoding='utf-8')
        sys.exit(0)

sys.exit(1)
PY
}

if [ -s "$STATE_FILE" ]; then
  SESSION_ID=$(cat "$STATE_FILE")
  PROMPT="The document was updated. Review it again. Do not nitpick. Only point out critical issues. Respond with raw JSON only, no code fences and no extra prose. Use this shape exactly: {\"status\":\"no_findings\"|\"needs_changes\",\"summary\":\"...\"}. Set status to no_findings when there are no critical issues. Set status to needs_changes when critical issues remain, and put a concise flat bullet list in summary: ${FILE_PATH}${REF_ARG}"
  run_review "resume" "$PROMPT" && REVIEW_OK=true
fi

if [ "$REVIEW_OK" != "true" ]; then
  PROMPT="Review this document. Do not nitpick. Only point out critical issues. Respond using the schema only. Set status to no_findings when there are no critical issues. Set status to needs_changes when critical issues remain, and put a concise flat bullet list in summary: ${FILE_PATH}${REF_ARG}"
  run_review "fresh" "$PROMPT" && REVIEW_OK=true
fi

SESSION_ID=$(
  jq -r '
    if .type == "session_meta" then
      .payload.id // empty
    elif .type == "thread.started" then
      .thread_id // empty
    else
      empty
    end
  ' "$JSONL_FILE" 2>/dev/null | head -1
)
if [ -n "$SESSION_ID" ]; then
  printf '%s' "$SESSION_ID" > "$STATE_FILE"
fi

if [ "$REVIEW_OK" != "true" ] || [ ! -s "$OUTPUT_FILE" ]; then
  exit 0
fi

STATUS=$(jq -r '.status // empty' "$OUTPUT_FILE" 2>/dev/null)
SUMMARY=$(jq -r '.summary // empty' "$OUTPUT_FILE" 2>/dev/null)

if [ "$STATUS" = "no_findings" ]; then
  jq -n --arg file "$FILE_PATH" --arg model "${USED_MODEL:-unknown}" '{
    hookSpecificOutput: {
      hookEventName: "PostToolUse",
      additionalContext: ("Codex review (" + $model + ") passed with no findings for: " + $file)
    }
  }'
  exit 0
fi

[ "$STATUS" = "needs_changes" ] || exit 0
[ -n "$SUMMARY" ] || SUMMARY="- Codex reported critical issues, but did not provide details."

jq -n --arg file "$FILE_PATH" --arg summary "$SUMMARY" --arg model "${USED_MODEL:-unknown}" '{
  hookSpecificOutput: {
    hookEventName: "PostToolUse",
    additionalContext: (
      "Codex review (" + $model + ") found critical issues in: " + $file + "\n\n" + $summary +
      "\n\nFix the critical issues above in this document, then write the file again. The review will re-run automatically until Codex reports no_findings."
    )
  }
}'
