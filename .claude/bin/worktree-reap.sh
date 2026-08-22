#!/usr/bin/env bash
# 使い終わった git worktree を「退避してから自動削除」する。
#
# 設計（codex レビューを反映）:
#   - PR の状態は「作業が終わった」の代理指標にすぎない。PR とローカルファイルは別物なので、
#     PR merged だけを根拠に消さない。untracked を必ず退避してから消す。
#   - 退避先（attic）は成果物の保管場所ではなく **事故回収層**。恒久的な成果物は
#     最初から worktree の外（~/.claude/artifacts/ 等）へ書くのが本筋。
#   - シークレットは attic に平文で置かない。パスとサイズだけ manifest に残す。
#
# 削除条件（すべて満たしたときだけ）:
#   1. PR が MERGED（または upstream ブランチが消えている）
#   2. その worktree を cwd にしているプロセスが居ない
#   3. 今のシェルがその worktree の中に居ない
#   4. 退避が成功した
set -uo pipefail

DRY=0; [ "${1:-}" = "--dry-run" ] && DRY=1
# 退避先は dotfiles リポジトリの外へ置く。
# 中に置くと `git clean -fdx` で「事故回収のための退避データ」ごと消える。
ATTIC="${WORKTREE_ATTIC:-${XDG_STATE_HOME:-$HOME/.local/state}/claude/worktree-attic}"
ATTIC_KEEP_DAYS="${WORKTREE_ATTIC_KEEP_DAYS:-30}"
MAX_FILE_KB="${WORKTREE_SALVAGE_MAX_KB:-2048}"

git rev-parse --git-dir >/dev/null 2>&1 || exit 0
command -v gh >/dev/null 2>&1 || { echo "gh が必要です" >&2; exit 0; }

root=$(git rev-parse --show-toplevel)
repo=$(basename "$root")
here=$(pwd -P)
git fetch origin --quiet 2>/dev/null || true

# 退避しないもの（生成物・巨大・秘密）
SKIP_RE='(^|/)(node_modules|\.next|dist|build|coverage|\.turbo|\.vercel|\.pnpm-store)/'
SECRET_RE='(^|/)(\.env([^/]*)?|[^/]*\.(pem|key|p12|keystore))$'

salvage() {  # $1=worktree  $2=dest ; 退避できたら0
  local wt="$1" dest="$2" n=0 sec=0
  mkdir -p "$dest" || return 1
  : > "$dest/MANIFEST.txt"
  # 追跡外 かつ ignore されていないファイルだけ（生成物は ignore 済みなので自然に外れる）
  while IFS= read -r f; do
    [ -z "$f" ] && continue
    [[ "$f" =~ $SKIP_RE ]] && continue
    local src="$wt/$f"
    [ -f "$src" ] || continue
    local kb=$(( ( $(wc -c < "$src" 2>/dev/null || echo 0) + 1023 ) / 1024 ))
    if [[ "$f" =~ $SECRET_RE ]]; then
      printf 'SECRET(未退避) %s  %sKB\n' "$f" "$kb" >> "$dest/MANIFEST.txt"; sec=$((sec+1)); continue
    fi
    if [ "$kb" -gt "$MAX_FILE_KB" ]; then
      printf 'TOO_LARGE(未退避) %s  %sKB\n' "$f" "$kb" >> "$dest/MANIFEST.txt"; continue
    fi
    mkdir -p "$dest/files/$(dirname "$f")" && cp -p "$src" "$dest/files/$f" || return 1
    printf 'saved %s  %sKB\n' "$f" "$kb" >> "$dest/MANIFEST.txt"; n=$((n+1))
  done < <(cd "$wt" && git ls-files --others --exclude-standard 2>/dev/null)
  # 追跡ファイルの未コミット差分も残す
  (cd "$wt" && git diff HEAD > "$dest/uncommitted.diff" 2>/dev/null) || true
  [ -s "$dest/uncommitted.diff" ] || rm -f "$dest/uncommitted.diff"
  echo "$n:$sec"
  return 0
}

reaped=0
while IFS=$'\t' read -r wt br; do
  [ -z "$wt" ] || [ "$wt" = "$root" ] && continue
  name=$(basename "$wt")
  case "$here" in "$wt"*) echo "  skip $name (このシェルが中に居る)"; continue;; esac

  pr=$(gh pr list --head "$br" --state all --limit 1 --json number,state \
        --jq 'if length==0 then "none" else "\(.[0].state)#\(.[0].number)" end' 2>/dev/null || echo "?")
  # 「一度も push していない」と「マージ後にリモートから消された」を区別する。
  # upstream 未設定のブランチは作業中とみなし、絶対に触らない。
  # `git worktree add -b X origin/main` は upstream を origin/main に設定するため、
  # 「upstream がある」だけでは push 済みの判定にならない。
  # upstream が **自分自身のリモート追跡ブランチ** を指しているときだけ push 済みとみなす。
  had_upstream=0
  up=$(git rev-parse --abbrev-ref --symbolic-full-name "${br}@{upstream}" 2>/dev/null || true)
  [ "$up" = "origin/$br" ] && had_upstream=1
  gone=0
  if [ "$had_upstream" -eq 1 ]; then
    git ls-remote --exit-code --heads origin "$br" >/dev/null 2>&1 || gone=1
  fi
  if [[ "$pr" != MERGED* ]] && [ "$gone" -eq 0 ]; then
    if [ "$had_upstream" -eq 0 ]; then
      ahead=$(git rev-list --count "origin/main..$br" 2>/dev/null || echo 0)
      echo "  skip $name (未 push の作業ブランチ。コミット $ahead 件)"
    else
      echo "  skip $name (PR=${pr}、リモートにブランチあり)"
    fi
    continue
  fi

  busy=""
  for p in $(pgrep -f . 2>/dev/null); do
    c=$(lsof -p "$p" -a -d cwd -Fn 2>/dev/null | sed -n 's/^n//p')
    case "$c" in "$wt"*) busy="$p"; break;; esac
  done
  [ -n "$busy" ] && { echo "  skip $name (PID $busy が使用中)"; continue; }

  dest="$ATTIC/$repo/${name}-$(date +%Y%m%d-%H%M%S)"
  if [ "$DRY" -eq 1 ]; then echo "  [dry-run] $name を退避→削除（PR=${pr}）"; reaped=$((reaped+1)); continue; fi

  res=$(salvage "$wt" "$dest") || { echo "  ⛔ $name 退避に失敗。削除しない"; continue; }
  if out=$(git worktree remove --force "$wt" 2>&1); then
    git branch -D "$br" >/dev/null 2>&1
    echo "  ✅ $name 削除（PR=${pr}、退避 ${res%%:*} 件 / 秘密 ${res##*:} 件は manifest のみ）"
    reaped=$((reaped+1))
  else
    echo "  ⛔ $name $out"
  fi
done < <(git worktree list --porcelain | awk '/^worktree /{w=$2} /^branch /{print w"\t"substr($2,12)}')

git worktree prune 2>/dev/null || true

# attic の期限切れを掃除
[ -d "$ATTIC" ] && find "$ATTIC" -mindepth 2 -maxdepth 2 -type d -mtime +"$ATTIC_KEEP_DAYS" -exec rm -rf {} + 2>/dev/null
[ "$reaped" -gt 0 ] && echo "  退避先: $ATTIC/$repo （${ATTIC_KEEP_DAYS}日で自動削除）"
exit 0
