# UniText Root Document Surface Review

> Status: active assessment
> Date: 2026-04-20
> Purpose: record the first consolidation pass for repo-root documents, explain whether the `UniText` folder location matters, and summarize how the current architecture differs from the earlier model.

## 1. Does the `UniText` folder location matter?

Yes, but only for the local delivery layer, not for the shared contract itself.

### What does not materially depend on the absolute path

- tracked shared docs
- `registry/` canonical resources
- `runtime/` tracked read model
- template-safe files such as the tracked `.mcp.json` seed

These should remain portable and must not depend on one specific drive letter.

### What does depend on the working location

- machine-local `bootstrap.py` delivery
- home-directory CLI targets such as `~/.claude/skills`, `~/.gemini/skills`, `~/.agents/skills`
- local MCP command arguments that point at the current repo root
- symlink creation and path resolution behavior on the host OS

### Recommended placement

Use a stable local projects root, for example:

- `Q:\\Projects\\UniText`
- `~/Projects/UniText`

Avoid placing the authoring repo in:

- cloud-synced folders
- Desktop / Downloads / temporary directories
- paths that change often
- deeply nested paths that increase Windows path risk
- locations with restricted symlink or scripting behavior

### Decision keys

Choose the location using these criteria:

1. local disk, not synced workspace
2. short and stable path
3. predictable write permission
4. safe for symlink/junction behavior
5. separate from export outputs, Obsidian vaults, or temporary review packages

## 2. First consolidation pass

This pass only moved low-risk reports and logs with limited inbound linkage.

### Moved out of repo root

- [docs/project-map/PROJECT_MAP_WEB_AUTOMATION_REPORT.md](../project-map/PROJECT_MAP_WEB_AUTOMATION_REPORT.md)
- [docs/project-map/PROJECT_MAP_YOLO_5H_DEVELOPMENT_LOG.md](../project-map/PROJECT_MAP_YOLO_5H_DEVELOPMENT_LOG.md)
- [docs/reports/status/PROJECT_STATUS_REPORT_2026-04-10.md](../reports/status/PROJECT_STATUS_REPORT_2026-04-10.md)
- [docs/reviews/SECURITY_ATTACK_INPUT_RESPONSE_REPORT.md](../reviews/SECURITY_ATTACK_INPUT_RESPONSE_REPORT.md)

### Why these moved first

- they are not startup docs
- they are not part of the runtime contract
- they are not first-pass template/rebuild requirements
- they behave more like reports, logs, or implementation notes than baseline specs

## 3. Root docs that should remain in the near-term core set

These files are still reasonable to keep at repo root for now:

- `AGENTS.md`
- `README.md`
- `INDEX.md`
- `RUNTIME.md`
- `VISION.md`
- `RESOURCE_SPEC.md`
- `OPERATIONS.md`
- `PROJECT_MODES.md`
- `DOCUMENT_PLACEMENT_POLICY.md`
- `WORKSPACE_SENSITIVE_METADATA_RULES.md`
- `WORKSPACE_SENSITIVE_METADATA_RULES.json`
- `NO_PUBLISH_POLICY.md`
- `SECRET_HANDLING_GUIDELINES.md`
- `TEMPLATE_RELEASE_PACKAGE.md`
- `TEMPLATE_RELEASE_CHECKLIST.md`
- `REBUILD_AS_NEW_PROJECT.md`
- `TEST_BASELINE.md`

These either act as startup/discovery surfaces, formal policy, or active release/rebuild constraints.

## 4. Second-wave consolidation candidates

The following files are likely move candidates, but were intentionally not moved in this first pass because they have broader linkage across exports, i18n, or review flows:

- `EXTERNAL_REVIEW_COVER_NOTE.md`
- `EXTERNAL_REVIEW_HIGHLIGHTS.md`
- `EXTERNAL_REVIEW_PACKAGE.md`
- `ESSENTIAL_SKILLS_SHORTLIST.md`
- `MILESTONES.md`
- `PROJECT_STATUS_REPORT_2026-03-23.md`
- `COPILOT_CLI_ADAPTER_NOTE.md`
- `CROSS_PLATFORM_SCRIPT_PORTABILITY_PLAN.md`
- `SKILL0_COLLABORATION_VISION.md`
- `BOUNDARY_INCIDENT_REVIEW_TEMPLATE.md`

Recommended future destinations:

- `docs/reviews/`
- `docs/reports/status/`
- `docs/adapters/`
- `docs/plans/`
- `docs/concepts/`

## 5. Current architecture vs. previous architecture

### Previous model

- root docs were overloaded as both human orientation and de facto agent startup
- `registry/skills` was still close to the effective delivery surface for some CLIs
- architecture reports, status snapshots, concept notes, and active specs all competed in the same repo-root area
- the runtime delivery boundary existed only partially in scripts and local conventions

### Current model

- `RUNTIME.md` plus `runtime/*` defines the consumer-agent startup surface
- `registry/` remains canonical authoring source
- `runtime/` is the tracked consumer read model
- `local/` is clearly the machine-local wiring and delivery layer
- repo-root docs are becoming more intentionally split between:
  - startup / discovery / policy
  - reports and implementation notes moved into `docs/`

### Practical effect

The repo is now easier to interpret in layers:

1. `README.md` / `INDEX.md` for humans
2. `RUNTIME.md` / `runtime/*` for consumer agents
3. `registry/` for canonical source
4. `local/` for delivery wiring
5. `docs/` for reports, logs, plans, and architecture background

## 6. Recommended next step

Do a second consolidation wave only after:

- export/review scripts are updated for moved files
- i18n references are intentionally migrated
- the repo-root target set is explicitly capped

Until then, keep root cleanup incremental rather than trying to move every secondary file in one pass.
