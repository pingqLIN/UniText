# UniText — Cross-Platform Script Portability Plan

> 狀態：Draft Plan
> 用途：定義如何逐步把目前偏 `PowerShell-first` 的本機治理腳本，收斂成更通用、可在 `Windows / macOS / Linux` 上重複執行的工具鏈。

## 1. Why This Plan Exists

UniText 的整體設計從一開始就把 `Windows`、`macOS`、`Linux` 當成 target baseline。

但目前的實際證據是：

- `Windows / PC` 已有較完整的 authoring-host 驗證
- 多數 governance / export / verification 腳本仍以 `*.ps1` 為主
- `macOS` / `Linux` 尚未完成同等強度的 end-to-end revalidation

因此接下來不應只在文件上宣稱 cross-platform，而應逐步把腳本層做成：

- shared logic 可跨平台執行
- Windows 仍保有熟悉入口
- 驗證與輸出格式維持一致
- 不因改寫而破壞既有治理 guardrails

## 2. Goal

把目前的 `PowerShell-first governance toolchain` 漸進式重構為：

- `Python-first core logic`
- `PowerShell wrapper / adapter` 作為 Windows convenience layer
- 需要時再補 `bash` / `sh` thin wrapper

也就是說，未來最理想的狀態不是完全消滅 `ps1`，而是：

- 真正的邏輯核心盡量平台無關
- `ps1` 只負責呼叫、參數轉送、或 Windows 特有整合

## 3. Design Principles

1. `behavior parity first`
   - 先確保新腳本的輸出、guardrails、exit behavior 與舊版一致，再談刪除舊入口
2. `dry-run must survive`
   - `dry-run`、`preview`、`verify`、`audit` 不能因改寫而弱化
3. `structured output first`
   - 優先讓新腳本輸出穩定 JSON / markdown / plain-text 摘要，便於 agent 與 human 共用
4. `shared logic should not live in wrappers`
   - Windows wrapper 不應再承載主要規則判斷
5. `migration by families`
   - 以腳本家族為單位改寫，而不是逐支隨機處理

## 4. Script Families

### A. Startup / bootstrap family

- `local/scripts/git-startup.ps1`
- `local/scripts/bootstrap.py`
- `local/scripts/verify-bootstrap.py`

判斷：

- `bootstrap.py` / `verify-bootstrap.py` 已是較好的跨平台起點
- `git-startup.ps1` 仍是 PowerShell-only，需要補跨平台 core

### B. Boundary / governance family

- `local/scripts/validate-workspace-sensitive-metadata-rules.ps1`
- `local/scripts/verify-workspace-boundaries.ps1`
- `local/scripts/get-publishability-report.ps1`
- `local/scripts/health-check.ps1`

判斷：

- 這一組最值得優先移植，因為是 shared governance 的核心檢查鏈
- `validate-workspace-sensitive-metadata-rules.py`、`verify-workspace-boundaries.py`、`get-publishability-report.py` 已作為第二批 Python core；同名 `ps1` 入口保留為 Windows wrapper

### C. Template / rebuild family

- `local/scripts/export-template-package.ps1`
- `local/scripts/verify-template-package.ps1`
- `local/scripts/export-rebuild-project.ps1`
- `local/scripts/verify-rebuild-project.ps1`

判斷：

- 這一組屬於 release-facing flow，改寫時必須保證 package layout 與 exclusion semantics 完整一致

### D. Renormalize / hygiene family

- `local/scripts/preview-renormalize.ps1`
- `local/scripts/run-renormalize.ps1`

判斷：

- 邏輯相對集中，適合早期改成 Python core + wrapper 的示範批次

### E. Legacy Windows delivery family

- `local/scripts/sync-skills.ps1`
- `local/scripts/scan-skills.ps1`
- `local/scripts/verify-delivery.ps1`
- `local/scripts/batch-adopt-skills.ps1`
- `local/scripts/generate-index-entries.ps1`
- `local/scripts/rollback-skills.ps1`
- `local/scripts/export-review-package.ps1`

判斷：

- 這一組較多歷史背景與 Windows 操作語意，應放在後段處理

## 5. Migration Order

建議順序：

1. `Renormalize / hygiene family`
2. `Boundary / governance family`
3. `Template / rebuild family`
4. `Startup / bootstrap family` 中仍為 `ps1` 的部分
5. `Legacy Windows delivery family`

原因：

- 前三組最能直接補足 `macOS / Linux` 的治理缺口
- 風險可控，且容易做 parity verification
- 最後再處理歷史較重、Windows 依賴較深的 delivery scripts

## 6. Recommended Target Shape

```text
local/scripts/
├── bootstrap.py
├── verify-bootstrap.py
├── health-check.py
├── verify-workspace-boundaries.py
├── get-publishability-report.py
├── export-template-package.py
├── verify-template-package.py
├── export-rebuild-project.py
├── verify-rebuild-project.py
├── preview-renormalize.py
├── run-renormalize.py
├── wrappers/
│   ├── health-check.ps1
│   ├── verify-workspace-boundaries.ps1
│   └── ...
└── lib/
    ├── workspace_sensitive_metadata.py
    ├── package_layout.py
    └── git_helpers.py
```

重點不是檔名一定照這個方案，而是：

- shared rules / file selection / validation logic 進 Python library
- wrapper 只保留入口功能

## 7. Required Guardrails

每一批改寫都必須保留：

- `dry-run first`
- `MaxFiles` 或等價 blast-radius guard
- 結構化輸出
- 非零 exit code 表示失敗
- 不自動越過 `NO_PUBLISH_POLICY.md`
- 不把 machine-local 路徑重新寫回 shared surfaces

## 8. Definition Of Done Per Family

每個家族完成時，至少要滿足：

1. Python 版可在 `Windows / macOS / Linux` 執行
2. 舊 `ps1` 入口仍可用，且只作 thin wrapper
3. 新舊腳本在相同輸入下的核心結果一致
4. README / scripts README / compatibility docs 已更新
5. 至少補一輪 cross-platform evidence，而不是只有 Windows smoke check

## 9. First Implementation Batch

第一批最建議做：

- `preview-renormalize.ps1`
- `run-renormalize.ps1`

原因：

- scope 與輸出相對明確
- 不直接牽涉 template export layout
- 可以作為 Python-first + PowerShell-wrapper 的最小成功案例

## 10. Validation Strategy

每一批至少做：

- `Windows` 本機 parity check
- `macOS` 一輪基礎執行驗證
- `Linux` 一輪基礎執行驗證
- 針對輸出 JSON / markdown 的 snapshot compare

若暫時做不到三平台同時驗證，文件中必須清楚標示：

- 哪個平台已 complete
- 哪個平台只做 smoke
- 哪個平台尚未驗證

## 11. Risks

- 直接大規模重寫所有 `ps1` 容易把治理行為一起改壞
- 若沒有 parity tests，容易出現「可執行但結果語意不同」
- export / rebuild family 若改寫過快，可能破壞 starter package 契約

## 12. Recommended Next Step

下一步建議不是全面改寫，而是以 bounded batch 延續已落地的 core / wrapper 樣板：

1. `Renormalize / hygiene family` 已完成 Python core + PowerShell wrapper。
2. `Boundary / governance family` 已開始完成 Python core + PowerShell wrapper。
3. 下一個批次應補 `health-check` 的 Python core，或開始把 `Template / rebuild family` 的 shared package layout logic 抽到 Python library。

這個順序可以讓 cross-platform 目標先覆蓋治理安全鏈，再進入 release-facing export / verify flow。
