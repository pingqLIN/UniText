# Codex Permission Notes

This note records operator-facing permission issues observed while validating
`external-audit-orchestrator` v0.1.4 from `<windows-project-root>\audit-agent-skill`.

## 2026-05-03 Codex exec external review

Context:

- Target repo: `<windows-project-root>\audit-agent-skill`
- Commit under review: `9fd3b0b Release external audit skill v0.1.4`
- Intended reviewer path: three read-only `codex exec` review runs
- Output folder: `validation\scratch\external-review-20260503-172515`

Observed issues:

- The interactive PowerShell `codex` command can be a function wrapper, not the
  executable itself. In that case, short CLI options such as `-o` may be parsed
  by PowerShell as ambiguous PowerShell parameters before they reach Codex.
- Running `%APPDATA%\npm\codex.cmd exec` inside the default
  sandbox failed with `存取被拒。 (os error 5)`.
- `codex exec` printed `WARNING: proceeding, even though we could not update PATH:
  存取被拒。 (os error 5)` before failing in the sandboxed attempt.
- The successful path required executing `codex.cmd exec` outside the sandbox,
  while still passing `--ephemeral --sandbox read-only -C .` to the reviewer.
- Some read-only reviewer shell commands were blocked by Codex exec policy when
  they used broad PowerShell command strings, semicolon-chained commands, or
  parser snippets. Simple single-purpose read-only commands were more reliable.

Recommended operator procedure:

1. Prefer the real executable path when scripting Codex:
   `%APPDATA%\npm\codex.cmd`.
2. Avoid relying on the interactive `codex` PowerShell function wrapper for
   non-interactive reviewer runs.
3. Keep reviewer runs explicitly read-only:
   `codex.cmd exec --ephemeral --sandbox read-only -C <repo> ...`.
4. Put generated prompts and review outputs under ignored scratch paths such as
   `validation\scratch\external-review-<timestamp>\`.
5. If the sandbox reports `存取被拒。 (os error 5)` for `codex.cmd exec`, rerun the
   same command with operator-approved escalation instead of weakening the
   reviewer sandbox.
6. For reviewer prompts, ask for narrow command use and avoid requiring broad
   shell pipelines; this reduces policy-blocked commands inside `codex exec`.

Related v0.1.4 follow-up hardening:

- Escape `CodexCommand` as a PowerShell single-quoted literal when generating
  `run-codex-exec-audit.ps1`.
- Add smoke coverage for `run-external-audit-flow.ps1 -Mode codex-exec`.
- Tighten the Codex audit schema for `reference_inputs_used`.
