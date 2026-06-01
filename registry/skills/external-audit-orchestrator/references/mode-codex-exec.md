# Mode: Codex Exec Audit

Use this mode when the reviewer should be Codex and the audit must run from scripts, CI, or another non-interactive operator workflow.

## Why this mode

OpenAI documents `codex exec` as the non-interactive Codex entrypoint for scripts and CI. It can run with explicit sandbox settings and can write a final response to a file. It can also request a final JSON response with `--output-schema`.

For Codex reviewer automation, prefer this mode over a TB2 `codex` interactive profile until that TB2 profile has reproducible real-runtime validation.

## Cross-project and official references

If this mode is selected, cite the relevant sources in the final audit report:

- `https://developers.openai.com/codex/noninteractive`
- `https://developers.openai.com/codex/cli/reference`
- `<windows-project-root>\tb2-claude-subagent-workflow\docs\platform-baseline-matrix.md`

## Procedure

1. build the audit packet
2. export a Codex exec prompt and JSON schema
3. review the generated runner before executing it
4. run a tiny health check before the full packet when the lane is unproven
5. run the generated runner only when the operator is ready to spend a Codex run
6. normalize the final response into the standard audit report if needed

## Recommended asset

Use [../assets/codex/audit-report.schema.json](../assets/codex/audit-report.schema.json) as the final response schema.
Use [../scripts/export-codex-exec-request.ps1](../scripts/export-codex-exec-request.ps1) to materialize the prompt, schema, and local runner into a target project.

## Health check and permission notes

Use [codex-permission-notes.md](codex-permission-notes.md) when diagnosing Codex exec failures. Prefer the real executable path, such as `%APPDATA%\npm\codex.cmd`, when scripting. A reviewer health check should return a substantive sentinel like `AUDIT_OK`; missing final output, policy-blocked shell commands, or `存取被拒。 (os error 5)` is a failed or unavailable lane until rerun with an operator-approved execution boundary.

## Startup gate limitation

`codex exec` still follows active platform, global, workspace, and repo instructions. If those instructions require the first assistant turn to ask a startup question, the non-interactive run may stop at that prompt instead of producing an audit.

The exporter supports `-StartupGateAnswer Y|N|O` so the generated prompt can record an operator-supplied gate answer. This is operator context, not an override for higher-priority instructions. If the gate still blocks execution, treat it as a reviewer-run blocker and use a session where the gate has already been satisfied or remove the blocking gate from the audit environment.

## Good fit

- scripted Codex audit
- CI or scheduled review jobs
- machine-readable reviewer output
- read-only reviewer runs with explicit sandbox settings

## Not preferred

- cross-provider experiments where TB2 session routing is the actual object under test
- visible human-supervised browser review
- real code modification unless the user explicitly asks for auto-fix and the sandbox is widened intentionally
