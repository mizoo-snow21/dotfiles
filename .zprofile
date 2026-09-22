# 下の 3 行は Docker Desktop が書いた。マーカー行を消すと次回起動時に再追記されるので原文のまま残す
# The following lines were added by Docker Desktop to add commands to your PATH.
export PATH="$PATH:/Users/mizoo/.docker/bin"
# End of Docker Desktop section.

if [ -x /opt/homebrew/bin/brew ]; then
  eval "$(/opt/homebrew/bin/brew shellenv)"
elif [ -x /usr/local/bin/brew ]; then
  eval "$(/usr/local/bin/brew shellenv)"
fi

# opencode は公式 curl インストーラ（~/.opencode/bin）。brew formula は v1 系、npm の @opencode/cli は
# mise の minimumPackageAge に引っかかるので mise/brew のどちらにも置かない。更新は `opencode upgrade`
export PATH="$HOME/.opencode/bin:$PATH"

# mise: 非interactiveなコンテキスト(LSPプラグイン起動等)向けにshimsをPATHへ。
# interactive shellでは.zshrcのmise activateがこれを上書きする。
# ~/.local/bin (hermes, cursor-agent など)。mise shims より前に置き、名前衝突時は mise が勝つ
export PATH="$HOME/.local/bin:$PATH"

export PATH="$HOME/.local/share/mise/shims:$PATH"
