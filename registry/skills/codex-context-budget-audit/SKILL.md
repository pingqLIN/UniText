---
name: codex-context-budget-audit
description: Audit Codex initial-context budget and token overhead from a specific workdir or Codex home. Use when the user asks to inspect, compare, reduce, or visualize initial prompt/token usage from skills, plugins, MCP servers, memories, AGENTS.md, or runtime configuration. Includes a CLI that reports phase-separated estimates and an ASCII prompt-composition chart.
metadata:
  runtime_support_files: true
---

# Codex Context Budget Audit

Use this skill when the task is about measuring or comparing Codex startup/context overhead from local configuration sources.

## Workflow

1. Identify the execution location.
   - Use the user's requested path as `--workdir`.
   - Default Codex home is `$env:USERPROFILE\.codex` unless the user provides another path.
2. Run the bundled CLI first:

```powershell
python "$env:USERPROFILE\.codex\skills\codex-context-budget-audit\scripts\context_budget_audit.py" --workdir <windows-project-root>
```

3. If comparing runs, save a baseline JSON and compare a later run:

```powershell
python "$env:USERPROFILE\.codex\skills\codex-context-budget-audit\scripts\context_budget_audit.py" --workdir <windows-project-root> --json-out <temp>\codex-context-before.json
python "$env:USERPROFILE\.codex\skills\codex-context-budget-audit\scripts\context_budget_audit.py" --workdir <windows-project-root> --baseline <temp>\codex-context-before.json
```

4. Report the result by phase:
   - Config state: memory, plugin, MCP enabled counts.
   - Memory summary estimate.
   - AGENTS/instructions estimate.
   - Local skill manifest estimate.
   - Plugin skill manifest estimate.
   - MCP enabled surface.
   - Optional triggered skill body upper bound.
5. State limits clearly:
   - Platform system/developer/tool-schema tokens are not fully observable from local files.
   - Existing sessions do not shrink after config changes; a new Codex session is required.
   - Token counts are estimates based on character ratios, not tokenizer telemetry.

## ASCII Prompt Ratio Sketch

Use the CLI dashboard as the main visualization. The visual style should stay pure ASCII and terminal-safe while borrowing these interface cues:

- Claude Code style: compact statusline-like metrics for subtotal, memory, MCP, and platform-base state.
- Gemini CLI style: terminal-first source rows that expose tools, MCP, and local workspace surfaces clearly.
- Codex audit requirement: keep unobservable platform prompt/tool-schema tokens separate from measured local estimates.
- Color is allowed when the terminal supports ANSI. Use `--color auto` by default, `--color always` for screenshots/log demos, and `--color never` for plain logs.
- For Codex-visible colored output, prefer `--render codex`; it emits Markdown/HTML inline colors instead of ANSI escape codes.
- Keep long vertical separators in source rows so the chart stays readable even without color.

If summarizing manually, use this shape:

```text
+--------------------------------------------------------------------------------------------------+
| CODEX CONTEXT BUDGET                                            local estimate / startup surface |
| STYLE RAIL  | dense statusline | clear tool surface | measured-local estimate                    |
+==================================================================================================+
| STATUS      | LOCAL SUBTOTAL  10.9k-14.6k tok                           MEMORY OFF | MCP 0 enabled |
| RUNTIME     | PLATFORM BASE   unknown                      system + developer + native tool schema |
+--------------------------------------------------------------------------------------------------+
| ID  | SOURCE                           | BAR                      | TOKENS       |   % | STATE     |
+--------------------------------------------------------------------------------------------------+
| SYS | platform system/developer/tools   | [????????????????????????] |      unknown | n/a | runtime-owned |
| MEM | memory summary                   | [------------------------] |      0-0 tok |   0% | config-gated |
| DOC | AGENTS/workspace instructions    | [==========--------------] | 2.7k-3.6k tok|  42% | local files  |
| SKL | local skill manifests            | [#############-----------] | 3.5k-4.7k tok|  55% | local roots  |
| PLG | plugin skill manifests           | [+-----------------------] |  180-241 tok |   3% | enabled plugins |
| MCP | enabled MCP tool surface         | [------------------------] |      0-0 tok |   0% | tool schema hidden |
+--------------------------------------------------------------------------------------------------+
```

Never present the sketch as exact telemetry. Label it as an estimate or measured-local subset. Keep `SYS` with question marks unless runtime telemetry exists.

## CLI

The script is intentionally self-contained and uses only Python standard library modules.

Useful options:

- `--workdir PATH`: target execution location.
- `--codex-home PATH`: Codex home directory.
- `--config PATH`: explicit config file.
- `--json-out PATH`: save report for future comparison.
- `--markdown-out PATH`: save the Codex-friendly colored Markdown/HTML dashboard.
- `--baseline PATH`: compare against a saved report.
- `--color auto|always|never`: control ANSI colors.
- `--render terminal|codex|both`: choose the ASCII/ANSI terminal dashboard, the Codex Markdown/HTML dashboard, or both.
- `--include-skill-bodies`: estimate full SKILL.md body size as an upper-bound, not startup cost.
