---
runtime_projection: true
source_of_truth: registry/skills/ai-runtime-governance/references/change-contract.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/ai-runtime-governance/references/change-contract.md`
> Source of truth: `registry/skills/ai-runtime-governance/references/change-contract.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Change Contract

## Required Pre-Change

- Risk classification: `L0/L1/L2/L3`
- Target scope and impact list
- Backup path and evidence
- Simulation output

## Required Post-Change Report

- Files Changed
- Reason
- Simulation Evidence
- Preview Evidence
- Verification Command + Result
- Risk Level
- Rollback Command + Verification
- Incident/Escalation section if failure

## Verification Minimum

- Path object type is expected (dir/file/reparse point/hard link)
- Config key exists with expected value or expected absence
- CLI still starts with non-error status for touched program

## Rollback Standard

- Every edited config file has timestamped backup copy
- Every moved path has `.bak.<timestamp>` sibling
- Rollback command is deterministic and logged

## Drift Monitoring

- Store baseline file hashes in `C:\Dev\AI_UNIFIED\ops\baseline.json`
- Compare current hashes with baseline in periodic audits
- Flag unauthorized drift and produce remediation list
