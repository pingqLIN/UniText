---
runtime_projection: true
source_of_truth: registry/skills/external-audit-orchestrator/references/reference-sources.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/external-audit-orchestrator/references/reference-sources.md`
> Source of truth: `registry/skills/external-audit-orchestrator/references/reference-sources.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
﻿---
---

# Reference Sources

This file records the main sources used to shape `external-audit-orchestrator` v0.1.

Repeat these citations in user-facing audit outputs when they materially affect the audit mode, recommendation, or wording.

## Official external references

1. OpenAI Codex docs
   - `https://developers.openai.com/codex/cloud`
   - Why used: capability baseline for Codex cloud tasks, parallel work, skills, hooks, subagents, and GitHub-connected review workflows

2. OpenAI Codex use cases
   - `https://developers.openai.com/codex/use-cases`
   - Why used: evidence that pull request review and workflowized skills are first-class Codex patterns

3. Anthropic Claude Code subagents
   - `https://code.claude.com/docs/en/sub-agents`
   - Why used: subagent structure, project-level agent placement, and read-only code-reviewer pattern

4. Anthropic Claude Code hooks
   - `https://code.claude.com/docs/en/hooks`
   - Why used: `PreToolUse` and `SubagentStop` review gating model

5. skills.sh docs
   - `https://skills.sh/docs`
   - Why used: leaderboard semantics and ranking caveat

6. Gemini CLI command reference
   - `https://geminicli.com/docs/reference/commands/`
   - Why used: `/agents` management commands and CLI command behavior for Gemini reviewer installation guidance

7. Gemini CLI subagents documentation
   - `https://geminicli.com/docs/core/subagents/`
   - Why used: project-level `.gemini/agents/*.md` placement, subagent frontmatter schema, temperature, tool isolation, and custom subagent behavior

8. Gemini CLI headless mode reference
   - `https://geminicli.com/docs/cli/headless/`
   - Why used: `gemini -p` and `--output-format json` automation pattern for actor-critic review loops

## Referenced public skill examples

1. CodeRabbit `code-review`
   - `https://skills.sh/coderabbitai/skills/code-review`
   - Why used: severity model and diff-oriented external reviewer pattern

2. ai-cortex `review-code`
   - `https://skills.sh/nesnilnehc/ai-cortex/review-code`
   - Why used: orchestrator skill pattern built from fixed-order atomic reviews

3. WomenDefiningAI `code-reviewer`
   - `https://skills.sh/womendefiningai/claude-code-skills/code-reviewer`
   - Why used: balanced review dimensions and pre-deploy security posture

4. wshobson `code-review-excellence`
   - `https://skills.sh/wshobson/agents/code-review-excellence`
   - Why used: severity labels and review communication model

5. rsmdt `code-review`
   - `https://skills.sh/rsmdt/the-startup/code-review`
   - Why used: multi-lens reviewer coordination model

## Local cross-project references

1. `<tb2-project-root>\README.md`
   - Why used: TB2 runtime capabilities, `codex_relay`, and built-in profile inventory

2. `<tb2-project-root>\docs\platform-baseline-matrix.md`
   - Why used: current validation status for `claude`, `codex`, and `copilot` profiles

3. Local Codex skill library under `<local-codex-skills-dir>`
   - Why used: adjacent skills that this orchestrator can compose with, especially:
     - `security-best-practices`
     - `security-threat-model`
     - `gh-address-comments`
     - `ai-first-readiness-review`
     - `conversation-memo`
     - `project-development-loop`

4. `<windows-project-root>\external-audit-orchestrator\references\codex-permission-notes.md`
   - Why used: observed Codex exec permission failures and reviewer-routing failure modes.

5. `<windows-project-root>\external-audit-orchestrator\docs\local\side-conversations\2026-06-01-reviewer-failure-handling.zh-TW.md`
   - Why used: failed, partial, and unavailable reviewer gate classification rules.

## Usage rule

If an audit used any of the above, repeat the relevant subset in the audit output. Do not dump the full list unless all of it was actually used.
