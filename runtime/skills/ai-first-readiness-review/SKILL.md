---
name: ai-first-readiness-review
description: Review existing projects, workflows, runbooks, and operational procedures for AI-first readiness. Use when future operators are expected to be primarily AI agents, or when auditing a system for faster agent understanding, better document discovery, safer tool operation, vendor-neutral abstraction layers, and sufficient human-AI-process communication.
runtime_projection: true
source_of_truth: registry/skills/ai-first-readiness-review/SKILL.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/ai-first-readiness-review/SKILL.md`
> Source of truth: `registry/skills/ai-first-readiness-review/SKILL.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill`
# AI-First Readiness Review

## Overview

Use this skill to assess whether an existing project or operating procedure is designed for AI-first use rather than human-only use. Keep the review practical: identify concrete friction that slows agents down, weakens safety, or leaves humans unable to understand what the AI is doing.

Do not optimize only for model output quality. Optimize for the full operating loop:

- how an agent finds the right documents and code
- how an agent understands current project state
- how an agent runs tools safely and repeatably
- how the system stays portable across providers and models
- how humans can monitor, guide, and recover the process

## Quick Start

1. Identify the review target.
- Determine whether the user wants to review a repository, a workflow, a runbook, a toolchain, or a cross-system procedure.
- Confirm the in-scope paths, services, and operators if they are not obvious.

2. Build a current-state map.
- Read local instruction files, README files, process docs, runbooks, command entrypoints, and any logs or task ledgers.
- Map where orientation, retrieval, tool use, handoff, and escalation information currently lives.
- Distinguish stable operator guidance from roadmap notes, dev-cycle journals, and temporary planning documents.

3. Score the system using the five review dimensions.
- Agent comprehension
- Document retrieval and reading ergonomics
- Tool operability
- Vendor-neutral abstraction
- Human-AI-process communication

4. Identify failures by severity.
- Critical: blocks reliable AI operation or creates hidden unsafe behavior
- Major: slows agents materially or creates frequent ambiguity
- Minor: annoying but survivable; worth fixing when touching adjacent areas

5. Recommend the smallest viable remediation set first.
- Prefer targeted structural fixes over "rewrite everything"
- Recommend new process layers only when the current system fails the communication minimum

6. Deliver a concise review.
- Summarize evidence
- List findings in severity order
- Propose concrete remediations
- State what should be added, simplified, or abstracted

Use [references/review-rubric.md](references/review-rubric.md) for the full checklist.
Use [references/report-template.md](references/report-template.md) when writing the final review.
Use [references/communication-baseline.md](references/communication-baseline.md) when deciding whether the project needs a dedicated human-AI-process communication layer.

## Review Dimensions

### 1. Agent Comprehension

Check whether an AI agent can quickly reconstruct the project without heroic inference.

- Look for a clear starting path: repo guide, architecture summary, workflow map, command catalog, environment notes, and common failure modes.
- Prefer layered orientation: short entrypoint docs first, deeper references second.
- Flag systems that force the agent to rediscover structure from scattered files or tribal knowledge.
- Flag ambiguous naming, missing ownership, and undocumented branch or execution conventions.

### 2. Document Retrieval And Reading Ergonomics

Check whether the project is optimized for targeted lookup rather than human browsing alone.

- Prefer stable filenames, predictable folder layout, short overview docs, and one-hop links from index docs.
- Prefer documents that separate high-level guidance from detailed references.
- Flag large undifferentiated documents without navigation hints.
- Flag duplicated or contradictory guidance across files.
- Flag cases where the right document exists but is hard to discover from naming or placement.

### 3. Tool Operability

Check whether an agent can safely and confidently use the system's tools.

- Prefer explicit command entrypoints, deterministic scripts, bounded parameters, dry-run modes, and good failure messages.
- Prefer tool outputs that expose state, next steps, and operator-facing context.
- Flag commands that require hidden setup, tacit operator knowledge, or interactive guesswork.
- Flag flows that force an agent to reverse engineer the right sequence each time.
- Distinguish human convenience wrappers from agent-safe automation surfaces.

### 4. Vendor-Neutral Abstraction

Check whether the design avoids deep lock-in to a single model, provider, or agent runtime.

- Prefer capability-oriented interfaces over provider-specific branching in business logic.
- Prefer adapter layers, configuration-driven backends, and well-defined custom interfaces.
- Prefer contracts based on tasks, tools, schemas, and policies rather than model branding.
- Flag assumptions that only hold for one provider, one prompting style, or one tool protocol.
- Flag hidden coupling between core process logic and a specific AI service.

### 5. Human-AI-Process Communication

Check whether humans can understand and steer the AI-driven process with low friction.

- Prefer visible execution state, task ownership, handoff points, escalation rules, and concise status records.
- Prefer communication channels that connect operator intent, AI actions, and process state in one place.
- Flag systems where humans cannot tell what the AI changed, attempted, or is waiting on.
- Flag workflows where an AI can proceed but the human cannot quickly review or intervene.
- If the current project fails the minimum communication baseline, recommend adding a dedicated communication, registration, or message platform rather than relying on ad hoc notes.

Use [references/communication-baseline.md](references/communication-baseline.md) to judge the minimum acceptable barrier for human operators.

## Review Workflow

### 1. Scope The Review

- Identify the concrete operating surface: codebase, documentation set, CLI toolchain, workflow, or service mesh.
- Exclude unrelated sibling projects unless the user explicitly includes them.
- State assumptions that materially affect the review.

### 2. Gather Evidence

- Read entrypoint docs first, then only the deeper references needed to support findings.
- Collect real command names, file paths, interfaces, and workflow checkpoints.
- Prefer evidence from the current implementation over aspirational documentation.
- If execution-based validation is unavailable, continue with code-and-doc evidence and state the limitation explicitly.

### 3. Score And Classify

- Use the rubric to identify where the system helps or hinders AI-first operation.
- Keep findings tied to observed evidence, not generic AI advice.
- Separate architecture problems from documentation problems and from workflow governance problems.

### 4. Recommend Remediations

- Suggest the minimum set of structural changes that unlock the next level of agent effectiveness.
- Favor fixes that improve both AI operability and human maintainability.
- When a dedicated communication layer is needed, explain why existing mechanisms are below the minimum baseline.

### 5. Write The Review

- Start with findings, not a long summary.
- Order findings by severity and operator impact.
- Include concrete examples of what the AI currently cannot do efficiently.
- Include concrete implementation directions, not only principles.

## Decision Rules

- Do not recommend model-specific lock-in unless the user explicitly wants provider specialization.
- Do not assume "works for humans" means "works for agents."
- Do not confuse verbose documentation with useful orientation.
- Do not introduce a new communication platform unless the current setup fails the minimum human visibility and control threshold.
- When tradeoffs exist, prefer safety, reversibility, and fast operator comprehension over clever automation.

## Deliverables

Default deliverables are:

- a short current-state summary
- a severity-ordered findings list
- a remediation plan grouped into now, next, and later
- a call on whether a dedicated human-AI-process communication layer is required

Use the report template when the user wants a formal written review.

## References

- Full scoring checklist: [references/review-rubric.md](references/review-rubric.md)
- Review write-up format: [references/report-template.md](references/report-template.md)
- Human-AI-process minimum baseline: [references/communication-baseline.md](references/communication-baseline.md)
