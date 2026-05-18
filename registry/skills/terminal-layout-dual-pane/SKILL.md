---
name: terminal-layout-dual-pane
description: Arrange the current Windows desktop into a dual-pane layout based on the terminal's working directory. Use when the user asks to place File Explorer on the left half and the active terminal on the right half, both full-height, with Explorer opened to the same folder as the terminal.
---

# Terminal Layout Dual Pane

Run the script in this skill to open File Explorer at the terminal folder and tile windows as 50/50 split.

## Workflow

1. Determine the target folder.
Use the current terminal directory by default: `-TargetPath (Get-Location).Path`.
2. Run the dual-pane script.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\ADMIN_miles\.codex\skills\terminal-layout-dual-pane\scripts\apply-dual-pane-layout.ps1"
```

3. Verify final arrangement.
The Explorer window fills the left half of the current monitor work area, and terminal fills the right half.

## Script

Use [scripts/apply-dual-pane-layout.ps1](C:\Users\ADMIN_miles\.codex\skills\terminal-layout-dual-pane\scripts\apply-dual-pane-layout.ps1) for the actual automation.
