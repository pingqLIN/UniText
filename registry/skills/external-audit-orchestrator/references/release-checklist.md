# Release Checklist

Use this checklist before publishing or installing `external-audit-orchestrator` outside this repository.

## Scope

- Confirm the release version in `VERSION`.
- Confirm `CHANGELOG.md` records the user-visible changes.
- Confirm `README.md` points to the current entrypoints and validation command.
- Confirm no generated smoke artifacts are staged.
- Run package export in dry-run mode before writing release artifacts.

## Validation

Run from the repository root:

```powershell
.\validation\run-smoke.ps1
```

The smoke test must pass before release. It covers:

- PowerShell parser checks for all skill scripts.
- Audit packet generation.
- Report normalization.
- TB2 request export.
- Claude reviewer bundle dry-run behavior.
- Unified flow runner output.

## Provenance

Before releasing docs, templates, or reviewer prompts, check that source attribution remains explicit:

- Local cross-project references must include exact paths and reasons.
- Official docs must include URLs and reasons.
- Public skills or repositories must include URLs or repository names and reasons.
- Do not hide provenance in an appendix-only note.

## Packaging Boundary

The package root for installation is:

```text
skill/external-audit-orchestrator
```

Do not package `validation/.smoke/` or `validation/scratch/` contents.

`validation/golden/` is useful for this repo's regression history, but it is not required for a minimal consumer install.

Preview package export:

```powershell
.\scripts\export-skill-package.ps1
```

Write the package:

```powershell
.\scripts\export-skill-package.ps1 -Apply
```

Generated packages are written under `dist/`, which is ignored by Git.

## Maturity Gate

- `same-provider-subagent`: allowed as the default v0.1 path.
- `external-web`: allowed as a visible, human-supervised operator path.
- `external-cli-mcp`: document-only unless a concrete target toolchain is supplied.
- `tb2-template`: template-only until the specific provider profile is validated in the real TB2 runtime.
