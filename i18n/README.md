# UniText i18n

This directory contains locale-specific translations for official UniText documentation.

## Layout

- `i18n/<locale>/` mirrors the same relative paths and filenames as the source docs.
- Locale tags follow BCP 47-style names used by the repository.
- `i18n/.clean/archived-locales/<locale>/` keeps retired translation waves as archived snapshots instead of active maintenance targets.

## Active locales

- `zh-TW`

English source docs remain the canonical baseline in repo root and are not duplicated under `i18n/`.

## Archived locales

The following locale waves are kept only as archived snapshots and are not part of the active translation maintenance baseline:

- `zh-CN`
- `ja`
- `de`
- `fr`
- `es`
- `ko`
- `it`

## Translation scope

The manifest lists all tracked source docs that the i18n system knows about, plus a smaller `required_source_docs` subset that defines the active gate for the currently maintained locales.
Registry content, template examples, archived reviews, and social drafts are excluded by default.

The current operating policy is:

- `en` + `zh-TW` are the only actively maintained documentation surfaces
- `required_source_docs` defines the minimum active translation surface that must stay synchronized for release and governance checks
- other mirrored docs may still exist as optional coverage, but their drift is reported separately from the required gate
- archived locales stay recoverable under `.clean`, but do not block drift audits or release readiness
- if a new locale is reactivated later, move it back out of `.clean`, add it to `manifest.json`, and treat it as a new translation wave

To audit missing or stale translations against the manifest, run:

```bash
python local/scripts/audit-i18n-drift.py
```

To narrow the audit to a smaller batch or generate a human-readable workboard:

```bash
python local/scripts/audit-i18n-drift.py --locale zh-TW --format markdown
python local/scripts/audit-i18n-drift.py --source-doc README.md --source-doc INDEX.md --format markdown --output local/docs/authoring/i18n-workboard.md --exit-zero
```
