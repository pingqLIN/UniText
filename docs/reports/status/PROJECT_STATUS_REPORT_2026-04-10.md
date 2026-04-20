# UniText 專案開發階段報告

> 報告日期：2026-04-10
> 報告性質：mainline consolidation / stage completion report
> 盤點範圍：目前 `main` 分支、近期主線整併結果、文件與測試基線、以及本輪驗證結果
> 審查狀態：已完成一輪外部事實一致性審查並整合修正

## 一、執行摘要

`UniText` 本輪已完成一次高風險但可回復的主線收斂：

- 恢復可用的本地 Git 執行路徑
- 將目前活躍產品線整併回 `main`
- 將本地 branch topology 收斂為 `main` only
- 建立 pre-prune `git bundle` 回復點
- 將本地 `origin/HEAD` 追蹤指向同步回 `main`
- 同步修正文檔敘事，釐清 `8 + 4` shortlist 與完整 inventory 的差異
- 建立可直接執行的最小 automated smoke baseline
- 將本地 `main` 成功推送到 `origin/main`

整體來看，專案目前已從「具備可審查 baseline 與多條平行整理線」進一步推進到「主線已收斂、可驗證、可持續迭代」的狀態。

## 二、目前主線狀態

截至本報告撰寫時：

- 目前工作分支：`main`
- 本地與遠端狀態：`main` 已同步到 `origin/main`
- remote default branch：`origin/HEAD` 已同步指向 `main`
- 本地 branch 狀態：只保留 `main`
- 本地回復點：`ops/git-bundles/pre-prune_20260410/unitext-pre-prune.bundle`
- 本地執行報告：保留於 `ops/reports/`，並已改為 ignore，不再污染 worktree

本輪主線最近的重要 commit 為：

- `492906e` `chore: ignore local ops reports`
- `260c9a0` `docs: align inventory narrative and test baseline`
- `86eb665` `Merge branch 'feature/new-task-20260402'`

## 三、本輪已完成項目

### 1. Git 與交付面

已完成：

- 恢復可用的 Windows Git 執行方式
- 在整併前建立 bundle backup
- 建立隔離 worktree 進行主線整併，避免直接在髒工作樹上 merge
- 刪除本地舊分支，完成 `main` only 收斂
- 將收斂後的 `main` 推送到 `origin/main`

### 2. 文件與敘事同步

已更新：

- `README.md`
- `INDEX.md`
- `PROJECT_STATUS_REPORT_2026-03-23.md`
- `ESSENTIAL_SKILLS_SHORTLIST.md`

本輪主要修正點是：

- `8 + 4` 是 external-review shortlist，不是完整 `registry/skills` inventory
- 舊報告中的 `12 adopted skills` 應被視為歷史基線，不代表當前全量狀態
- 補上目前測試基線的正式說明文件

### 3. 測試基線

已新增：

- `TEST_BASELINE.md`
- `tests/test_registry_inventory.py`
- `tests/test_project_map_baseline.py`

已修正：

- `tests/security/test_hardening.py`

目前最小可執行 automated baseline 為：

- security hardening guardrails
- registry inventory integrity
- project map / governance entry surfaces

## 四、驗證結果

本輪已直接確認：

- `main` 已成功推送至 `origin/main`
- `origin/HEAD` 已從舊的 feature 指向修正為 `main`
- worktree 已從多 branch 狀態收斂到 `main` only
- bundle backup 已成功產出
- `ops/reports/` 已不再造成未追蹤噪音

已執行測試：

```powershell
py -3 -m unittest tests.security.test_hardening tests.test_registry_inventory tests.test_project_map_baseline
```

結果：

```text
Ran 11 tests in 3.912s
OK (skipped=2)
```

## 五、目前階段判定

目前最合理的專案階段定位是：

**mainline consolidated baseline**

這個階段代表：

- 主要開發成果已回到 `main`
- 主線敘事已比先前一致
- 有最低限度的 smoke-test safety net
- 可在單一主線上繼續擴張，而不是繼續依賴平行 branch 生長

這還不代表：

- release hardening 已全部完成
- bootstrap / export / i18n / release flow 已有完整測試覆蓋
- 所有歷史支線的有效內容都已重新吸收回主線

## 六、仍存在的缺口與風險

### 1. release-hardening 線尚未重整回主線

`fix/pre-push-hygiene` 與其下游 release-hardening 工作仍有潛在價值，但本輪未直接 cherry-pick 回 `main`。

原因是：

- 差異面積大
- 涉及多個腳本、報表與測試面
- 與本輪的主線收斂目標不同，若強行一併吸收會提高回歸風險

### 2. 測試仍偏向最低基線

目前 baseline 足以守住主線收斂後的最基本完整性，但尚未完整涵蓋：

- `bootstrap.py` / `verify-bootstrap.py` 正向 smoke path
- project map 生成正確性
- template / rebuild export success path
- i18n drift 與 release hygiene 的完整檢查鏈

## 七、整體判斷

本輪不是新增單一 feature，而是完成一次基礎治理層級的收斂：

- branch 結構更單純
- 主線狀態更可信
- 文件敘事更接近真實
- 測試雖少，但開始形成可持續維護的 baseline

因此，`UniText` 現在最重要的變化不是「功能突然變很多」，而是：

**專案重新回到可以在單一主線上持續開發的狀態。**

## 八、下一階段建議

下一輪最合理的工作順序為：

1. 審核 `fix/pre-push-hygiene` 的有效增量，拆成可安全吸收的主線補丁
2. 擴張測試基線到 bootstrap、project map、export flow
3. 驗證並修正 remote default-branch / startup automation 假設
4. 視需要再進行第二輪文件整併，減少歷史報告與現況之間的理解落差
