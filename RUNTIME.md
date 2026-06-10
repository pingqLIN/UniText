# UniText Runtime Entry

> Status: active baseline
> Role: shortest safe entrypoint for consumer agents and automation.

If you are an agent executing work in this repository, start here. Do not use `README.md` or `INDEX.md` as your default startup surface, except when the request is explicitly human-facing discovery.

## First Read Order

1. [runtime/START.md](runtime/START.md)
2. [runtime/RULES.md](runtime/RULES.md)
3. [runtime/ROUTES.md](runtime/ROUTES.md)
4. [runtime/catalog.json](runtime/catalog.json)

Read only the deeper source files that the runtime view points to.

## Runtime Contract

- `registry/` is the canonical authoring source, not the default consumer runtime.
- `runtime/` is the tracked read model for agents. It is generated from `registry/` and intentionally keeps startup context low-noise.
- `runtime/catalog.json` is discovery-first. It should contain stable IDs, resource types, status, summary, source pointers, runtime projection pointers, delivery hints, and references.
- `bootstrap.py` rebuilds the runtime layer before applying local delivery wiring.
- Codex should read its configured local `skills_path` target, not point directly at `registry/skills`.
- If a task needs canonical content, follow the runtime projection back to its `source_of_truth` or use the project-local MCP surface.

## Request Budget Routing

Classify the request before opening deeper files, skills, connectors, or web tools. Default to the smallest budget that can answer correctly:

| Budget | Use for | Runtime rule |
|---|---|---|
| `L0 no-tool` | General answers, wording, translation, brainstorming, static reasoning | Do not load skills, files, connectors, or web tools. |
| `L1 light-retrieval` | Known file lookup, metadata checks, small snippets | Read only the route file, catalog entry, or narrow snippet needed. |
| `L2 targeted-retrieval` | Questions that require specific file evidence or limited comparison | Search first, then open only matching sections. |
| `L3 artifact` | Creating, editing, converting, or exporting PDF, DOCX, PPTX, XLSX, images, or similar artifacts | Load only the matching artifact skill and its direct support files. |
| `L4 complex` | Multi-file synthesis, migration, governance rewrite, broad analysis, or data-heavy work | State the expanded scope, keep intermediate summaries, and avoid unrelated skill/tool loading. |

Escalate only when the current budget cannot satisfy the request. Do not pre-load artifact skills, registry folders, connector instructions, or full documents just because they exist.

## Tool And Skill Triggers

| Surface | Use when | Avoid when |
|---|---|---|
| Web/search | The user asks for current, latest, recently changed, uncertain, citation-required, legal, financial, medical, schedule, price, or product information | Rewriting, translation, static repo reasoning, or known local facts |
| File search/read | The user references an uploaded file, repo file, prior document, or asks what a file says | Pure conceptual discussion or ordinary writing |
| Artifact skills | The user asks to create, edit, convert, export, validate, or package that artifact type | Draft text only, brainstorming, or ordinary explanation |
| Connectors | The task requires the user's connected email, calendar, drive, issue tracker, deployment, or account data | Public info, local repo work, or simulated examples |
| Code/runtime tools | The task requires local execution, tests, generated files, repo inspection, or reproducible evidence | Simple explanation where execution adds no confidence |

## Task Routing

| Task | Start here |
|---|---|
| Understand what UniText is | [README.md](README.md), then [VISION.md](VISION.md) |
| Find human-facing docs or catalog excerpts | [INDEX.md](INDEX.md) |
| Inspect runtime inventory | [runtime/catalog.json](runtime/catalog.json) |
| Understand metadata requirements | [RESOURCE_SPEC.md](RESOURCE_SPEC.md) |
| Plan delivery into host tools | [OPERATIONS.md](OPERATIONS.md) |
| Work on Codex runtime duplication | [docs/operations/skill-runtime-codex-duplication.SOP.md](docs/operations/skill-runtime-codex-duplication.SOP.md) |
| Attach UniText to an existing machine | [docs/plans/EXISTING_ENVIRONMENT_ADOPTION_PLAN.md](docs/plans/EXISTING_ENVIRONMENT_ADOPTION_PLAN.md) |

## Safety Rules

- Do not push, upload, paste, or publish repository content unless the user explicitly approves that action.
- Do not mutate host configuration without a dry-run plan, backup or rollback path, and verification step.
- Do not treat generated `ops/` evidence, local notes, or review packets as publishable docs by default.
- Do not edit `runtime/catalog.json` manually for documentation-only work. Rebuild it through `python local/scripts/build-runtime-layer.py --write` only when registry/runtime source files changed.

## Minimal Verification

For documentation or governance changes, prefer this small baseline first:

```powershell
git diff --check
python local/scripts/build-runtime-layer.py
python local/scripts/verify-workspace-boundaries.py --format json
python local/scripts/audit-i18n-drift.py --format json --sample-size 0 --exit-zero
python -m unittest tests.test_registry_inventory tests.security.test_i18n_drift tests.security.test_workspace_sensitive_metadata tests.security.test_release_hygiene
```

Expand to [TEST_BASELINE.md](TEST_BASELINE.md) when registry, runtime generation, template export, or project-map behavior changes.
