#!/bin/bash

# portless の起動サービス（root の launchd、443番）を入れる。sudo を使うので、エージェント経由ではなく手元のターミナルで実行する。
# portless は plist に node と portless の版付きの絶対パスを書き込むため、mise up で旧版が消えると起動しなくなる。
# 書き込まれたパスを mise の latest リンクに差し替えて、mise up のあとも起動できるようにする。

set -euo pipefail

plist=/Library/LaunchDaemons/sh.portless.proxy.plist
label=sh.portless.proxy
installs="$HOME/.local/share/mise/installs"
node="$installs/node/latest/bin/node"
cli="$installs/npm-portless/latest/node_modules/portless/dist/cli.js"

for f in "$node" "$cli"; do
    [ -e "$f" ] || { echo "❌ $f not found. Run: mise install"; exit 1; }
done

PORTLESS_SYNC_HOSTS=0 portless service install

sudo sed -i '' -E \
    -e "s#<string>$installs/node/[^<]*/bin/node</string>#<string>$node</string>#" \
    -e "s#<string>$installs/npm-portless/[^<]*/portless/dist/cli\.js</string>#<string>$cli</string>#" \
    "$plist"

if ! grep -q "<string>$node</string>" "$plist" || ! grep -q "<string>$cli</string>" "$plist"; then
    echo "❌ $plist still has versioned paths. portless may have changed its plist format."
    exit 1
fi

sudo launchctl bootout system "$plist" 2>/dev/null || true
sudo launchctl bootstrap system "$plist"
sudo launchctl enable "system/$label"
sudo launchctl kickstart -k "system/$label"
portless service status
