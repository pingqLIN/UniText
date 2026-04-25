---
name: cloudflare-runtime-sync
description: Use when checking or changing the local TB2 development and production runtime split, sync scripts, release metadata, and related service state.
runtime_projection: true
source_of_truth: registry/skills/cloudflare-runtime-sync/SKILL.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/cloudflare-runtime-sync/SKILL.md`
> Source of truth: `registry/skills/cloudflare-runtime-sync/SKILL.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill`
# Cloudflare Runtime Sync

## Scope

- TB2 source repo and runtime directories
- `release-info.json`
- prod/staging sync scripts
- local service state tied to Cloudflare

## Use This Skill When

- You need to confirm whether dev and runtime are separated.
- You need to sync a stage to prod or staging.
- You need to record the current release metadata.

## Checks

- Source repo path
- Runtime directory path
- `release-info.json`
- sync and run scripts

## References

- [workspace baseline](../../../registry/skills/cloudflare-governance/references/current-baseline.md)

## Escalate

- Use [cloudflare-governance](../../../registry/skills/cloudflare-governance/SKILL.md) when the runtime change also requires Tunnel, DNS, Access, or edge-security review.
