# Install: TB2 Template Export

Use this path when the target project wants a prebuilt TB2 request artifact rather than an immediate live reviewer run.

## Default export target

The exporter writes:

- `.audit/tb2/requests/product-process.request.json`
- `.audit/tb2/requests/engineering-test.request.json`
- `.audit/tb2/requests/compatibility-provenance.request.json`
- `.audit/tb2/requests/manifest.json`

When `-ReviewerRole` is specified, the exporter writes only that reviewer request.

## Inputs

- target project path
- audit packet markdown path
- optional reviewer role
- optional correlation id for reruns
- optional output path
- optional embedded packet transport opt-in

## Dry-run rule

The exporter must default to preview only.

Only write files when `-Apply` is explicitly provided.

## Expected operator flow

1. Build the audit packet in the target project.
2. Export the TB2 request JSON with dry-run first.
3. Review the request body and confirm the packet content is correct.
4. Re-run with `-Apply` if the target repo should keep the request artifact.
5. Send the generated JSON to the actual TB2 runtime only in a later explicit execution step.
6. Save reviewer results under `.audit/tb2/results/*.result.json` when live execution finishes.

Exporting request JSON is not proof that a reviewer ran. A completed audit also needs reviewer result JSON and a normalized report.

## Suggested export command

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\export-tb2-audit-request.ps1 `
  -SkillRoot <skill-root>\external-audit-orchestrator `
  -TargetProject <repo-path> `
  -AuditPacketPath <repo-path>\audit-packet.md
```

Apply only after review:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\export-tb2-audit-request.ps1 `
  -SkillRoot <skill-root>\external-audit-orchestrator `
  -TargetProject <repo-path> `
  -AuditPacketPath <repo-path>\audit-packet.md `
  -Apply
```

Export a single reviewer request:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\export-tb2-audit-request.ps1 `
  -SkillRoot <skill-root>\external-audit-orchestrator `
  -TargetProject <repo-path> `
  -AuditPacketPath <repo-path>\audit-packet.md `
  -ReviewerRole engineering-test `
  -Apply
```

The default packet transport is path-reference plus SHA-256 hash. Use `-EmbedPacket` only when the operator explicitly accepts that the request artifact will contain raw audit packet text.

## Attribution rule

If this mode is selected, cite:

- `<tb2-project-root>\README.md`
- `<tb2-project-root>\docs\platform-baseline-matrix.md`

The TB2 mode is explicitly derived from those local references.

