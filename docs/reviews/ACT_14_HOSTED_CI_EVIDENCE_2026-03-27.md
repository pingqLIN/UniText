---
description: Hosted CI evidence check for ACT-14, recording branch-level GitHub Actions proof and the remaining default-branch visibility gap
---

# ACT-14 Hosted CI Evidence

> 日期：2026-03-27  
> 用途：確認 `ACT-14 cross-platform confidence expansion` 是否已具備可引用的 GitHub-hosted evidence，並說明目前證據缺口的真實原因。

## 1. Verification Scope

本次檢查的問題不是 `.github/workflows/ci.yml` 是否已在本地建立，而是：

- branch / PR scope 是否已有可引用的 hosted run
- GitHub remote default branch 是否已可見 `ci.yml`
- `ubuntu-latest` / `macos-latest` 的 `portable-smoke` 是否已有實際綠燈證據

## 2. Fresh Verification

### 2.1 Local workflow definition exists

本地檔案 [../../.github/workflows/ci.yml](../../.github/workflows/ci.yml) 已存在，且內容包含：

- `baseline-windows`
- `portable-smoke`
  - `ubuntu-latest`
  - `macos-latest`

這表示 `ACT-14` 的 workflow 配置已在 local working tree 內完成。

### 2.2 Branch / PR hosted run evidence

於 `Q:\UniText` 執行：

```powershell
gh pr checks 1
gh run list --limit 10 --json databaseId,workflowName,headBranch,status,conclusion,url,createdAt,event
gh run view 23674160299 --json jobs,url,headBranch,event,status,conclusion
```

可確認目前 branch 已有至少兩組 `CI` 成功 run：

- PR run：`23674160299`
  - URL: <https://github.com/pingqLIN/UniText/actions/runs/23674160299>
  - event: `pull_request`
  - `baseline-windows`：`success`
  - `portable-smoke (ubuntu-latest)`：`success`
  - `portable-smoke (macos-latest)`：`success`
- branch push run：`23674159554`
  - URL: <https://github.com/pingqLIN/UniText/actions/runs/23674159554>
  - event: `push`
  - `baseline-windows`：`success`
  - `portable-smoke (ubuntu-latest)`：`success`
  - `portable-smoke (macos-latest)`：`success`

這表示 `ACT-14` 所需的 GitHub-hosted cross-platform smoke evidence，已經在目前 PR branch 上存在，而且 Linux / macOS smoke 也已有實際綠燈證據。

### 2.3 Remote workflow discovery

於 `Q:\UniText` 執行：

```powershell
gh workflow list
```

結果列出：

```text
CI                    active  252438352
Copilot coding agent  active  250802893
```

這表示 GitHub repository 層級現在已能辨識 `CI` workflow；也就是說，branch / PR 上的 run 已足以讓 workflow 被遠端服務端看見。

### 2.4 Remote workflow file lookup

於 `Q:\UniText` 執行：

```powershell
gh api -X GET repos/pingqLIN/UniText/contents/.github/workflows/ci.yml -f ref=main
```

結果：

```text
gh: Not Found (HTTP 404)
{"message":"Not Found","documentation_url":"https://docs.github.com/rest/repos/contents#get-repository-content","status":"404"}
```

這表示 remote repository 的 default branch `main` 目前**不存在** `.github/workflows/ci.yml`，即使 repo 層級已可看見 `CI` workflow，default branch source file 仍未承接。

### 2.5 Default-branch hosted run lookup

於 `Q:\UniText` 執行：

```powershell
gh run list --workflow ci.yml --limit 10
```

結果：

```text
HTTP 404: workflow ci.yml not found on the default branch (https://api.github.com/repos/pingqLIN/UniText/actions/workflows/ci.yml)
```

另外執行：

```powershell
gh run list --workflow CI --branch main --limit 5 --json databaseId,headBranch,status,conclusion,url,createdAt,event
```

結果為空陣列：

```json
[]
```

這表示 `main` 目前仍沒有可引用的 `CI` run；branch-level hosted evidence 已存在，但 default-branch visibility gap 仍未關閉。

### 2.6 Citation note

- 建議在 review 文檔中同時記錄 `run id` 與 `run URL`
- GitHub Actions logs 與細部 step output 受 retention policy 影響，長期引用時不應只依賴單一 log 畫面
- 目前對外較穩定的證據單位應以：
  - workflow/job 名稱
  - run id
  - run URL
  - 執行日期
  為主

## 3. Conclusion

截至 2026-03-28，`ACT-14` 的最準確狀態是：

- local workflow configured
- branch / PR hosted evidence available
- remaining gap = remote default branch still lacks `.github/workflows/ci.yml`

因此目前可保守主張：

> Cross-platform smoke is configured locally and already has GitHub-hosted green evidence on the current branch / PR; however, the remote default branch still lacks `ci.yml`, so default-branch visibility is still pending.

不宜主張：

- `main` 已具備同等 hosted evidence
- default branch 已完成 external-facing CI baseline publication

## 4. Why This Is Still Open

這個缺口目前已不再是 hosted run 不存在，而是證據只存在於目前 branch / PR scope，尚未延伸到 remote default branch。

在本 repository 的 `No-Publish Rule` 下，未經明確授權不得主動 publish default-branch content。因此：

- 我們可以在 branch 上建立並驗證 `.github/workflows/ci.yml`
- 但若沒有進一步讓 `main` 承接，default-branch evidence gap 仍會保留

也就是說，`ACT-14` 現在屬於：

- engineering baseline 已建立
- branch-level hosted proof 已建立
- remote default-branch publication 仍待完成

## 5. Follow-up Condition

若要正式關閉這條 evidence gap，需完成以下條件：

1. 將 `.github/workflows/ci.yml` 發布到 remote default branch
2. `main` 上實際跑出至少一組 `ubuntu-latest` / `macos-latest` 的 `portable-smoke` 成功紀錄
3. 將 default-branch run URL / run id / 時間戳補入 review evidence

在此之前，`OPEN_ITEMS` 中對 `ACT-14` 的說法應維持為：

- `branch-level hosted evidence available`
- `default-branch visibility still pending`
