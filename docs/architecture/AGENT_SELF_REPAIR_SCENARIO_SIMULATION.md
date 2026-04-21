# UniText — Agent Self-Repair Scenario Simulation

> 狀態：Active Baseline  
> 用途：定義 `UniText` 在未來執行過程遇到障礙時，系統 agent 應如何用情境模擬評估「是否能自我修復」、應採取哪一類 repair 動作、以及何時必須升級給人類決策。

## 1. Why This Exists

`UniText` 已經有 `bootstrap -> verify`、boundary checks、review package export、workspace-sensitive metadata validation 等治理腳本，但這些工具本身不自動等於「agent 一定會修復成功」。

要讓 agent 在未來執行中更穩定，需要額外回答三件事：

1. 這個障礙是否有足夠明確的 failure signal？
2. 是否存在可回復、可驗證、且 blast radius 受控的 repair path？
3. 若 repair 失敗，系統是否知道何時停止並升級，而不是持續亂修？

本文件把這三件事轉成可重複套用的 scenario simulation 規則。

## 2. Decision Ladder

遇到障礙時，先依照以下順序判斷：

1. `detectable`
   - 是否有可機器判讀的失敗訊號，例如 exit code、缺檔、contract mismatch、verify 失敗、health check 異常
2. `bounded`
   - 修復動作是否只影響單一層，例如 `runtime/`、`local wiring`、`review bundle contract`
3. `reversible`
   - 是否已有 backup、tracked source of truth、或可重新生成的 read model
4. `verifiable`
   - 修完後是否有對應 `verify` / `dry-run` / `health-check` 可以立即驗證
5. `escalatable`
   - 若修復不成立，是否能明確升級成 `blocked`，而不是持續擴大修改面

只有當 `detectable + bounded + reversible + verifiable` 都成立時，agent 才應嘗試 autonomous self-repair。

## 3. Repair Classes

| Class | Meaning | Agent action |
|---|---|---|
| `A0 detect-only` | 只能可靠偵測，不能安全改動 | 記錄 blocker、停止、升級 |
| `A1 bounded repair` | 可在單一邊界內修復，且驗證明確 | 允許 agent 自主修復 |
| `A2 guided repair` | 可修，但必須遵守明確 contract / sequence | 允許 agent 在規則內修復，需完整 report |
| `A3 human gate` | 涉及 canonical source、敏感邊界、或長期架構分歧 | 不自動修復，交給人類決策 |

## 4. Scenario Config Template

未來新增情境時，至少用這個欄位集合：

```yaml
id: runtime-target-drift
layer: local-wiring
class: A1
trigger:
  - verify-bootstrap false
failure_signal:
  - symlink target mismatch
  - config target mismatch
repair_action:
  - rerun bootstrap
verify_action:
  - verify-bootstrap
rollback:
  - restore previous local target
escalate_when:
  - repo identity mismatch
  - repeated verify failure
```

欄位設計原則：

- `layer`
  - `registry`, `runtime`, `local-wiring`, `review-bundle`, `boundary`, `i18n`, `release`
- `class`
  - `A0` 到 `A3`
- `trigger`
  - 人類或 agent 何時應啟動該情境
- `failure_signal`
  - 具體可觀測的異常
- `repair_action`
  - 允許 agent 嘗試的最小修復集
- `verify_action`
  - 修復後必跑的驗證
- `rollback`
  - 若修復失敗如何退回
- `escalate_when`
  - 何時必須停止並交人

## 5. Current UniText Assessment

### 5.1 Runtime target drift

- `layer`: `local-wiring`
- `class`: `A1`
- 現況：已有 `bootstrap.py` 與 `verify-bootstrap.py`
- executable scenario: `docs/architecture/scenarios/runtime-target-drift.json`
- runner: `local/scripts/run-self-repair-simulation.py --scenario runtime-target-drift`
- 判定：**可以自我修復**

Reason:

- failure signal 明確
- repair path 固定
- repair 後可立刻 verify
- canonical source 不會被直接改寫

### 5.2 Runtime projection drift

- `layer`: `runtime`
- `class`: `A2`
- 現況：已有 `build-runtime-layer.py`，可從 canonical source 重建 `runtime/`
- 判定：**可做 guided repair**

Reason:

- 可重建，但前提是 canonical docs / registry 沒壞
- 應限定在 read model 重建，不可順便改 canonical content

### 5.3 External review bundle drift

- `layer`: `review-bundle`
- `class`: `A2`
- 現況：已有 `external-review-bundle.contract.json` 與 `export-review-package.ps1`
- executable scenario: `docs/architecture/scenarios/review-bundle-contract-drift.json`
- runner: `local/scripts/run-self-repair-simulation.py --scenario review-bundle-contract-drift`
- 判定：**可做 guided repair**

Reason:

- 只要 contract 與引用一致，就能 dry-run 驗證
- 但若要改 package 成員，仍是文檔決策，不是純技術修復
- 目前可自動修復的範圍只限於 legacy 路徑正規化與 `reading_order -> files` 對齊，不包含擴大或縮減審查範圍

### 5.4 Workspace-sensitive metadata drift

- `layer`: `boundary`
- `class`: `A2`
- 現況：已有 `WORKSPACE_SENSITIVE_METADATA_RULES.*` 與 validation script
- executable scenario: `docs/architecture/scenarios/workspace-sensitive-boundary-drift.json`
- runner: `local/scripts/run-self-repair-simulation.py --scenario workspace-sensitive-boundary-drift`
- 判定：**可偵測，且可局部修復**

Reason:

- 規則與 self-test 已存在
- 但若 drift 牽涉 canonical docs 的內容取捨，需保守處理
- 目前可自動修復的範圍只限於 `shared_surface_scope` 中已知 moved docs 的 reference drift；不自動修改 regex、self-test 或內容策略

### 5.5 I18n drift

- `layer`: `i18n`
- `class`: `A1` for `zh-TW`, `A0` for archived locales
- 現況：active locale 只剩 `zh-TW`
- 判定：**只對 active locale 做自我修復**

Reason:

- archived locales 不再是 release gate，也不應觸發自動修復
- `zh-TW` 則可透過 manifest 與 drift audit 持續維護

### 5.6 Canonical source disagreement

- `layer`: `registry` / `core-docs`
- `class`: `A3`
- 現況：若 canonical docs 彼此矛盾，agent 不應自行裁決
- 判定：**必須 human gate**

Reason:

- 這不是 repair，而是 architecture / policy decision
- 自動修會導致長期規格漂移

## 6. Simulation Method

每次做治理模擬時，請固定跑這四步：

1. `pick one failure class`
   - 只模擬一個 bounded scenario，不混多種障礙
2. `force one observable failure`
   - 例如 target mismatch、contract path mismatch、missing runtime artifact
3. `run repair path only`
   - 不允許順手擴修其他區塊
4. `verify and classify`
   - 結果只能是：
     - `recovered`
     - `blocked-with-escalation`
     - `unsafe-to-autorepair`

第一個可執行 baseline 應優先採用「temporary fixture + bounded override」方式，避免為了模擬而改壞真實 home target。`runtime-target-drift` 現在就是用 `--home-dir`、`--history-root`、`--skip-runtime-build` 等 bounded overrides 在臨時目錄中演練。

## 7. Design Rules For New Scenarios

要讓 scenario 配置有邏輯，一律遵守：

- 一個 scenario 只對應一個主要 layer
- 一個 scenario 只定義一個主 failure signal
- repair action 不可跨 canonical / local 兩層同時大幅改動
- verify action 必須是 repo 內現有工具，或能在同批次補齊
- 若沒有 rollback，就不能標成 `A1`
- 若需要人類判斷 canonical truth，就不能標成 `A1/A2`

## 8. Recommended Next Scenarios

下一輪若要正式演練，優先順序如下：

1. `runtime-target-drift`
2. `review-bundle-contract-drift`
3. `workspace-sensitive-boundary-drift`
4. `active-zh-TW-i18n-drift`

暫時不要先演練：

- `canonical source disagreement`
- `secret handling policy drift`
- `cross-repo publication boundary change`

這些都太接近 human gate，不適合作為第一批 autonomous self-repair simulation。
