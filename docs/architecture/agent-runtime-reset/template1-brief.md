# Template 1 Brief

## Problem

UniText 目前把 `registry/` 同時當成 canonical authoring source 與 consumer runtime surface 使用。

具體表現：

- Codex `skills_path` 直接對齊 `registry/skills`
- `verify-bootstrap.py` 也把這件事當成正確狀態
- `README.md` / `INDEX.md` 同時服務 human discovery、curator discovery、consumer runtime lookup
- agent 為了回答簡單規則，常需要穿過大量不相干治理文件

## Required Direction

- 保留 `registry-first` 作為 canonical authoring 核心
- 新增 tracked `runtime/` 作為 consumer first-read surface
- 明確拆開 `registry/`、`runtime/`、`local/`、`ops/`
- Codex-first 修正，但保持 cross-CLI extensibility
- 用 20 題 acceptance suite 驗證 runtime surface

## Required Sections For Template 2

- Diagnosis
- Target State
- Layer Model
- Runtime Surface
- Delivery and Verify Contract
- Migration
- Validation
- Risks

## Non-Goals

- 不把 `ops/` 當 runtime 層
- 不把 machine-local overlay 混進 shared runtime layer
- 不繼續讓 consumer 直接把 `registry/*` 當第一入口
