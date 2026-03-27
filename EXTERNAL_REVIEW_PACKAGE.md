# UniText — External Review Package

> 狀態：Active Baseline  
> 用途：定義外部審查要看什麼、不要看什麼，以及如何重複產出 review package。

## 1. Purpose

`UniText` 已經進入可供外部審查的 baseline 階段，但審查重點應集中在：

- 核心架構是否合理
- canonical registry 是否已落地
- operations safety model 是否可執行
- 精選 shared resources 是否足以代表專案方向

本文件的目的是把這些內容收斂成一個可重複整理的審查包，而不是把整個作者工作區原封不動交出去。

## 2. Recommended Reading Order

建議外部審查者依以下順序閱讀：

1. `EXTERNAL_REVIEW_COVER_NOTE.md`
2. `EXTERNAL_REVIEW_HIGHLIGHTS.md`
3. `README.md`
4. `INDEX.md`
5. `VISION.md`
6. `RESOURCE_SPEC.md`
7. `OPERATIONS.md`
8. `SECRET_HANDLING_GUIDELINES.md`
9. `MILESTONES.md`
10. `PROJECT_STATUS_REPORT_2026-03-23.md`
11. `ESSENTIAL_SKILLS_SHORTLIST.md`
12. `docs/reviews/README.md`
13. `docs/reviews/DEVILS_ADVOCATE_REVIEW_CLOSURE_NOTE_2026-03-27.md`
14. `docs/reviews/ACT_11_I18N_SPOT_CHECK_2026-03-27.md`
15. `docs/reviews/DEVILS_ADVOCATE_REVIEW_2026-03-27.md`
16. `docs/reviews/SECOND_ROUND_REMEDIATION_ADDENDUM_2026-03-27.md`
17. `docs/reviews/ACT_14_HOSTED_CI_EVIDENCE_2026-03-27.md`

若要看實際資源樣本，再往下看：

- `ESSENTIAL_SKILLS_SHORTLIST.md` 與 `SKILLS_PUBLIC_RELEASE_POLICY.md`
- `registry/skills/SOURCES.md`
- `registry/skills/example-skill/`
- 目前可公開再分發的 public subset skills
- `registry/agents/registry-curator/`
- `registry/mcp/claude-project-mcp-seed/`
- `registry/workflow/claude-plans/`
- `local/scripts/` 中的最小治理腳本與 cross-platform first-run 腳本

## 3. Review Scope

目前 review package 應包含以下內容：

- 核心文件
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
  - `PROJECT_STATUS_REPORT_2026-03-23.md`
  - `ESSENTIAL_SKILLS_SHORTLIST.md`
  - `docs/reviews/README.md`
  - `docs/reviews/DEVILS_ADVOCATE_REVIEW_COMBINED_REVIEW_2026-03-27.md`
  - `docs/reviews/DEVILS_ADVOCATE_REVIEW_CLOSURE_NOTE_2026-03-27.md`
  - `docs/reviews/ACT_11_I18N_SPOT_CHECK_2026-03-27.md`
  - `docs/reviews/DEVILS_ADVOCATE_REVIEW_2026-03-27.md`
  - `docs/reviews/SECOND_ROUND_REMEDIATION_ADDENDUM_2026-03-27.md`
  - `docs/reviews/ACT_12_DOCS_SCALE_BASELINE_2026-03-27.md`
  - `docs/reviews/ACT_13_SKILLS_PROVENANCE_AUDIT_2026-03-27.md`
  - `docs/reviews/ACT_14_HOSTED_CI_EVIDENCE_2026-03-27.md`
  - `docs/reviews/REVIEW_FINDINGS_REMEDIATION_PLAN_2026-03-27.md`
  - `docs/reviews/SECURITY_REVIEW_ADVISORY.md`
  - `docs/reviews/SECURITY_ATTACK_INPUT_RESPONSE_REPORT.md`
  - `SKILLS_PUBLIC_RELEASE_POLICY.md`
  - `EXTERNAL_REVIEW_PACKAGE.md`
  - `registry/skills/SOURCES.md`
- 最小治理文件
  - `local/docs/ADOPTION_CHECKLIST.md`
  - `local/docs/CLI_COMPAT_MATRIX.md`
  - `local/docs/SUPPORT_PROOF_MATRIX.md`
  - `local/docs/DOCS_GOVERNANCE_RULES.md`
  - `local/docs/INDEPENDENT_VALIDATION_RUNBOOK.md`
  - `local/docs/INDEPENDENT_VALIDATION_REPORT_TEMPLATE.md`
  - `registry/skills/SOURCE_SCHEMA.md`
  - `local/scripts/README.md`
- 最小治理腳本
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
  - `ESSENTIAL_SKILLS_SHORTLIST.md` 中的 skills metadata 與收錄理由
  - `registry/skills/SOURCES.md`
  - `registry/skills/example-skill/`
  - GitHub-backed public subset skills
  - `registry/agents/registry-curator/`
  - `registry/mcp/claude-project-mcp-seed/`
  - `registry/workflow/claude-plans/`

## 4. Out Of Scope

以下內容不應作為外部審查主體：

- `backup/`
- `recovered_*`
- `.bak_*`
- `ops/history/`
- 本機特定 path mapping 與個人環境殘留
- 未納入 shortlist 的候選 skills
- 未追蹤或實驗中的內容

作者工作筆記、審查 archive 與其他 local-only 補充材料不屬於 canonical review source。

另外，授權邊界不明或限制再分發的 skills 不應納入公開 review package；若本地驗證曾使用這些 materials，應僅以說明文件記錄，不附原始檔案。公開版目前優先納入附 `SOURCE.yaml` 的 GitHub-backed public subset skills。

## 5. Export Command

在 repo root 執行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-review-package.ps1
```

預設輸出到：

```text
ops/review-package/review_YYYYMMDD_HHMMSS/
```

若只想先檢查內容，不寫入檔案：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-review-package.ps1 -DryRun
```

## 6. Validation

建議在 export 前至少先跑一次：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\health-check.ps1
```

若要確認 canonical skills delivery 對齊：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-delivery.ps1
```

## 7. Current Interpretation

截至 2026-03-24，`UniText` 已具備：

- reviewer-facing cover note 與 highlights summary
- 外部審查可讀的核心文件
- `8 + 4` 精選 skills 主集
- skills public release boundary 說明
- 一批可實際檢視的 public subset skills
- agent / workflow seed 與可實跑的 MCP baseline
- 可重複產出 review package 的整理流程
- cross-platform `bootstrap -> verify`
- 可攜 `git bundle` 備份流程

因此目前最適合的定位是：

**external-review-ready baseline**

而不是：

**fully generalized release template**
