# Skill Source Schema

> 狀態：Working Draft
> 最後更新：2026-03-27
> 用途：定義 `registry/skills/*/SOURCE.yaml` 的最小欄位與建議擴充欄位，補強 provenance 可追溯性。

## Required Fields

| Field | Purpose |
|---|---|
| `registry_name` | UniText 內的 skill id |
| `source_type` | 來源型別，例如 `github-import` |
| `source_repo` | 上游 repo |
| `source_url` | 上游 URL |
| `source_path` | 上游相對路徑 |
| `source_license` | 目前採用的授權標記 |
| `imported_at` | 匯入日期 |
| `import_method` | 匯入方式，例如 `curated-copy` |
| `notes` | 補充說明 |

## Current Public Baseline Fields

對目前 active public skills，除上述欄位外，應再補上：

| Field | Purpose |
|---|---|
| `source_revision` | 上游 commit / tag / snapshot 識別 |
| `license_evidence_path` | 在本地 source clone 中實際找到的 LICENSE / COPYING / COPYRIGHT 相對路徑 |
| `license_evidence_scope` | 該授權證據屬於 `repository-root`、`skill-subtree`、或 `not-found` |
| `license_scope_note` | 說明授權判讀是 repo-level、path-level 或其他依據 |
| `provenance_confidence` | 例如 `repo-license-relied-upon`、`path-level-evidence-stronger` |

## Extended Review Fields

| Field | Purpose |
|---|---|
| `import_reviewed_by` | 記錄匯入審視者 |
| `import_review_note` | 匯入時的例外與限制 |

## Current Interpretation

截至 2026-03-27，現有 `SOURCE.yaml` 已足以提供：

- upstream repo
- upstream path
- 匯入日期
- license 標記
- license 證據路徑與 scope（在可找到時）

但仍不足以完整回答：

- 具體匯入自哪一個 revision
- 具體 LICENSE / COPYING / COPYRIGHT 文件位於哪個路徑、屬於哪個 scope
- 授權判讀依據是 repo-level 還是 path-level
- 該 provenance 的信心等級為何

截至目前，active public skills 應至少具備：

- `source_revision`
- `license_evidence_path`
- `license_evidence_scope`
- `license_scope_note`
- `provenance_confidence`

這些欄位不保證授權問題完全解決，但可以明確區分：

- 是否已記錄上游快照
- 授權判讀依據停留在哪個層級
- provenance 信心目前有多強

## Confidence Guidance

- `repo-license-relied-upon`
  - 適用於 `license_evidence_scope = repository-root`，代表已記錄 repo 與 path，但授權證據仍主要停留在 repo 根層級
- `path-level-evidence-stronger`
  - 適用於 `license_evidence_scope = skill-subtree`，代表在 skill 子樹內已有更接近匯入內容的授權證據
- 不應僅因為找到了任一 LICENSE 路徑就一律升級為較強 confidence；confidence 應反映 scope，而不只是檔案存在與否
