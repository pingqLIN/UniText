# UniText — Resource Spec

> 狀態：active baseline
> 範圍：shared resources 的 metadata 與 projection contract。

本 spec 讓 resource metadata 對人類可讀、對 agents 可發現，並足夠穩定可供 runtime builders 與 adapter scripts 使用。

## 1. Resource Types

| Type | Canonical root | Purpose |
|---|---|---|
| `skill` | `registry/skills/` | Reusable procedure、prompt、capability pack、support assets |
| `mcp` | `registry/mcp/` | MCP server definition、policy、adoption notes |
| `agent` | `registry/agents/` | Persona、role instructions、playbook |
| `workflow` | `registry/workflow/` | Repeatable process、runbook、plan template |

Operations artifacts、local notes、generated reports、backups、review packets 預設不是 shared resource types。

## 2. Required Fields

每個 catalogable resource 應透過 frontmatter、definition file 或 generated catalog metadata 暴露：

| Field | Type | Meaning |
|---|---|---|
| `id` | string | Stable kebab-case identifier |
| `type` | enum | `skill`、`mcp`、`agent`、`workflow` |
| `title` | string | Human-readable display name |
| `status` | enum | `draft`、`active`、`deprecated`、`archived` |
| `summary` | string | Short discovery-first description |
| `source_of_truth` | path | Canonical authoring entrypoint |
| `runtime_projection` | path | Main runtime entrypoint, when projected |

## 3. Recommended Fields

| Field | Type | Meaning |
|---|---|---|
| `owners` | array | Maintainers 或 responsible role |
| `tags` | array | Search and routing hints |
| `audiences` | array | `human`、`agent`、`operator` 或 host-specific audience |
| `delivery` | object | Preferred delivery hints by host or surface |
| `compatibility` | object | Host-specific limitations and dated verification |
| `references` | array | Related docs、policies、examples、source links |
| `last_reviewed` | date | Last human review date |
| `release_surface` | enum | `shared`、`local-only`、`template-only` |

## 4. Naming Rules

- `id` 使用 kebab-case。
- 不要為同一 semantic resource 建立多個 IDs。
- `summary` 要短，適合 progressive disclosure。
- `title` 服務 humans，`summary` 服務 discovery，`source_of_truth` 服務 exact file targeting。
- Shared metadata 避免 machine-specific absolute paths。

## 5. Runtime Catalog Projection

`runtime/catalog.json` 是 discovery artifact，不是 full content dump。它至少應保留：

- `id`
- `type`
- `status`
- `summary`
- `source_of_truth`
- `runtime_projection`
- `delivery`
- `references`

Docs-only work 不應手動編輯 `runtime/catalog.json`。若 registry 或 runtime source files 改變，使用：

```powershell
python local/scripts/build-runtime-layer.py --write
```

先用 dry-run：

```powershell
python local/scripts/build-runtime-layer.py
```

## 6. Conflict Rules

若同一 `(type, id)` 對應不同內容：

- 不自動 overwrite
- 不靜默推定 canonical source
- 停在 `REVIEW / DRY-RUN`
- 選定 canonical source、重新命名競爭 resource，或標記為 `deprecated` / `archived`

## 7. Common Mistakes

| Mistake | Correction |
|---|---|
| `summary` 塞長篇說明 | 保持短摘要，deep content 透過 `source_of_truth` |
| `source_of_truth` 只指到資料夾 | 指到 main entry file |
| Delivery mode 被當永久屬性 | 在 adapter time resolve |
| Shared metadata 出現 local absolute path | 放到 `local/` 或 ignored operational evidence |
| 手改 runtime catalog | 改 registry/runtime source，再 rebuild |
