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

# pnpm
export PNPM_HOME="$HOME/Library/pnpm"
export PATH="$PNPM_HOME:$PATH"

if command -v mise >/dev/null 2>&1; then
  eval "$(mise activate zsh)"
fi
