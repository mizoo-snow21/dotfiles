#!/bin/bash

# ~/.agents/.skill-lock.json (実際にインストール済みのグローバルスキルの正) から
# skills-list.txt を再生成する。スキルの追加/削除後に手動で実行してコミットする。

set -e

DOTFILES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOCK_FILE="$HOME/.agents/.skill-lock.json"
LOCK_FILE_COPY="$DOTFILES_DIR/.config/agent-skills/skill-lock.json"
SKILLS_LIST="$DOTFILES_DIR/.config/agent-skills/skills-list.txt"

if [[ ! -f "$LOCK_FILE" ]]; then
    echo "❌ Lock file not found: $LOCK_FILE"
    exit 1
fi

cp "$LOCK_FILE" "$LOCK_FILE_COPY"

python3 - "$LOCK_FILE" "$SKILLS_LIST" << 'PYEOF'
import json
import sys

lock_path, list_path = sys.argv[1], sys.argv[2]
with open(lock_path) as f:
    lock = json.load(f)

lines = [
    "# Agent Skills List",
    "# scripts/sync-agent-skills-list.sh により ~/.agents/.skill-lock.json から自動生成されます。",
    "# 手動編集しないこと。スキル追加/削除後にこのスクリプトを再実行してください。",
    "",
]
for skill_name, meta in sorted(lock.get("skills", {}).items()):
    source = meta["source"]
    lines.append(f"{source}@{skill_name}")

with open(list_path, "w") as f:
    f.write("\n".join(lines) + "\n")

print(f"✅ Wrote {len(lock.get('skills', {}))} skills to {list_path}")
PYEOF
