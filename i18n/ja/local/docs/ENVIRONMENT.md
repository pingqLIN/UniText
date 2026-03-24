# Environment Notes

> 状態：Active
> 用途：現在の authoring workspace の path と履歴上の deployment 関係を記録する。

## Current Working Root

- 現在の主要作業ディレクトリ：`Q:\UniText`

## Historical Paths

- 旧い ops snapshots、inventory、path notes は `C:\Dev\UniText` に見つかる
- これらの path は歴史的な deployment の痕跡として扱い、新しい scripts の真相源にはしない

## Current Rule

- 新規追加または修正する scripts は repo-relative path を優先する
- canonical skills source は `registry/skills/` とする
- 文書と実際の path が衝突した場合は、repo 内の現行 scripts と registry 構造を優先する
