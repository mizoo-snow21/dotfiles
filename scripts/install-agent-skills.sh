#!/bin/bash

# エージェントスキル一括インストールスクリプト
# skills-list.txtに記載されたスキルを一括インストールします

set -e

DOTFILES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_LIST="$DOTFILES_DIR/.config/agent-skills/skills-list.txt"

echo "📚 Installing agent skills..."

# skills-list.txtの存在確認
if [[ ! -f "$SKILLS_LIST" ]]; then
    echo "⚠️  Skills list not found: $SKILLS_LIST"
    echo "   Creating empty skills list..."
    mkdir -p "$(dirname "$SKILLS_LIST")"
    echo "# Agent Skills List" > "$SKILLS_LIST"
    echo "# Add skills in format: owner/repo" >> "$SKILLS_LIST"
fi

# npx skillsが利用可能か確認
if ! command -v npx &> /dev/null; then
    echo "❌ npx not found. Please install Node.js first."
    exit 1
fi

# スキルリストを読み込んでインストール
installed_count=0
skipped_count=0

while IFS= read -r line || [[ -n "$line" ]]; do
    # コメント行と空行をスキップ
    if [[ "$line" =~ ^[[:space:]]*# ]] || [[ -z "${line// }" ]]; then
        continue
    fi
    
    # スキル名を取得（owner/repo形式）
    skill_name=$(echo "$line" | sed 's/[[:space:]]*#.*$//' | xargs)
    
    if [[ -z "$skill_name" ]]; then
        continue
    fi
    
    echo ""
    echo "📦 Installing: $skill_name"
    
    if npx skills add "$skill_name" 2>/dev/null; then
        echo "✅ Installed: $skill_name"
        ((installed_count++))
    else
        echo "⚠️  Failed to install: $skill_name (may already be installed)"
        ((skipped_count++))
    fi
done < "$SKILLS_LIST"

echo ""
echo "🎉 Agent skills installation completed!"
echo "   Installed: $installed_count"
echo "   Skipped/Failed: $skipped_count"
