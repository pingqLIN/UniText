# UniText — Vision v2.1

> 狀態：Official
> 原則：以邏輯契約為準，不以單一本機作業系統、目錄結構或工具配置作為規格前提。

## 1. What UniText Is

`UniText` 是一個 **text-native、registry-first、AI-first 的 shared resource hub**，用來讓多個 AI CLI / agent 系統共享同一套資源定義與採用方式。

它同時包含兩層：

1. `Registry`
   - 定義有哪些 shared resources
   - 定義它們的 canonical source 與最小契約
   - 提供 human 與 AI 可讀的 discovery 入口

2. `Adapter / Operations Control Plane`
   - 將 registry 內容對接到不同 AI 工具
   - 負責 install、sync、adopt、repair、backup、drift detection
   - 處理各 CLI、作業系統與部署環境上的差異

因此，`UniText` 不是單純的配置檔資料夾，也不是只講理念的索引頁。
它是「共享資源登錄所 + 對接控制面」。

## 2. Problem It Solves

當同一位使用者同時使用 Claude Code、Codex、Gemini CLI 等工具時，常會出現以下問題：

- 相同 skill 重複存在於多個位置
- MCP server 定義分散在不同格式與設定檔
- agent 指令與 workflow 慣例無法共用
- 使用者需要記得每個工具、作業系統與工作環境的特殊路徑與安裝方式
- AI 工具彼此看不到對方已經擁有的資源

`UniText` 的目標不是把所有工具變成同一個工具，而是建立一個共同語言，讓它們至少能共享：

- skills
- MCP definitions
- agent instructions
- workflow conventions

## 3. Architecture Position

### 3.1 Registry First

系統的核心不是同步腳本，而是 shared resources 的可發現性與可定義性。

換句話說：

- 沒有 registry，就沒有共同來源與共同語義
- 沒有 adapter，就無法把 registry 真正送進各 CLI

所以 v2.1 採用的正式定位是：

**Registry-first, adapter-enabled, operations-governed**

### 3.2 AI Is a Consumer, Not the Only Integrator

AI 模型仍然是重要的整合層，但不再假設「只要模型看到文字指針，就一定能穩定完成整合」。

v2.1 的假設是：

- AI 可以協助 discovery、建議採用方式、執行操作流程
- 真正的 delivery 仍需透過明確的 adapter 與 operations 規則來完成

這樣能避免把可靠性建立在模型偶然遵循提示的能力上。

## 4. System Model

### 4.1 Core Concepts

- `registry`
  - 描述 shared resources 的層
- `resource`
  - 被納管的共享單位，例如 skill、MCP definition、agent instruction
- `canonical source`
  - 該資源的正式來源位置與正式內容
- `adapter`
  - 對接單一 CLI 的規則與實作
- `delivery`
  - 把 canonical resource 送到特定 CLI 的過程
- `operations`
  - install、sync、backup、adopt、repair、audit、drift detection 等治理行為
- `adoption`
  - 讓既有 CLI 或既有資源納入 UniText 的過程

在實作上，adapter 可以表現為 per-CLI 腳本、統一命令下的子模組，或由 operations layer 呼叫的 delivery worker；這些都是可能的封裝方式，而不是架構本身的限制。

### 4.2 Resource Types

v2.1 預設納管以下資源類型：

- `skills`
- `mcp`
- `agents`
- `workflow`

`ops` 不屬於 shared resource type。它代表 operations layer 產生的 state artifacts，例如 inventory、backup、drift logs，應在 `OPERATIONS.md` 中獨立定義，而不是作為被分發給 CLI 的 resource。

未來可增加新的 shared resource type，但必須先進入 shared resource contract，而不是直接靠慣例擴張。

## 5. Registry vs Adapter Responsibilities

### 5.1 Registry Responsibilities

Registry 負責：

- 定義有哪些資源
- 定義每個資源的 canonical location
- 提供 discovery 入口
- 定義 shared resource metadata contract
- 宣告資源狀態與相容性資訊

Registry 不直接負責：

- 背景自動同步
- 任意改寫 CLI 設定
- 隱式搬移使用者檔案
- 將某個平台特定路徑視為普遍規範

### 5.2 Adapter / Operations Responsibilities

Adapter / Operations 負責：

- 把 registry 的資源送入不同 CLI
- 根據 CLI 能力與環境條件解析 delivery mode
- 管理備份、回滾、drift 檢查與修復
- 保留過渡期的兼容策略

它們不應重新定義 canonical content，只應實作 delivery 與治理。

## 6. Discovery and Delivery

v2.1 明確區分兩件事：

### 6.1 Discovery

Discovery 是回答：

- 這裡有什麼資源
- 資源在哪裡
- 誰是 source of truth
- 哪些 CLI 被支援

`INDEX.md` 是 discovery 的第一入口。

### 6.2 Delivery

Delivery 是回答：

- 某個 CLI 要如何取得某個資源
- 何時執行安裝、同步、修復或遷移
- 採用何種對接方式

Delivery mode 不視為資源本身的固定硬屬性，而是由 adapter 根據 CLI 能力、作業系統、權限模型與操作情境解析出的結果。

因此，`INDEX.md` 應呈現的是 delivery guidance、adapter 入口或相容性提示，而不是把某個已解析完成的 delivery mode 當成資源的永久屬性。

可用的 delivery modes：

- `pointer`
- `mirror`
- `symlink`
- `native-config`

對 mode 的實際決策與觸發規則，由 `OPERATIONS.md` 定義。

## 7. Delivery Triggers

delivery 不能是模糊的背景概念，必須有明確 trigger。

v2.1 預設的 trigger taxonomy：

- `bootstrap`
  - 新 CLI 第一次接入 UniText
- `sync`
  - 將 canonical changes 送到既有 CLI
- `adopt`
  - 將既有本地資源正式納入 registry
- `repair`
  - 根據 drift 檢查結果執行修復

原則：

- 不做未經宣告的背景自動變更
- 所有 delivery 都必須由明確 trigger 啟動
- 所有破壞性操作都必須先 backup
- `repair` 可以自動提出建議，但真正變更仍需明確確認

## 8. Adoption Model

### 8.1 Soft Adoption

預設採用方式是低風險接入：

- CLI 先獲得 shared registry 的入口
- 使用者與 AI 先能發現資源
- 不要求立刻遷移既有資源

這條路徑適合：

- 想先導入 discovery
- 不想立刻改動現有工作環境
- 想觀察系統價值後再深化整合

### 8.2 Ceremony Adoption

當使用者想立刻看到統一效果時，可進入明確的納管流程：

1. `SCAN`
2. `REVIEW`
3. `DRY-RUN`
4. `ADOPT`
5. `DELIVER`
6. `VERIFY`

其中 `DRY-RUN` 的目的是在真正改動本地檔案、設定或連結前，先產出一份可檢視的變更計畫，讓使用者確認即將採用的 source of truth、delivery mode、備份點與預期影響。

若 `SCAN` 發現同名但內容不同的既有資源，流程必須停在 `REVIEW / DRY-RUN`，不能靜默推定 canonical source。衝突解決的具體規則應由 `RESOURCE_SPEC.md` 與 `OPERATIONS.md` 定義。

這條路徑的核心不是「強制搬家」，而是「把 ownership、source of truth、預覽結果與回滾能力都說清楚後再納管」。

## 9. Documentation Set

v2.1 不再讓單一願景文件承載全部責任。

正式 doc set 應包含：

- `INDEX.md`
  - discovery 入口
- `RESOURCE_SPEC.md`
  - shared resource contract
- `OPERATIONS.md`
  - delivery、triggers、backup、drift、mapping
- `PROJECT_MODES.md`
  - 區分 authoring repo 與 starter/template
- `VISION.md`
  - why、positioning、boundaries、adoption model

文件之間的關係是：

- `INDEX.md` 解鎖 discovery
- `RESOURCE_SPEC.md` 解鎖納管與擴充
- `OPERATIONS.md` 解鎖安全 delivery
- `PROJECT_MODES.md` 解鎖 repo 身分與發佈邊界
- `VISION.md` 提供總體架構與原則

## 10. Path Strategy

v2.1 主文使用 **logical canonical paths**，避免把願景層綁死在單一作業系統或掛載方式。

邏輯路徑例如：

- `/registry/skills`
- `/registry/mcp`
- `/registry/agents`
- `/registry/workflow`

operations state artifacts 應位於獨立的邏輯區，例如 `/operations`，而不是放在 `/registry` 之下。

實體路徑映射不在願景文中展開，應由 `OPERATIONS.md` 的 appendix 作為唯一正式 mapping 表。

任何作業系統上的絕對路徑、掛載點、家目錄位置或設定檔檔名，都屬於實作映射，而不是願景層的契約。

## 11. Reference Implementations vs Target State

不同使用者、不同 CLI 組合與不同作業系統，可能會出現不同的實作樣貌。v2.1 關心的是概念與責任邊界，而不是某一份本機資料夾長相。

| Concept | Example artifact shapes | Architectural role |
|---|---|---|
| `registry` | `INDEX.md`、catalog、manifest、資源索引 | 提供 discovery 與 canonical metadata |
| `operations state` | inventories、baselines、history logs、audit trails | 記錄治理狀態，不屬於 resource 本身 |
| `delivery implementation` | scripts、adapter modules、workers、install commands | 執行 delivery 與 repair |
| `canonical definitions` | skill sources、MCP definitions、agent instruction roots | 成為 source of truth |
| `path mapping` | adapter docs、platform mapping appendix | 將邏輯路徑映射到實體路徑 |
| `workflow notes` | workflow docs、runbooks、planning guides | 描述流程而不是定義資源本體 |

### Current Implementations

目前的實作可能已經具備部分控制面能力，例如：

- 同步腳本或 adapter worker
- canonical definitions 的集中位置
- inventory / backup / drift 歷史紀錄
- 跨 CLI 的路徑調查或對照文件

這些都可以是合理的 reference implementation，但不應被誤認為規格唯一正解。

### Authoring Repo vs Template

v2.1 也明確區分兩種 repo 身分：

- `authoring repo / local development project`
  - 用來保存治理狀態、遷移痕跡、reference implementations
- `starter / template project`
  - 用來提供他人初始化自己的 UniText 實例

前者可以攜帶本機狀態與 operations artifacts；後者應只攜帶 template-safe docs、範例與抽象契約。具體邊界由 `PROJECT_MODES.md` 定義。

### Target State

目標狀態是：

- registry 成為所有 shared resources 的正式來源
- adapters 成為 CLI-specific delivery 的正式層
- operations 成為可審計、可回滾的治理層
- doc set 讓 human 與 AI 都能在相同語義下工作

## 12. Design Principles

- `Registry first`
  - 先定義資源，再談分發
- `Discovery before automation`
  - 先讓資源可見，再決定如何接入
- `Explicit triggers`
  - 不依賴模糊或背景式操作
- `Minimum viable metadata`
  - 先要求系統可運作的最小欄位
- `Canonical source of truth`
  - 真正的內容來源只能有一個
- `CLI-specific delivery`
  - 不強迫所有工具使用同一種對接方式
- `Platform-agnostic contract`
  - 以邏輯契約為準，實體映射留給 adapter 與 operations
- `Safe mutation`
  - 任何破壞性操作都必須可備份、可回滾、可審計

## 13. Non-Goals

v2.1 明確不把以下內容納入目前範圍：

- 多 AI 之間的 runtime message bus
- 即時共享記憶體或分散式狀態同步
- 把所有 CLI 包裝成單一統一介面
- 依賴模型自發理解而缺乏明確契約
- 將某一套本機目錄配置視為所有使用者的唯一標準

## 14. One-Sentence Positioning

> UniText 是一個 text-native、registry-first、AI-first 的 shared resource hub，透過明確的 adapter 與 operations control plane，讓多個 AI CLI 能安全地發現、採用並共享同一套 canonical resources。
