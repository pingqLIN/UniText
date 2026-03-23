# UniText — Vision

> 狀態：Template Base
> 原則：以邏輯契約為準，不以任何單一作業系統、目錄結構或部署方式作為規格前提。

## 1. What UniText Is

`UniText` 是一個 text-native、registry-first、AI-first 的 shared resource hub，讓多個 AI CLI / agent 系統能用同一套純文本契約共享資源定義與採用方式。

它包含兩層：

1. `Registry`
   - 定義 shared resources、canonical identity 與最小契約
2. `Adapter / Operations Control Plane`
   - 將 registry 內容對接到不同 CLI，並處理 install、sync、adopt、repair

## 2. Problem It Solves

`UniText` 要解決的是跨工具共享資源時常見的碎片化問題：

- skills 散落在不同位置
- MCP 定義分散在不同設定格式
- agent instructions 無法共用
- workflow 慣例難以跨工具延續
- 缺少一套 AI 容易讀取、版本控制友善的純文本共同介面

## 3. Architecture Position

正式定位：

**Registry-first, adapter-enabled, operations-governed**

關鍵原則：

- 沒有 registry，就沒有共同來源與共同語義
- 沒有 adapter，就無法把 registry 真正送進各 CLI
- AI 是重要的 consumer 與協作者，但不是唯一可靠的整合機制

## 4. Resource Types

預設 shared resource types：

- `skills`
- `mcp`
- `agents`
- `workflow`

`operations state` 不屬於 shared resource type，應獨立存在於 `/operations`。

## 5. Discovery and Delivery

`INDEX.md` 負責 discovery，回答：

- 有哪些資源
- 各資源的邏輯位置在哪裡
- 哪些 CLI 被支援

`OPERATIONS.md` 負責 delivery，回答：

- 某個 CLI 如何取得資源
- 何時執行 install、sync、adopt、repair
- delivery mode 如何解析

可用的 delivery modes：

- `pointer`
- `mirror`
- `symlink`
- `native-config`

## 6. Delivery Triggers

delivery 只能由明確 trigger 啟動：

- `bootstrap`
- `sync`
- `adopt`
- `repair`

所有破壞性操作都應遵守：

- 先 dry-run
- 先 backup
- 不可靜默決定 canonical source

## 7. Adoption Model

### Soft Adoption

- 先導入 discovery
- 不強迫立刻遷移既有資源

### Formal Adoption

正式納管流程：

1. `SCAN`
2. `REVIEW`
3. `DRY-RUN`
4. `ADOPT`
5. `DELIVER`
6. `VERIFY`

若發現同名異內容資源，流程必須停在 `REVIEW / DRY-RUN`。

## 8. Documentation Set

核心文檔：

- `VISION.md`
- `INDEX.md`
- `RESOURCE_SPEC.md`
- `OPERATIONS.md`
- `PROJECT_MODES.md`

## 9. Path Strategy

主文使用 logical canonical paths，例如：

- `/registry/skills`
- `/registry/mcp`
- `/registry/agents`
- `/registry/workflow`
- `/operations`

絕對路徑與平台專屬設定只屬於 deployment mapping，不屬於願景層契約。

## 10. Design Principles

- `Registry first`
- `Discovery before automation`
- `Explicit triggers`
- `Minimum viable metadata`
- `Canonical source of truth`
- `CLI-specific delivery`
- `Platform-agnostic contract`
- `Safe mutation`

## 11. One-Sentence Positioning

> UniText 是一個 text-native、registry-first、AI-first 的 shared resource hub，透過明確的 adapter 與 operations control plane，讓多個 AI CLI 能安全地發現、採用並共享同一套 canonical resources。
