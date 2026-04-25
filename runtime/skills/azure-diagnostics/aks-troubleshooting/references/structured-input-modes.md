---
runtime_projection: true
source_of_truth: registry/skills/azure-diagnostics/aks-troubleshooting/references/structured-input-modes.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/azure-diagnostics/aks-troubleshooting/references/structured-input-modes.md`
> Source of truth: `registry/skills/azure-diagnostics/aks-troubleshooting/references/structured-input-modes.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# AKS Structured Input Modes

Use this reference when the troubleshooting request already contains structured inputs.

## Detector-backed Mode

Use when AKS-aware detectors or AppLens-style insights are available.

Decision rules:

- Ignore findings where the detector is `emergingIssues`.
- Prefer critical findings over warnings.
- Prefer findings with more concrete remediation detail when choosing the likely root problem.
- Preserve per-insight output: problem summary, root-problem flag, affected resources, suggested commands.

## Warning Events Mode

Use when the request includes Kubernetes warning events.

Expected output:

- summary of the events and their impact
- likely cause or causes
- next kubectl checks
- monitoring follow-up

## Metrics Scan Mode

Use when the request includes CPU or memory time-series data.

Expected output:

- healthy or unhealthy status
- anomaly timestamps and explanations
- suggestion tied to the observed metric pressure

## Generic Symptoms Mode

Use when the request includes resource symptoms but not detector results, warning events, or time-series metrics.

Expected output:

- symptom summary by resource
- likely failure domain
- next evidence-collection steps

## Learn Grounding Fallback

If the first troubleshooting pass is incomplete, search Microsoft Learn using:

- the user prompt
- the parsed problem names
- the AKS troubleshooting context

Use Learn grounding to refine or validate the root-cause hypothesis, not to replace observed evidence.
