---
runtime_projection: true
source_of_truth: registry/skills/project-bootstrap-architect/references/desktop-helper-hard-requirements.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/project-bootstrap-architect/references/desktop-helper-hard-requirements.md`
> Source of truth: `registry/skills/project-bootstrap-architect/references/desktop-helper-hard-requirements.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Desktop Helper Hard Requirements

Use this file for local assistant, local daemon, tray app, desktop automation, or local model orchestration bootstrap work.

These are hard structural constraints for desktop helper projects. They matter because local-helper repos fail in practice when runtime boundaries, state directories, and tool permissions are left implicit.

## Clear operating mode

At bootstrap time, decide which of these the project is:

- foreground CLI helper
- background daemon or agent
- tray app
- desktop UI shell plus local service

Do not mix all modes into one vague entrypoint without showing which process owns what.

## Clear process boundary

If the project has more than one runtime surface, keep the boundary explicit:

- CLI entrypoint
- background agent or daemon
- optional UI shell
- optional tool runners or integrations

Another developer should be able to tell which process stays resident, which process is interactive, and which process is only a wrapper.

## Local state directories are architecture, not implementation detail

At bootstrap time, define where these live:

- config
- durable local data
- cache
- logs
- temporary files

Do not leave this to ad-hoc string literals scattered through the codebase.
If the project is Windows-first, the scaffold should still make these paths configurable instead of hard-coding one machine-specific location.

## Tool and permission boundary must be explicit

For local assistants and desktop automation, plan the tool boundary from day one:

- what can read files
- what can write files
- what can execute shell commands
- what can call web APIs
- what needs explicit confirmation

Do not let the scaffold imply "the model can do anything on the machine."

## Prompt and model config boundary

If the project uses local or remote models, the scaffold should show where these live:

- system prompts
- model/provider config
- API base URLs
- model names
- inference or timeout settings

Do not mix prompt text directly into unrelated runtime modules without a visible ownership boundary.

## One obvious startup path

Another developer should know:

- how to start the helper once
- how to run it in interactive mode
- how to run it in resident mode, if applicable
- where health or status checks live

If the project is supposed to be always-on, the scaffold should show that explicitly instead of treating persistence as an afterthought.

## Required first-wave surfaces

For most desktop helper projects, the bootstrap output should account for:

- primary entrypoint
- state/config path strategy
- integrations or tool registry location
- prompt or model config location when LLMs exist
- logs location
- status or smoke-test path

If these are absent from the scaffold plan, the bootstrap is underspecified.

## Packaging and portability

If the helper is meant to be shared with others:

- avoid machine-specific absolute paths in source defaults
- keep runtime configuration externalizable
- make startup commands reproducible
- make local dependencies visible from the repo root

If the helper is Windows-first, that is fine, but the boundary between "Windows assumption" and "user-specific machine path" should stay explicit.

## Desktop-helper anti-patterns

- one giant script containing CLI, daemon, prompt text, state paths, and tool execution logic
- model prompts embedded through multiple files with no obvious source of truth
- hidden local paths tied to one machine account
- no logs or status check path for a supposed resident helper
- no explicit tool permission boundary

## Default advice

For a new desktop helper, prefer a scaffold that another developer can recognize immediately as:

- having one clear entrypoint
- having one clear state/config boundary
- having one clear prompt/model config boundary
- having one clear tool registry or integrations layer
- having one clear status or smoke-test path
- being runnable on another machine without reverse-engineering your personal folder assumptions
