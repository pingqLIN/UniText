# Independent Validation Report Template

> 狀態：Template
> 最後更新：2026-03-27
> 用途：供非作者 operator 回填最小獨立驗證結果，與 `INDEPENDENT_VALIDATION_RUNBOOK.md` 搭配使用。

## Report Metadata

| Field | Value |
|---|---|
| report_id | |
| operator | |
| role | |
| date | |
| repo_or_package | |
| validation_scope | bootstrap / review-export / template-export / full |

## Environment

| Field | Value |
|---|---|
| platform | |
| shell | |
| python | |
| powershell | |
| repo_source | git clone / review package / template package |

## Validation Results

| Step | Result | Notes |
|---|---|---|
| install core dependencies | pass / fail | |
| bootstrap dry-run | pass / fail | |
| bootstrap force | pass / fail | |
| verify-bootstrap | pass / fail | |
| review package dry-run | pass / fail | |
| template package export | pass / fail | |
| template package verify | pass / fail | |

## Manual Interventions

- none / list each intervention

## Issues Encountered

- none / list each issue with reproduction note

## Overall Disposition

- `pass`
- `pass with manual intervention`
- `fail`

## Suggested Follow-up

- none / list concrete follow-up items
