---
name: project-bootstrap-architect
description: "Bootstrap new greenfield projects by choosing the right project type, storage model, repo layout, and architecture template before implementation starts. Use when Codex needs to create a new project from scratch, scaffold an initial repo, decide between app types such as CLI, web app, browser extension, service API, desktop helper, or library, and produce the starting file/config structure for that choice."
metadata:
  runtime_support_files: true
---

# Project Bootstrap Architect

## Overview

Use this skill for greenfield work only.
Choose a concrete project archetype, match it with a sensible storage strategy, select the right repository layout, and produce the initial scaffold plan before writing feature code.

Do not use this skill for an already-active codebase that needs audit, maintenance, or iterative delivery. Use `project-development-loop` for that case.

## Workflow

### 0. Check planning and governance entrypoints

Before choosing templates, check whether the user asked for a written plan, plan mode, review gate, skill selection, or local service/port governance.

- If the user asked for a plan before execution, use `plan-first-execution` for the plan template and review gate.
- If the task involves skill creation or consolidation, read [references/skill-entrypoints.md](./references/skill-entrypoints.md).
- If the project needs implementation-support skills, read [references/development-skill-selection.md](./references/development-skill-selection.md).
- If the project will start localhost services, read [references/local-port-registry.md](./references/local-port-registry.md).

### 1. Confirm the bootstrap target

Start by identifying these inputs from the user's request and the creation target only.
Use local context only to understand where the new project should live, what neighboring workspace conventions already exist, or whether the target directory is empty.
If there is already an active codebase with meaningful implementation, stop treating it as bootstrap work and switch to `project-development-loop`.

- Storage root decision is mandatory for every bootstrap invocation.
- Actively ask the user for a project storage root before creating files.
- If the user does not provide a path within the same turn, select an explicit default and use it immediately for all generated artifacts:
  - Default: `<cwd>/projects/<project-slug>` when current directory is not an existing repo root.
  - If current directory already looks like a repo root, default to `<current-dir>`.
- Explicitly state the resolved storage root and lock it as canonical for all subsequent generated files.

- project goal
- primary runtime or platform
- expected interface surface
- persistence needs
- deployment or distribution target
- whether the repo should be monorepo or single-package

If the request is ambiguous, make the smallest reasonable assumption and state it.
Only stop to ask the user when the choice would materially change the architecture or long-term storage model.

### 2. Choose the project type

Map the request to one concrete archetype first.
Read only the relevant section in [references/project-types.md](./references/project-types.md).

Supported archetypes:

- CLI tool
- web app
- browser extension
- service API
- desktop helper
- shared library or SDK
- automation or worker service

If the request spans multiple surfaces, choose the primary runtime first and explicitly note any secondary surfaces.

### 3. Check type-specific hard requirements first

Before choosing style, tooling, or storage, check whether the selected project type has non-negotiable structural or distribution constraints.
These constraints outrank personal preference and generic conventions.

Use them to answer questions like:

- which files must exist
- which file must be at the repo root or build root
- which directory layout is required for packaging
- which runtime boundaries are fixed by the platform
- which config fields are mandatory for the artifact to run or be distributed

Read the matching hard-requirement reference when it exists.
Start with [references/browser-extension-hard-requirements.md](./references/browser-extension-hard-requirements.md) for Chrome or Chromium extension work.
Use [references/service-api-hard-requirements.md](./references/service-api-hard-requirements.md) for service API or backend service bootstrap work.
Use [references/desktop-helper-hard-requirements.md](./references/desktop-helper-hard-requirements.md) for local assistant, local daemon, tray app, or desktop automation bootstrap work.

### 4. Choose persistence and state handling

Pick the lightest storage model that satisfies the product need.
Read [references/storage-patterns.md](./references/storage-patterns.md) after the project type is known.

Default order of preference:

- in-memory only
- local file storage
- SQLite
- hosted relational database
- object storage plus metadata store

Separate these concerns clearly:

- app configuration
- runtime cache
- user content
- durable product data
- logs and audit artifacts

### 5. Choose the repository layout and config set

After type and storage are known, choose the repository shape.
Read [references/repo-layouts.md](./references/repo-layouts.md) for the matching archetype.
Read [references/toolchain-selection.md](./references/toolchain-selection.md) to choose framework, package manager, test stack, linting, and scaffold template defaults.
For local web apps, service APIs, MCP servers, browser bridges, daemons, or worker dashboards, read [references/local-port-registry.md](./references/local-port-registry.md) before assigning dev-server ports.

Decide:

- single package vs monorepo
- package manager
- language choice
- framework or runtime template
- test runner
- lint and format tools
- environment variable files
- docs expected at repo start
- local port block and registry path, when localhost services are involved
- development-support skills, when the project needs AI-agent workflow support

Prefer the smallest layout that still leaves a clear path for growth.

### 6. Produce the bootstrap output

For a new project, output these items in order unless the user asked for a different format:

1. chosen archetype
2. hard requirements that drive the structure
3. chosen storage model
4. chosen repo layout
5. key architecture decisions
6. initial file and folder scaffold
7. config files to create
8. local port allocation, if needed
9. recommended development/support skills, if needed
10. review gate, if planning or governance was requested
11. next implementation step

When the user wants code immediately, create the scaffold after presenting the decision summary.

## Output rules

- Be explicit about assumptions.
- Treat project-type hard requirements as mandatory, not optional suggestions.
- Explain why the chosen template fits better than the nearest alternative.
- Keep the first scaffold intentionally small.
- Do not invent production infrastructure that the user did not ask for.
- Default to i18n-ready structure for user-facing applications.
- Default to English source strings with additional locale folders when the app has UI or end-user copy.
- If the user explicitly chooses Python, Go, Rust, or another non-JavaScript stack, use the language-specific defaults in `toolchain-selection.md` instead of forcing JavaScript assumptions.

## Reference loading guide

- Read [references/project-types.md](./references/project-types.md) to choose the archetype.
- Read the matching hard-requirement reference for any platform with strict packaging or runtime structure.
- Read [references/browser-extension-hard-requirements.md](./references/browser-extension-hard-requirements.md) for Chrome or Chromium extension work before choosing templates.
- Read [references/service-api-hard-requirements.md](./references/service-api-hard-requirements.md) for service API work before choosing frameworks or folder layout.
- Read [references/desktop-helper-hard-requirements.md](./references/desktop-helper-hard-requirements.md) for local assistant, daemon, tray app, or desktop automation work before choosing templates.
- Read [references/storage-patterns.md](./references/storage-patterns.md) after the archetype is known.
- Read [references/toolchain-selection.md](./references/toolchain-selection.md) before choosing framework and starter stack defaults.
- Read [references/repo-layouts.md](./references/repo-layouts.md) last to produce the file/config scaffold.
- Read [references/skill-entrypoints.md](./references/skill-entrypoints.md) when the task includes skill creation, installation, duplicate skill entries, or skill consolidation.
- Read [references/development-skill-selection.md](./references/development-skill-selection.md) when the project should start with a recommended skill set.
- Read [references/local-port-registry.md](./references/local-port-registry.md) when localhost ports or long-running local services are involved.

Load only the relevant sections for the selected project type.
