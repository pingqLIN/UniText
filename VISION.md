# UniText — Vision

> Status: active baseline
> Principle: UniText defines a platform-neutral resource governance contract, not a single machine layout.

## 1. What UniText Is

UniText is a text-native, registry-first, AI-first governance layer for shared agent resources.

It exists because modern AI runtimes have converged on similar surfaces:

- skill or capability folders
- repository or project instructions
- MCP definitions
- workflow/runbook files
- local settings and delivery targets

UniText does not invent a replacement format for every tool. It gives those surfaces a common authoring, review, projection, and verification model.

## 2. Why It Exists

Without a shared governance layer, AI resources tend to drift:

- skills live in tool-specific folders with unclear provenance
- MCP definitions are copied into incompatible config files
- agent instructions become long prompts that cannot be reviewed or reused
- workflow decisions disappear into chat history
- local paths and private metadata leak into shared docs

UniText turns those materials into versioned resources with a stable identity, clear source of truth, and deliberate delivery path.

## 3. Architecture Position

UniText is:

**Registry-first, runtime-first, adapter-enabled, operations-governed.**

| Principle | Meaning |
|---|---|
| Registry-first | Shared resources have canonical identity and source before delivery |
| Runtime-first | Consumer agents start from a small generated read model |
| Adapter-enabled | Host tools receive resources through their supported surfaces |
| Operations-governed | Mutations use scan, review, dry-run, backup, deliver, verify |

## 4. Resource Types

The default shared resource types are:

- `skill`
- `mcp`
- `agent`
- `workflow`

Operations state is not a shared resource type. Inventories, baselines, backups, drift reports, repair plans, and audit trails belong to the operations layer, currently `ops/`, unless explicitly promoted into a publishable document.

## 5. Discovery And Delivery

`INDEX.md` answers human discovery questions:

- what docs exist
- where resource families live
- which page answers a task

`RUNTIME.md` answers agent startup questions:

- what to read first
- which runtime files are authoritative for consumer context
- when to follow pointers back to canonical sources

`OPERATIONS.md` answers delivery questions:

- which delivery mode to use
- when to scan, review, dry-run, adopt, deliver, or verify
- how to handle conflicts and local mutation

## 6. Delivery Modes

UniText recognizes four delivery modes:

- `pointer`: expose a discoverable reference without copying content
- `mirror`: copy a reviewed resource into a host-owned surface
- `symlink`: link a host surface back to a shared runtime projection
- `native-config`: write to an official host configuration or instruction surface

The mode is resolved by the adapter and operation context. It is not a permanent property of the resource itself.

## 7. Adoption Model

Formal adoption follows this path:

```text
SCAN -> REVIEW -> DRY-RUN -> ADOPT -> DELIVER -> VERIFY
```

If a resource is machine-specific, user-specific, sensitive, or not reusable, it stays in a smaller lane such as local-only overlay or project-local companion. Only reusable, share-safe, reviewed assets should become governed registry resources.

## 8. Non-Goals

UniText does not:

- silently rewrite global CLI configuration
- publish or push content without user approval
- treat private remotes as publication approval
- make `registry/` the default context dump for agents
- preserve local secrets, absolute paths, or personal operational notes in shared surfaces
- claim full support for a host tool without dated verification

## 9. Design Principles

- Discovery before automation
- Stable IDs before delivery
- Short summaries before deep content
- Runtime read model before canonical source deep dives
- Dry-run before mutation
- Backup before overwrite
- Explicit user approval before publication
- Local-only by default for reports, plans, reviews, and operational evidence

## 10. Positioning

> UniText is a registry-first governance layer that lets multiple AI runtimes safely discover, share, and receive the same reviewed resources without turning local machine state into public documentation.
