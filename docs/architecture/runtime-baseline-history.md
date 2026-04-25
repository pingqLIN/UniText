# Runtime Baseline History

> Status: active historical summary
> Date: 2026-04-20
> Purpose: preserve the useful decisions from the runtime reset design round without keeping the full template and ballot set in the active architecture surface.

## Outcome

UniText now uses a runtime-first operating model:

- `registry/` stays the canonical authoring source
- `runtime/` is the tracked consumer read model
- CLI targets are wired to machine-local runtime targets rebuilt from `runtime/`, not directly from `registry/skills`
- `README.md` and `INDEX.md` remain human-oriented discovery docs, not the default startup surface for consumer agents

This outcome is implemented by the active baseline in [RUNTIME.md](../../RUNTIME.md) and `runtime/*`.

## What Won

The design round made two source documents especially important:

- `template2-b.md`
  - contributed the strongest runtime-first contract
  - established `RUNTIME.md` as the stable first-read surface
  - made the key separation explicit: canonical authoring stays in `registry/`, delivery goes through a curated runtime surface
- `template2-d.md`
  - contributed the strongest implementation realism
  - emphasized explicit delivery/verify contracts
  - reinforced that no CLI should read `registry/skills` directly in steady state

The score summary recorded `template2-b.md` as the clear winner, while `template2-d.md` was the main implementation-strength follow-up.

## What Was Carried Forward

The current baseline keeps these durable ideas from the archived design set:

### 1. Runtime-first startup

Consumer agents should start from:

1. `RUNTIME.md`
2. `runtime/START.md`
3. `runtime/RULES.md`
4. `runtime/ROUTES.md`
5. `runtime/catalog.json`

### 2. Registry stays canonical

`registry/` is still the only authoring source of truth. Runtime projections are delivery artifacts and must not become a second authoring tree.

### 3. Delivery must be contract-based

The repo should answer:

- what the active runtime surface is
- how it gets rebuilt
- how local CLI targets are wired
- how drift is detected

That contract is now carried by:

- `build-runtime-layer.py`
- `bootstrap.py`
- `verify-bootstrap.py`
- runtime entry docs and catalog

### 4. Discovery remains available without bloating default startup

Deep discovery still goes through the MCP backplane (`unitext-registry`), while the default runtime surface remains intentionally smaller and lower-noise.

## Review Gate Result

The archived review gate confirmed two important post-cutover fixes before this baseline was considered stable:

- tracked `.mcp.json` must remain a template-safe seed rather than being rewritten into machine-specific form
- `verify-bootstrap.py` must share the same home-directory fallback strategy as `bootstrap.py`

After those fixes, the runtime reset baseline passed review and `verify-bootstrap.py` returned `ok = true`.

## What Did Not Carry Forward

The archived design set also contained ideas that were intentionally not adopted as part of the current shared baseline:

- keeping consumer CLIs pointed directly at `registry/skills`
- continuing to use `README.md` or `INDEX.md` as the default agent startup surface
- treating design templates, ballots, and review scorecards as active architecture docs
- promoting machine-local migration helpers into shared runtime policy

## Archive Location

The full design-stage source set was moved to:

- [docs/architecture/.del/agent-runtime-reset/](.del/agent-runtime-reset/)

Use the archive only when you need:

- the full design debate
- ballot-level justification
- historical comparison between rejected and adopted approaches

For normal development, the active baseline is `RUNTIME.md` plus `runtime/*`.
