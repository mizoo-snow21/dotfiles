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

if claude mcp get flint-chart &> /dev/null; then
    echo "✅ Already registered: flint-chart"
else
    echo "📦 Registering: flint-chart"
    claude mcp add -s user flint-chart -- npx -y flint-chart-mcp
fi

if claude mcp get ms365 &> /dev/null; then
    echo "✅ Already registered: ms365"
else
    if [[ -z "$MS365_MCP_TENANT_ID" ]]; then
        echo "⚠️  MS365_MCP_TENANT_ID environment variable is not set (Entra tenant id, not stored in this repo)"
        read -p "Enter MS365_MCP_TENANT_ID now (or press Enter to skip): " ms365_tenant
        if [[ -n "$ms365_tenant" ]]; then
            MS365_MCP_TENANT_ID="$ms365_tenant"
        else
            echo "⏭️  Skipping ms365 registration"
            MS365_MCP_TENANT_ID=""
        fi
    fi
    if [[ -n "$MS365_MCP_TENANT_ID" ]]; then
        echo "📦 Registering: ms365"
        claude mcp add -e MS365_MCP_TENANT_ID="$MS365_MCP_TENANT_ID" -s user ms365 -- npx -y @softeria/ms-365-mcp-server --preset files
    fi
fi

# pi は Claude Code の mcpServers 形式をそのまま読む（pi docs mcp.md: "Copy the existing mcpServers entry"）。
# ~/.claude.json を正本にして丸ごと写す。pi 専用のエントリは持たない。
# 一時ファイル + mv: 旧 install.sh が張った symlink が残っていても辿らず置き換える（dotfiles に秘密が落ちない）。
# `pi mcp list` は未接続サーバー（mfc_ca はサインイン前）があると exit 1 するのでここでは呼ばない。
if command -v pi &> /dev/null && command -v jq &> /dev/null; then
    mkdir -p "$HOME/.pi/agent"
    pi_mcp_tmp=$(mktemp "$HOME/.pi/agent/mcp.json.XXXXXX")
    jq '{mcpServers}' "$HOME/.claude.json" > "$pi_mcp_tmp" && mv -f "$pi_mcp_tmp" "$HOME/.pi/agent/mcp.json"
    echo "✅ Copied mcpServers to pi: ~/.pi/agent/mcp.json (run 'pi mcp login mfc_ca' once for OAuth)"
fi

echo ""
echo "🔎 Current Claude Code MCP servers:"
claude mcp list
