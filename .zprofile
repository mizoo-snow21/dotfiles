if [ -x /opt/homebrew/bin/brew ]; then
  eval "$(/opt/homebrew/bin/brew shellenv)"
elif [ -x /usr/local/bin/brew ]; then
  eval "$(/usr/local/bin/brew shellenv)"
fi

# mise: 非interactiveなコンテキスト(LSPプラグイン起動等)向けにshimsをPATHへ。
# interactive shellでは.zshrcのmise activateがこれを上書きする。
export PATH="$HOME/.local/share/mise/shims:$PATH"
