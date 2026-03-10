# MCP Configuration

このディレクトリにはMCP（Model Context Protocol）サーバーの設定を管理します。

## セットアップ

1. 環境変数を設定（`~/.zshrc`または`~/.zprofile`に追加）:
   ```bash
   export CONTEXT7_API_KEY="your-api-key-here"
   ```

2. テンプレートから設定ファイルを生成:
   ```bash
   cd ~/dotfiles
   ./scripts/setup-mcp.sh
   ```

## ファイル説明

- `mcp.json.template` - テンプレートファイル（Git管理）
- `mcp.json.local` - ローカル設定ファイル（.gitignore対象）

## 対応ツール

- **Cursor**: `~/.cursor/mcp.json` (JSON形式)
- **Claude Desktop/Code**: `~/Library/Application Support/Claude/claude_desktop_config.json` (JSON形式)

設定は各ツールにシンボリックリンクで共有されます。CodexはMCP設定を行わず、`~/.codex/config.toml`は別途手動管理します。
