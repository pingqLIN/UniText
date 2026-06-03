# Skill Runtime / Codex Duplication SOP

> Audience: operators maintaining UniText skills across `registry/`, `runtime/`, and the local Codex skills bundle.

## Purpose

Use this SOP when a skill appears in both `Q:\UniText\runtime\skills\<skill-id>` and `C:\Users\miles\.codex\skills\<skill-id>`, or when a user reports that the system can see both a UniText runtime skill and a Codex-local skill with the same id.

The goal is to keep one governance source of truth while allowing multiple runtime delivery surfaces.

## Source Order

Use this order for formal changes:

```text
registry source -> runtime projection -> Codex local bundle
```

- `Q:\UniText\registry\skills\<skill-id>` is the canonical governed source.
- `Q:\UniText\runtime\skills\<skill-id>` is the consumer-facing runtime projection.
- `C:\Users\miles\.codex\skills\<skill-id>` is the machine-local Codex bundle or local install.

Do not treat the runtime projection or Codex-local copy as the canonical source unless the user explicitly asks for a temporary local experiment.

## Detection

List duplicate skill ids across the two active delivery surfaces:

```powershell
$roots = @(
  'Q:\UniText\runtime\skills',
  'C:\Users\miles\.codex\skills'
)
Get-ChildItem $roots -Directory |
  Group-Object Name |
  Where-Object Count -gt 1 |
  Select-Object Name, Count
```

Check whether the duplicate is expected:

```powershell
Get-FileHash -Algorithm SHA256 `
  'Q:\UniText\registry\skills\<skill-id>\SKILL.md', `
  'Q:\UniText\runtime\skills\<skill-id>\SKILL.md', `
  'C:\Users\miles\.codex\skills\<skill-id>\SKILL.md'
```

The runtime projection may have a different hash because it adds projection metadata such as `runtime_projection` and `source_of_truth`.

## Classification

| Classification | Meaning | Action |
| --- | --- | --- |
| `same-content` | Codex-local copy matches the registry source. | Accept as a normal delivery duplicate. |
| `runtime-wrapper-only` | Runtime differs only by generated projection metadata. | Accept as normal. |
| `content-drift` | Runtime or Codex-local body differs from registry source. | Move intended changes back to `registry/`, rebuild/project, then resync Codex if needed. |
| `wrong-root-exposure` | A runtime context loads both roots as peers or points directly to `registry/skills`. | Fix configuration or bootstrap wiring before editing skill content. |

## Repair Path

1. Confirm the UniText worktree state:

```powershell
git -C Q:\UniText status --short --branch
```

2. If the desired change exists only in `runtime/` or `C:\Users\miles\.codex\skills`, copy that change back into:

```text
Q:\UniText\registry\skills\<skill-id>
```

3. Validate the registry skill:

```powershell
python Q:\UniText\registry\skills\skill-creator\scripts\quick_validate.py Q:\UniText\registry\skills\<skill-id>
```

4. Dry-run the runtime rebuild before writing:

```powershell
python Q:\UniText\local\scripts\build-runtime-layer.py --output-dir Q:\UniText\.tmp\runtime-dryrun
```

5. If the dry-run shows only expected drift, rebuild tracked runtime:

```powershell
python Q:\UniText\local\scripts\build-runtime-layer.py --write
python Q:\UniText\local\scripts\verify-bootstrap.py --skip-codex
```

6. If Codex local bundle must be updated, preview host wiring first:

```powershell
python Q:\UniText\local\scripts\bootstrap.py --dry-run
```

Run `bootstrap.py --force` only when the task explicitly includes host target changes.

## Escalation

Stop and report before writing when:

- `build-runtime-layer.py` dry-run shows broad unrelated payload drift.
- `git status --short --branch` shows unrelated dirty files in the same paths you need to modify.
- Codex `skills_path` points to `registry/skills`.
- The same skill id has different intended behavior in runtime and Codex-local copies.

In those cases, preserve evidence and decide whether to isolate the work in a new branch, a worktree, or a separate local experiment.
