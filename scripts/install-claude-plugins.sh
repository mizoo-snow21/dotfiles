#!/bin/bash

# Claude Code プラグイン一括インストールスクリプト
# settings.json の extraKnownMarketplaces / enabledPlugins を唯一の情報源として
# マーケットプレース追加 → プラグインインストールを実行します。
# ponytail: プラグインを増やすときはこのスクリプトではなく settings.json を編集する

set -euo pipefail

SETTINGS="${HOME}/.claude/settings.json"

echo "🔌 Installing Claude Code plugins..."

if ! command -v claude &> /dev/null; then
    echo "⚠️  claude CLI not found. Skipping plugin installation."
    echo "   Install Claude Code first, then re-run: ./scripts/install-claude-plugins.sh"
    exit 0
fi

if [[ ! -f "$SETTINGS" ]]; then
    echo "⚠️  $SETTINGS not found. Skipping."
    exit 0
fi

# ==============================================================================
# Marketplaces (claude-plugins-official は組み込みなので登録不要)
# ==============================================================================

echo ""
echo "📦 Setting up marketplaces..."

known_marketplaces="$(claude plugin marketplace list 2>/dev/null || true)"

while IFS=$'\t' read -r name src; do
    [[ -n "$name" ]] || continue
    if grep -qF "$name" <<< "$known_marketplaces"; then
        echo "✅ $name marketplace already configured"
    else
        echo "📥 Adding $name marketplace..."
        claude plugin marketplace add "$src"
    fi
done < <(jq -r '.extraKnownMarketplaces // {} | to_entries[]
                | "\(.key)\t\(.value.source.repo // .value.source.url)"' "$SETTINGS")

# ==============================================================================
# Plugins
# ==============================================================================

echo ""
echo "🔧 Installing plugins..."

known_plugins="$(claude plugin list 2>/dev/null || true)"

while read -r plugin; do
    [[ -n "$plugin" ]] || continue
    if grep -qF "$plugin" <<< "$known_plugins"; then
        echo "✅ $plugin already installed"
    else
        echo "📥 Installing $plugin..."
        claude plugin install "$plugin"
    fi
done < <(jq -r '.enabledPlugins // {} | keys[]' "$SETTINGS")

echo ""
echo "🎉 Claude Code plugins installation completed!"
echo "   Run '/reload-plugins' in Claude Code to activate."
