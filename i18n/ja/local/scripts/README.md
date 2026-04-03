# Local Scripts

ここには **ローカル運用スクリプト** を置きます。

- `*.ps1` は Windows-first の参照実装として残します
- `*.py` は cross-platform の `bootstrap` / `verify` / `backup` パスを提供します

## Current Scripts

- `bootstrap.py`
  - cross-platform で skills delivery、Codex native-config、Copilot MCP config、project `.mcp.json` を初期化します
- `verify-bootstrap.py`
  - first-run の結果が現在の repo と一致しているかを cross-platform で検証し、template-safe な `.mcp.json` seed と bootstrapped 済みのローカル wiring の両方を受け入れます
- `create-git-bundle.py`
  - 持ち運び可能な `git bundle` backup を作成し、ローカル worktree だけに依存する single-point-of-failure リスクを下げます
- `git-startup.ps1`
  - 新しい session 向けに canonical base branch を解決し、clean worktree を要求し、明示的な fast-forward 更新を行い、新しい feature branch を作成します
- `sync-skills.ps1`
  - `registry/skills/` をローカルの skills targets に同期します
- `scan-skills.ps1`
  - 候補 skills を scan し、adoption チェック結果を出力します
- `verify-delivery.ps1`
  - source と一般的な skills targets が存在するか、リンクか、解決できるかを検証します
- `health-check.ps1`
  - registry と scripts に対する最小限の health check を行います
- `batch-adopt-skills.ps1`
  - 候補 skills をまとめて `registry/skills/` に移します
- `generate-index-entries.ps1`
  - `registry/skills/` から INDEX 用の catalog ブロックを生成します
- `rollback-skills.ps1`
  - `ops/history/adopt_*` の backup から指定 skill を復元します
- `export-review-package.ps1`
  - 外部 review に必要な cover note、highlights、core docs、選抜 registry entries、最小 scripts を `ops/review-package/` に export します
- `export-template-package.ps1`
  - template-safe docs、generic examples、starter layout を `ops/template-package/` に export します
- `verify-template-package.ps1`
  - export された template package に必要な starter 構造があり、review-only / local-only の内容が含まれていないことを検証します
- `verify-workspace-boundaries.ps1`
  - 現在の authoring repo にある tracked shared surfaces に live workspace metadata、authoring-only docs、operations state が混入していないかを検証します
- `get-publishability-report.ps1`
  - 現在の branch にある local-only / ops / shared-surface 変更と boundary verify 結果を集約し、push suitability のローカル報告を作ります
- `lib/workspace-sensitive-metadata.ps1`
  - shared `WORKSPACE_SENSITIVE_METADATA_RULES.json` を読み込み、boundary / template / publishability の検証で同じルールセットを共有できるようにします
- `validate-workspace-sensitive-metadata-rules.ps1`
  - shared `WORKSPACE_SENSITIVE_METADATA_RULES.json` の構造、regex のコンパイル可否、同梱ケースの通過可否を検証します
- `preview-renormalize.ps1`
  - dry-run のみ実行し、`git add --renormalize .` が何件の tracked files に触れるかを preview して、line-ending cleanup の blast radius を先に確認できるようにします
- `run-renormalize.ps1`
  - `repo / root / registry / i18n / local / template` を scope にして制御付き renormalize を実行します。既定は dry-run で、`-Apply` を明示したときだけ変更を stage し、`MaxFiles` guard も持ちます
- `audit-i18n-drift.py`
  - `i18n/manifest.json` を読み、各 locale でどの公式文書が未翻訳か、翻訳が古いか、Git 履歴で未追跡かを列挙します。`json / markdown`、`locale / source-doc` による絞り込み、workboard 出力にも対応します
- `export-rebuild-project.ps1`
  - 現在の repo を、改名や再初期化が可能な fresh-project baseline として `ops/rebuild-project/` に出力します
- `verify-rebuild-project.ps1`
  - template package の検証に加えて、rebuild guide と fresh-project の入口が存在することも確認します

## Governance Note

- `sync-skills.ps1` と `batch-adopt-skills.ps1` はどちらも次を守る必要があります：
  - dry-run first
  - mutation の前に backup
  - 追跡可能な log を残す

## Platform Note

- 新しい first-run パスでは `bootstrap.py` と `verify-bootstrap.py` を優先します。
- `sync-skills.ps1` は引き続き Windows PowerShell の参照実装と governance テンプレートとして残します。
