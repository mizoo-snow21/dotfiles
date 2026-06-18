#!/bin/bash

# Claude Code プラグイン一括インストールスクリプト
# マーケットプレース追加 → プラグインインストールを実行します

set -e

echo "🔌 Installing Claude Code plugins..."

# claude CLIが利用可能か確認
if ! command -v claude &> /dev/null; then
    echo "⚠️  claude CLI not found. Skipping plugin installation."
    echo "   Install Claude Code first, then re-run: ./scripts/install-claude-plugins.sh"
    exit 0
fi

# ==============================================================================
# Marketplaces
# ==============================================================================

echo ""
echo "📦 Setting up marketplaces..."

# Anthropic公式マーケットプレース
if claude plugin marketplace list 2>/dev/null | grep -q "claude-code-plugins"; then
    echo "✅ claude-code-plugins marketplace already configured"
else
    echo "📥 Adding Anthropic official marketplace..."
    claude plugin marketplace add https://github.com/anthropics/claude-code
    echo "✅ Added claude-code-plugins marketplace"
fi

# ponytail マーケットプレース
if claude plugin marketplace list 2>/dev/null | grep -q "ponytail"; then
    echo "✅ ponytail marketplace already configured"
else
    echo "📥 Adding ponytail marketplace..."
    claude plugin marketplace add DietrichGebert/ponytail
    echo "✅ Added ponytail marketplace"
fi

# ==============================================================================
# Plugins
# ==============================================================================

echo ""
echo "🔧 Installing plugins..."

# code-review プラグイン
if claude plugin list 2>/dev/null | grep -q "code-review@claude-code-plugins"; then
    echo "✅ code-review already installed"
else
    echo "📥 Installing code-review..."
    claude plugin install code-review
    echo "✅ Installed code-review"
fi

# ponytail プラグイン
if claude plugin list 2>/dev/null | grep -q "ponytail@ponytail"; then
    echo "✅ ponytail already installed"
else
    echo "📥 Installing ponytail..."
    claude plugin install ponytail
    echo "✅ Installed ponytail"
fi

# 今後プラグインを追加する場合はここに追記:
# if claude plugin list 2>/dev/null | grep -q "plugin-name@marketplace"; then
#     echo "✅ plugin-name already installed"
# else
#     claude plugin install plugin-name
# fi

echo ""
echo "🎉 Claude Code plugins installation completed!"
echo "   Run '/reload-plugins' in Claude Code to activate."
