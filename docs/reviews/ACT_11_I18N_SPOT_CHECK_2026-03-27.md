---
description: Spot-check report for non-English documentation coverage and translation drift across README, OPERATIONS, and TEMPLATE_RELEASE_PACKAGE
---

# ACT-11 i18n Spot Check

> 日期：2026-03-27
> 用途：完成 Phase 3 的 i18n confidence spot check，記錄多語文件是否與目前英文主文件一致。

## 1. Scope

本次抽查依據 `REVIEW_FINDINGS_REMEDIATION_PLAN_2026-03-27.md` 的 ACT-11 執行，採樣：

- 語言：
  - `ja`
  - `de`
  - `es`
- 文件：
  - `README.md`
  - `OPERATIONS.md`
  - `TEMPLATE_RELEASE_PACKAGE.md`

本次不是全面翻修，而是抽樣確認：

- 是否存在明顯語義漂移
- 是否遺漏 Phase 1 / Phase 2 後新增的關鍵敘事
- 是否出現明顯 machine-translation / mixed-language 問題

## 2. Overall Result

整體判定為：

- `OPERATIONS.md`：**大致對齊，可接受**
- `README.md`：**明顯過時，需要更新**
- `TEMPLATE_RELEASE_PACKAGE.md`：**明顯過時，需要更新**

因此本次 i18n confidence 的結論是：

> 多語文件已具備基本可讀性，但尚未全面跟上 2026-03-27 的 release-boundary、support-class、與 template export 敘事更新。

## 3. Findings

### F1 — README 譯本仍停留在舊版 CLI / support 敘事

抽查的 `ja`、`de`、`es` README 仍使用舊的 CLI 表格，內容包括：

- `Delivery Mode` 欄位
- `GitHub CLI`
- 舊版 path-oriented 說明

但目前英文主文件已改成：

- `Support Class`
- `Verification Scope`
- `verified / partial / target`
- `Copilot CLI` 為 `adapter pending`
- `Current Material Sets`

這表示目前譯本尚未同步 Phase 2 的 ACT-08 收斂結果。

### F2 — TEMPLATE_RELEASE_PACKAGE 譯本缺少新版 release-boundary 內容

抽查的 `ja`、`de`、`es` 版本都缺少英文主文件後續加入的關鍵段落，例如：

- 公開授權且可再分發 skills
- `SOURCE.yaml` provenance 要求
- `local-only validation materials`
- `proprietary / restricted-license skills`
- `rebuild-project` export / verify 路徑
- `Skills Release Rule`

這不是單純用語偏差，而是會影響讀者對「template package 究竟能包含什麼」的理解。

### F3 — OPERATIONS 譯本結構大致一致

抽查的 `ja`、`de`、`es` `OPERATIONS.md` 在以下部分仍與英文主文件一致：

- delivery modes
- delivery resolution rules
- safety rules
- adoption flow
- operations state

雖然仍有部分英文術語保留，但目前未看到足以影響操作判讀的明顯語義漂移。

### F4 — 多語文件有明顯 mixed-language 痕跡

抽查樣本普遍保留大量英文術語與短語，例如：

- `starter template`
- `authoring workspace snapshot`
- `local-only`
- `reviewer-facing`
- `template release cleanup`

這不一定是錯誤，但對外觀感上仍有 machine-assisted translation 的痕跡，特別是在 `README.md` 與 `TEMPLATE_RELEASE_PACKAGE.md`。

## 4. Evidence Notes

### README

英文主文件已使用：

- support class / verification scope
- `verified / partial / target`
- `Copilot CLI`
- `Current Material Sets`

但抽查語言的譯本仍停留在：

- `Delivery Mode`
- `GitHub CLI`
- 舊版 bootstrap / path mapping 敘事

### TEMPLATE_RELEASE_PACKAGE

英文主文件已明確區分：

- 公開可再分發 skills
- local-only validation materials
- proprietary / restricted-license exclusions
- template package 與 authoring workspace 的邊界

抽查譯本只保留了較早期的 include / exclude 骨架，尚未同步完整 release-boundary 規則。

### OPERATIONS

雖有 mixed-language 現象，但目前核心操作語義仍與英文主文件對齊，暫無高風險偏差。

## 5. Recommended Disposition

建議目前將 i18n 狀態定義為：

- `README.md` translations: `stale / update needed`
- `TEMPLATE_RELEASE_PACKAGE.md` translations: `stale / update needed`
- `OPERATIONS.md` translations: `acceptable with terminology cleanup follow-up`

若要對外保守表述，建議使用：

> 非英文主文件已具備基本閱讀價值，但英文主文件仍是 2026-03-27 當前 release-boundary 與 support baseline 的 authoritative version。

## 6. ACT-11 Completion Status

ACT-11 的交付物是：

- `i18n 抽查報告`

因此，**ACT-11 可視為完成**。  
但「完成 spot check」不等於「翻譯已全面對齊」，後續仍應安排譯本更新波次。
