---
runtime_projection: true
source_of_truth: registry/skills/external-audit-orchestrator/references/mode-gemini-cli.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/external-audit-orchestrator/references/mode-gemini-cli.md`
> Source of truth: `registry/skills/external-audit-orchestrator/references/mode-gemini-cli.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Mode: Gemini CLI Actor-Critic Audit

Use this mode when the external reviewer should be Gemini CLI, either through project-local `.gemini/agents/*.md` subagents or a headless `gemini -p` runner.

Default model route:

- `external_plan_architect`: Gemini 3.1 Flash-class model for fast planning drafts.
- `external_plan_critic`: Gemini 3.1 Pro-class model for stricter feasibility and edge-case review.

Treat the exact model ids as operator-configurable. The bundled exporter defaults to `gemini-3.1-flash` and `gemini-3.1-pro`, but callers should override them when the installed Gemini CLI exposes different names.

## Why this mode

- keeps the reviewer outside the current Codex or Claude execution context
- supports project-local Gemini subagents that can be inspected with `/agents list` and reloaded with `/agents reload`
- supports headless automation with `gemini -p` and JSON output capture
- fits the actor-critic pattern: one agent drafts a plan, another independently reviews it

## Required Gemini CLI surfaces

Gemini CLI custom subagents are Markdown files with YAML frontmatter. Install them at one of these locations:

- project-level: `.gemini/agents/*.md`
- user-level: `~/.gemini/agents/*.md`

For this skill, prefer project-level installation so the reviewer is scoped to the target project. Use `scripts/export-gemini-reviewer-bundle.ps1` to prepare the bundle.

Useful interactive Gemini commands:

- `/agents list` - confirm the agents are discovered
- `/agents reload` - reload after editing `.gemini/agents/*.md`
- `/agents config <agent-name>` - inspect or adjust model, temperature, or limits
- `/plan` - switch Gemini into read-only plan mode when the operator is supervising an actor step

Useful headless pattern:

```powershell
gemini -p "<prompt text>" --output-format json
```

When using headless mode for automation, capture raw stdout and stderr as audit evidence before normalizing the result.

## Included agents

- `external_plan_architect`: actor agent that drafts a software implementation plan only.
- `external_plan_critic`: critic agent that reviews a plan as a senior system architect and returns strict JSON.

The critic is intentionally read-only. It must not edit files, run migrations, stage changes, commit, push, or auto-fix.

## Actor-critic loop

1. Build the audit packet with `scripts/build-audit-packet.ps1`.
2. Ask `external_plan_architect` to draft or revise the plan.
3. Ask `external_plan_critic` to review the plan.
4. Parse the critic JSON.
5. If `status` is `pass`, archive the final plan and move to the next phase.
6. If `status` is `revise`, pass `improvement_prompt` back to the architect.
7. Stop after a bounded retry count, usually three rounds, and escalate to a human if the critic still returns `revise`.

## Expected critic JSON

The critic must return only one JSON object:

```json
{
  "status": "pass",
  "risk_score": 1,
  "issues": [],
  "improvement_prompt": ""
}
```

If any concern exists, `status` must be `revise`, `risk_score` must reflect the severity, `issues` must describe each concern, and `improvement_prompt` must be directly reusable as the next prompt for the plan author.

## Guardrails

- Keep Gemini agents read-only unless the user explicitly asks for implementation.
- Use Flash for the actor and Pro for the critic by default; do not silently downgrade the critic model without recording it in the flow output.
- Use temperature `0.1` to `0.2` for the critic so JSON stays stable while still allowing edge-case reasoning.
- Preserve the raw Gemini output before normalizing reports.
- Always include Gemini CLI documentation and any copied or adapted prompt template in `Reference Inputs`.
- If Gemini CLI is unauthenticated or unavailable, report that the mode is blocked and fall back to web-manual or same-provider mode only if the user accepts the change.

## Good fit

- plan-first development gates
- external review of implementation plans before coding
- CI-style headless review where raw JSON can be archived
- local workflows where the operator already uses Gemini CLI

## Bad fit

- tasks that require hidden browser profile state
- unbounded autonomous implementation
- environments where Gemini CLI cannot be authenticated or logged
