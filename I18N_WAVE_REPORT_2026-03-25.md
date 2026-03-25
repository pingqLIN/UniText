# I18n Wave Report 2026-03-25

## Scope

This report classifies the current dirty `i18n/` tree without touching translation content.

The goal is to answer one question: are these changes substantive translation edits, or are they line-ending-only drift that can be split into a separate technical cleanup commit?

## Command

```bash
python3 local/scripts/report-i18n-wave.py --markdown
```

## Result

- dirty entries: `63`
- `eol_only`: `63`
- `substantive`: `0`
- `new_file`: `0`
- `safe_to_split`: `true`

## Interpretation

Every currently dirty `i18n/` file in the worktree is line-ending-only after ignoring CR and trailing-space EOL changes.

That means the `i18n` wave is safe to split as its own commit, and it should be treated as a formatting / normalization commit rather than a translation-content commit.

## Recommended Boundary

The commit scope for the i18n wave should include only the `i18n/` files that are currently dirty.

It should exclude:

- `.mcp.json`
- unrelated `registry/skills/` content waves
- binary assets
- security drafts
- release-hygiene tooling
