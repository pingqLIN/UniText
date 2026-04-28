# Project Map Governance UI Rework Plan

Date: `2026-04-28`
Scope: project-map interactive UI, governance resolver, and local-only governance reports.
Primary files:

- `local/scripts/build-project-map.py`
- `local/scripts/project-map-runtime.js`
- `local/scripts/project-map-template.html`
- `local/scripts/resolve-agent-governance.py`
- `local/config/agent-governance-layers.json`
- `docs/project-map/DESIGN.md`

## Goal

Make the governance UI explain and resolve the real layered instruction environment that affects agents in practice:

1. include global-home `C:\Users\miles\.codex\AGENTS.md` as a first-class governance source;
2. keep project-controlled files automatic while allowing manual selection for external files and alternate install paths;
3. add an interactive funnel-style explanation page for how rules are layered by location and execution environment;
4. allow governance resolution for a user-selected path, including paths outside the repo when the user explicitly provides them;
5. fix current project-map ergonomics: masthead collapse loop, map dragging/viewport control, duplicate navigation/filter controls, and text-scale range.

## Current State

The current resolver reads only:

- workspace overlay: `Q:\AGENTS.md`
- repo-local: `Q:\UniText\AGENTS.md`

The real global-home file exists at:

- `C:\Users\miles\.codex\AGENTS.md`

The UI already has a governance panel, but it is mostly a resolver form. It does not yet teach the layered execution model visually, and it does not expose source-path configuration or arbitrary path analysis as first-class controls.

## Design Principles

1. Keep structured policy and discovered instruction files separate.
   `agent-governance-layers.json` defines model/environment/profile policy. `AGENTS.md` files provide file-based instruction evidence.

2. Treat project-external paths as user-controlled inputs.
   The repo can auto-suggest `C:\Users\miles\.codex\AGENTS.md`, but browser-side reading or report writing outside the repo must rely on explicit user selection or manual path configuration.

3. Preserve share-safe boundaries.
   The interactive page may show native paths and governance controls. The share-safe page must continue removing native repo paths, governance source details, write controls, and browser scan capability.

4. Keep Python and browser resolver behavior aligned.
   Changes to source precedence or output shape must be mirrored between `resolve-agent-governance.py`, `build-project-map.py`, and `project-map-runtime.js`.

## Required Architecture

### Governance Resolution Contract

All resolver surfaces must use one shared output contract:

- Python CLI: `local/scripts/resolve-agent-governance.py`
- Python generator payload: `local/scripts/build-project-map.py`
- Browser resolver: `local/scripts/project-map-runtime.js`

The resolution output must contain:

- `matched_layers`
- `effective_config`
- `provenance`
- `agents_sources`
- `effective_file_rules`
- `effective_hard_rules`
- `operational_guidance`
- `instruction_evaluation`
- `analysis_path`
- `path_classification`

`effective_config` is authoritative only for structured `agent-governance-layers.json` policy. AGENTS-derived rules are evidence, not a complete override engine. Each file rule should carry:

- `rule_category`: `hard_rule` or `operational_guidance`
- `inspectable`: boolean
- `effective`: boolean
- `evidence_only`: boolean
- `shadowed`: boolean
- `conflict`: boolean
- `unresolved_reason`

The UI must not present file-based AGENTS extraction as the complete runtime/system/developer/user-request instruction stack. The funnel view must mark platform/system/developer/runtime/session instructions as higher-priority but non-inspectable from repo files.

### Source Layers

Add a three-tier file-source model:

- `global-home`: `C:\Users\miles\.codex\AGENTS.md`
- `workspace`: `Q:\AGENTS.md`
- `repo`: `Q:\UniText\AGENTS.md`

The source model should report:

- `scope`
- `path`
- `suggested_path`
- `manual_path`
- `exists`
- `readable`
- `source_kind`: `auto`, `manual`, or `missing`
- `project_external`: boolean
- `handle_bound`
- `permission_state`
- `last_loaded_at`
- `applies_to_path`
- `inspectable`
- `precedence`
- `unresolved_reason`
- parsed sections and rules when readable

External sources may be visible in interactive local-only artifacts, but their raw full text must not be copied into share-safe artifacts or handoff artifacts. The share-safe path must strip global-home paths, manual external paths, source rule content, governance panels, governance navigation, and write controls.

### Manual Source Configuration

Add a UI-facing settings model for key files:

- global-home AGENTS path
- workspace AGENTS path
- repo AGENTS path
- optional analysis path
- output directory for generated governance reports

Browser-side storage can use localStorage for UI preferences. Actual external-file content reading should require explicit browser permission where available. If a browser cannot read a manually provided external path, the UI should still display the path and mark it as unresolved rather than pretending it was analyzed.

The governance report output remains repo-scoped for the first implementation batch. A typed external output path should be rejected with a clear explanation unless a later explicit external directory picker is added.

### Arbitrary Path Governance Resolution

Add a path-analysis mode:

- user enters or selects a path
- resolver classifies whether the path is inside repo, workspace, global-home, or external/unknown
- result explains which file-based sources would affect that path
- UI shows inherited source order and unresolved sources

This is a governance explanation mode. It must not mutate files.

Path classification rules:

- Python should use resolved/canonical paths where possible.
- Browser-side classification must mark string-only decisions as `unverified_path_classification`.
- Prefix checks must be boundary-aware so `Q:\UniText-other` is not classified as inside `Q:\UniText`.
- The test matrix must include case-insensitive Windows paths, trailing slashes, sibling prefixes, missing paths, UNC-like paths, WSL-like paths, and external drive paths.
- Applicable sources should be computed for the analysis path. Global-home is always-above file evidence; workspace and repo sources apply only when the path is inside their corresponding tree.

## UI Changes

### Governance Explanation Page

Add a dedicated governance explanation section under the governance workspace. It should render a dynamic funnel:

- top: runtime/system/developer/session instructions, shown as higher but not inspectable from repo files
- next: global-home AGENTS
- next: workspace AGENTS
- next: repo-local AGENTS
- bottom: direct user request/current task

Mouse interaction:

- hover a funnel layer to highlight the corresponding source, rules, and effective config provenance
- click a layer to pin its detail
- path-analysis result should visually highlight the layers that apply
- non-inspectable layers must be visually distinct from file-based inspectable layers

### Governance Settings

Add a feature/settings panel under the main navigation controls:

- lists key source files and existence status
- allows manual path overrides
- makes project-external sources visually distinct
- persists UI-only settings locally

This panel is part of the interactive operator page only.

### Masthead Collapse

Replace the current height-sensitive auto-expand behavior with a sticky latch:

- once the masthead auto-collapses, it stays collapsed
- it expands again only through an explicit user action
- this prevents collapse/expand loops caused by layout height crossing the threshold after collapse
- add a visible expand/collapse control with `aria-expanded`
- add `autoCollapsedLatch` state
- tour mode may temporarily expand the masthead without clearing the latch
- manual expand clears the latch until the next user navigation or explicit collapse

### Map Dragging And Viewport

Add direct map panning:

- pointer-drag on map background moves the viewport
- wheel or controls adjust zoom/pan within bounded limits
- add manual viewport controls for reset, zoom in, zoom out, and fit
- keep minimap and selected-node behavior coherent with the current viewport

Use a single viewport contract:

- `viewport.scale`
- `viewport.offsetX`
- `viewport.offsetY`
- `viewport.mode`: `scroll` or `transform`

The first implementation should prefer the existing scroll-container model and add drag-to-scroll plus manual scroll/fit/zoom affordances before introducing an SVG transform. If zoom is implemented as CSS transform, node focus, minimap viewport, and selected-node scroll must all use the same contract. Background drag must use a threshold so node clicks do not become accidental drags.

### Duplicate Controls Cleanup

Reduce duplicated UI:

- keep the top workspace tabs as the primary workspace navigation surface
- remove the lower workspace preview rail
- keep one quick-filter chip surface and move counts into the primary navigation/control area
- remove duplicate quick-filter chips from the operator focus area
- make the remaining navigation controls more visible
- return the saved vertical space to the main visual map area

### Text Scale Range

Expand text-scale choices beyond current `sm / md / lg`.

Proposed range:

- `xs`
- `sm`
- `md`
- `lg`
- `xl`

Proposed multipliers:

- `xs = 0.84`
- `sm = 0.92`
- `md = 1.00`
- `lg = 1.12`
- `xl = 1.24`

The map, list, detail, and compact panels should continue fitting text without overlap.

## Implementation Phases

### Phase 1: Plan Review And Source Model

- write this plan
- get three external review passes
- revise the plan
- add a single governance source model contract
- add source-model helpers shared by Python generator and CLI resolver
- include global-home AGENTS in CLI output, generator payload, and browser resolver source list
- add tests for source discovery, precedence, source status, and Python/browser schema parity

### Phase 2: External Source Safety And Path Classification

- implement path classification contract
- add source leak tests for share-safe HTML, handoff JSON, and handoff markdown
- ensure global-home and manual external paths do not appear in share-safe artifacts
- keep governance report output repo-scoped until explicit external directory support exists

### Phase 3: Governance UI And Settings

- add governance settings panel
- add path-analysis inputs and source-status rendering
- add funnel-style interactive explanation
- align UI resolver output with Python resolver output

### Phase 4: Map Ergonomics

- fix masthead collapse latch
- add map panning and viewport controls
- expand text-scale range
- remove duplicate nav/filter surfaces and recover space for the map

### Phase 5: Verification And Review

- regenerate project-map artifacts
- run syntax and unit checks
- perform browser/manual smoke on the local UI
- run three external implementation reviews
- fix review findings
- write final stage report

## Validation Plan

Minimum checks:

- `python -m py_compile local/scripts/build-project-map.py local/scripts/resolve-agent-governance.py`
- `node --check local/scripts/project-map-runtime.js`
- `python local/scripts/build-project-map.py`
- project-map output contains governance source status for global-home, workspace, and repo
- share-safe output does not expose native paths or governance write controls
- UI can resolve governance without writing
- UI can write reports only after repo handle selection
- masthead does not enter collapse/expand loop
- map can pan, reset, zoom in, zoom out, and fit
- share-safe HTML does not contain `C:\\Users\\miles\\.codex`
- share-safe HTML does not contain manual external source paths
- handoff artifacts do not contain external AGENTS content
- path classifier covers case-insensitive paths, trailing slash, sibling-prefix, missing path, UNC-like path, WSL-like path, and external drive
- browser smoke checks masthead latch, drag-to-pan, viewport controls, and settings persistence when Playwright is available

## Done Criteria

- global-home `C:\Users\miles\.codex\AGENTS.md` is represented in resolver output when present
- UI shows key governance files and allows manual path override
- governance explanation page makes the layered rule funnel visible and interactive
- arbitrary path analysis produces a clear applicable-source report
- duplicated navigation/filter surfaces are reduced
- map viewport can be directly manipulated by mouse
- static and share-safe artifacts are regenerated
- three external reviewers have reviewed the implementation and all accepted findings are addressed

## Reviewer Findings Incorporated

The initial three-review gate required these plan changes before implementation:

- make global-home a real source in CLI, generator payload, and browser resolver, not just a UI label
- define a single governance resolution contract and reduce Python/browser schema drift
- treat AGENTS rules as file-based evidence with explicit inspectability and unresolved-state flags
- define external source permissions and avoid leaking global-home/manual external data into share-safe or handoff artifacts
- define boundary-aware path classification before arbitrary path analysis
- split implementation into reviewable batches
- specify masthead latch control, viewport model, duplicate-control choice, and text-scale multipliers
