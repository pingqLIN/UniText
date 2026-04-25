---
name: claude-plans
description: Canonical planning workflow seed for structured plan documents used during design and execution review.
runtime_projection: true
source_of_truth: registry/workflow/claude-plans/WORKFLOW.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/workflow/claude-plans/WORKFLOW.md`
> Source of truth: `registry/workflow/claude-plans/WORKFLOW.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `workflow`
# Claude Plans Workflow

## Purpose

這份 workflow 用來規範計畫文件的最小結構，讓 human 與 AI 都能穩定閱讀與擴充。

## Recommended Structure

1. Goal
2. Scope
3. Constraints
4. Risks
5. Plan
6. Verification

## Checkpoints

- `taskAnalysis`
- `resourceAllocation`
- `preExecution`
- `phaseComplete`
- `finalReview`

## Usage

- 用於規劃文件
- 用於審查前的 execution outline
- 用於多階段交付的 verification planning
