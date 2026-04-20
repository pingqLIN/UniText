# UniText — Milestones

> 状態：Active
> 目的：外部審査と内部実行の両方で共通に使える、定量的な完成条件を定義する。

## Phase 1 — Skills Registry Online

- `registry/skills/` が作成済みである
- 少なくとも 5 個の skills が canonical adoption 済みである
- `INDEX.md` に対応する catalog entries がある
- `local/scripts/sync-skills.ps1` が `registry/skills` を指している
- `local/scripts/verify-delivery.ps1` で skills source と target の状態を検証できる
- `local/scripts/health-check.ps1` が基本チェックを通過できる

## Phase 2 — Full Registry Baseline

- `registry/agents/` が作成済みである
- `registry/mcp/` に少なくとも 1 つの空でない示例があり、読み取り可能である
- `registry/workflow/` に少なくとも 1 つの catalog entry が正式に列挙されている
- `scan` / `verify` / `sync` の 3 種の操作に最小ツール支援がある
- `CLI_COMPAT_MATRIX.md` に現在依存する CLI 挙動と最終検証日が記録されている

## Phase 3 — External Review Ready

- Git repository が初期化済みである
- `.gitignore` が local-only と大きな履歴産物を除外している
- `README.md`、`INDEX.md`、`docs/reports/status/PROJECT_STATUS_REPORT_2026-03-23.md` の 3 つの状態が一致している
- `EXTERNAL_REVIEW_PACKAGE.md` が審査範囲、読書順、除外項目を定義している
- `EXTERNAL_REVIEW_COVER_NOTE.md` と `EXTERNAL_REVIEW_HIGHLIGHTS.md` が reviewer-facing entry docs として使える
- `SECRET_HANDLING_GUIDELINES.md` が治理境界を定義し、コア読書順に含まれている
- `local/scripts/export-review-package.ps1` で review package を繰り返し生成できる
- cross-platform の `bootstrap -> verify` first-run path が提供されている
- 外部審査では次を直接確認できる
  - コア架構文書
  - adoption 済み canonical skills
  - 最小 operations scripts
  - 次段階の明確な milestone

## Phase 4 — Template Release Ready

- local-only artifacts が発行 package に入らない
- template export 流れが文書化されている
- `TEMPLATE_RELEASE_PACKAGE.md` と `TEMPLATE_RELEASE_CHECKLIST.md` が存在する
- `local/scripts/export-template-package.ps1` で starter package を繰り返し生成できる
- `local/scripts/verify-template-package.ps1` で starter package 構造を検証できる
- `SECRET_HANDLING_GUIDELINES.md` が starter package に含まれている
- `local/scripts/create-git-bundle.py` で持ち運び可能な backup artifact を作成できる
- `skills`、`mcp`、`agents`、`workflow` をカバーする template-safe generic examples がある
- template-safe な `local/` skeleton がある
- `mcp` に少なくとも 1 つの本当に実行可能な baseline がある
- canonical resource coverage が `skills`、`mcp`、`agents`、`workflow` に拡大し続けている
- 少なくとも 2 つの CLI が delivery 検証を実際に通過している
