# Install: Claude Same-Provider Audit

Use this path when the target project will run review inside Claude Code using a local project subagent.

## Default install target

The bundle exporter writes:

- `.claude/agents/code-reviewer.md`
- `.claude/settings.json`

## Dry-run rule

The exporter must default to preview only.

Only write files when `-Apply` is explicitly provided.

## Expected operator flow

1. Generate or update the audit packet in the target repo.
2. Export the reviewer bundle into the target repo with dry-run first.
3. Review the planned writes.
4. Re-run with `-Apply` if the target repo should adopt the bundle.
5. Invoke the reviewer subagent against the audit scope.
6. Normalize findings into the standard report format.

## Suggested export command

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\export-claude-reviewer-bundle.ps1 `
  -SkillRoot <skill-root>\external-audit-orchestrator `
  -TargetProject <repo-path>
```

Apply only after review:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\export-claude-reviewer-bundle.ps1 `
  -SkillRoot <skill-root>\external-audit-orchestrator `
  -TargetProject <repo-path> `
  -Apply
```

## Merge behavior

- `code-reviewer.md` is copied directly from this skill asset.
- `settings.json` is merged conservatively:
  - if the target file does not exist, create it from the template
  - if the target file exists, preserve unknown keys and merge `hooks.SubagentStop`
  - do not delete existing hooks

## Attribution rule

If this install path was derived from official Claude Code docs, include those URLs in `Reference Inputs` of any generated audit report or setup memo.
