# Install: TB2 Template Export

Use this path when the target project wants a prebuilt TB2 request artifact rather than an immediate live reviewer run.

## Default export target

The exporter writes:

- `.audit/tb2/request.json`

## Inputs

- target project path
- audit packet markdown path
- optional output path

## Dry-run rule

The exporter must default to preview only.

Only write files when `-Apply` is explicitly provided.

## Expected operator flow

1. Build the audit packet in the target project.
2. Export the TB2 request JSON with dry-run first.
3. Review the request body and confirm the packet content is correct.
4. Re-run with `-Apply` if the target repo should keep the request artifact.
5. Send the generated JSON to the actual TB2 runtime only in a later explicit execution step.

## Suggested export command

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\export-tb2-audit-request.ps1 `
  -SkillRoot Q:\Projects\audit-agent-skill\skill\external-audit-orchestrator `
  -TargetProject <repo-path> `
  -AuditPacketPath <repo-path>\audit-packet.md
```

Apply only after review:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\export-tb2-audit-request.ps1 `
  -SkillRoot Q:\Projects\audit-agent-skill\skill\external-audit-orchestrator `
  -TargetProject <repo-path> `
  -AuditPacketPath <repo-path>\audit-packet.md `
  -Apply
```

## Attribution rule

If this mode is selected, cite:

- `Q:\Projects\tb2-claude-subagent-workflow\README.md`
- `Q:\Projects\tb2-claude-subagent-workflow\docs\platform-baseline-matrix.md`

The TB2 mode is explicitly derived from those local references.
