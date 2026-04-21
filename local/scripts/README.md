# Local Scripts

這裡放的是 **本機操作腳本**。

- `*.ps1` 保留 Windows-first 參考實作
- `*.py` 提供跨平台 bootstrap / verify / backup 路徑，並逐步承接更多 shared governance core logic

## Current Scripts

- `bootstrap.py`
  - 跨平台先重建 `runtime/`，再初始化 skills delivery、Codex native-config、Copilot MCP config，並維持 project `.mcp.json` 為 template-safe seed
- `verify-bootstrap.py`
  - 跨平台檢查 first-run 結果是否與目前 repo 的 runtime surface 對齊，並接受 template-safe `.mcp.json` seed 或 legacy bootstrapped 的本機 wiring
  - Codex 目標若已 materialize 成 machine-local bundle，也接受「包含完整 runtime baseline + 額外 local skills」的模式
  - 支援 `--home-dir`、`--skip-codex`、`--skip-copilot`、`--skip-project-mcp`，可用於 bounded self-repair simulation
- `build-runtime-layer.py`
  - 由 `registry/` 生成 tracked `runtime/` read model，提供 consumer agents 的低噪音入口與 runtime projections
- `register-codex-skills.py`
  - 以 `--source` 指定舊的 Codex skills tree，比對目前 `C:\\Users\\miles\\.codex\\skills`，並把缺掉的 legacy skills 重新掛回 machine-local Codex bundle
- `create-git-bundle.py`
  - 建立可攜的 `git bundle` 備份，降低僅靠本地工作樹的單點風險
- `preview-renormalize.py`
  - 跨平台 dry-run 預覽 `git add --renormalize` 的 candidate files 與 top-level scope 分布
- `run-renormalize.py`
  - 跨平台執行受控的 renormalize core；支援 `scope`、`dry-run`、`MaxFiles` guard 與真正的 apply mode
- `git-startup.ps1`
  - 為新 session 解析 canonical base branch、要求乾淨工作樹、顯式 fast-forward 更新，並建立新的 feature branch
- `sync-skills.ps1`
  - 將 `runtime/skills/` 同步到本機 skills targets
- `scan-skills.ps1`
  - 掃描候選 skills 並輸出 adoption 檢查結果
- `verify-delivery.ps1`
  - 驗證 source 與常見 skills targets 是否存在、是否為連結、是否可解析
- `health-check.ps1`
  - 對 registry 與 scripts 做最小健康檢查
  - 額外輸出 non-blocking `i18n drift` telemetry，讓 backlog 可見但不直接把 health gate 打成失敗
- `report-i18n-wave.py`
  - 分析目前 `i18n/` dirty worktree，區分純行尾變更、實質翻譯改動與新檔案波次
- `report-release-hygiene.py`
  - 分類目前 dirty worktree，區分 release scope、已知例外與真正 blocker
- `collect-release-evidence.py`
  - 彙整 bootstrap、security tests、i18n wave、release hygiene、MCP smoke 與 Copilot session 的本地 evidence bundle
- `verify-copilot-session.py`
  - 以非互動方式執行 Copilot CLI 驗證，確認 session payload 與 project MCP wiring 是否正常
- `batch-adopt-skills.ps1`
  - 將候選 skills 批次遷入 `registry/skills/`
- `generate-index-entries.ps1`
  - 由 `registry/skills/` 生成 INDEX 所需的 catalog 區塊
- `sync-index-skill-summary.ps1`
  - 同步 `INDEX.md` 的 skills 摘要行（截至日期與 `registry/skills/` 目錄數量）
- `rollback-skills.ps1`
  - 從 `ops/history/adopt_*` 的 backup 回復指定 skill
- `export-review-package.ps1`
  - 將外部審查所需的 cover note、highlights、核心文件、精選 registry entries 與最小 scripts 匯出到 `ops/review-package/`
- `export-template-package.ps1`
  - 將 template-safe docs、generic examples 與 starter layout 匯出到 `ops/template-package/`
- `verify-template-package.ps1`
  - 驗證輸出的 template package 是否包含必要 starter 結構，且不含 review-only / local-only 內容
- `verify-workspace-boundaries.ps1`
  - 驗證目前 authoring repo 的 tracked shared surfaces 是否混入 live workspace metadata、authoring-only docs、或 operations state
- `get-publishability-report.ps1`
  - 彙整 branch 目前的 local-only / ops / shared-surface 變更與 boundary verify 結果，作為 push suitability 的本地報告
  - 對 changed markdown docs 補上 document placement observation，幫助判斷它目前落點是否符合 policy
- `get-document-placement-recommendation.ps1`
  - 依文件角色輸出建議落點，區分 tracked shared layer、`local/docs/`、`local/docs/authoring/`、與 `ops/`
- `lib/workspace-sensitive-metadata.ps1`
  - 載入 shared `WORKSPACE_SENSITIVE_METADATA_RULES.json`，讓 boundary / template / publishability 驗證共用同一套規則
- `validate-workspace-sensitive-metadata-rules.ps1`
  - 驗證 shared `WORKSPACE_SENSITIVE_METADATA_RULES.json` 的結構、regex 可編譯性與自帶案例是否通過
- `preview-renormalize.ps1`
  - Windows PowerShell wrapper；呼叫 `preview-renormalize.py` 並回傳 PowerShell object
- `run-renormalize.ps1`
  - Windows PowerShell wrapper；呼叫 `run-renormalize.py`，保留既有 `Scope / Apply / Force` 入口
- `audit-i18n-drift.py`
  - 讀取 `i18n/manifest.json`，列出各 locale 哪些官方文件缺翻譯、翻譯落後，或尚未被 Git 歷史追蹤到；支援 `json / markdown`、依 `locale / source-doc` 縮小範圍，以及直接輸出成工作報表
  - active gate 由 `required_source_docs` 決定，其餘 mirrored docs 以 optional coverage 顯示，不直接阻斷 release/health gate
- `run-self-repair-simulation.py`
  - 執行 bounded self-repair 情境模擬；v1 先支援 `runtime-target-drift`
  - 使用 temporary home fixture 與 override flags，避免為了模擬直接改動真實本機 wiring
- `export-rebuild-project.ps1`
  - 將目前 repo 重建成可重新命名、可重新初始化的 fresh-project baseline，輸出到 `ops/rebuild-project/`
- `verify-rebuild-project.ps1`
  - 在 template package 驗證之上，再確認 rebuild guide 與 fresh-project 入口存在

## Governance Note

- `sync-skills.ps1` 與 `batch-adopt-skills.ps1` 都應遵守：
  - dry-run first
  - backup before mutation
  - 產生可追溯 log

## Platform Note

- 新的 first-run 路徑優先使用 `bootstrap.py` 與 `verify-bootstrap.py`。
- `preview-renormalize` / `run-renormalize` 已進入第一批 `Python core + PowerShell wrapper` 改寫。
- `sync-skills.ps1` 仍保留作 Windows PowerShell 參考實作與治理樣板。
