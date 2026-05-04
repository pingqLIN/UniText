# Claude Code Standard Paths Report - 2026-05-04

> Scope: standard Claude Code path and output-surface assessment.
> Local observations are treated as deviation samples, not as the standard.

## Conclusion

The current local symlink:

```text
C:\Users\miles\.claude\skills -> Q:\UniText\runtime\skills
```

is a custom local configuration. It should not be treated as Claude Code's standard skill configuration.

For UniText governance, do not use this symlink as the baseline. Keep Claude Code's official user/project/managed surfaces separate from UniText's registry/runtime projections.

## Standard Read Surfaces

Claude Code should be evaluated in these layers:

1. Managed
   - Organization or machine-level policy.
   - Highest-priority configuration layer.
2. User
   - Personal user home configuration.
   - Usually `~/.claude/`.
3. Project
   - Repository-local configuration and instructions.
   - Usually `.claude/`, root `CLAUDE.md`, and `.mcp.json`.
4. Local
   - Personal per-project local state.
   - Should not be published or treated as shared project configuration.

The effective settings priority is:

```text
Managed > CLI args > Local > Project > User
```

## Managed Paths

Known standard managed locations:

| Platform | Managed path |
| --- | --- |
| Windows | `C:\Program Files\ClaudeCode\` |
| Linux / WSL | `/etc/claude-code/` |
| macOS | `/Library/Application Support/ClaudeCode/` |

macOS may also use the managed preferences domain:

```text
com.anthropic.claudecode
```

## User Paths

Expected user-level Claude Code surfaces:

```text
~/.claude/settings.json
~/.claude/CLAUDE.md
~/.claude/skills/<name>/SKILL.md
~/.claude/agents/
~/.claude/commands/
```

User-level state may also be stored in:

```text
~/.claude.json
```

This file can include OAuth state, MCP configuration, project state, trust decisions, allowed tools, and other local metadata.

## Project Paths

Expected project-level surfaces:

```text
.claude/settings.json
.claude/settings.local.json
.claude/skills/<name>/SKILL.md
.claude/agents/
.claude/commands/
CLAUDE.md
CLAUDE.local.md
.mcp.json
```

`settings.local.json` and `CLAUDE.local.md` are local/personal surfaces and should not be treated as shared configuration.

## Skills And Namespacing

Standard Claude Code skill behavior should be assessed separately from local symlinked roots.

Relevant standard model:

- Personal skills live under `~/.claude/skills/<name>/SKILL.md`.
- Project skills live under `.claude/skills/<name>/SKILL.md`.
- Managed/enterprise skills have higher precedence than personal and project skills.
- Plugin skills are namespaced as `plugin-name:skill-name`, so they should not collide with normal personal/project skill names.

For UniText, this means:

- Do not mirror all UniText runtime skills directly into Claude personal skills.
- Prefer a clean projection for Claude-specific output.
- Use plugin packaging when namespacing is required.
- Keep upstream/default/plugin skills read-only and separate from UniText-authored skills.

## Accumulated Output And State

Do not confuse read surfaces with accumulated state.

Likely accumulated output/state areas include:

```text
~/.claude/projects/
~/.claude/transcripts/
~/.claude/debug/
~/.claude/tasks/
~/.claude/todos/
~/.claude/file-history/
~/.claude/history.jsonl
```

The Claude CLI also exposes:

```text
claude project purge
```

which indicates that transcripts, tasks, file history, and config entries are project state that can be purged.

## Windows, WSL, And macOS Notes

### Windows

Windows standard user path maps to:

```text
C:\Users\<user>\.claude
```

Managed configuration should be evaluated under:

```text
C:\Program Files\ClaudeCode\
```

Do not assume `C:\ProgramData\ClaudeCode\` is the current standard managed path without confirming the installed version and documentation.

### WSL / Linux

WSL should be evaluated as Linux:

```text
/home/<user>/.claude
/etc/claude-code/
```

Windows and WSL Claude Code state are separate unless the user explicitly symlinks or bridges them.

### macOS

macOS should be evaluated as:

```text
~/.claude
/Library/Application Support/ClaudeCode/
```

Managed preferences may also be distributed through:

```text
com.anthropic.claudecode
```

This report did not validate a live macOS machine.

## Clean Baseline Recommendation For UniText

Do not treat the current local Claude symlink into UniText runtime as the baseline.

Recommended model:

1. Preserve a clean Claude standard baseline.
2. Keep UniText's canonical source under `registry/`.
3. Generate Claude-specific projections instead of pointing Claude directly at the full UniText runtime.
4. Use plugin packaging for shared skills that need namespacing.
5. Keep realtime or experimental skills in an intake queue before promotion.
6. Validate with clean-mode runs such as `claude --bare -p ...` when comparing standard behavior.

`claude --bare` is useful because it skips hooks, LSP, plugin sync, attribution, auto-memory, background prefetches, keychain reads, and `CLAUDE.md` auto-discovery. It is a better baseline probe than the current customized local environment.

## Bridge Project Note

`Q:\Projects\codex-claude-code-bridge` is an MCP bridge project.

It registers through Claude Code MCP, for example:

```powershell
claude mcp add -s user codex-bridge -- node Q:\Projects\codex-claude-code-bridge\server.mjs
```

It is not a Claude skill root and should not be treated as part of Claude Code skill discovery.

## References

- https://code.claude.com/docs/en/configuration
- https://code.claude.com/docs/en/memory
- https://code.claude.com/docs/en/skills
- https://code.claude.com/docs/en/plugins
- https://code.claude.com/docs/en/cli-reference
