# UniText — Resource Spec

> 状态：Template Base
> 适用范围：shared resources 的逻辑契约，不绑定单一作业系统、目录结构或储存格式。

本 spec 预设所有核心 metadata 都应可被纯文本稳定承载，方便 AI 与人类共同阅读、比对与版本管理。

## 1. Scope

本 spec 适用于：

- `skills`
- `mcp`
- `agents`
- `workflow`

不适用于：

- operations state artifacts
- 平台特定路径映射
- adapter 的内部执行细节

## 2. Identity Rules

一个 shared resource 的主识别由以下组合构成：

- `type`
- `id`

`id` 应：

- 使用小写英文字母、数字与 `-`
- 不含空白
- 不含作业系统特定分隔符

## 3. Canonical Location

`canonical_location` 必须是逻辑 canonical path，而不是某台机器的绝对路径。

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

允许的 `status`：

- `draft`
- `active`
- `deprecated`
- `archived`

## 6. Defaults

- `source_of_truth` 缺省时，视为等于 `canonical_location`
- `supported_clis` 缺省时，视为 `undocumented`
- `delivery_guidance` 缺省时，由 adapter / operations 文件推导

## 7. Delivery Guidance

`delivery_guidance` 是 discovery 用提示，不是固定 delivery mode。

它可以说明：

- 该去看哪类 adapter
- 是否存在平台差异
- 是否需要查看 `OPERATIONS.md`

它不应写死：

- 平台绝对路径
- 永久固定的 delivery mode

## 8. Conflict Rules

若发现同一组 `(type, id)` 对应多个内容不同的候选资源：

- 不得自动覆盖
- 不得静默推定 canonical source
- 必须停在 `REVIEW / DRY-RUN`

允许的结果：

- 明确选定 canonical source
- 重新命名为不同 `id`
- 标记为 `deprecated` 或 `archived`
- 暂时维持 `draft`

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
