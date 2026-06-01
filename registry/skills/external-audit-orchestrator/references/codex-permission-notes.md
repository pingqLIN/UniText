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

## 2026-06-01 design-system reviewer routing

Context:

- Target repo: `<windows-project-root>\dev-governance-kit`
- Task under review: promote visual style and design-system sidecar docs.
- Intended reviewer path: multiple external reviewers for design-system,
  governance, and bilingual documentation perspectives.
- Captured evidence path in the target repo: ignored `reports\` audit packet
  and reviewer output files.

Observed issues:

- Same-provider subagents repeatedly returned only AGENTS/runtime
  acknowledgement text or lifecycle state such as `shutdown`, without reading
  the packet or returning findings. Treat this as a failed review gate, not a
  weak approval.
- A follow-up prompt asking the reviewer to perform the actual review was not
  enough to recover acknowledgement-only behavior after the first turn stalled.
- `claude --print --permission-mode plan` failed with
  `API Error: Unable to connect to API (ConnectionRefused)`. This is an
  unavailable reviewer path.
- `opencode run` timed out twice while inspecting the working tree or attached
  packet. Timeout remains a failed or partial gate until raw reviewer output is
  captured.
- `gemini --prompt --approval-mode plan --output-format text --skip-trust`
  produced substantive findings while also emitting environment noise. Capture
  stdout to an ignored report file and do not treat stderr noise as findings
  unless it blocks output.
- A reviewer can produce useful findings before a later final-report retry
  times out. Preserve the useful raw output, but report the retry timeout
  instead of claiming a clean final reviewer pass.

Recommended operator procedure:

1. Before a full packet, run a tiny reviewer health check that must return a
   substantive sentinel, not just AGENTS acknowledgement text.
2. For same-provider reviewer subagents, make the first prompt narrow and
   action-oriented: name the exact files, forbid edits, and require findings or
   an explicit no-findings verdict in the first response.
3. If the first response is acknowledgement-only, `shutdown`, timeout, or
   request-only, mark the gate failed and switch lanes instead of repeatedly
   nudging the same stalled reviewer.
4. For CLI reviewers, run one role at a time when the host is already noisy or
   slow; parallel CLI review can make timeout diagnosis ambiguous.
5. Capture reviewer stdout and stderr separately when possible.
6. Put the output contract before the packet and include: "Do not ask for
   confirmation. Do not write files. Output only the normalized audit report."
7. Classify `ConnectionRefused`, auth, quota, billing, and account errors as
   unavailable reviewer paths that require operator action.
8. If a reviewer produces actionable findings but the normalized final rerun
   fails, use the findings to fix the target project, then report the final
   normalization gap explicitly.
