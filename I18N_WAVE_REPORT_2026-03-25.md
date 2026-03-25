# I18N Wave Report 2026-03-25

## Scope

This report captures the current `i18n/` dirty-tree wave after the release-integrity, catalog-governance, Copilot baseline, and release-hygiene tooling commits were separated out.

The goal is to determine whether the remaining `i18n` changes are substantive translation work or a formatting-only wave that should be handled separately.

## Evidence

Generated from:

```bash
python3 local/scripts/report-i18n-wave.py --json
```

Observed result at the time of writing:

- dirty i18n files: `63`
- `eol_only`: `63`
- `substantive`: `0`
- `new_file`: `0`
- `safe_to_split`: `true`

## Interpretation

The current `i18n` wave is not a translation-content update. It is a line-ending / formatting wave.

Representative checks:

- [i18n/zh-CN/README.md](/mnt/q/UniText/i18n/zh-CN/README.md)
- [i18n/zh-CN/INDEX.md](/mnt/q/UniText/i18n/zh-CN/INDEX.md)
- [i18n/zh-CN/local/docs/CLI_COMPAT_MATRIX.md](/mnt/q/UniText/i18n/zh-CN/local/docs/CLI_COMPAT_MATRIX.md)
- [i18n/zh-CN/AGENTS.md](/mnt/q/UniText/i18n/zh-CN/AGENTS.md)
- [i18n/zh-TW/README.md](/mnt/q/UniText/i18n/zh-TW/README.md)
- [i18n/de/README.md](/mnt/q/UniText/i18n/de/README.md)

All of these classify as `eol_only`, with no remaining content delta after ignoring CR-at-EOL and trailing-space-at-EOL differences.

## Release Guidance

This wave should not be mixed into release-infrastructure commits.

It is safe to treat the current `i18n/` wave as its own formatting-only stream, but it should be reviewed and committed independently from:

- release-integrity work
- Copilot baseline work
- release-hygiene tooling
- catalog / security governance work

## Recommended Next Step

If you want to clean the worktree further, handle the `i18n/` wave as a dedicated newline-normalization commit.

If you do not need that cleanup immediately, it is also safe to leave the current `i18n/` wave out of release-facing commits, because it does not represent missing translation content.
