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

`skills-list.txt` は手動編集しません。`scripts/sync-agent-skills-list.sh` が
`~/.agents/.skill-lock.json`（実際にグローバルインストール済みのスキルの正）から自動生成します。

スキルを追加/削除したら:
```bash
npx skills add <owner/repo>@<skill> -g -y   # または npx skills remove
cd ~/dotfiles
./scripts/sync-agent-skills-list.sh          # skills-list.txt と skill-lock.json を最新化
git add .config/agent-skills && git commit -m "..."
```

`.config/agent-skills/skill-lock.json` は `~/.agents/.skill-lock.json` のコピー(参照用、
インストール日時やハッシュなどの provenance を確認する用途)。

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
