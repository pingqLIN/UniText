# Documentation Governance Rules

> 狀態：Active Guidance  
> 用途：定義文件規模解讀、authoritative boundary 與 stale translation 的最低治理規則。

## 1. Purpose

UniText 的 `.md` 數量容易被 maintainer workspace residue 放大，因此不能直接把 repository-wide markdown total 視為 release-facing documentation 規模。

本文件定義最低治理口徑，讓後續 audit、review 與 status report 使用一致分類。

## 2. Required Document Buckets

討論文件規模時，至少要區分以下區塊：

1. `canonical docs`
   - root docs
   - `local/docs/`
   - `template/`
2. `review archive`
   - `docs/reviews/`
3. `i18n translations`
   - `i18n/`
4. `workspace residue`
   - `.tmp/`
   - `ops/`
   - `.bak_*`
   - `recovered_*`

若未先分層，不得直接使用單一 markdown 總數作為 release-facing 結論。

## 3. Authoritative Language Rule

- 英文主文件是 authoritative version
- 非英文譯本若尚未同步 current release-boundary / support-baseline，必須顯式標示為 stale、update-needed，或加上 current-baseline note

## 4. Review Reporting Rule

若 audit 或 review 引用文件規模，至少應提供：

- repository-wide markdown count
- top-level area distribution
- canonical docs count
- review archive count
- i18n count

建議使用：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\report-docs-scale.ps1
```

若需機器可讀輸出：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\report-docs-scale.ps1 -AsJson
```

## 5. Current Interpretation

截至 2026-03-27：

- documentation scale baseline 已建立
- reporting routine 已存在
- 長期自動化監測仍屬 follow-up

因此目前可主張：

> documentation scale is measured and classifiable, but long-term automated governance is still maturing.
