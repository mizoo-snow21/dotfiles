# pi global instructions

## Exception: reviewing code

コードレビューやデバッグで差分・ログを精読するときは圧縮しないこと。
`rtk proxy git diff` / `rtk proxy git show` を使い、`rtk git diff` は使わない。
bash は rtk 拡張 (`extensions/rtk.ts`) が自動で rtk に書き換えるため、明示的に `rtk proxy` を付けないと圧縮される。
