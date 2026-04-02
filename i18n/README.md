# UniText i18n

This directory contains locale-specific translations for official UniText documentation.

## Layout

- `i18n/<locale>/` mirrors the same relative paths and filenames as the source docs.
- Locale tags follow BCP 47-style names used by the repository.

## Current locales

- `zh-TW`
- `zh-CN`
- `ja`
- `de`
- `fr`
- `es`
- `ko`
- `it`

## Translation scope

The manifest lists the official docs that should be translated into each locale.
Registry content, template examples, archived reviews, and social drafts are excluded by default.

To audit missing or stale translations against the manifest, run:

```bash
python local/scripts/audit-i18n-drift.py
```

To narrow the audit to a smaller batch or generate a human-readable workboard:

```bash
python local/scripts/audit-i18n-drift.py --locale zh-TW --locale ja --format markdown
python local/scripts/audit-i18n-drift.py --source-doc README.md --source-doc INDEX.md --format markdown --output local/docs/authoring/i18n-workboard.md --exit-zero
```
