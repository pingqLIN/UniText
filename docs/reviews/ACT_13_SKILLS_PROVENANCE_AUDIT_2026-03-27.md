---
description: Provenance audit for active GitHub-backed skills, clarifying current evidence depth and the remaining gaps beyond repo-level licensing
---

# ACT-13 Skills Provenance Audit

> 日期：2026-03-27
> 用途：說明目前 active skills 的來源證據強度，並界定哪些部分仍停留在 repo-level 授權判讀。

## 1. Current Active Skill Sources

目前 active skills 共 `36` 個，來源分布如下：

| Source repo | Count |
|---|---:|
| `obra/superpowers` | 14 |
| `sickn33/antigravity-awesome-skills` | 9 |
| `github/awesome-copilot` | 5 |
| `affaan-m/everything-claude-code` | 4 |
| `nextlevelbuilder/ui-ux-pro-max-skill` | 4 |

## 2. What Current SOURCE.yaml Already Proves

目前每個 active skill 已有 `SOURCE.yaml`，可追溯到：

- 上游 repo
- 上游 URL
- 上游相對路徑
- 匯入日期
- 匯入方式
- 當前採用的 license 標記
- LICENSE / COPYING / COPYRIGHT 的 evidence path 與 scope（在可找到時）

這代表目前 provenance 已超過「只有 repo 名稱」的程度。

## 3. What Current SOURCE.yaml Still Does Not Fully Prove

目前 active skills 已補上：

- `source_revision`
- `license_evidence_path`
- `license_evidence_scope`
- `license_scope_note`
- `provenance_confidence`

而且目前這些欄位的現況已是：

- `source_revision = source clone HEAD commit`
- `license_evidence_path = detected LICENSE/COPYING/COPYRIGHT path when available`
- `license_evidence_scope = repository-root / skill-subtree / not-found`
- `license_scope_note = evidence path plus conservative scope note`
- `provenance_confidence` 仍保守分級，預設不把機械偵測誤寫成法律審查

目前 `license_evidence_scope` 的分布是：

- `repository-root`：25
- `skill-subtree`：11
- `not-found`：0

因此，第二輪外部審查對「目前多數證據仍偏 repo-level」的質疑，**已部分降級**；但 `revision-level pin` 與 `license evidence path` 這兩項已不再缺失。現在真正剩下的是 license 判讀深度與人工法務確認，而不是欄位本身沒有紀錄。

## 4. Current Best-Effort Interpretation

截至目前，較準確的說法是：

- active skills 已具有 `repo + path + source-revision + license evidence path + confidence` 層級的來源資料
- 能找到的 LICENSE / COPYING / COPYRIGHT 文件已記錄其相對路徑與 scope
- `skill-subtree` evidence 已能區分出來，不再只寫成模糊的 repo-level note
- 但 license 判讀仍主要是機械化 evidence capture，不等於完整法務結論
- `provenance_confidence` 仍應保守使用，不應因為找到了 path 就直接升格成已完全解決

## 5. Recommended Next Step

建議後續下一步改成：

- 將 `license_scope_note` / `provenance_confidence` 的對應規則固定成可重跑檢查，避免後續匯入把分級寫回較舊格式
- 對目前仍停留在 `repository-root` 的 skills，只有在取得更細的 subtree/path-level 或人工審視證據後才提高 `provenance_confidence`

欄位基準見 [SOURCE_SCHEMA.md](/Q:/UniText/registry/skills/SOURCE_SCHEMA.md)。

## 6. Current Conservative Wording

對外建議採用以下說法：

> Active public skills 已具有 GitHub-backed repo、path-level source metadata、pinned source revision 與可機械化捕捉的 license evidence path；但 license confidence 仍需保守看待，path/file-level evidence capture 不等於完整法務審查。
