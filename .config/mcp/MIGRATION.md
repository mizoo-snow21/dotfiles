# MCP設定の移行ガイド

既存の`mcp.json`から新しいセキュアな設定方法への移行手順です。

## 移行手順

### 1. 現在のAPIキーを確認

現在の`.cursor/mcp.json`からAPIキーをコピーしてください。

### 2. 環境変数を設定

`~/.zshrc`または`~/.zprofile`に以下を追加:

```bash
# MCP Configuration
export CONTEXT7_API_KEY="your-api-key-here"
```

### 3. シェルを再読み込み

```bash
source ~/.zshrc
# または
source ~/.zprofile
```

### 4. 新しい設定をセットアップ

```bash
cd ~/dotfiles
./scripts/setup-mcp.sh
```

### 5. 既存の設定ファイルを削除（オプション）

新しい設定が動作することを確認したら、既存の`.cursor/mcp.json`を削除できます（シンボリックリンクに置き換わっているはずです）。

```bash
# 確認
ls -la ~/.cursor/mcp.json
# シンボリックリンクになっていることを確認

# もし通常のファイルのままなら、バックアップしてから削除
mv ~/.cursor/mcp.json ~/.cursor/mcp.json.old
```

## 確認

設定が正しく動作しているか確認:

1. Cursorを再起動
2. MCPサーバーが接続されているか確認
3. 必要に応じてClaude Desktop/Codeも再起動

## トラブルシューティング

### 環境変数が読み込まれない場合

```bash
# 環境変数を確認
echo $CONTEXT7_API_KEY

# 設定されていない場合、~/.zshrcに追加して再読み込み
```

### シンボリックリンクが作成されない場合

手動で作成:

```bash
ln -sf ~/dotfiles/.config/mcp/mcp.json.local ~/.cursor/mcp.json
```
