
## Exception: reviewing code

コードレビューやデバッグで差分・ログを精読するときは圧縮しないこと。
`rtk proxy git diff` / `rtk proxy git show` を使い、`rtk git diff` は使わない。
情報の欠落がレビューの誤判定に直結するため。
