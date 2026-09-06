autoload -Uz colors && colors
PROMPT="%F{green}%n%f %F{cyan}($(arch))%f:%F{blue}%~%f"$'\n'"%# "
zstyle ":completion:*:commands" rehash 1

if type brew &>/dev/null; then
  FPATH=$(brew --prefix)/share/zsh-completions:$FPATH
  if [ -r "$(brew --prefix)/share/zsh-autosuggestions/zsh-autosuggestions.zsh" ]; then
    source "$(brew --prefix)/share/zsh-autosuggestions/zsh-autosuggestions.zsh"
  fi
  autoload -Uz compinit && compinit
fi

# bun completions
[ -s "/Users/mizoo/.bun/_bun" ] && source "/Users/mizoo/.bun/_bun"

# bun
export BUN_INSTALL="$HOME/.bun"
export PATH="$BUN_INSTALL/bin:$PATH"

# ~/.local/bin (cursor-agent, session-manager-plugin など)
export PATH="$HOME/.local/bin:$PATH"

if command -v mise >/dev/null 2>&1; then
  eval "$(mise activate zsh)"
fi

# codex は mise 管理（config.toml の npm:@openai/codex）。self-updater は install 先を
# pnpm と誤判定して `pnpm add -g` を打ち ERR_PNPM_NO_GLOBAL_BIN_DIR で落ちるので mise に振り替える
codex() {
  if [[ "$1" == update ]]; then mise up npm:@openai/codex; else command codex "$@"; fi
}
