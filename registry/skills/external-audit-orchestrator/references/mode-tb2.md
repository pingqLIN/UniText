# Mode: TB2 Audit Template

Use this mode when you want an external reviewer path that is session-based, traceable, and reusable across providers.

## Supported states

This skill currently supports `tb2-template-export`.

- `tb2-template-export`: build audit packets and reviewer request JSON artifacts.
- `tb2-live-review`: run the reviewer through TB2 runtime tools. This requires TB2 runtime MCP tools such as `workstream_create`, `reviewer_send`, `reviewer_wait`, and `reviewer_read`; do not assume this state is available from this skill alone.

If only template export is available, stop at the request artifacts and report that no live reviewer execution occurred.

## No-TB2 Runtime Fallback

When the active system does not expose TB2 live reviewer tools, keep the audit moving through a supported non-TB2 path:

1. Build the audit packet.
2. Optionally export TB2 request artifacts as a future handoff record.
3. Run `same-provider-subagent` when a local Codex or Claude reviewer path is available.
4. Use `external-web` as the visible human-supervised fallback when no local subagent path is available.
5. Normalize the report only after raw reviewer output exists; do not treat exported request JSON as a completed review.

## Cross-project reference

This mode explicitly reuses ideas from:

- `<tb2-project-root>\README.md`
- `<tb2-project-root>\docs\platform-baseline-matrix.md`

If this mode is selected, cite those paths in the final audit report.

## Current maturity note

The referenced TB2 project currently documents:

- built-in profiles for `claude`, `codex`, `copilot`, and `python-repl`
- `codex_relay`
- validated runtime baseline for core runtime flows

But the same project also records that:

- `python-repl` has real interactive validation
- `claude`, `codex`, and `copilot` are currently `metadata-only`

So treat TB2 `claude` and `codex` reviewer flows as templates until the user validates them in their own runtime.

## Procedure

1. build the audit packet
2. adapt it into one or three TB2 reviewer request JSON files
3. hand the request artifacts to TB2 live tooling only when those tools are available
4. preserve redacted runtime transcript metadata in TB2, not in this skill
5. normalize structured reviewer results into the standard report format

## Template-only boundary

Generated request JSON is an execution handoff artifact. It is not evidence that the reviewer ran.

The default request uses `packet_path` and `packet_sha256` rather than embedding the full audit packet in the prompt. Embedded packet transport should be explicit operator opt-in because audit packets can contain diffs, local paths, and other sensitive project context.

## Recommended asset

Use [../assets/tb2/tb2-audit-request.template.json](../assets/tb2/tb2-audit-request.template.json) as the starting request shape.
Use [install-tb2-template.md](install-tb2-template.md) for the dry-run export path.
Use [../scripts/export-tb2-audit-request.ps1](../scripts/export-tb2-audit-request.ps1) to materialize the request into a target project.

## Good fit

- cross-provider experiments
- traceable long-running reviewer session
- future audit template library work

## Not preferred for v0.1

Do not make this the default v0.1 execution path until real reviewer profile validation exists for the intended provider CLI.

