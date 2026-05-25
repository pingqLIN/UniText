# Skill Runtime / Codex 重複曝光 SOP

> 對象：維護 UniText `registry/`、`runtime/` 與本機 Codex skills bundle 的操作者。

## 目的

當同一個 skill 同時出現在 `Q:\UniText\runtime\skills\<skill-id>` 與 `C:\Users\miles\.codex\skills\<skill-id>`，或使用者回報系統同時看見 UniText runtime skill 與 Codex-local 同名 skill 時，使用本 SOP。

目標是保留單一治理 source of truth，同時允許多個 runtime delivery surface。

## Source Order

正式修改固定使用以下順序：

```text
registry source -> runtime projection -> Codex local bundle
```

- `Q:\UniText\registry\skills\<skill-id>` 是 canonical governed source。
- `Q:\UniText\runtime\skills\<skill-id>` 是 consumer-facing runtime projection。
- `C:\Users\miles\.codex\skills\<skill-id>` 是 machine-local Codex bundle 或 local install。

除非使用者明確要求臨時本機實驗，否則不要把 runtime projection 或 Codex-local copy 當成 canonical source。

## Detection

列出兩個 active delivery surface 之間的同名 skill：

```powershell
$roots = @(
  'Q:\UniText\runtime\skills',
  'C:\Users\miles\.codex\skills'
)
Get-ChildItem $roots -Directory |
  Group-Object Name |
  Where-Object Count -gt 1 |
  Select-Object Name, Count
```

檢查這個重複是否符合預期：

```powershell
Get-FileHash -Algorithm SHA256 `
  'Q:\UniText\registry\skills\<skill-id>\SKILL.md', `
  'Q:\UniText\runtime\skills\<skill-id>\SKILL.md', `
  'C:\Users\miles\.codex\skills\<skill-id>\SKILL.md'
```

runtime projection 可能 hash 不同，因為它會加入 `runtime_projection`、`source_of_truth` 等投影 metadata。

## Classification

| 分類 | 意義 | 動作 |
| --- | --- | --- |
| `same-content` | Codex-local copy 與 registry source 相同。 | 視為正常 delivery duplicate。 |
| `runtime-wrapper-only` | runtime 只因生成的 projection metadata 不同。 | 視為正常。 |
| `content-drift` | runtime 或 Codex-local 主體內容與 registry source 不同。 | 將預期修改回寫到 `registry/`，再重建或投影，必要時同步 Codex。 |
| `wrong-root-exposure` | runtime context 把兩個 root 當同等來源載入，或直接指向 `registry/skills`。 | 先修 config 或 bootstrap wiring，不要先改 skill 內容。 |

## Repair Path

1. 確認 UniText worktree 狀態：

```powershell
git -C Q:\UniText status --short --branch
```

2. 若預期修改只存在於 `runtime/` 或 `C:\Users\miles\.codex\skills`，先回寫到：

```text
Q:\UniText\registry\skills\<skill-id>
```

3. 驗證 registry skill：

```powershell
python Q:\UniText\registry\skills\skill-creator\scripts\quick_validate.py Q:\UniText\registry\skills\<skill-id>
```

4. 寫入前先 dry-run runtime rebuild：

```powershell
python Q:\UniText\local\scripts\build-runtime-layer.py --output-dir Q:\UniText\.tmp\runtime-dryrun
```

5. 若 dry-run 只顯示預期 drift，才重建 tracked runtime：

```powershell
python Q:\UniText\local\scripts\build-runtime-layer.py --write
python Q:\UniText\local\scripts\verify-bootstrap.py --skip-codex
```

6. 若需要更新 Codex local bundle，先 preview host wiring：

```powershell
python Q:\UniText\local\scripts\bootstrap.py --dry-run
```

只有在任務明確包含 host target 變更時，才執行 `bootstrap.py --force`。

## Escalation

遇到以下情況先停止並回報：

- `build-runtime-layer.py` dry-run 顯示大範圍 unrelated payload drift。
- `git status --short --branch` 顯示你要修改的相同路徑已有 unrelated dirty files。
- Codex `skills_path` 指向 `registry/skills`。
- 同一個 skill id 在 runtime 與 Codex-local copy 中有不同預期行為。

此時應保留證據，再決定是否用新 branch、worktree 或獨立本機實驗隔離處理。
