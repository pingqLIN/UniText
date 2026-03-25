# Release Hygiene Report 2026-03-25

## Scope

This report captures the current `UniText` worktree state after the release-integrity, catalog-governance, and Copilot bootstrap-baseline workstreams were separated into dedicated commits.

The goal is not to force-clean unrelated authoring changes. The goal is to make the remaining release blockers explicit so the next release decision can be evidence-based.

## Current Snapshot

Generated from:

```bash
python3 local/scripts/report-release-hygiene.py --json
```

Observed result at the time of writing:

- total dirty entries: `317`
- release scope: `3`
- blockers: `314`
- release ready: `false`

### Blockers

- machine-specific tracked config is dirty
- excluded stray registry items are present in the worktree
- untracked binary assets are present
- large unrelated content wave is mixed into the worktree

### Category Counts

- `machine_specific`: `1`
- `stray_registry`: `76`
- `binary_asset`: `3`
- `review_noise`: `2`
- `translation_wave`: `63`
- `outside_release_scope`: `169`
- `release_scope`: `3`

## Interpretation

### 1. Machine-specific blocker

- [`.mcp.json`](/mnt/q/UniText/.mcp.json) is still rewritten by local bootstrap to absolute paths.
- This file must remain outside release commits unless it is first restored to a template-safe relative seed.

### 2. Explicit stray item blocker

- [`registry/skills/microsoft-foundry/`](/mnt/q/UniText/registry/skills/microsoft-foundry) is still present in the worktree.
- [`catalog-exclusions.json`](/mnt/q/UniText/registry/catalog-exclusions.json) already marks it as stray, so it must not be folded into release-facing commits.

### 3. Unrelated content waves

- `i18n/` currently contains a large translation wave.
- `registry/skills/` currently contains a large content wave across multiple skill families.
- These are not inherently bad, but they should be partitioned into their own content stream rather than silently mixed into release-infrastructure commits.

### 4. Local assets and draft materials

- Untracked assets such as [001.jpg](/mnt/q/001.jpg), [002.jpg](/mnt/q/002.jpg), and [banner.psd](/mnt/q/banner.psd) are not part of the current release boundary.
- Drafts such as [SECURITY_ATTACK_INPUT_CHECKLIST.md](/mnt/q/UniText/SECURITY_ATTACK_INPUT_CHECKLIST.md) and [SECURITY_REVIEW_ADVISORY.md](/mnt/q/UniText/SECURITY_REVIEW_ADVISORY.md) should be reviewed as a separate documentation/security stream.

## Safe Release Boundary

The safe release boundary remains:

- committed release-integrity fixes
- committed catalog-governance fixes
- committed Copilot bootstrap-baseline fixes

The following should stay out of release commits until explicitly handled:

- [`.mcp.json`](/mnt/q/UniText/.mcp.json)
- [`registry/skills/microsoft-foundry/`](/mnt/q/UniText/registry/skills/microsoft-foundry)
- unrelated `i18n/` translation waves
- unrelated `registry/skills/` content waves
- local binary assets
- unreviewed security draft documents

## Recommended Next Step

Use `local/scripts/report-release-hygiene.py` as a required pre-release gate.

Only when it reports no blockers, or when all reported blockers are deliberately excluded from the planned commit scope, should the repository be treated as release-clean.
