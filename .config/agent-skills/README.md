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
- Connex: 設定により異なる

## 参考

- [Agent Skills Hub](https://installagentskills.com/)
- [npx skills documentation](https://skills.sh/docs/cli)
