[English](../../DOCUMENT_PLACEMENT_POLICY.md) | [繁體中文](DOCUMENT_PLACEMENT_POLICY.md) | [简体中文](../zh-CN/DOCUMENT_PLACEMENT_POLICY.md) | [日本語](../ja/DOCUMENT_PLACEMENT_POLICY.md) | [Deutsch](../de/DOCUMENT_PLACEMENT_POLICY.md) | [Français](../fr/DOCUMENT_PLACEMENT_POLICY.md) | [Español](../es/DOCUMENT_PLACEMENT_POLICY.md) | [한국어](../ko/DOCUMENT_PLACEMENT_POLICY.md) | [Italiano](../it/DOCUMENT_PLACEMENT_POLICY.md)

# UniText — 文件放置政策

> 狀態：Active Baseline
> 用途：定義治理、reference、authoring、operations 類文件應該放在哪一層，避免 shared 與 live workspace 內容錯層。

## 1. Purpose

UniText 同時是：

- authoring workspace
- shared registry baseline
- template / rebuild export source

因此文件若只看「主題像不像相關」，很容易放到錯層。

這份規則回答的是：

- 哪一類文件應該放 `registry/`
- 哪一類文件應該放 `local/`
- 哪一類文件應該放 `ops/`
- 哪些文件可以 tracked
- 哪些文件只能留在 ignored local authoring 空間

## 2. Core Rule

判斷文件放置位置時，優先看內容性質，而不是看主題領域。

- 如果文件描述的是 shared canonical truth，就放 shared layer
- 如果文件描述的是單一作者工作區目前狀態，就放 local layer
- 如果文件描述的是操作歷史、輸出結果、audit evidence 或 generated state，就放 operations layer

作者是在哪個「工作窗口」或哪台 authoring 機器裡編寫這份文件，不是主判準。

- 在 UniText authoring workspace 內編寫，不自動等於 `local/docs/authoring/`
- 被 tracked，也不自動等於「可公開」或「可 push」
- 先問文件要服務誰、要描述哪一層真相，再決定放置位置

## 3. Placement Matrix

| Content type | Canonical location | Tracked | Share-safe | Notes |
|---|---|---|---|---|
| 架構原則、治理規則、template-safe spec | root docs 或 `registry/` | Yes | Yes | 必須避免 live workspace values |
| shared sanitized reference | `registry/.../references/` | Yes | Yes | 可描述欄位結構，但值需 redacted 或 placeholder 化 |
| shared workflow / runbook / template | `registry/workflow/` | Yes | Yes | 不可綁定單一作者機器 |
| machine-local path map / wiring notes | `local/docs/` | Case-by-case | Usually no | 可記錄 location / state，不可記錄 plaintext secret |
| live workspace baseline | `local/docs/*_WORKSPACE_BASELINE.md` | No | No | 必須 ignore |
| live operational checklist | `local/docs/*_LIVE.md` | No | No | 必須 ignore |
| authoring plans / drafts / review notes | `local/docs/authoring/` | No | No | 必須 ignore |
| generated audit trail / export output / drift report | `ops/` | No | No | 屬於 state，不是 canonical source |

## 4. Naming Rules

若某個主題同時需要 shared 版與 live 版，預設使用成對命名：

- shared sanitized doc
  - `registry/.../references/<topic>.md`
- live workspace doc
  - `local/docs/<TOPIC>_WORKSPACE_BASELINE.md`
  - 或 `local/docs/<TOPIC>_LIVE.md`

## 5. Pair Rule

若 shared sanitized doc 與 live workspace doc 同時存在，應遵守：

1. shared 版只保留 template-safe 結構與 redacted placeholder
2. live 版只留在 `local/docs/` 或 `local/docs/authoring/`
3. shared 版應明示 live 版位置
4. live 版也應指出它對應的 shared sanitized reference

## 6. Publishing Rule

下列說法不可混為一談：

- template export passes
- rebuild export passes
- branch is publish-safe

template / rebuild 匯出安全，只代表匯出產物的邊界較乾淨，不代表 authoring repo 內目前所有 tracked content 都適合 push。

## 7. Quick Decisions

如果你不確定一份文件要放哪裡，先問這三題：

1. 這份文件是不是在描述單一作者工作區目前長什麼樣
   - 是：優先放 `local/docs/`
2. 這份文件是不是一個操作結果、audit 產物、匯出包、或 drift report
   - 是：優先放 `ops/`
3. 這份文件是不是希望未來 template / rebuild / shared registry 都能安全引用
   - 是：優先放 root docs、`registry/`、或 shared workflow layer

## 8. Decision Ladder

需要更穩定的判斷時，照這個順序：

1. 這是不是 generated state、audit evidence、drift report、或 export output
   - 是：放 `ops/`
2. 這是不是在描述單一 authoring workspace、單一機器、或目前 live wiring
   - 是：放 `local/docs/`
3. 如果它描述單一 workspace，它是不是 draft、review note、或 authoring workboard
   - 是：放 `local/docs/authoring/`
4. 這是不是給未來 shared readers 重複引用的 canonical truth，而且應該 template-safe
   - 是：放 tracked shared layer
5. 如果是 tracked shared layer，它更像哪一種
   - repo-wide policy / spec：放 root docs
   - sanitized reference：放 `registry/.../references/`
   - shared workflow / runbook：放 `registry/workflow/`
6. 如果 shared 與 live 兩種版本都需要存在
   - 建立 sanitized/live pair，不要把兩種邊界混在同一檔

若仍不確定，先用：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\get-document-placement-recommendation.ps1 -Topic "cloudflare workflow" -CanonicalSharedTruth -SharedForm registry-reference
```

## 9. Common Misplacements

- 把 live Cloudflare baseline 放到 `registry/.../references/`
- 把 strategy / review plan 放到 root
- 把 export output 或 audit evidence 當成 canonical reference
- 把 machine-specific path 直接寫進 shared governance docs

## 10. Review Gate

在新增任何 governance / reference 類文件前，至少先確認：

- 它是不是在描述 shared truth，而不是 live workspace state
- 它若被 push，是否仍符合 `NO_PUBLISH_POLICY.md` 與 template-safe 預期
- 它是否需要一個 sanitized/live pair，而不是單檔同時承載兩者

## 11. Related Docs

- `README.md`
- `INDEX.md`
- `OPERATIONS.md`
- `PROJECT_MODES.md`
- `SECRET_HANDLING_GUIDELINES.md`
- `NO_PUBLISH_POLICY.md`
