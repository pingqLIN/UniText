# UniText — Index

> 状態：Template Base
> 役割：すべての human / AI にとっての最初の読書点であり、discovery の入口。

`UniText` は純文本を共有インターフェースとして用い、cross-CLI の統一互換性と AI-first discovery を重視します。

## 1. Core Docs

推奨読書順：

1. `INDEX.md`
2. `VISION.md`
3. `RESOURCE_SPEC.md`
4. `OPERATIONS.md`
5. `PROJECT_MODES.md`
6. `MILESTONES.md`
7. `EXTERNAL_REVIEW_PACKAGE.md`
8. `EXTERNAL_REVIEW_COVER_NOTE.md`
9. `EXTERNAL_REVIEW_HIGHLIGHTS.md`
10. `TEMPLATE_RELEASE_PACKAGE.md`
11. `TEMPLATE_RELEASE_CHECKLIST.md`
12. `SECRET_HANDLING_GUIDELINES.md`
13. `NO_PUBLISH_POLICY.md`
14. `SKILL0_COLLABORATION_VISION.md`

## 2. Resource Catalog

現在の registry が扱う shared resource types は次の通りです。

| Type | Logical root | Purpose |
|---|---|---|
| `skills` | `/registry/skills` | 複数 CLI で共用できる skill 定義 |
| `mcp` | `/registry/mcp` | canonical MCP definitions |
| `agents` | `/registry/agents` | 共用 agent 指示と persona 定義 |
| `workflow` | `/registry/workflow` | 共通の流れ、runbook、planning guidance |

次の内容は shared resource type ではありません。

| Area | Logical root | Role |
|---|---|---|
| `operations state` | `/operations` | inventories、backups、drift logs、history records |

## 3. Starter Catalog Shape

最小の catalog entry は、少なくとも次を含むべきです。

- `id`
- `type`
- `canonical_location`
- `status`

推奨の追加項目：

- `source_of_truth`
- `supported_clis`
- `delivery_guidance`

完全な欄位規則は `RESOURCE_SPEC.md` を参照してください。

## 4. Current Catalog Entries

### Review Shortlist

現在の外部審査主集は、全量候補ではなく [ESSENTIAL_SKILLS_SHORTLIST.md](ESSENTIAL_SKILLS_SHORTLIST.md) の `8 + 4` 精選 skills を基準にします。

### Review Package

外部審査者向けに資料を整理する場合は、[EXTERNAL_REVIEW_PACKAGE.md](EXTERNAL_REVIEW_PACKAGE.md) を入口にし、`local/scripts/export-review-package.ps1` で再生成可能な review package を出力してください。

審査者に最短で見せたい場合は、まず次を確認します。

- [EXTERNAL_REVIEW_COVER_NOTE.md](EXTERNAL_REVIEW_COVER_NOTE.md)
- [EXTERNAL_REVIEW_HIGHLIGHTS.md](EXTERNAL_REVIEW_HIGHLIGHTS.md)

### Template Release

乾いた starter package にまとめたい場合は、[TEMPLATE_RELEASE_PACKAGE.md](TEMPLATE_RELEASE_PACKAGE.md) を確認し、`local/scripts/export-template-package.ps1` を使ってください。

出力済み starter package を検証するには、`local/scripts/verify-template-package.ps1` を使います。

新しい machine で最初の initialize → verify を完了するには、まず次を使ってください。

- `local/scripts/bootstrap.py`
- `local/scripts/verify-bootstrap.py`

### Related Concept Notes

`UniText` と `skill-0` の協業方法を評価したい場合は、[SKILL0_COLLABORATION_VISION.md](SKILL0_COLLABORATION_VISION.md) を確認してください。

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

### Workflow

| Field | Value |
|---|---|
| `id` | `claude-plans` |
| `type` | `workflow` |
| `canonical_location` | `/registry/workflow/claude-plans` |
| `status` | `draft` |
| `source_of_truth` | `/registry/workflow/claude-plans` |
| `supported_clis` | `claude` |
| `delivery_guidance` | CLI の能力に応じて workflow adapter または project-local plan mapping を使う。 |

### MCP

| Field | Value |
|---|---|
| `id` | `claude-project-mcp-seed` |
| `type` | `mcp` |
| `canonical_location` | `/registry/mcp/claude-project-mcp-seed` |
| `status` | `active-baseline` |
| `source_of_truth` | `/registry/mcp/claude-project-mcp-seed/definition.json` |
| `supported_clis` | `claude, codex` |
| `delivery_guidance` | bootstrap は project `.mcp.json` と、bundled read-only MCP server を指す Codex native-config entry を書き込む。 |

### Agents

| Field | Value |
|---|---|
| `id` | `registry-curator` |
| `type` | `agents` |
| `canonical_location` | `/registry/agents/registry-curator` |
| `status` | `active` |
| `source_of_truth` | `/registry/agents/registry-curator/AGENT.md` |
| `supported_clis` | `claude, codex, gemini` |
| `delivery_guidance` | review と adoption 作業に使う shared agent persona として扱う。実際の wiring は CLI の能力に依存する。 |

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
| `delivery_guidance` | skills adapter を使う。解決される mode は CLI の能力と local environment に依存する。 |

### Example: MCP Definition

| Field | Value |
|---|---|
| `id` | `example-mcp` |
| `type` | `mcp` |
| `canonical_location` | `/registry/mcp/example-mcp` |
| `status` | `draft` |
| `source_of_truth` | `/registry/mcp/example-mcp/definition` |
| `supported_clis` | `undocumented` |
| `delivery_guidance` | MCP adapter を通じて登録する。最終的な delivery mode は CLI の能力と local environment に依存する。 |

## 6. Discovery Rules

`INDEX.md` が答えるのは次の内容です。

- ここにどんな資源があるか
- 各資源の論理位置はどこか
- どの CLI がサポートされているか

`INDEX.md` が直接答えないのは次の内容です。

- ある platform の absolute path
- 最終的に解決済みの delivery mode
- ある作者 workspace の本機設定

## 7. How To Use This Baseline

### For Humans

1. まず `VISION.md` を読む
2. `INDEX.md` を使って starter catalog を組み立てる
3. `RESOURCE_SPEC.md` で資源欄位を定義する
4. `OPERATIONS.md` で platform と CLI の接続方法を定義する

### For AI Agents

1. まず `INDEX.md` を discovery の入口として扱う
2. schema が必要なら `RESOURCE_SPEC.md` を読む
3. delivery / mutation が必要なら `OPERATIONS.md` を読む
4. 単一 deployment の path を規格上の真実と見なさない
