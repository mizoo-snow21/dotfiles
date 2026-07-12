#!/bin/bash

# Claude Code CLI (~/.claude.json の mcpServers) 向けの MCP サーバー登録スクリプト。
# 冪等: 既に登録済みのサーバーはスキップする。
# OAuth connector (claude.ai Google Drive 等) やプラグイン付随の MCP はここでは扱わない。

set -e

if ! command -v claude &> /dev/null; then
    echo "❌ claude CLI not found. Install Claude Code first."
    exit 1
fi

if claude mcp get mfc_ca &> /dev/null; then
    echo "✅ Already registered: mfc_ca"
else
    if [[ -z "$MFC_CA_MCP_URL" ]]; then
        echo "⚠️  MFC_CA_MCP_URL environment variable is not set (internal endpoint, not stored in this repo)"
        read -p "Enter MFC_CA_MCP_URL now (or press Enter to skip): " mfc_ca_url
        if [[ -n "$mfc_ca_url" ]]; then
            MFC_CA_MCP_URL="$mfc_ca_url"
        else
            echo "⏭️  Skipping mfc_ca registration"
            MFC_CA_MCP_URL=""
        fi
    fi
    if [[ -n "$MFC_CA_MCP_URL" ]]; then
        echo "📦 Registering: mfc_ca"
        claude mcp add -s user --transport http mfc_ca "$MFC_CA_MCP_URL"
    fi
fi

if claude mcp get gitnexus &> /dev/null; then
    echo "✅ Already registered: gitnexus"
else
    echo "📦 Registering: gitnexus"
    claude mcp add -s user gitnexus -- npx -y gitnexus mcp
fi

echo ""
echo "🔎 Current Claude Code MCP servers:"
claude mcp list
