# Independent Validation Runbook

> 狀態：Working Draft
> 最後更新：2026-03-27
> 用途：提供非作者 operator 進行最小獨立驗證的步驟，降低 self-validation 的閉合風險。

## Scope

本 runbook 的目標不是完整產品評估，而是回答：

- 非作者是否能在自己的環境中完成最小 bootstrap
- review / template package 是否可重複匯出與驗證
- 是否需要額外人工補救

## Suggested Validation Path

1. 取得 repo 或匯出的 starter / review package
2. 安裝 Python 3.11
3. 安裝 core dependencies

```bash
python -m pip install -r requirements.txt
```

4. 執行 bootstrap dry-run

```bash
python local/scripts/bootstrap.py --dry-run
```

5. 執行 bootstrap

```bash
python local/scripts/bootstrap.py --force
python local/scripts/verify-bootstrap.py
```

6. 執行 review package dry-run

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-review-package.ps1 -DryRun
```

7. 執行 template package export / verify

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-template-package.ps1 -Name independent-smoke
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-template-package.ps1 -Path .\ops\template-package\independent-smoke
```

## What To Record

至少記錄：

- operator role
- date
- OS / shell / Python version
- 是否需要手動調整 PATH / execution policy
- bootstrap 是否成功
- verify 是否成功
- export / verify 是否成功
- 任何需要人工補救的步驟

## Suggested Output Template

| Field | Value |
|---|---|
| operator | |
| date | |
| platform | |
| python | |
| bootstrap dry-run | pass / fail |
| bootstrap force | pass / fail |
| verify-bootstrap | pass / fail |
| review export dry-run | pass / fail |
| template export | pass / fail |
| template verify | pass / fail |
| manual interventions | |
| notes | |

也可直接使用：

- [INDEPENDENT_VALIDATION_REPORT_TEMPLATE.md](INDEPENDENT_VALIDATION_REPORT_TEMPLATE.md)

## Current Limitation

截至 2026-03-27，這份 runbook 已建立，但尚未附上實際的非作者驗證報告。  
因此目前狀態是：**runbook ready, independent evidence pending**.
