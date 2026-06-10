# UniText — Index

> Human navigation for the repository. Agents and automation should start at `RUNTIME.md`.

UniText is split into: public framing, human navigation, agent startup, operations, and document placement. Use this page when you know your task but not yet the exact file to open.

## Start by reader

| Reader | Open first | Then |
|---|---|---|
| New human reader | `README.md` | `INDEX.md` |
| Traditional Chinese reader | `README.zh-TW.md` | `INDEX.md` |
| Agent or automation | `RUNTIME.md` | `runtime/START.md`, `runtime/catalog.json` |
| Maintainer | `VISION.md` | `OPERATIONS.md` |
| Contributor | `CONTRIBUTING.md` | `OPERATIONS.md` |
| Documentation editor | `DOCUMENT_PLACEMENT_POLICY.md` | `WORKSPACE_SENSITIVE_METADATA_RULES.md` |

## Start by task

| Task | Read first | Then |
|---|---|---|
| Understand what UniText is | `README.md` | `VISION.md` |
| Find the right repo document | `INDEX.md` | relevant root doc |
| Start an agent task | `RUNTIME.md` | `runtime/` files |
| Change delivery behavior | `OPERATIONS.md` | adapter note |
| Decide document placement | `DOCUMENT_PLACEMENT_POLICY.md` | `WORKSPACE_SENSITIVE_METADATA_RULES.md` |
| Contribute safely | `CONTRIBUTING.md` | `NO_PUBLISH_POLICY.md` |
| Inspect shared resource metadata | `RESOURCE_SPEC.md` | `registry/` |
| Navigate long-form supporting docs | `docs/README.md` | selected subtree |

## Repository areas

| Path | Role |
|---|---|
| root `*.md` | repo-wide governance and core contracts |
| `registry/` | canonical shared resources |
| `runtime/` | tracked runtime-facing read model |
| `local/` | machine-local delivery overlay and local notes |
| `ops/` | reports, backups, review packages, and evidence |
| `docs/` | long-form supporting notes and adapter material |

## Core documents

| File | Role |
|---|---|
| `README.md` | Public front door |
| `README.zh-TW.md` | Maintained Traditional Chinese companion |
| `RUNTIME.md` | Agent-first startup surface |
| `VISION.md` | Architecture intent and non-goals |
| `OPERATIONS.md` | Delivery modes, verification, rollback, troubleshooting |
| `RESOURCE_SPEC.md` | Shared resource metadata contract |
| `DOCUMENT_PLACEMENT_POLICY.md` | Document placement rules |
| `CONTRIBUTING.md` | Contribution workflow and validation expectations |

## Navigation principle

A document file belongs here when it helps users pick the next file quickly.

If a document starts to define cross-repo policy, move it to the root.

## Current review-facing excerpts

This page may link to review packets, but it is **not** the full inventory.

- `docs/reviews/ESSENTIAL_SKILLS_SHORTLIST.md`
- `docs/reviews/EXTERNAL_REVIEW_PACKAGE.md`

For runtime discovery, use `runtime/catalog.json`.
