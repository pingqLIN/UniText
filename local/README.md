# Local Overlay

這個目錄承載的是 **deployment overlay 與 cross-platform bootstrap scripts**。

它的設計目的很單純：

- 不讓本機配置污染根目錄的核心概念
- 讓平台對接與初始化邏輯可以集中管理
- 讓本機特定內容可以被刪除或重建，而不影響 shared baseline

## Contents

- `docs/`
  - 只追蹤 template-safe 的 generic docs
- `scripts/`
  - cross-platform bootstrap / verify / export scripts

## Tracked Baseline

- `docs/ADOPTION_CHECKLIST.md`
  - adoption flow 的最小檢查表
- `docs/CLI_COMPAT_MATRIX.md`
  - Claude / Codex / Gemini 的行為基線
- `scripts/`
  - cross-platform 與 Windows-first 的治理腳本集合

## Local-Only Notes

若需要記錄當前工作站的 path map、deployment notes、authoring archives 或 review archives，建議保留在未追蹤的 local-only 檔案中，而不要進入共享 repo baseline。

## Rule

若某份內容描述的是：

- 這個系統應該如何運作
  - 它不應放在 `local/`
- 這個實例目前怎麼配置
  - 它可以放在 `local/`，但預設不應追蹤進 shared template
