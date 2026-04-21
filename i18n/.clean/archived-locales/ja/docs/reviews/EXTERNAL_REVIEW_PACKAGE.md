# UniText — External Review Package

> 状態：Active Baseline  
> 用途：外部審査が何を見るべきか、何を見ないべきか、review package をどう再生成するかを定義する。

## 1. Purpose

`UniText` はすでに外部審査に供せる baseline 段階に入っていますが、審査の焦点は次に集中すべきです。

- core architecture は妥当か
- canonical registry は実装されているか
- operations safety model は実行可能か
- 精選 shared resources はプロジェクトの方向性を示すのに十分か

この文書の目的は、ワークスペース全体をそのまま渡すことではなく、これらの内容を再利用可能な審査包に収束させることです。

## 2. Recommended Reading Order

外部審査者には次の順で読むことを推奨します。

1. `EXTERNAL_REVIEW_COVER_NOTE.md`
2. `EXTERNAL_REVIEW_HIGHLIGHTS.md`
3. `README.md`
4. `INDEX.md`
5. `VISION.md`
6. `RESOURCE_SPEC.md`
7. `OPERATIONS.md`
8. `SECRET_HANDLING_GUIDELINES.md`
9. `MILESTONES.md`
10. `../reports/status/PROJECT_STATUS_REPORT_2026-03-23.md`
11. `ESSENTIAL_SKILLS_SHORTLIST.md`

実際の resource sample を見る場合は、次を確認します。

- `registry/skills/` の `8 + 4` 精選主集
- `registry/agents/registry-curator/`
- `registry/mcp/claude-project-mcp-seed/`
- `registry/workflow/claude-plans/`
- `local/scripts/` の最小治理 scripts と cross-platform first-run scripts

## 3. Review Scope

現在の review package には次を含めるべきです。

- コア文書
  - `EXTERNAL_REVIEW_COVER_NOTE.md`
  - `EXTERNAL_REVIEW_HIGHLIGHTS.md`
  - `README.md`
  - `INDEX.md`
  - `VISION.md`
  - `RESOURCE_SPEC.md`
  - `OPERATIONS.md`
  - `SECRET_HANDLING_GUIDELINES.md`
  - `PROJECT_MODES.md`
  - `MILESTONES.md`
  - `../reports/status/PROJECT_STATUS_REPORT_2026-03-23.md`
  - `ESSENTIAL_SKILLS_SHORTLIST.md`
  - `EXTERNAL_REVIEW_PACKAGE.md`
- 最小治理文書
  - `local/docs/ADOPTION_CHECKLIST.md`
  - `local/docs/CLI_COMPAT_MATRIX.md`
  - `local/scripts/README.md`
- 最小治理 scripts
  - `bootstrap.py`
  - `verify-bootstrap.py`
  - `create-git-bundle.py`
  - `scan-skills.ps1`
  - `sync-skills.ps1`
  - `verify-delivery.ps1`
  - `health-check.ps1`
  - `batch-adopt-skills.ps1`
  - `generate-index-entries.ps1`
  - `rollback-skills.ps1`
  - `export-review-package.ps1`
- 精選 shared resources
  - `registry/skills/` の `8 + 4` 主集
  - `registry/agents/registry-curator/`
  - `registry/mcp/claude-project-mcp-seed/`
  - `registry/workflow/claude-plans/`

## 4. Out Of Scope

以下は外部審査の主対象にすべきではありません。

- `backup/`
- `recovered_*`
- `.bak_*`
- `ops/history/`
- 本機特有の path mapping と個人環境の残留物
- shortlist に入っていない candidate skills
- 未追跡または実験中の内容

authoring notes and review archives は作者の参考資料であり、canonical review source ではありません。

## 5. Export Command

repo root で次を実行します。

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-review-package.ps1
```

既定の出力先：

```text
ops/review-package/review_YYYYMMDD_HHMMSS/
```

書き込みせず内容だけ確認したい場合は次を使います。

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-review-package.ps1 -DryRun
```

## 6. Validation

export 前に少なくとも 1 回は次を実行することを推奨します。

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\health-check.ps1
```

canonical skills delivery の整合を確認するには次を使います。

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-delivery.ps1
```

## 7. Current Interpretation

2026-03-24 時点で `UniText` は次を備えています。

- reviewer-facing cover note と highlights summary
- 外部審査で読める core documents
- `8 + 4` 精選 skills 主集
- agent / workflow seed と、実際に動く MCP baseline
- review package を再生成できる整理フロー
- cross-platform `bootstrap -> verify`
- 持ち運び可能な `git bundle` backup フロー

したがって、現在の最も適切な位置づけは次の通りです。

**external-review-ready baseline**

それよりも次のように呼ぶのは適切ではありません。

**fully generalized release template**
