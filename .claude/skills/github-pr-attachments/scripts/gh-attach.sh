#!/usr/bin/env bash
# Upload image/video files to GitHub's user-attachments store and print Markdown
# image tags. Verifies each upload actually serves the same byte count as the
# source, so a truncated upload fails here instead of silently rendering broken.
#
#   gh-attach.sh -r owner/repo before.png after.png
#   gh-attach.sh before.png                     # repo inferred from cwd
#
# Requires: gh (authenticated), curl, python3.
set -euo pipefail

REPO=""
while getopts "r:h" opt; do
  case "$opt" in
    r) REPO="$OPTARG" ;;
    h) sed -n '2,9p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) exit 2 ;;
  esac
done
shift $((OPTIND - 1))

[ $# -gt 0 ] || { echo "usage: $(basename "$0") [-r owner/repo] FILE..." >&2; exit 2; }

if [ -z "$REPO" ]; then
  REPO=$(gh repo view --json nameWithOwner --jq .nameWithOwner) ||
    { echo "error: not in a GitHub repo; pass -r owner/repo" >&2; exit 1; }
fi

TOKEN=$(gh auth token)
REPO_ID=$(gh api "repos/$REPO" --jq .id)

mime_for() {
  case "${1##*.}" in
    png) echo image/png ;; jpg|jpeg) echo image/jpeg ;; gif) echo image/gif ;;
    webp) echo image/webp ;; svg) echo image/svg+xml ;; mp4) echo video/mp4 ;;
    mov) echo video/quicktime ;; *) echo application/octet-stream ;;
  esac
}

status=0
for FILE in "$@"; do
  [ -r "$FILE" ] || { echo "error: cannot read $FILE" >&2; status=1; continue; }
  NAME=$(basename "$FILE")
  MIME=$(mime_for "$NAME")
  SRC_SIZE=$(wc -c < "$FILE" | tr -d ' ')

  URL=$(curl -sf -X POST \
    "https://uploads.github.com/user-attachments/assets?name=$NAME&content_type=$MIME&repository_id=$REPO_ID" \
    -H "Authorization: Bearer $TOKEN" -H "Accept: application/json" \
    --data-binary "@$FILE" \
    | python3 -c 'import sys,json; print(json.load(sys.stdin)["url"])') || {
      echo "error: upload failed for $NAME" >&2; status=1; continue; }

  # The asset URL 302s to a pre-signed S3 URL. Follow it manually: curl -L would
  # forward the Authorization header to S3, which rejects it, and HEAD against
  # the signed URL fails because the signature is scoped to GET.
  LOC=$(curl -sI -H "Authorization: Bearer $TOKEN" "$URL" \
        | grep -i '^location:' | tr -d '\r' | sed 's/^[Ll]ocation: //')
  GOT_SIZE=$(curl -s -o /dev/null -w '%{size_download}' "$LOC")

  if [ "$GOT_SIZE" != "$SRC_SIZE" ]; then
    echo "error: $NAME uploaded but served $GOT_SIZE bytes, expected $SRC_SIZE" >&2
    status=1; continue
  fi
  printf '![%s](%s)\n' "${NAME%.*}" "$URL"
done
exit $status
