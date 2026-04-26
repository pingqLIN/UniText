# Skills Governance Scan — 2026-04-26

> Source: `Q:\Projects\skills-governance`
> Target scanned: `Q:\UniText\registry\skills`
> Publication: local-only until explicitly approved.

## Result

Command:

```powershell
pwsh -NoProfile -File scripts/sg.ps1 scan --out reports\unitext-scan-2026-04-26.json
```

Summary:

- total skills: `54`
- hard validation ok: `54`
- hard validation fail: `0`
- skills with warnings: `54`

## Warning Triage

Warnings are quality backlog, not hard failures.

| Category | Count | Interpretation |
|---|---:|---|
| Optional registration missing | 54 | `registry/skills-registry.json` in `skills-governance` is optional and currently empty; this should not block UniText runtime adoption. |
| Deep reference path | 96 | Several skills keep SDK or service-specific references under nested folders. This is usually acceptable for large provider families, but should be reviewed when a skill becomes hard to re-enter. |
| No direct references link | 10 | `references/` exists, but `SKILL.md` does not link directly to reference files. This is the highest-value warning class to reduce first. |

Top warning-heavy skills:

| Skill | Warning Count | Main Cause |
|---|---:|---|
| `azure-ai` | 15 | SDK reference nesting plus optional registration |
| `azure-prepare` | 12 | Service reference nesting plus optional registration |
| `azure-storage` | 12 | SDK reference nesting plus optional registration |
| `azure-deploy` | 11 | Recipe reference nesting plus optional registration |
| `azure-compliance` | 10 | SDK/reference nesting plus optional registration |

## Policy Decision

Use `skills-governance` as a read-only quality gate for UniText:

- `fail > 0` blocks the current batch.
- `warn > 0` opens a quality backlog, but does not block runtime projection or bootstrap verification.
- Optional registration warnings should stay non-blocking until UniText explicitly adopts `skills-governance` as a registration authority.
- Deep reference path warnings should be assessed by skill family; Azure provider skills may legitimately need deeper SDK/reference trees.
- Missing direct reference links are good candidates for small maintenance batches because they improve progressive disclosure without changing behavior.

## Next Maintenance Candidate

Start with the 10 skills where `references/` exists but `SKILL.md` does not link directly to reference files. The likely fix is to add concise first-read links from `SKILL.md` into the most important reference files, then rerun:

```powershell
pwsh -NoProfile -File scripts/sg.ps1 scan
python -m unittest discover -s tests -p "test*.py"
```

