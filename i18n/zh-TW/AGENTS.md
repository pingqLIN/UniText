# AGENTS.md

## 不可發布規則

除非使用者明確授權，本 repository 可能包含應維持私有的材料。

在此 repository 中運作的 agents 必須遵守以下規則：

1. 除非使用者明確要求 push，否則不得將 commits push 到任何 remote。
2. 除非使用者明確要求 upload，否則不得將 repository 內容上傳到 GitHub、社群平台、雲端文件、paste site 或任何其他網路服務。
3. 下列內容預設視為特別敏感：
   - social post drafts
   - project comparison notes
   - cross-project collaboration discussions
   - review notes
   - strategic planning documents
4. 如果使用者要求 publishing、push、upload 或 posting，只能發布使用者明確核准的特定內容。
5. 如有疑慮，保留在本機並在發布前詢問。

## 適用範圍說明

即使符合下列情況，本規則仍然適用：

- remote 已存在
- repository 是 private
- 內容看起來已可發布

Private repository 不等於自動取得發布授權。

## Git Startup

新的 development session 在此 repository 中開始時，優先使用：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\git-startup.ps1
```

此 helper 會先從 `origin/HEAD` 解析 canonical base branch，只有必要時才 fallback 到本機 `main` 或 `master`。它也會要求工作樹乾淨、執行 `origin --prune` fetch、明確 fast-forward 到解析出的 base branch，並拒絕重複使用既有 feature branch 名稱。
