# Agent Skills Management

このディレクトリにはエージェントスキル（Cursor、Claude Code、Connexなどで使用）の管理ファイルを配置します。

## インストール方法

### 個別インストール
```bash
npx skills add vercel-labs/agent-skills
```

### 一括インストール（推奨）
```bash
cd ~/dotfiles
./scripts/install-agent-skills.sh
```

## スキルリスト管理

`skills-list.txt`にインストールしたいスキルを記載してください。
1行に1つのスキル（`owner/repo`形式）を記載します。

## 対応ツール

- Cursor: `~/.cursor/skills/`
- Claude Code: `~/.claude/skills/`
- Codex: `~/.codex/skills/`

## 注意点

- `npx skills` が検出できたクライアントのみ自動インストールされます。
- 使うクライアントのスキル保存先が異なる場合は手動で調整が必要です。
- `install-agent-skills.sh` は Codex 用に `~/.codex/skills` を `~/.cursor/skills` へリンクします。

## 参考

- [Agent Skills Hub](https://installagentskills.com/)
- [npx skills documentation](https://skills.sh/docs/cli)
