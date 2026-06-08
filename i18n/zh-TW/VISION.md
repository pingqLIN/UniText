# UniText — Vision

> 狀態：active baseline
> 原則：UniText 定義 platform-neutral resource governance contract，不定義單一機器 layout。

## 1. What UniText Is

UniText 是 text-native、registry-first、AI-first 的 shared agent resources governance layer。

它存在的原因，是現代 AI runtimes 已在幾種 surface 上收斂：

- skill 或 capability folders
- repository 或 project instructions
- MCP definitions
- workflow / runbook files
- local settings 與 delivery targets

UniText 不試圖替每個工具發明替代格式；它為這些 surface 提供共同的 authoring、review、projection、verification model。

## 2. Why It Exists

沒有 shared governance layer 時，AI resources 很容易 drift：

- skills 分散在 tool-specific folders，provenance 不清楚
- MCP definitions 被複製進不相容的 config files
- agent instructions 變成無法 review 或 reuse 的長 prompt
- workflow decisions 消失在 chat history
- local paths 與 private metadata 混入 shared docs

UniText 把這些材料轉成有 stable identity、clear source of truth、deliberate delivery path 的 versioned resources。

## 3. Architecture Position

UniText 是：

**Registry-first, runtime-first, adapter-enabled, operations-governed.**

| Principle | Meaning |
|---|---|
| Registry-first | Shared resources 先有 canonical identity 與 source，再 delivery |
| Runtime-first | Consumer agents 從小型 generated read model 開始 |
| Adapter-enabled | Host tools 透過其 supported surfaces 接收 resources |
| Operations-governed | Mutations 使用 scan、review、dry-run、backup、deliver、verify |

## 4. Resource Types

Default shared resource types：

- `skill`
- `mcp`
- `agent`
- `workflow`

Operations state 不是 shared resource type。Inventories、baselines、backups、drift reports、repair plans、audit trails 屬於 operations layer，目前是 `ops/`，除非被明確 promoted 成 publishable document。

## 5. Discovery And Delivery

`INDEX.md` 回答 human discovery：

- 有哪些 docs
- resource families 在哪裡
- 哪個 task 應該讀哪頁

`RUNTIME.md` 回答 agent startup：

- 先讀什麼
- 哪些 runtime files 是 consumer context 的 authority
- 何時 follow pointers 回 canonical sources

`OPERATIONS.md` 回答 delivery：

- 用哪種 delivery mode
- 何時 scan、review、dry-run、adopt、deliver、verify
- 如何處理 conflicts 與 local mutation

## 6. Non-Goals

UniText 不會：

- 靜默改寫 global CLI configuration
- 未經使用者批准就 publish 或 push
- 把 private remotes 當成 publication approval
- 讓 `registry/` 成為 agents 預設 context dump
- 把 local secrets、absolute paths、personal operational notes 放進 shared surfaces
- 在沒有 dated verification 時聲稱完整支援某個 host tool

## 7. Design Principles

- Discovery before automation
- Stable IDs before delivery
- Short summaries before deep content
- Runtime read model before canonical source deep dives
- Dry-run before mutation
- Backup before overwrite
- Explicit user approval before publication
- Local-only by default for reports、plans、reviews、operational evidence

## 8. Positioning

> UniText 是 registry-first governance layer，讓多個 AI runtimes 能安全地 discover、share、receive 同一組 reviewed resources，而不會把 local machine state 變成 public documentation。
