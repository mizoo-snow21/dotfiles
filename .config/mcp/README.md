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
- **Claude Desktop**: `~/Library/Application Support/Claude/claude_desktop_config.json` (JSON形式)
- **Claude Code CLI**: `~/.claude.json` の `mcpServers` (Claude Desktopとは別ファイル。上記テンプレートの対象外)

設定は各ツールにシンボリックリンクで共有されます。CodexはMCP設定を行わず、`~/.codex/config.toml`は別途手動管理します。

## Claude Code CLI の MCP サーバー登録

Claude Code CLI は `~/.claude.json` を直接読むため、上のテンプレート方式ではカバーできません。
`claude mcp add` コマンドで冪等に登録します:

```bash
export MFC_CA_MCP_URL="社内ベータエンドポイントのURL"  # 実行するシェルセッションで指定するだけでよい(このリポジトリには書かない)
cd ~/dotfiles
./scripts/setup-claude-code-mcp.sh
```

`MFC_CA_MCP_URL` は社内インフラの詳細を含むため、このリポジトリ(public)にはコミットしません。
未設定のまま実行すると対話的にプロンプトされます。

新しいサーバーを追加する場合は `scripts/setup-claude-code-mcp.sh` に登録ブロックを追記してください。
OAuth connector（claude.ai Google Drive 等）やプラグイン付随の MCP（claude-mem 等）はスクリプトの対象外です
（前者はスクリプト化に向かず、後者はプラグインのインストールに付随して自動的に登録されるため）。
