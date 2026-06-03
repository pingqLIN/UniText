---
name: terminal-layout-three-pane
description: Arrange the current Windows desktop into a three-pane layout based on the terminal's working directory. Use when the user asks for 1/4 File Explorer on the left, 1/2 code editor in the center, and 1/4 terminal on the right, with Explorer opened to the terminal folder.
metadata:
  runtime_support_files: true
---

# Terminal Layout Three Pane

Run the script in this skill to open File Explorer at the terminal folder, ensure a code editor window is available, and tile windows as 1/4 + 1/2 + 1/4 split.

## Workflow

1. Determine target folder.
Use the current terminal directory by default: `-TargetPath (Get-Location).Path`.
2. Run the three-pane script.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\terminal-layout-three-pane\scripts\apply-three-pane-layout.ps1"
```

If you need to force a specific monitor, pass `-MonitorIndex` (0-based):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\terminal-layout-three-pane\scripts\apply-three-pane-layout.ps1" -MonitorIndex 1
```

3. Verify final arrangement.
Explorer fills the left quarter, editor fills the center half, and terminal fills the right quarter of the current monitor work area.

## Script

Use [scripts/apply-three-pane-layout.ps1](scripts/apply-three-pane-layout.ps1) for the actual automation.
