#!/bin/bash

# MCP設定セットアップスクリプト
# テンプレートから環境変数を置換して設定ファイルを生成します

set -e

DOTFILES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MCP_CONFIG_DIR="$DOTFILES_DIR/.config/mcp"
JSON_TEMPLATE="$MCP_CONFIG_DIR/mcp.json.template"
JSON_LOCAL_CONFIG="$MCP_CONFIG_DIR/mcp.json.local"

echo "🔧 Setting up MCP configuration for Cursor and Claude Code..."

# テンプレートファイルの存在確認
if [[ ! -f "$JSON_TEMPLATE" ]]; then
    echo "❌ JSON template file not found: $JSON_TEMPLATE"
    exit 1
fi

# 環境変数の確認
if [[ -z "$CONTEXT7_API_KEY" ]]; then
    echo "⚠️  CONTEXT7_API_KEY environment variable is not set"
    echo "   Please set it in ~/.zshrc or ~/.zprofile:"
    echo "   export CONTEXT7_API_KEY=\"your-api-key\""
    echo ""
    read -p "Enter CONTEXT7_API_KEY now (or press Enter to skip): " api_key
    if [[ -n "$api_key" ]]; then
        export CONTEXT7_API_KEY="$api_key"
    else
        echo "⚠️  Skipping MCP configuration setup"
        exit 0
    fi
fi

# JSON設定ファイルを生成（Cursor/Claude用）
if command -v envsubst &> /dev/null; then
    envsubst < "$JSON_TEMPLATE" > "$JSON_LOCAL_CONFIG"
    echo "✅ Created JSON MCP configuration: $JSON_LOCAL_CONFIG"
elif command -v sed &> /dev/null; then
    sed "s|\${CONTEXT7_API_KEY}|$CONTEXT7_API_KEY|g" "$JSON_TEMPLATE" > "$JSON_LOCAL_CONFIG"
    echo "✅ Created JSON MCP configuration: $JSON_LOCAL_CONFIG"
else
    echo "❌ Neither envsubst nor sed found. Cannot generate configuration."
    exit 1
fi

# Cursor用にシンボリックリンクを作成
CURSOR_MCP="$HOME/.cursor/mcp.json"
if [[ -d "$(dirname "$CURSOR_MCP")" ]]; then
    if [[ -f "$CURSOR_MCP" ]] && [[ ! -L "$CURSOR_MCP" ]]; then
        echo "📋 Backing up existing Cursor MCP config"
        cp "$CURSOR_MCP" "$CURSOR_MCP.backup"
    fi
    ln -sf "$JSON_LOCAL_CONFIG" "$CURSOR_MCP"
    echo "✅ Linked MCP config to Cursor: $CURSOR_MCP"
fi

# Claude Desktop/Code用にシンボリックリンクを作成
CLAUDE_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
if [[ -d "$(dirname "$CLAUDE_CONFIG")" ]]; then
    if [[ -f "$CLAUDE_CONFIG" ]] && [[ ! -L "$CLAUDE_CONFIG" ]]; then
        echo "📋 Backing up existing Claude Desktop config"
        cp "$CLAUDE_CONFIG" "$CLAUDE_CONFIG.backup"
    fi
    ln -sf "$JSON_LOCAL_CONFIG" "$CLAUDE_CONFIG"
    echo "✅ Linked MCP config to Claude Desktop/Code: $CLAUDE_CONFIG"
fi

echo ""
echo "🎉 MCP configuration setup completed!"
echo "   Configured for: Cursor, Claude Desktop/Code"
echo "   Please restart the applications for changes to take effect."
