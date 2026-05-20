---
runtime_projection: true
source_of_truth: registry/skills/project-bootstrap-architect/references/development-skill-selection.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/project-bootstrap-architect/references/development-skill-selection.md`
> Source of truth: `registry/skills/project-bootstrap-architect/references/development-skill-selection.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Development Skill Selection

Use this reference when a new project needs a starting set of skills for implementation, documentation, design, communication, or governance.

## Baseline Development Set

| Need | Candidate skills | When to choose |
| --- | --- | --- |
| Existing-codebase iteration | `project-development-loop` | The project already has meaningful code and needs progress, maintenance, or repeated delivery batches. |
| New-project bootstrap | `project-bootstrap-architect` | The project is greenfield and needs type, storage, layout, and initial scaffold decisions. |
| Plan before execution | `plan-first-execution` | The user explicitly asks for a plan, plan mode, a written plan, or review gates before work. |
| Skill creation | `skill-creator` | Creating or updating skills. Use `.system` Codex-oriented copy when available. |
| AI-first operability review | `ai-first-readiness-review` | Checking whether a repo is ready for AI-assisted maintenance and handoff. |

## Design and Frontend

| Need | Candidate skills |
| --- | --- |
| Production UI implementation | `frontend-design` |
| Design critique, polish, hardening | `impeccable` |
| Design-system or aesthetic playbook | `claude-design-playbook`, `theme-factory` |
| Complex web artifacts | `web-artifacts-builder` |
| Browser/UI verification | `webapp-testing`, `playwright` |

## Documentation and Documents

| Need | Candidate skills |
| --- | --- |
| README quality | `readme-quality` |
| Co-authoring docs | `doc-coauthoring` |
| PDF/DOCX/PPTX/XLSX work | `pdf`, `docx`, `pptx`, `xlsx` |
| Project or session memo | `conversation-memo`, `obsidian-index-adapter` |

## Communication and Coordination

| Need | Candidate skills |
| --- | --- |
| Internal announcements, status, stakeholder updates | `internal-comms` |
| Email triage or drafting | `gmail` plugin skills when connected |
| Google Drive docs/sheets/slides collaboration | `google-drive` plugin skills when connected |
| Multi-agent review or audit | `external-audit-orchestrator`, `ai-first-readiness-review` |

## Platform and Operations

| Need | Candidate skills |
| --- | --- |
| MCP server | `mcp-builder`, `building-mcp-server-on-cloudflare` |
| Cloudflare platform | `cloudflare-governance`, then narrower Cloudflare skills |
| Workers/Wrangler | `wrangler`, Cloudflare plugin skills |
| Azure App Insights | `appinsights-instrumentation` |
| Microsoft identity | `entra-app-registration` |
| Security ownership and threat model | `security-ownership-map`, `security-threat-model`, `security-best-practices` |

## Selection Rule

Pick a primary skill and at most two support skills at bootstrap time. Add more only when the workflow actually reaches that domain.
