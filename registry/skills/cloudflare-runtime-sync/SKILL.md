---
name: cloudflare-runtime-sync
description: Use when the request is specifically about the local TB2 development and production runtime split, sync scripts, release metadata, and related local service state. Do not use for Cloudflare account inventory, WARP device policy, tunnel ingress, or Access auth review unless the runtime issue clearly depends on those layers.
---

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

## Do Not Use This Skill When

- The task is primarily about Cloudflare account, zone, or Zero Trust dashboard settings.
- The task is primarily about tunnel ingress and DNS mapping.
- The task is primarily about WARP, split tunnel vs full tunnel, or credential validation.

## Checks

- Source repo path
- Runtime directory path
- `release-info.json`
- sync and run scripts

## References

- [workspace baseline](../cloudflare-governance/references/current-baseline.md)

## Escalate

- Use [cloudflare-governance](../cloudflare-governance/SKILL.md) first for broad Cloudflare review, or when the runtime change also requires Tunnel, DNS, Access, edge-security, or WARP/device review.
