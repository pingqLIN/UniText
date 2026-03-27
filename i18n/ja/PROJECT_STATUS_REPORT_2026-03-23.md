# UniText プロジェクト開発進捗レポート

> 報告日：2026-03-24
> 報告性質：プロジェクト現況棚卸し / Status Report
> 棚卸し範囲：この workspace から見える文書、`registry/`、`local/`、`ops/` の成果物、および本輪の検証結果

## 1. 実行概要

`UniText` は現在、「外部審査に供せる baseline」からさらに進み、「cross-platform first-run を完了でき、template release candidate を出力でき、portable bundle backup を用意できる」段階に到達しています。

今回の最重要の追加進展は次の通りです。

- `mcp` が純粋な示意 seed から、実際に動く read-only baseline へ進化した
- cross-platform の `bootstrap.py` と `verify-bootstrap.py` を追加した
- Codex の `skills_path` と project `.mcp.json` を本番環境で検証した
- `create-git-bundle.py` を追加し、単一 workspace 依存のリスクを下げた

全体として、プロジェクトはもはや architecture と文書だけではなく、次を備えています。

- canonical registry
- operations safety baseline
- reviewer-facing package flow
- template export + verify flow
- cross-platform initialize -> verify path
- runnable MCP baseline

## 2. 現在の完成状態

### 1. コア文書と治理

以下は完成しており、継続的に整合を取っています。

- `README.md`
- `INDEX.md`
- `VISION.md`
- `RESOURCE_SPEC.md`
- `OPERATIONS.md`
- `PROJECT_MODES.md`
- `MILESTONES.md`
- `SECRET_HANDLING_GUIDELINES.md`

### 2. Registry 状態

4 種の shared resources はすべて審査可能な内容を持っています。

- `skills`
  - `8 + 4` の審査主集に収束済み
- `agents`
  - `registry-curator` がある
- `mcp`
  - `claude-project-mcp-seed` がある
  - `definition.json` と実行可能な `server.py` を含む
- `workflow`
  - `claude-plans` がある

### 3. Scripts と実行可能フロー

現在備わっているのは次の通りです。

- Windows-first operations scripts
  - `scan-skills.ps1`
  - `sync-skills.ps1`
  - `verify-delivery.ps1`
  - `health-check.ps1`
  - `batch-adopt-skills.ps1`
  - `generate-index-entries.ps1`
  - `rollback-skills.ps1`
  - `export-review-package.ps1`
  - `export-template-package.ps1`
  - `verify-template-package.ps1`
- Cross-platform first-run scripts
  - `bootstrap.py`
  - `verify-bootstrap.py`
  - `create-git-bundle.py`

### 4. Review と Template の線

以下は完了しています。

- reviewer-facing cover note
- reviewer-facing highlights summary
- review package export flow
- template package export + verify flow
- starter local overlay skeleton
- template-safe generic examples

## 3. 検証結果

今回、直接確認できた内容は次の通りです。

- `health-check.ps1` = `ok`
- `verify-delivery.ps1` 通過
- `verify-bootstrap.py` = `ok`
- Codex の `skills_path` が `/registry/skills` に整合している
- repo root の `.mcp.json` が正常に書き込まれている
- `claude-project-mcp-seed/server.py` が最小 MCP protocol smoke test を通過した
- `create-git-bundle.py` が bundle backup の生成に成功した

現在の定量的な状態は次の通りです。

- adopted skills = `12`
- invalid skills = `0`
- agent seed = `true`
- mcp seed = `true`
- workflow seed = `true`

## 4. 段階判定

| Phase | 現在の判定 |
|---|---|
| Phase 1: Skills Registry Online | 完了 |
| Phase 2: Full Registry Baseline | baseline 完了、しかも `mcp` はもはや stub ではない |
| Phase 3: External Review Ready | 完了 |
| Phase 4: Template Release Ready | release candidate 水準に達しているが、remote backup とより広い CLI 検証を補うのが望ましい |

## 5. 現在残るギャップ

### 1. 遠隔安全網はなお補う価値がある

`git bundle` による portable backup はあるものの、正式な remote backup のほうがより堅牢です。

### 2. `agents / workflow` はまだ seed 寄り

どちらも空の root ではなくなりましたが、深さはまだ `skills` 主集ほど成熟していません。

### 3. `mcp` は実行可能だが coverage は最小 baseline

external review と first-run baseline を支えるには十分ですが、多数の MCP 類型を持つ完全な catalog にはまだなっていません。

### 4. template release には最後の製品化余地がある

主に次が残っています。

- local-only artifacts のさらに徹底した整理
- release artifact の version strategy
- より広い非作者ユーザーによる first-run 検証

## 6. 全体判断

`UniText` の現在の最も妥当な位置づけは次の通りです。

**external-review-ready baseline + template release candidate**

これは、プロジェクトが次を備えていることを意味します。

- 審査可能な canonical registry
- 治理可能な operations model
- 実行可能な cross-platform first-run
- 実行可能な最小 MCP baseline
- review / template package の再生成

したがって、もはや「設計は成熟しているが実装が足りない」段階ではありません。すでに「交付可能、検証可能、候補発行可能」な段階に入っています。

