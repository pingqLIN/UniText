---
description: Hosted CI evidence check for ACT-14, confirming current remote workflow visibility and why Linux/macOS hosted proof is still pending
---

# ACT-14 Hosted CI Evidence

> 日期：2026-03-27  
> 用途：確認 `ACT-14 cross-platform confidence expansion` 是否已具備可引用的 GitHub-hosted evidence，並說明目前證據缺口的真實原因。

## 1. Verification Scope

本次檢查的問題不是 `.github/workflows/ci.yml` 是否已在本地建立，而是：

- GitHub remote default branch 是否已可見 `ci.yml`
- GitHub Actions 是否已有可引用的 hosted run
- `ubuntu-latest` / `macos-latest` 的 `portable-smoke` 是否已有實際綠燈證據

## 2. Fresh Verification

### 2.1 Local workflow definition exists

本地檔案 [../../.github/workflows/ci.yml](../../.github/workflows/ci.yml) 已存在，且內容包含：

- `baseline-windows`
- `portable-smoke`
  - `ubuntu-latest`
  - `macos-latest`

這表示 `ACT-14` 的 workflow 配置已在 local working tree 內完成。

### 2.2 Remote workflow discovery

於 `Q:\UniText` 執行：

```powershell
gh workflow list
```

結果僅列出：

```text
Copilot coding agent  active  250802893
```

未出現 `CI` 或 `ci.yml`。

### 2.3 Remote workflow file lookup

於 `Q:\UniText` 執行：

```powershell
gh api repos/pingqLIN/UniText/contents/.github/workflows/ci.yml
```

結果：

```text
gh: Not Found (HTTP 404)
{"message":"Not Found","documentation_url":"https://docs.github.com/rest/repos/contents#get-repository-content","status":"404"}
```

這表示 remote repository 的 default branch 目前**不存在** `.github/workflows/ci.yml`。

### 2.4 Hosted run lookup

於 `Q:\UniText` 執行：

```powershell
gh run list --workflow ci.yml --limit 10
```

結果：

```text
HTTP 404: workflow ci.yml not found on the default branch (https://api.github.com/repos/pingqLIN/UniText/actions/workflows/ci.yml)
```

這表示目前不是「workflow 存在但尚未跑出成功 run」，而是更前面的條件尚未成立：remote default branch 還沒有這個 workflow。

## 3. Conclusion

截至 2026-03-27，`ACT-14` 的最準確狀態是：

- local workflow configured
- hosted evidence not yet available
- immediate blocker = remote default branch lacks `.github/workflows/ci.yml`

因此目前可保守主張：

> cross-platform smoke configured locally; GitHub-hosted Linux/macOS evidence remains pending because the CI workflow is not yet present on the remote default branch.

不宜主張：

- 已完成 GitHub-hosted cross-platform validation
- 已有 Linux / macOS hosted green evidence

## 4. Why This Is Still Open

這個缺口目前不是本地測試未通過，而是 remote visibility 問題。

在本 repository 的 `No-Publish Rule` 下，未經明確授權不得主動 push / publish。因此：

- 我們可以在本地建立 `.github/workflows/ci.yml`
- 但在未獲得發布許可前，不能自行把 workflow 推到 remote 以換取 hosted evidence

也就是說，`ACT-14` 現在屬於：

- engineering baseline 已建立
- hosted proof pending
- remote publication required before evidence can exist

## 5. Follow-up Condition

若要正式關閉這條 evidence gap，需完成以下條件：

1. 使用者明確授權將 `.github/workflows/ci.yml` 發布到 remote
2. GitHub Actions 實際跑出至少一組 `ubuntu-latest` / `macos-latest` 的 `portable-smoke` 成功紀錄
3. 將 run URL / run id / 時間戳補入 review evidence

在此之前，`OPEN_ITEMS` 中對 `ACT-14` 的說法應維持為：

- `configured locally`
- `hosted evidence blocked by remote workflow absence`
