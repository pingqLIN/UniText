# Runtime Start

`runtime/` 是 consumer agent 的第一讀取面。

先讀順序固定如下：

1. `runtime/START.md`
2. `runtime/RULES.md`
3. `runtime/ROUTES.md`
4. `runtime/catalog.json`
5. 需要時再讀對應的 `runtime/skills/*`、`runtime/agents/*`、`runtime/workflow/*`

不要先做的事：

- 不要把 `registry/` 當第一入口
- 不要先讀 `INDEX.md` 找一般任務答案
- 不要先讀 `ops/` 或 `local/docs/authoring/`

什麼時候才允許進 `registry/`：

- `runtime/*` 明確以連結指向某個 deeper reference
- 你正在做 adoption / curator / rebuild / template / debug runtime projection 缺口
- 你需要 source-of-truth 判斷，而不是 consumer runtime 答案

層級速記：

- `registry/` = canonical authoring source
- `runtime/` = tracked consumer read model
- `local/` = machine-local wiring and delivery
- `ops/` = evidence, reports, generated state

常見問題直接從這裡走：

- 規則查詢：`runtime/RULES.md`
- 任務路由：`runtime/ROUTES.md`
- 技能入口：`runtime/skills/<id>/SKILL.md`
- agent persona：`runtime/agents/<id>/AGENT.md`
- workflow 入口：`runtime/workflow/<id>/WORKFLOW.md`
- 驗證與觀察：`runtime/validation/`
