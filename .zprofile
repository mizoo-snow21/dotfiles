if [ -x /opt/homebrew/bin/brew ]; then
  eval "$(/opt/homebrew/bin/brew shellenv)"
elif [ -x /usr/local/bin/brew ]; then
  eval "$(/usr/local/bin/brew shellenv)"
fi

# mise: 非interactiveなコンテキスト(LSPプラグイン起動等)向けにshimsをPATHへ。
# interactive shellでは.zshrcのmise activateがこれを上書きする。
# ~/.local/bin (hermes, cursor-agent など)。mise shims より前に置き、名前衝突時は mise が勝つ
export PATH="$HOME/.local/bin:$PATH"

export PATH="$HOME/.local/share/mise/shims:$PATH"
