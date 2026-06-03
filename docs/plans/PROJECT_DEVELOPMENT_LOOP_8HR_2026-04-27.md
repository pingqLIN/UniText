# Project Development Loop — 2026-04-27 (8HR)

## 1) 目前進度與健康度

- Repo: `Q:\UniText`
- Branch: `main`
- Status: `main...origin/main [ahead 62]`
- 工作區健康：乾淨（本次驗證後無未提交變更）

### 已核對
- `python -m py_compile local/scripts/build-runtime-layer.py`：通過
- `python local/scripts/build-runtime-layer.py --output-dir runtime/.runtime-dryrun-8`：通過，輸出成功
- `python -m unittest tests.test_runtime_bundle_hidden_entries tests.test_bootstrap_verify_smoke`：通過
- `runtime/.runtime-dryrun-8` 已移入 `runtime/.del/.runtime-dryrun-8`（未刪除）
- 相關核心腳本在 dry-run/比較前置條件上仍可重複執行

## 2) 相關專案快照

- `Q:\Projects\skills-governance`：`main`、工作區清潔
- `Q:\UniText-wt-bugfix`：`fix/revamp-regressions...origin/main [ahead 1, behind 17]`
- `Q:\UniText-wt-dev`：`HEAD (no branch)`（需要先確定是否為預期工作樹）
- `Q:\UniText-wt-ui`：`feature/interface-console`
- `Q:\Projects\dbos-ai-evaluation-poc`：`main`，有未追蹤檔：
  - `tests/conftest.py`
  - `tests/test_agent_poc.py`
  - 目前疑似需要先整理 ownership / 追蹤方針後再列入主線決策

## 3) 結論（回到你的問題）

1. **下次 push 走 rebuild 的方向可維持**
2. **runtime generator 的 `--write` 仍需先完成「生成結果分類回報」再作為常態流程**
3. **DBOS 是否納入 UniText：目前建議先不納入 main runtime，維持隔離 PoC**

## 4) 這 8HR 的建議任務計畫

### Phase A：Runtime generator 風險消弭（預計 2HR）
1. 新增/完成 `build-runtime-layer` 的差異輸出摘要（預期變更 vs 意外差異）
2. 定義最小可回歸檢核清單並加一個高訊號測試
3. 建立 `--write` 使用條件檢查與 dry-run 對比門檻（`no-payload-only` 策略）

Phase A 結束條件：能在不改動 tracked runtime 的情況下，輸出可讀 diff summary 且 `--write` 觸發前有可追蹤門檻。

### Phase B：Push 可行性封包（預計 2HR）
1. 更新 push 檢查清單：`git status`、`build-runtime-layer`、`verify-bootstrap`、敏感檔排除
2. 生成 `push suitability report`（含與 `origin/main` 偏差）
3. 明確標記不該隨 push 帶出的檔案

Phase B 結束條件：可輸出「可推/不可推」報告並且可重複生成。

### Phase C：DBOS 深度評估（預計 2HR）
1. 明確定義你希望 DBOS 參與的第一個 workflow（優先：rebuild/export pipeline）
2. 在 `Q:\Projects\dbos-ai-evaluation-poc` 補齊兩項最小測試：
   - crash/restart 可恢復
   - side effect 不重跑（idempotency）
3. 在未通過前保持 Level 0（隔離），只做研究報告

### Phase D：決策與收斂（預計 2HR）
1. 匯總 `runtime --write` + DBOS 兩軸結論
2. 是否進入 rebuild route、是否開啟實驗性 adapter
3. 對 `wt` 系列子專案決議：先做基準再動主線

## 5) 下次 checkpoint

- 如果 runtime 風險未清，仍維持「不直接」使用 `python local/scripts/build-runtime-layer.py --write` 作為日常修補
- DBOS 保持隔離 PoC；待上述 crash/restart + idempotency 測試通過後，再回到 1 小時評估會議
