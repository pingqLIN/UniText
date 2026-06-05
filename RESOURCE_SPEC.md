# UniText — Resource Spec

> Status: active baseline
> Scope: metadata and projection contract for shared resources.

This spec keeps resource metadata readable by humans, discoverable by agents, and stable enough for runtime builders and adapter scripts.

## 1. Resource Types

| Type | Canonical root | Purpose |
|---|---|---|
| `skill` | `registry/skills/` | Reusable procedure, prompt, capability pack, and support assets |
| `mcp` | `registry/mcp/` | MCP server definition, policy, and adoption notes |
| `agent` | `registry/agents/` | Persona, role instructions, or playbook |
| `workflow` | `registry/workflow/` | Repeatable process, runbook, or plan template |

Operations artifacts, local notes, generated reports, backups, and review packets are not shared resource types by default.

## 2. Required Fields

Every catalogable resource should expose these fields, either through frontmatter, a definition file, or generated catalog metadata:

| Field | Type | Meaning |
|---|---|---|
| `id` | string | Stable kebab-case identifier |
| `type` | enum | `skill`, `mcp`, `agent`, or `workflow` |
| `title` | string | Human-readable display name |
| `status` | enum | `draft`, `active`, `deprecated`, or `archived` |
| `summary` | string | Short discovery-first description |
| `source_of_truth` | path | Canonical authoring entrypoint |
| `runtime_projection` | path | Main runtime entrypoint, when projected |

## 3. Recommended Fields

| Field | Type | Meaning |
|---|---|---|
| `owners` | array | Maintainers or responsible role |
| `tags` | array | Search and routing hints |
| `audiences` | array | `human`, `agent`, `operator`, or host-specific audience |
| `delivery` | object | Preferred delivery hints by host or surface |
| `compatibility` | object | Host-specific limitations and dated verification |
| `references` | array | Related docs, policies, examples, or source links |
| `trigger_examples` | array | Short phrases that should route to this resource |
| `avoid_when` | array | Short phrases or contexts that should not route here |
| `context_budget_hint` | enum | Suggested minimum budget such as `L0`, `L1`, `L2`, `L3`, or `L4` |
| `last_reviewed` | date | Last human review date |
| `release_surface` | enum | `shared`, `local-only`, or `template-only` |

## 4. Naming Rules

- Use kebab-case for `id`.
- Do not create multiple IDs for the same semantic resource.
- Make `summary` short enough for progressive disclosure.
- Use `title` for humans, `summary` for discovery, and `source_of_truth` for exact file targeting.
- Keep `trigger_examples`, `avoid_when`, and `context_budget_hint` compact. They are routing hints, not full instructions.
- Avoid machine-specific absolute paths in shared metadata.

## 5. Runtime Catalog Projection

`runtime/catalog.json` is a discovery artifact, not a full content dump. It should preserve enough information for an agent or adapter to decide what to open next:

- `id`
- `type`
- `status`
- `summary`
- `source_of_truth`
- `runtime_projection`
- `delivery`
- `references`
- compact trigger and context-budget hints when available

Documentation-only work should not edit `runtime/catalog.json` by hand. If registry or runtime source files change, rebuild with:

```powershell
python local/scripts/build-runtime-layer.py --write
```

Use the dry-run form first:

```powershell
python local/scripts/build-runtime-layer.py
```

## 6. Example Skill Metadata

```yaml
id: review-pr
type: skill
title: Review Pull Request
status: active
summary: Review a pull request for regressions, missing tests, and unsafe behavior.
source_of_truth: registry/skills/review-pr/SKILL.md
runtime_projection: runtime/skills/review-pr/SKILL.md
trigger_examples:
  - review this PR
  - inspect this uncommitted diff
avoid_when:
  - implement the fix directly
context_budget_hint: L2
audiences:
  - agent
  - reviewer
delivery:
  codex:
    mode: symlink
    preferred_surface: .agents/skills
  claude:
    mode: mirror
    preferred_surface: .claude/skills
references:
  - OPERATIONS.md
  - docs/adapters/CODEX_CLI_ADAPTER_NOTE.md
```

## 7. Example MCP Metadata

```yaml
id: project-docs-mcp
type: mcp
title: Project Docs MCP
status: draft
summary: Expose reviewed project docs through a read-only MCP server.
source_of_truth: registry/mcp/project-docs-mcp/definition.json
runtime_projection: runtime/catalog.json
delivery:
  codex:
    mode: native-config
  copilot:
    mode: native-config
release_surface: shared
```

## 8. Conflict Rules

If the same `(type, id)` maps to different content:

- do not overwrite automatically
- do not silently infer the canonical source
- stop at `REVIEW / DRY-RUN`
- choose one canonical source, rename the competing resource, or mark one as `deprecated` / `archived`

## 9. Common Mistakes

| Mistake | Correction |
|---|---|
| Long essay in `summary` | Keep summary short and route deep content through `source_of_truth` |
| Full instructions in routing fields | Keep routing fields short and load the resource only after the trigger matches |
| `source_of_truth` points to a folder only | Point to the main entry file |
| Delivery mode treated as permanent | Resolve mode at adapter time |
| Local absolute path in shared metadata | Put machine paths in `local/` or ignored operational evidence |
| Runtime catalog changed manually | Change registry/runtime source, then rebuild |

## 10. Related Docs

- [RUNTIME.md](RUNTIME.md)
- [OPERATIONS.md](OPERATIONS.md)
- [DOCUMENT_PLACEMENT_POLICY.md](DOCUMENT_PLACEMENT_POLICY.md)
