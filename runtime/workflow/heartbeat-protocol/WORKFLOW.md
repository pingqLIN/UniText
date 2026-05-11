---
name: heartbeat-protocol
description: Sanitized shared workflow guidance for heartbeat producer and consumer handoffs.
runtime_projection: true
source_of_truth: registry/workflow/heartbeat-protocol/WORKFLOW.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/workflow/heartbeat-protocol/WORKFLOW.md`
> Source of truth: `registry/workflow/heartbeat-protocol/WORKFLOW.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `workflow`
# Heartbeat Protocol Workflow

## Purpose

The heartbeat protocol gives tools a shared way to describe whether a long-running local process is still alive, who produced the signal, and how a consumer should interpret the signal.

This document is the UniText shared guidance layer. It preserves only the stable protocol shape and responsibilities. It does not preserve live heartbeat records, session state, local runtime evidence, terminal transcripts, or private session JSON.

## Field Meaning

Use implementation-specific field names only when a downstream adapter requires them. The shared meaning is:

| Field | Meaning | Shared-safe guidance |
|---|---|---|
| `protocol` | Identifies the heartbeat protocol family or version. | Use a stable string or semantic version; do not encode a local hostname, account, or session id. |
| `producer` | Identifies the component that emits the heartbeat. | Describe the role, not the machine-specific instance. |
| `consumer` | Identifies the component expected to read or act on the heartbeat. | Describe the role or workflow stage. |
| `subject` | Names the process, task, job, or workflow being monitored. | Use a logical label. Keep private project names out unless the repository already owns that public name. |
| `status` | Current lifecycle signal. | Prefer a small vocabulary such as `starting`, `alive`, `paused`, `stopping`, `complete`, `failed`, or `unknown`. |
| `observed_at` | Time the signal was observed or emitted. | Store live timestamps only in local state. Shared examples should use placeholders. |
| `ttl` | Maximum age before the signal should be treated as stale. | Express as a duration policy, not as evidence from one machine. |
| `message` | Short human-readable context. | Keep it generic and avoid transcripts, prompts, secrets, paths, or raw command output. |
| `correlation` | Optional logical link between producer and consumer views. | Use opaque placeholders in shared examples; real correlation ids belong in local/live state. |

## Producer Responsibilities

- Emit heartbeat records only to the appropriate local/live state layer.
- Keep shared specs limited to field meaning, status vocabulary, and handoff expectations.
- Avoid writing private session JSON, raw terminal output, prompts, environment dumps, absolute paths, account identifiers, hostnames, tokens, or machine-specific runtime evidence into shared documents.
- When a live record needs local path mapping or adapter wiring notes, keep that material in a local-only layer.

## Consumer Responsibilities

- Treat shared UniText heartbeat guidance as protocol documentation, not as a current state source.
- Read live heartbeat state only from the runtime surface owned by the producing tool or local adapter.
- Apply freshness rules before acting on a heartbeat. If a signal is older than its local ttl policy, treat it as stale or unknown.
- Do not promote live state into UniText unless it has been sanitized into durable guidance.
- Do not infer machine paths, active sessions, or terminal history from this shared workflow.

## Local And Live State Boundary

UniText may store:

- protocol purpose
- field semantics
- status vocabulary
- producer and consumer responsibilities
- privacy rules and non-goals
- sanitized adapter-neutral examples with placeholders

UniText must not store:

- live heartbeat records
- private session JSON
- terminal transcripts or full conversation text
- machine-specific path maps, unless they are kept in a local-only layer
- runtime evidence from one machine
- secrets, tokens, account identifiers, hostnames, or personal filesystem paths

If a future workflow needs both stable guidance and live state, split them into a sanitized/shared document and a local/live document. The shared document may point to the kind of local surface to consult, but it must not include the live values.

## Privacy And Non-Goals

This workflow is not a session database, monitoring log, transcript archive, or incident evidence store. It is also not a bridge for copying state back from Tips Terminal, codex-calendar-todo, or any other producer repository.

Promotion into UniText is allowed only after removing live values and reducing the material to reusable workflow guidance. The result must remain useful without revealing which machine, terminal, session, or user produced the original heartbeat.
