# Local Scripts

ここには **本機操作 scripts** を置きます。

- `*.ps1` は Windows-first の参照実装として残します
- `*.py` は cross-platform の bootstrap / verify / backup path を提供します

## Current Scripts

- `bootstrap.py`
  - cross-platform で skills delivery、Codex native-config、project `.mcp.json` を初期化する
- `verify-bootstrap.py`
  - first-run の結果が現在の repo と一致しているかを cross-platform で確認する
- `create-git-bundle.py`
  - 持ち運び可能な `git bundle` backup を作り、本機 workspace だけに依存する single point of failure を減らす
- `sync-skills.ps1`
  - `registry/skills/` を本機 skills target に同期する
- `scan-skills.ps1`
  - candidate skills を走査し、adoption チェック結果を出力する
- `verify-delivery.ps1`
  - source と一般的な skills target が存在するか、link かどうか、解決可能かを検証する
- `health-check.ps1`
  - registry と scripts に対する最小 health check を行う
- `batch-adopt-skills.ps1`
  - candidate skills を一括で `registry/skills/` に移行する
- `generate-index-entries.ps1`
  - `registry/skills/` から INDEX 用 catalog 区画を生成する
- `rollback-skills.ps1`
  - `ops/history/adopt_*` の backup から指定 skill を復元する
- `export-review-package.ps1`
  - 外部審査に必要な cover note、highlights、core docs、精選 registry entries、最小 scripts を `ops/review-package/` に出力する
- `export-template-package.ps1`
  - template-safe docs、generic examples、starter layout を `ops/template-package/` に出力する
- `verify-template-package.ps1`
  - 出力した template package が必要な starter structure を含み、review-only / local-only 内容を含まないことを検証する

## Governance Note

- `sync-skills.ps1` と `batch-adopt-skills.ps1` は次を守るべきです。
  - dry-run first
  - backup before mutation
  - 追跡可能な log を生成する

## Platform Note

- 新しい first-run path では `bootstrap.py` と `verify-bootstrap.py` を優先してください。
- `sync-skills.ps1` は、Windows PowerShell の参照実装と治理の雛形として残します。
