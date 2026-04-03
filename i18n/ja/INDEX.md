# UniText — Index

> 状態：Template Base
> 役割：すべての human / AI にとっての最初の読取点であり、discovery の入口です。

`UniText` は純文本を共有インターフェースとして使い、cross-CLI の統一互換性と AI-first discovery を重視します。

## 1. Core Docs

推奨される読書順：

1. `INDEX.md`
2. `VISION.md`
3. `RESOURCE_SPEC.md`
4. `OPERATIONS.md`
5. `PROJECT_MODES.md`
6. `DOCUMENT_PLACEMENT_POLICY.md`
7. `WORKSPACE_SENSITIVE_METADATA_RULES.md`
8. `TEMPLATE_RELEASE_PACKAGE.md`
9. `TEMPLATE_RELEASE_CHECKLIST.md`
10. `REBUILD_AS_NEW_PROJECT.md`
11. `SECRET_HANDLING_GUIDELINES.md`
12. `NO_PUBLISH_POLICY.md`
13. `COPILOT_CLI_ADAPTER_NOTE.md`
14. `SKILL0_COLLABORATION_VISION.md`

## 2. Resource Catalog

現在の registry が扱う shared resource types は次のとおりです：

| Type | Logical root | Purpose |
|---|---|---|
| `skills` | `/registry/skills` | 複数の CLI で共有できる skill 定義 |
| `mcp` | `/registry/mcp` | canonical MCP definitions |
| `agents` | `/registry/agents` | 共通 agent 指示と persona 定義 |
| `workflow` | `/registry/workflow` | 共通フロー、runbook、planning guidance |

次の内容は shared resource type ではありません：

| Area | Logical root | Role |
|---|---|---|
| `operations state` | `/operations` | inventories、backups、drift logs、history records |

## 3. Starter Catalog Shape

最小の catalog entry に最低限必要なもの：

- `id`
- `type`
- `canonical_location`
- `status`

追加推奨：

- `source_of_truth`
- `supported_clis`
- `delivery_guidance`

完全な項目ルールは `RESOURCE_SPEC.md` を参照してください。

## 4. Current Catalog Entries

### Review Shortlist

現在の外部 review 主集は、全候補ではなく [ESSENTIAL_SKILLS_SHORTLIST.md](ESSENTIAL_SKILLS_SHORTLIST.md) にある `8 + 4` の選抜 skills に基づきます。

### Review Package

外部 reviewer 向けの資料をまとめる場合は、[EXTERNAL_REVIEW_PACKAGE.md](EXTERNAL_REVIEW_PACKAGE.md) を入口にし、`local/scripts/export-review-package.ps1` を使って再生成可能な review package を作ってください。

reviewer への最短入口をそのまま渡したい場合は、まず次を見てください：

- [EXTERNAL_REVIEW_COVER_NOTE.md](EXTERNAL_REVIEW_COVER_NOTE.md)
- [EXTERNAL_REVIEW_HIGHLIGHTS.md](EXTERNAL_REVIEW_HIGHLIGHTS.md)

### Template Release

クリーンな starter package を作るには、[TEMPLATE_RELEASE_PACKAGE.md](TEMPLATE_RELEASE_PACKAGE.md) を読み、`local/scripts/export-template-package.ps1` を使ってください。

export 済み starter package を検証するには、`local/scripts/verify-template-package.ps1` を使います。

authoring repo の tracked shared surfaces に live workspace metadata が混入していないかを先に確認したい場合は、`local/scripts/verify-workspace-boundaries.ps1` を使います。

将来 push suitability を議論する前にローカル報告を作りたい場合は、`local/scripts/get-publishability-report.ps1` を使います。

shared metadata の検出ルールを調整したり、ルール事例を理解したい場合は、先に [WORKSPACE_SENSITIVE_METADATA_RULES.md](WORKSPACE_SENSITIVE_METADATA_RULES.md) を読み、その後 `local/scripts/validate-workspace-sensitive-metadata-rules.ps1` を使ってください。

現在の repo を新しい starter project としてそのまま再構築したい場合は、[REBUILD_AS_NEW_PROJECT.md](REBUILD_AS_NEW_PROJECT.md) を読み、次を使ってください：

- `local/scripts/export-rebuild-project.ps1`
- `local/scripts/verify-rebuild-project.ps1`

新しいマシンで最初の initialize → verify を完了したい場合は、次を優先します：

- `local/scripts/bootstrap.py`
- `local/scripts/verify-bootstrap.py`

### Related Concept Notes

`Copilot CLI` の現在の repo-level bootstrap baseline、制約、今後の cross-platform 検証方針を理解したい場合は、[COPILOT_CLI_ADAPTER_NOTE.md](COPILOT_CLI_ADAPTER_NOTE.md) を見てください。

`UniText` と `skill-0` の協力方法を評価したい場合は、[SKILL0_COLLABORATION_VISION.md](SKILL0_COLLABORATION_VISION.md) を見てください。

### Skills

| `id` | Tier | `canonical_location` | `status` |
|---|---|---|---|
| `pdf` | Core 8 | `/registry/skills/pdf` | `active` |
| `docx` | Core 8 | `/registry/skills/docx` | `active` |
| `xlsx` | Core 8 | `/registry/skills/xlsx` | `active` |
| `pptx` | Core 8 | `/registry/skills/pptx` | `active` |
| `mcp-builder` | Core 8 | `/registry/skills/mcp-builder` | `active` |
| `skill-creator` | Core 8 | `/registry/skills/skill-creator` | `active` |
| `webapp-testing` | Core 8 | `/registry/skills/webapp-testing` | `active` |
| `doc-coauthoring` | Core 8 | `/registry/skills/doc-coauthoring` | `active` |
| `frontend-design` | Expansion 4 | `/registry/skills/frontend-design` | `active` |
| `web-artifacts-builder` | Expansion 4 | `/registry/skills/web-artifacts-builder` | `active` |
| `internal-comms` | Expansion 4 | `/registry/skills/internal-comms` | `active` |
| `theme-factory` | Expansion 4 | `/registry/skills/theme-factory` | `active` |

### Workspace-Specific Skills

次の skills は shared registry には存在しますが、現在の外部 review 主集である `8 + 4` shortlist には含まれていません。

| `id` | Tier | `canonical_location` | `status` |
|---|---|---|---|
| `cloudflare` | Workspace | `/registry/skills/cloudflare` | `active` |
| `wrangler` | Workspace | `/registry/skills/wrangler` | `active` |
| `building-mcp-server-on-cloudflare` | Workspace | `/registry/skills/building-mcp-server-on-cloudflare` | `active` |
| `cloudflare-governance` | Workspace | `/registry/skills/cloudflare-governance` | `active` |
| `cloudflare-access-mcp` | Workspace | `/registry/skills/cloudflare-access-mcp` | `active` |
| `cloudflare-edge-security` | Workspace | `/registry/skills/cloudflare-edge-security` | `active` |
| `cloudflare-runtime-sync` | Workspace | `/registry/skills/cloudflare-runtime-sync` | `active` |
| `cloudflare-tunnel-dns` | Workspace | `/registry/skills/cloudflare-tunnel-dns` | `active` |

### Workflow

| Field | Value |
|---|---|
| `id` | `claude-plans` |
| `type` | `workflow` |
| `canonical_location` | `/registry/workflow/claude-plans` |
| `status` | `draft` |
| `source_of_truth` | `/registry/workflow/claude-plans` |
| `supported_clis` | `claude` |
| `delivery_guidance` | Use workflow adapter or project-local plan mapping depending on CLI capability. |

### MCP

| Field | Value |
|---|---|
| `id` | `claude-project-mcp-seed` |
| `type` | `mcp` |
| `canonical_location` | `/registry/mcp/claude-project-mcp-seed` |
| `status` | `active-baseline` |
| `source_of_truth` | `/registry/mcp/claude-project-mcp-seed/definition.json` |
| `supported_clis` | `claude, codex, copilot` |
| `delivery_guidance` | Bootstrap writes a project `.mcp.json`, a Codex native-config entry, and a Copilot `~/.copilot/mcp-config.json` entry pointing to the bundled read-only MCP server. |

### Agents

| Field | Value |
|---|---|
| `id` | `registry-curator` |
| `type` | `agents` |
| `canonical_location` | `/registry/agents/registry-curator` |
| `status` | `active` |
| `source_of_truth` | `/registry/agents/registry-curator/AGENT.md` |
| `supported_clis` | `claude, codex, gemini` |
| `delivery_guidance` | Use as a shared agent persona for review and adoption tasks; actual wiring depends on CLI capability. |

## 5. Example Catalog Entries

### Example: Skill

| Field | Value |
|---|---|
| `id` | `example-skill` |
| `type` | `skills` |
| `canonical_location` | `/registry/skills/example-skill` |
| `status` | `draft` |
| `source_of_truth` | `/registry/skills/example-skill/SKILL.md` |
| `supported_clis` | `undocumented` |
| `delivery_guidance` | Use the skills adapter; resolved mode depends on CLI capabilities and local environment. |

### Example: MCP Definition

| Field | Value |
|---|---|
| `id` | `example-mcp` |
| `type` | `mcp` |
| `canonical_location` | `/registry/mcp/example-mcp` |
| `status` | `draft` |
| `source_of_truth` | `/registry/mcp/example-mcp/definition` |
| `supported_clis` | `undocumented` |
| `delivery_guidance` | Register through the MCP adapter; the final delivery mode depends on CLI capabilities and local environment. |

## 6. Discovery Rules

`INDEX.md` が答えるのは：

- ここにどんな resource があるか
- 各 resource の論理位置はどこか
- どの仕様書や運用文書を見るべきか

`INDEX.md` が直接答えないのは：

- 特定プラットフォームの絶対パス
- 最終的に解決された delivery mode
- ある author workspace のローカル設定
- local authoring plans、review notes、live workspace baselines をどこに置くか。この部分は `DOCUMENT_PLACEMENT_POLICY.md` を参照してください

## 7. How To Use This Baseline

### For Humans

1. まず `VISION.md` を読む
2. `INDEX.md` を使って自分の starter catalog を作る
3. `RESOURCE_SPEC.md` で resource 項目を定義する
4. `OPERATIONS.md` で platform と CLI の接続方式を定義する

### For AI Agents

1. まず `INDEX.md` を discovery の入口として使う
2. schema が必要なら `RESOURCE_SPEC.md` を読む
3. delivery / mutation が必要なら `OPERATIONS.md` を読む
4. 単一環境のパスを仕様上の真実だとみなさない
