---
description: Documentation-scale baseline for UniText, separating canonical docs from review archive, i18n, ops artifacts, and workspace residue
---

# ACT-12 Documentation Scale Baseline

> 日期：2026-03-27
> 用途：建立文件規模基線，避免把 `.md` 總量直接誤讀成 canonical documentation 規模。

## 1. Measured Counts

本次量測結果：

- repository-wide `.md` files: `6762`
- `ops/` files: `11557`
- active skills: `36`

但 `.md` 的主要分布不是單一來源：

| Area | Count |
|---|---:|
| `.tmp/` | 5128 |
| `ops/` | 1082 |
| `i18n/` | 169 |
| `registry/` | 135 |
| `.bak_20260315_00/` | 98 |
| `recovered_20260318_165117/` | 97 |
| root | 23 |
| `docs/reviews/` | 15 |
| `template/` | 9 |
| `local/` | 6 |

## 2. Key Interpretation

第二輪外部審查正確指出 `.md` 總量大幅增加，但「主要由 i18n 膨脹造成」這個歸因並不成立。

目前較準確的判讀是：

- canonical root docs 並不大
- review archive 也不是主因
- i18n 的確增加文件量，但不是最大來源
- 最大來源其實是 workspace residue：
  - `.tmp/`
  - `ops/`
  - 歷史 `.bak_*`
  - `recovered_*`

## 3. Governance Rule

未來討論文件規模時，至少應區分：

1. `canonical docs`
   - root docs
   - `local/docs`
   - `template/`
2. `review archive`
   - `docs/reviews`
3. `i18n translations`
   - `i18n/`
4. `workspace residue`
   - `.tmp/`
   - `ops/`
   - `.bak_*`
   - `recovered_*`

若不先分層，只用一個總數字，會把 release-facing 問題與 maintainer workspace 狀態混為一談。

## 4. Recommended Follow-up

- 在 README 與 docs archive 中持續強調 authoritative document boundaries
- 將 stale translations 的狀態顯式化
- 對 `.tmp/`、`ops/`、`.bak_*`、`recovered_*` 維持 workspace-only 解讀，不得當作 release surface 規模
- 將規模盤點 routine 化，避免後續 review 只引用一次性的手工數字

## 5. Current Progress Update

截至 2026-03-27 晚間：

- 已新增 [../../local/scripts/report-docs-scale.ps1](../../local/scripts/report-docs-scale.ps1)
- 已新增 [../../local/docs/DOCS_GOVERNANCE_RULES.md](../../local/docs/DOCS_GOVERNANCE_RULES.md)

這代表 `ACT-12` 已從「只有 baseline」往前推到「有可重跑的 reporting routine」，但長期自動化監測仍屬 follow-up。
