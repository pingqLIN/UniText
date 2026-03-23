# UniText — Resource Spec v1

> 狀態：Draft
> 適用範圍：shared resources 的邏輯契約，不綁定單一作業系統、目錄結構或儲存格式。

## 1. Purpose

這份文件定義 `UniText` 中 shared resource 的最小契約，讓不同 CLI、不同 adapter、不同作業系統上的實作，都能以同一組語義描述資源。

這份 spec 要解決的問題是：

- 新增一個資源時，哪些欄位一定要有
- 哪些欄位能提升 discoverability，但不是第一天就必填
- 當 delivery mode 不是固定屬性時，INDEX 應該展示什麼
- 當 adopt 遇到同名異內容資源時，什麼情況不能自動決定 canonical source

## 2. Scope

本 spec 適用於以下 shared resource types：

- `skills`
- `mcp`
- `agents`
- `workflow`

本 spec 不適用於：

- operations state artifacts
  - 例如 inventory、backup、drift logs、history records
- 平台特定的路徑映射
- adapter 的內部執行細節

這些內容應由 `OPERATIONS.md` 定義。

## 3. Normative Model

### 3.1 Resource Entry

每個 shared resource 都應有一個對應的 registry entry。

這個 entry 描述的是：

- 這個資源是什麼
- 它的 canonical identity 是什麼
- 它的 source of truth 在哪裡
- 它目前的生命週期狀態是什麼
- 哪些 CLI 已知可以使用它
- 對 discovery 有幫助的採用提示是什麼

### 3.2 Format Neutrality

本 spec 定義的是邏輯欄位，不強制規定唯一序列化格式。

可接受的承載方式包括：

- `INDEX.md` 中的結構化條目
- YAML frontmatter
- JSON manifest
- 其他能忠實表達相同欄位語義的格式

## 4. Identity Rules

### 4.1 Primary Key

一個 shared resource 的主識別由以下組合構成：

- `type`
- `id`

兩者組合後必須唯一。

### 4.2 `id` Rules

`id` 應符合以下規則：

- 使用小寫英文字母、數字與 `-`
- 不含空白
- 不含作業系統特定路徑分隔符
- 表達資源的穩定名稱，而不是暫時性位置

建議形式：

- `frontend-design`
- `claude-default-agent`
- `core-workflow`

### 4.3 `type` Values

目前允許的 `type` 值：

- `skills`
- `mcp`
- `agents`
- `workflow`

若要新增新類型，必須先更新 spec 與 registry contract，而不是直接臨時擴張。

### 4.4 `canonical_location`

`canonical_location` 必須是邏輯 canonical path，而不是某台機器上的絕對路徑。

例如：

- `/registry/skills/frontend-design`
- `/registry/mcp/core-servers`
- `/registry/agents/default-coding-agent`

這個欄位的目的是提供穩定邏輯位置，讓實體路徑映射可由 adapter / operations 層獨立處理。

## 5. Metadata Tiers

### 5.1 Required

以下欄位為必填。缺少它們時，系統無法穩定辨識與管理該資源。

| Field | Meaning | Rule |
|---|---|---|
| `id` | 資源穩定識別 | 必須符合 `id` rules |
| `type` | 資源類型 | 必須是允許值之一 |
| `canonical_location` | 邏輯 canonical path | 必須使用邏輯路徑，不可綁定本機絕對路徑 |
| `status` | 生命週期狀態 | 必須是允許值之一 |

### 5.2 Recommended

以下欄位強烈建議提供。缺少它們不會阻止資源存在，但會降低 discoverability、adoption 品質或 adapter 判斷品質。

| Field | Meaning | Default when omitted |
|---|---|---|
| `source_of_truth` | 正式內容來源 | 視為等於 `canonical_location` |
| `supported_clis` | 已知支援的 CLI 列表 | `undocumented` |
| `delivery_guidance` | 給 discovery 使用的採用提示 | 交由 adapter / operations 文件推導 |

### 5.3 Optional

以下欄位為選填，用於治理、追溯與協作品質提升。

| Field | Meaning |
|---|---|
| `owner` | 對該資源負責的人、團隊或系統 |
| `provenance` | 資源來源、遷移來源或採納背景 |
| `notes` | 補充說明 |
| `last_verified` | 最後人工或工具驗證日期 |

## 6. Lifecycle

`status` 目前允許以下值：

- `draft`
  - 已建立，但尚未視為穩定可用
- `active`
  - 正式可用
- `deprecated`
  - 仍存在，但不建議新採用
- `archived`
  - 僅保留歷史用途，不再作為現行資源

## 7. Defaults and Derived Behavior

為了降低現有資源納管門檻，本 spec 採最小可行 metadata 策略。

預設規則如下：

- 若缺少 `source_of_truth`
  - 視為等於 `canonical_location`
- 若缺少 `supported_clis`
  - 視為 `undocumented`
  - 不可解讀為 `all`
- 若缺少 `delivery_guidance`
  - 由 `INDEX.md`、adapter docs 或 `OPERATIONS.md` 提供採用說明
- 若缺少 `owner`
  - 不阻止資源存在
  - 但 adopt / conflict resolution 時建議補上

## 8. Delivery Guidance

### 8.1 Why This Field Exists

`delivery mode` 在 `UniText` 中不是資源的固定硬屬性。它會受到 CLI 能力、作業系統、權限模型與操作情境影響。

因此 resource entry 不應把 `mirror`、`symlink` 或 `native-config` 當成永久真相寫死。

`delivery_guidance` 的用途是：

- 幫助 `INDEX.md` 呈現「如何開始採用」
- 告訴 human / AI 應該看哪個 adapter 或哪份操作文件
- 提供高層建議，而不是替 adapter 做最後解析

### 8.2 Field Shape

在 v1 中，`delivery_guidance` 定義為 **短文字說明**，而不是複雜的內嵌設定物件。

建議內容：

- 指向哪類 adapter
- 是否存在已知平台差異
- 是否需要查看 `OPERATIONS.md`

建議不要在這個欄位內嵌：

- 每個平台的絕對路徑
- 已解析完成的固定 delivery mode
- 平台專屬腳本名稱作為唯一真相

### 8.3 Example

`delivery_guidance` 範例：

- `Use the skills adapter; resolved mode depends on CLI capabilities and local environment.`
- `Register through the MCP adapter; most CLIs use native-config delivery.`

## 9. Conflict and Adoption Rules

### 9.1 No Silent Canonicalization

若 `SCAN` 或 adoption 流程發現同一組 `(type, id)` 對應到多個內容不同的候選資源：

- 不得自動覆蓋其中任一方
- 不得靜默推定 canonical source
- 必須停在 `REVIEW / DRY-RUN`

### 9.2 Allowed Outcomes

衝突情況下，允許的結果只有：

- 明確選定其中一個候選成為 canonical source
- 將候選重新命名為不同 `id`
- 將其中一個標記為 `deprecated` 或 `archived`
- 暫時維持 `draft`，直到人工決策完成

### 9.3 Provenance

若資源是透過 adopt 從既有環境納入，建議補上 `provenance`，說明：

- 來源類型
- 原始位置或來源系統
- 納管日期或背景

具體的操作流程、備份與回滾責任，應由 `OPERATIONS.md` 定義。

## 10. Initial Backfill Policy

為了避免現有資源因為 metadata 補不完而停滯，初始納管採分階段策略：

### Phase 1

先補齊必填欄位：

- `id`
- `type`
- `canonical_location`
- `status`

### Phase 2

在被修改、驗證、正式採用或發生衝突時，再補齊推薦欄位：

- `source_of_truth`
- `supported_clis`
- `delivery_guidance`

### Phase 3

在需要治理追溯時補齊選填欄位：

- `owner`
- `provenance`
- `notes`
- `last_verified`

## 11. Examples

以下範例使用 YAML 表示欄位形狀；實際儲存格式可不同。

### 11.1 Skill

```yaml
id: frontend-design
type: skills
canonical_location: /registry/skills/frontend-design
status: active
source_of_truth: /registry/skills/frontend-design/SKILL.md
supported_clis:
  - claude-code
  - codex
  - gemini-cli
delivery_guidance: Use the skills adapter; resolved mode depends on CLI capabilities and local environment.
owner: UniText
notes: Shared UI/UX skill for production-grade frontend work.
```

### 11.2 MCP Definition

```yaml
id: core-servers
type: mcp
canonical_location: /registry/mcp/core-servers
status: active
source_of_truth: /registry/mcp/core-servers/definition
supported_clis:
  - claude-code
  - codex
delivery_guidance: Register through the MCP adapter; most CLIs use native-config delivery.
provenance: Consolidated from existing per-CLI MCP definitions.
```

## 12. Non-Goals

本 spec 不打算在 v1 解決以下問題：

- 規定唯一的 registry serialization format
- 規定唯一的 adapter 實作語言或封裝方式
- 讓 resource metadata 攜帶所有平台特定路徑
- 把 delivery mode 寫死在每個資源上
- 把 operations artifacts 混成 shared resources
