# Review Archive

> 狀態：Active Archive  
> 用途：集中存放審查、回應、audit、advisory 與 remediation 相關文件，避免根目錄被歷史分析文件稀釋。

## Purpose

這個目錄收納的是：

- historical snapshot
- code-state verification
- current decision basis
- remediation plan
- security advisory / attack-input analysis
- regression disposition / audit archive

根目錄保留的是高訊號核心文件；review 類材料則集中到這裡，方便追蹤脈絡又不污染 starter baseline 的主要入口。

## Current Review Chain

建議閱讀順序：

1. [DEVILS_ADVOCATE_REVIEW_2026-03-26.md](DEVILS_ADVOCATE_REVIEW_2026-03-26.md)
   - `historical snapshot`
2. [DEVILS_ADVOCATE_REVIEW_RESPONSE_2026-03-26.md](DEVILS_ADVOCATE_REVIEW_RESPONSE_2026-03-26.md)
   - `code-state verification`
3. [DEVILS_ADVOCATE_REVIEW_COMBINED_REVIEW_2026-03-27.md](DEVILS_ADVOCATE_REVIEW_COMBINED_REVIEW_2026-03-27.md)
   - `current decision basis`
4. [DEVILS_ADVOCATE_REVIEW_CLOSURE_NOTE_2026-03-27.md](DEVILS_ADVOCATE_REVIEW_CLOSURE_NOTE_2026-03-27.md)
   - `current-state closure note`
5. [REVIEW_FINDINGS_REMEDIATION_PLAN_2026-03-27.md](REVIEW_FINDINGS_REMEDIATION_PLAN_2026-03-27.md)
   - `execution plan`
6. [ACT_06_REGRESSION_DISPOSITION_2026-03-27.md](ACT_06_REGRESSION_DISPOSITION_2026-03-27.md)
   - `historical test-failure disposition`
7. [ACT_11_I18N_SPOT_CHECK_2026-03-27.md](ACT_11_I18N_SPOT_CHECK_2026-03-27.md)
   - `i18n confidence spot check`
8. [DEVILS_ADVOCATE_REVIEW_2026-03-27.md](DEVILS_ADVOCATE_REVIEW_2026-03-27.md)
   - `independent-opposition`
9. [SECOND_ROUND_REMEDIATION_ADDENDUM_2026-03-27.md](SECOND_ROUND_REMEDIATION_ADDENDUM_2026-03-27.md)
   - `confidence-hardening addendum`
10. [ACT_12_DOCS_SCALE_BASELINE_2026-03-27.md](ACT_12_DOCS_SCALE_BASELINE_2026-03-27.md)
   - `documentation scale baseline`
11. [ACT_13_SKILLS_PROVENANCE_AUDIT_2026-03-27.md](ACT_13_SKILLS_PROVENANCE_AUDIT_2026-03-27.md)
   - `skills provenance audit`
12. [ACT_14_HOSTED_CI_EVIDENCE_2026-03-27.md](ACT_14_HOSTED_CI_EVIDENCE_2026-03-27.md)
   - `hosted CI evidence status note`
13. [OPEN_ITEMS_2026-03-27.md](OPEN_ITEMS_2026-03-27.md)
   - `current open-items register`

## Security Review Set

- [SECURITY_ATTACK_INPUT_CHECKLIST.md](SECURITY_ATTACK_INPUT_CHECKLIST.md)
  - original attack-input checklist
- [SECURITY_REVIEW_ADVISORY.md](SECURITY_REVIEW_ADVISORY.md)
  - current-state security advisory
- [SECURITY_ATTACK_INPUT_RESPONSE_REPORT.md](SECURITY_ATTACK_INPUT_RESPONSE_REPORT.md)
  - treatment status, residual risk, and validation evidence

## Audit Archive

- [PRE_PUSH_AUDIT_2026-03-26.md](PRE_PUSH_AUDIT_2026-03-26.md)
  - historical pre-push snapshot

這些檔案可作為審查脈絡與證據鏈，但不應被誤讀成 starter package 的核心使用手冊。
