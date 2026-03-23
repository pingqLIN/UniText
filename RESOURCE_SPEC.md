# UniText — Resource Spec

> 狀態：Template Base
> 適用範圍：shared resources 的邏輯契約，不綁定單一作業系統、目錄結構或儲存格式。

本 spec 預設所有核心 metadata 都應可被純文本穩定承載，方便 AI 與人類共同閱讀、比對與版本管理。

## 1. Scope

本 spec 適用於：

- `skills`
- `mcp`
- `agents`
- `workflow`

不適用於：

- operations state artifacts
- 平台特定路徑映射
- adapter 的內部執行細節

## 2. Identity Rules

一個 shared resource 的主識別由以下組合構成：

- `type`
- `id`

`id` 應：

- 使用小寫英文字母、數字與 `-`
- 不含空白
- 不含作業系統特定分隔符

## 3. Canonical Location

`canonical_location` 必須是邏輯 canonical path，而不是某台機器的絕對路徑。

例如：

- `/registry/skills/example-skill`
- `/registry/mcp/example-mcp`
- `/registry/agents/example-agent`

## 4. Metadata Tiers

### Required

- `id`
- `type`
- `canonical_location`
- `status`

### Recommended

- `source_of_truth`
- `supported_clis`
- `delivery_guidance`

### Optional

- `owner`
- `provenance`
- `notes`
- `last_verified`

## 5. Lifecycle

允許的 `status`：

- `draft`
- `active`
- `deprecated`
- `archived`

## 6. Defaults

- `source_of_truth` 缺省時，視為等於 `canonical_location`
- `supported_clis` 缺省時，視為 `undocumented`
- `delivery_guidance` 缺省時，由 adapter / operations 文件推導

## 7. Delivery Guidance

`delivery_guidance` 是 discovery 用提示，不是固定 delivery mode。

它可以說明：

- 該去看哪類 adapter
- 是否存在平台差異
- 是否需要查看 `OPERATIONS.md`

它不應寫死：

- 平台絕對路徑
- 永久固定的 delivery mode

## 8. Conflict Rules

若發現同一組 `(type, id)` 對應多個內容不同的候選資源：

- 不得自動覆蓋
- 不得靜默推定 canonical source
- 必須停在 `REVIEW / DRY-RUN`

允許的結果：

- 明確選定 canonical source
- 重新命名為不同 `id`
- 標記為 `deprecated` 或 `archived`
- 暫時維持 `draft`

## 9. Example

```yaml
id: example-skill
type: skills
canonical_location: /registry/skills/example-skill
status: draft
source_of_truth: /registry/skills/example-skill/SKILL.md
supported_clis: undocumented
delivery_guidance: Use the skills adapter; resolved mode depends on CLI capabilities and local environment.
```
