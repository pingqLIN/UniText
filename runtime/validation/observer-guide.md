# Runtime Observer Guide

每次執行 acceptance task 時，觀察者至少要記：

- 任務編號
- 執行代理與模型
- first-read 檔案
- 後續讀取來源
- 最終答案
- 是否命中 `forbidden_sources`
- 四項評分
- 偏差說明

## 四項評分

- `routing_correctness`
- `source_hygiene`
- `output_correctness`
- `efficiency`

每項只記 `0` 或 `1`。

## Critical Fail

以下任一情況直接記 critical fail：

- 先讀 `registry/*` 而不是 `runtime/*`
- 把 `ops/*` 當 canonical source
- 把 `local/docs/authoring/*` 當 canonical source
- 直接虛構不存在的 `Q:\AGENTS.md`

## Evidence Location

執行證據固定落到：

- `ops/reports/agent-runtime-eval/<timestamp>/`

不要把執行證據寫回 `registry/` 或 `runtime/`。
