# Review Rubric

Use this rubric to drive an evidence-based AI-first readiness review.

## 1. Agent Comprehension

Ask:

- Can a new agent identify the project goal within a few file reads?
- Can it locate the main entrypoints, command surfaces, and operational boundaries quickly?
- Are project instructions layered from short orientation to deep detail?
- Are ownership, branch conventions, and common failure modes explicit?

Strong signals:

- clear root instruction file
- concise architecture or workflow overview
- stable command catalog
- explicit process vocabulary

Weak signals:

- orientation spread across many unrelated files
- docs that assume prior tribal knowledge
- high-value information hidden in issue threads, commit messages, or chat history

## 2. Document Retrieval And Reading Ergonomics

Ask:

- Can the agent predict where to search for a given kind of information?
- Are filenames and directories semantically meaningful?
- Are large references split into overview plus detailed sections?
- Are links and cross-references one hop away from the overview?

Strong signals:

- entrypoint docs with targeted links
- small, focused references
- naming conventions that match tasks
- documents written for lookup, not only narrative reading

Weak signals:

- giant mixed-purpose docs
- duplicate guidance with different wording
- missing index docs
- documentation that requires broad search before every task

## 3. Tool Operability

Ask:

- Are the preferred commands explicit and reproducible?
- Do scripts expose safe parameters, status, and clear failure modes?
- Is it obvious which operations are safe, risky, read-only, or destructive?
- Are there dry-run or validation paths before high-impact actions?

Strong signals:

- deterministic scripts
- bounded interfaces
- explicit command examples
- outputs that explain next steps

Weak signals:

- hidden setup steps
- interactive-only flows
- commands that assume operator memory
- wrappers whose side effects are unclear

## 4. Vendor-Neutral Abstraction

Ask:

- Is core process logic independent from a single model vendor or runtime?
- Are AI integrations hidden behind capability or policy interfaces?
- Can the project swap model providers without rewriting business logic?
- Are schemas, tools, and prompts expressed as contracts rather than brand-specific assumptions?

Strong signals:

- adapter layers
- backend selection through config
- custom provider interfaces
- provider-specific code isolated to edge modules

Weak signals:

- provider names embedded in domain logic
- prompts or workflows tightly coupled to one model behavior
- no seam between orchestration logic and transport/provider layer

## 5. Human-AI-Process Communication

Ask:

- Can a human see what the AI is doing, waiting on, or changing?
- Is there a clear handoff path between human, agent, and process state?
- Can operators review history, decisions, and escalation points quickly?
- Is there a shared place for status, registration, or messaging when the work crosses multiple steps or people?

Strong signals:

- visible task ledger
- concise execution records
- escalation rules
- operator-facing summaries

Weak signals:

- AI actions buried in raw logs
- no durable record of intent or state
- humans must reconstruct status from multiple tools
- no clear place to intervene

## Severity Guidance

- Critical: hidden unsafe automation, no reliable orientation path, no operator visibility, or deep provider lock-in at the core layer
- Major: recurring ambiguity, repeated rediscovery cost, brittle tool usage, or poor handoff between human and AI
- Minor: paper cuts, missing shortcuts, or local inconsistencies that do not block safe operation

## Remediation Priorities

- Now: unblock reliable understanding and safe execution
- Next: improve speed, predictability, and portability
- Later: polish, compression, and experience improvements
