---
description: Consolidated open-items list after the Phase 1-3 remediation pass and second-round confidence-hardening work
---

# Open Items

> 日期：2026-03-27
> 用途：集中列出目前仍待處理、待補證據、或刻意保留為後續 follow-up 的事項，避免它們散落在多份審查與修補文件中。

## 1. Summary

截至 2026-03-27，`Phase 1` 的 release blockers 已關閉，`Phase 2` 的工程可信度基線已建立，`Phase 3` 的 review chain 與 i18n spot check 已完成。

目前剩餘的事項主要屬於：

- evidence hardening
- documentation synchronization
- target-scope follow-up
- residual risk tracking

這些項目**不再構成 release blocker**，但仍影響對外敘事的完整度與保守表述。

## 2. Open Execution Items

### OI-01 — ACT-16 獨立驗證尚未落實

**狀態**

- `open`

**目前已完成**

- 已有 [INDEPENDENT_VALIDATION_RUNBOOK.md](../../local/docs/INDEPENDENT_VALIDATION_RUNBOOK.md)
- 已有 [INDEPENDENT_VALIDATION_REPORT_TEMPLATE.md](../../local/docs/INDEPENDENT_VALIDATION_REPORT_TEMPLATE.md)

**尚缺**

- 至少一份由非作者實際執行並回填的驗證報告

**影響**

- 目前只能主張 `runbook ready, independent evidence pending`
- 對外仍需區分 self-validation 與 independent validation

### OI-02 — ACT-13 provenance 強化仍待補更細的 license / path-level 證據

**狀態**

- `follow-up`

**目前已完成**

- 36 個 active skills 都有 `SOURCE.yaml`
- schema 已擴充 `source_revision`、`license_scope_note`、`provenance_confidence`
- `source_revision` 已補成 local source clone 的真實 commit pin
- `license_scope_note` 已標準化區分 `repository-root` 與 `skill-subtree`
- `provenance_confidence` 已依目前 evidence depth 區分 `repo-license-relied-upon` 與 `path-level-evidence-stronger`

**尚缺**

- 對目前仍停留在 `repository-root` 的 skills，補上更細的 subtree/path-level 證據 where available
- 只在有更強證據時才把 `provenance_confidence` 從 `repo-license-relied-upon` 提高

**影響**

- 目前已能證明 `repo + path + revision pin`
- 但仍不能聲稱所有 active skills 都已具備更強的 path/file-level license provenance

依據見 [ACT_13_SKILLS_PROVENANCE_AUDIT_2026-03-27.md](ACT_13_SKILLS_PROVENANCE_AUDIT_2026-03-27.md) 與 [SOURCE_SCHEMA.md](../../registry/skills/SOURCE_SCHEMA.md)。

### OI-03 — 譯本同步波次尚未執行

**狀態**

- `mitigated`

**目前已完成**

- `ACT-11` spot check 已完成
- `ja/de/es` 的 `README.md` 與 `TEMPLATE_RELEASE_PACKAGE.md` 已補上 2026-03-27 current-baseline 同步注記
- `ja/de/es` 的 `README.md` 與 `TEMPLATE_RELEASE_PACKAGE.md` 已同步高風險章節，避免 support / release-boundary 判讀停留在舊版敘事
- `fr/it/ko/zh-CN/zh-TW` 的 `README.md`、`TEMPLATE_RELEASE_PACKAGE.md`、`OPERATIONS.md` 已補上 current-baseline / authoritative markers
- `fr/it/ko/zh-CN/zh-TW` 的 `README.md` 現在也明確列出仍應以英文主文件為準的未同步章節；`TEMPLATE_RELEASE_PACKAGE.md` 也明確標示 `5.1 Skills Release Rule` 仍由英文主文件管轄
- 上述五種語言的高風險文件現在已明確標示 English 主文件為 authoritative version

**尚缺**

- 是否要對 `fr/it/ko/zh-CN/zh-TW` 進行更深入的低風險逐段同步，仍待決定；目前只完成缺口顯式化與邊界收斂，尚未做完整逐段補譯
- 其他語言是否需要同樣策略，仍待後續評估

**影響**

- 英文主文件仍須作為 authoritative version
- 非英文譯本若未同步 current-baseline 標示，仍應視為 `stale / update needed`
- 現在這五種語言已不再屬於「未標示狀態」；它們只是尚未做完整逐段同步

依據見 [ACT_11_I18N_SPOT_CHECK_2026-03-27.md](ACT_11_I18N_SPOT_CHECK_2026-03-27.md)。

## 3. Configured but Evidence-Pending

### OI-04 — ACT-14 已配置 cross-platform smoke，但 hosted evidence 目前被 remote workflow 缺失阻塞

**狀態**

- `blocked`

**目前已完成**

- `.github/workflows/ci.yml` 已包含 `windows-latest`
- 也已加入 `ubuntu-latest` 與 `macos-latest` 的 portable smoke

**尚缺**

- 將 `.github/workflows/ci.yml` 發布到 remote default branch
- 一組可引用的 hosted CI 執行證據，證明 Linux / macOS smoke 實際跑綠

**影響**

- 目前較準確的說法是 `cross-platform smoke configured locally`
- 尚不宜過度擴大為「已完成外部可見的 cross-platform validation」
- 在 `No-Publish Rule` 下，若無明確授權，這個證據缺口不會自行消失

依據見 [SECOND_ROUND_REMEDIATION_ADDENDUM_2026-03-27.md](SECOND_ROUND_REMEDIATION_ADDENDUM_2026-03-27.md) 與 [ACT_14_HOSTED_CI_EVIDENCE_2026-03-27.md](ACT_14_HOSTED_CI_EVIDENCE_2026-03-27.md)。

### OI-05 — ACT-12 文件規模治理仍屬 baseline 階段

**狀態**

- `baseline established`

**目前已完成**

- 已有文件規模盤點與分布基線
- 已有可重跑的 docs-scale reporting routine
- 已有文件治理規則，定義 canonical / review / i18n / residue 的解讀口徑

**尚缺**

- 規模成長監測是否要自動化，仍未決定

**影響**

- 目前能說明文件膨脹來源，且可重跑相同量測口徑
- 但還不能說已建立完整長期自動化治理機制

依據見 [ACT_12_DOCS_SCALE_BASELINE_2026-03-27.md](ACT_12_DOCS_SCALE_BASELINE_2026-03-27.md)。

## 4. Intentional Target-Scope Follow-up

### OI-06 — Copilot CLI 仍為 `target / adapter pending`

**狀態**

- `intentional target`

**說明**

- 這不是漏修，而是目前 repo 有意保守收斂的未完成目標面
- 相關語氣已在 README 與 matrix 中明確標成：
  - `target`
  - `adapter pending`
  - `未驗證`

**影響**

- 不應把 Copilot CLI 說成已完成 first-run baseline

依據見 [CLI_COMPAT_MATRIX.md](../../local/docs/CLI_COMPAT_MATRIX.md) 與 [COPILOT_CLI_ADAPTER_NOTE.md](../../COPILOT_CLI_ADAPTER_NOTE.md)。

## 5. Residual Risk Tracking

### OI-07 — SEC-001 explicit opt-in shell risk

**狀態**

- `residual risk`

**說明**

- `with_server.py` 已改成 default-safe
- 但仍保留 `--allow-shell` 的 explicit opt-in 路徑

**影響**

- 應維持目前的保守敘事：`mitigated / residual risk remains`

## 6. Recommended External Wording

若要對外用一句話保守表述目前狀態，建議使用：

> UniText 目前已完成主要 release blocker 與工程可信度基線修補；剩餘項目主要集中在獨立驗證、provenance 深化、譯本同步，以及少量已知 residual risk 管理。

## 7. Closure Condition

若要將目前 open items 再進一步關閉，優先順序建議為：

1. 完成至少一份非作者驗證報告
2. 執行一輪 `README.md` / `TEMPLATE_RELEASE_PACKAGE.md` 譯本同步
3. 在獲得發布授權後，補上 hosted Linux / macOS CI evidence
4. 將 public skills 的 `license_scope_note` 補強到 path/file-level evidence where available
