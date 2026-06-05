# UniText Runtime 入口

> 狀態：active baseline
> 角色：consumer agents 與 automation 的最短安全入口。

若你是正在此 repository 中執行工作的 agent，請從這裡開始。不要將 `README.md` 或 `INDEX.md` 作為你的預設啟動介面。

## 優先閱讀順序

1. [runtime/START.md](runtime/START.md)
2. [runtime/RULES.md](runtime/RULES.md)
3. [runtime/ROUTES.md](runtime/ROUTES.md)
4. [runtime/catalog.json](runtime/catalog.json)

只閱讀 runtime view 所指向的更深層 source files。

## Runtime 契約

- `registry/` 是 canonical authoring source，不是預設的 consumer runtime。
- `runtime/` 是供 agents 使用、受版本追蹤的 read model。它由 `registry/` 產生，並刻意讓啟動 context 保持低噪音。
- `runtime/catalog.json` 採 discovery-first 設計。它應包含 stable IDs、resource types、status、summary、source pointers、runtime projection pointers、delivery hints，以及 references。
- `bootstrap.py` 會在套用 local delivery wiring 之前，先重建 runtime layer。
- Codex 應讀取其已設定的本機 `skills_path` 目標，不應直接指向 `registry/skills`。
- 如果任務需要 canonical content，請沿著 runtime projection 回溯到它的 `source_of_truth`，或使用 project-local MCP surface。

## Request Budget 路由

在打開更深層 files、skills、connectors 或 web tools 前，先分類 request。預設使用能正確完成任務的最小 budget：

| Budget | 適用情境 | Runtime rule |
|---|---|---|
| `L0 no-tool` | 一般問答、文字潤飾、翻譯、腦暴、靜態推理 | 不載入 skills、files、connectors 或 web tools。 |
| `L1 light-retrieval` | 已知檔案查找、metadata checks、小片段查證 | 只讀必要的 route file、catalog entry 或 narrow snippet。 |
| `L2 targeted-retrieval` | 需要特定 file evidence 或有限比對的問題 | 先 search，再只打開命中的 sections。 |
| `L3 artifact` | 建立、編輯、轉換或匯出 PDF、DOCX、PPTX、XLSX、images 或類似 artifacts | 只載入對應 artifact skill 與它直接需要的 support files。 |
| `L4 complex` | 多檔 synthesis、migration、governance rewrite、廣泛分析或 data-heavy work | 說明擴大的 scope，保留中間 summaries，並避免載入無關 skill/tool。 |

只有目前 budget 無法滿足 request 時才升級。不要因為 artifact skills、registry folders、connector instructions 或完整文件存在，就預先載入它們。

## Tool 與 Skill 觸發

| Surface | 使用時機 | 避免時機 |
|---|---|---|
| Web/search | 使用者要求 current、latest、recently changed、不確定、需要 citation，或涉及法律、金融、醫療、時程、價格、產品資訊 | 改寫、翻譯、靜態 repo reasoning，或已知 local facts |
| File search/read | 使用者提到 uploaded file、repo file、prior document，或詢問某檔案內容 | 純概念討論或一般寫作 |
| Artifact skills | 使用者要求建立、編輯、轉換、匯出、驗證或打包該 artifact type | 只需要 draft text、腦暴或一般解釋 |
| Connectors | 任務需要使用者已連接的 email、calendar、drive、issue tracker、deployment 或 account data | Public info、本機 repo work 或模擬 examples |
| Code/runtime tools | 任務需要 local execution、tests、generated files、repo inspection 或可重現 evidence | 單純說明，且執行不會增加 confidence |

## 任務路由

| 任務 | 從這裡開始 |
|---|---|
| 了解 UniText 是什麼 | [README.md](README.md)，接著閱讀 [VISION.md](VISION.md) |
| 尋找面向人的文件或 catalog 摘錄 | [INDEX.md](INDEX.md) |
| 檢查 runtime inventory | [runtime/catalog.json](runtime/catalog.json) |
| 了解 metadata requirements | [RESOURCE_SPEC.md](RESOURCE_SPEC.md) |
| 規劃交付到 host tools | [OPERATIONS.md](OPERATIONS.md) |
| 處理 Codex runtime duplication | [docs/operations/skill-runtime-codex-duplication.SOP.md](docs/operations/skill-runtime-codex-duplication.SOP.md) |
| 將 UniText 接到既有機器 | [docs/plans/EXISTING_ENVIRONMENT_ADOPTION_PLAN.md](docs/plans/EXISTING_ENVIRONMENT_ADOPTION_PLAN.md) |

## 安全規則

- 除非使用者明確核准，否則不要 push、upload、paste 或 publish repository content。
- 在沒有 dry-run plan、backup 或 rollback path，以及 verification step 的情況下，不要變更 host configuration。
- 不要預設將產生的 `ops/` evidence、local notes 或 review packets 視為 publishable docs。
- 對於 documentation-only work，不要手動編輯 `runtime/catalog.json`。只有在 registry/runtime source files 變更時，才透過 `python local/scripts/build-runtime-layer.py --write` 重建它。

## 最小驗證

針對 documentation 或 governance 變更，優先使用這組小型 baseline：

```powershell
git diff --check
python local/scripts/build-runtime-layer.py
python local/scripts/verify-workspace-boundaries.py --format json
python local/scripts/audit-i18n-drift.py --format json --sample-size 0 --exit-zero
python -m unittest tests.test_registry_inventory tests.security.test_i18n_drift tests.security.test_workspace_sensitive_metadata tests.security.test_release_hygiene
```

當 registry、runtime generation、template export 或 project-map behavior 有變更時，再擴充到 [TEST_BASELINE.md](TEST_BASELINE.md)。
