# Support Proof Matrix

> 狀態：Working Draft
> 最後更新：2026-03-27
> 用途：將 README / CLI matrix 中的 support claim 連到具體 proof artifact，避免只靠敘事宣稱支持範圍。

## CLI Proofs

| Surface | Current claim | Proof type | Current artifact |
|---|---|---|---|
| Claude Code | `verified` / `delivery path verified` | delivered skill path + project-local MCP seed | `tests/test_portable_proofs.py::test_bootstrap_force_delivers_public_skills_in_isolated_home` |
| Gemini CLI | `verified` / `delivery path verified` | delivered skill path | `tests/test_portable_proofs.py::test_bootstrap_force_delivers_public_skills_in_isolated_home` |
| Codex CLI | `partial` / `bootstrap path defined` | `skills_path` write + MCP config block write | `tests/test_portable_proofs.py::test_bootstrap_force_delivers_public_skills_in_isolated_home` |
| MCP baseline | bundled read-only seed available | tool contract proof | `tests/test_portable_proofs.py::test_mcp_seed_registry_summary_tool_returns_counts` |
| MCP file access | core docs and registry files readable | tool contract proof | `tests/test_portable_proofs.py::test_mcp_seed_can_read_core_docs_and_registry_files` |

## Platform Proofs

| Platform | Current claim | Proof type | Current artifact |
|---|---|---|---|
| Windows | `verified` / `authoring + export baseline verified` | full repo baseline | `.github/workflows/ci.yml` job `baseline-windows` |
| macOS | `target` | configured Python portable smoke | `.github/workflows/ci.yml` job `portable-smoke` on `macos-latest` |
| Linux | `target` | configured Python portable smoke | `.github/workflows/ci.yml` job `portable-smoke` on `ubuntu-latest` |

## Interpretation Rules

- 這份矩陣記錄的是 proof artifact 是否存在，不自動等於 hosted CI 已在所有平台成功跑過。
- 若 proof 只證明 path / config / process-start，則不得對外寫成 full end-to-end task verification。
- `verified`、`partial`、`target` 的正式定義仍以 `README.md` 與 `local/docs/CLI_COMPAT_MATRIX.md` 為準。
- 若未來新增新的 support claim，應同步新增對應 proof artifact；否則不應升級 support class。
