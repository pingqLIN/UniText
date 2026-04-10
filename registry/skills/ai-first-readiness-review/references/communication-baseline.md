# Human-AI-Process Communication Baseline

Use this reference when deciding whether the existing project already provides enough communication support for AI-first operation.

## Minimum Acceptable Baseline

The current system is acceptable only if a human can do all of the following without heavy reconstruction effort:

- understand the current task or process state
- see what the AI most recently attempted or changed
- identify what the AI is waiting on
- review the last meaningful decision or handoff
- know where to intervene or escalate

If any of these are missing, treat the baseline as below minimum.

## Signals That The Baseline Is Good Enough

- one obvious place to read status
- one obvious place to record handoff or intervention
- durable task or run history
- clear mapping between operator intent and AI action
- short summaries rather than raw low-level logs only

## Signals That A Dedicated Layer Is Needed

Recommend adding a human-AI-process communication, registration, or messaging layer when several of these are true:

- status is fragmented across tools
- AI actions are visible only in technical logs
- humans cannot tell whether the AI is blocked, complete, or awaiting approval
- there is no durable handoff record
- workflow spans multiple people, tools, or days
- auditability matters but current notes are ad hoc

This layer does not need to be a new standalone product. An embedded dashboard panel, a durable ledger inside the existing system, or a lightweight workflow register can satisfy the requirement if it restores human visibility and control.

## What The Added Layer Must Provide

At minimum, the new layer should support:

- task or run registration
- current state and owner visibility
- checkpoint or approval markers
- concise AI activity summaries
- escalation or intervention messages
- durable history that humans can read quickly

## Decision Rule

Do not add a new platform just because "more tooling sounds better."

Add it when:

- the current setup is below the minimum baseline, and
- lightweight documentation cleanup alone will not restore human visibility and control

If the problem can be solved by improving the existing ledger, ticketing flow, run log, or status channel, prefer that before introducing a new platform.
