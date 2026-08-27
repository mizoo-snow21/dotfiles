#!/bin/bash

# Codex CLI プラグイン一括インストールスクリプト
# ~/.codex/config.toml はマシン状態(trust_level, hooks hash 等)を含むため gitignore 対象。
# よって「どのプラグインを入れるか」の唯一の情報源はこの配列。
# ponytail: プラグインを増やすときは下の配列に1行足す

set -euo pipefail

# marketplace ソース (owner/repo | HTTPS/SSH URL | ローカルパス)
MARKETPLACES=(
    "michael-denyer/pstack-claude"
)

# <plugin>@<marketplace>
PLUGINS=(
    "pstack@pstack-claude"
)

# 並列サブエージェント系スキル (arena/interrogate/how/why/reflect/architect) に必要
FEATURES=(
    "multi_agent"
)

CODEX_CONFIG="${HOME}/.codex/config.toml"

echo "🔌 Installing Codex plugins..."

if ! command -v codex &> /dev/null; then
    echo "⚠️  codex CLI not found. Skipping Codex plugin installation."
    exit 0
fi

# ==============================================================================
# Marketplaces
# ==============================================================================

echo ""
echo "📦 Setting up marketplaces..."

known_marketplaces="$(codex plugin marketplace list 2>/dev/null || true)"

for src in "${MARKETPLACES[@]}"; do
    name="${src##*/}"
    if grep -qF "$name" <<< "$known_marketplaces"; then
        echo "✅ $name marketplace already configured"
    else
        echo "📥 Adding $name marketplace..."
        codex plugin marketplace add "$src"
    fi
done

# ==============================================================================
# Plugins
# ==============================================================================

echo ""
echo "🔧 Installing plugins..."

known_plugins="$(codex plugin list 2>/dev/null || true)"

for plugin in "${PLUGINS[@]}"; do
    if grep -qF "$plugin" <<< "$known_plugins" && grep -qF "installed" <<< "$(grep -F "$plugin" <<< "$known_plugins")"; then
        echo "✅ $plugin already installed"
    else
        echo "📥 Installing $plugin..."
        codex plugin add "$plugin"
    fi
done

# ==============================================================================
# Features
# ==============================================================================

echo ""
echo "🚩 Enabling features..."

for feature in "${FEATURES[@]}"; do
    if grep -qE "^[[:space:]]*${feature}[[:space:]]*=" "$CODEX_CONFIG" 2>/dev/null; then
        echo "✅ features.$feature already set"
    elif grep -qE '^\[features\]' "$CODEX_CONFIG" 2>/dev/null; then
        # [features] テーブルが既にある。2つ目を追記すると TOML の重複テーブルで壊れるので直下に差し込む
        awk -v f="$feature" '/^\[features\]/ { print; print f " = true"; next } { print }' \
            "$CODEX_CONFIG" > "${CODEX_CONFIG}.tmp" && mv "${CODEX_CONFIG}.tmp" "$CODEX_CONFIG"
        echo "🚩 Enabled features.$feature"
    else
        printf '\n[features]\n%s = true\n' "$feature" >> "$CODEX_CONFIG"
        echo "🚩 Enabled features.$feature"
    fi
done

echo ""
echo "🎉 Codex plugins installation completed!"
