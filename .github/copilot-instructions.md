# UniText Copilot Instructions

UniText is registry-first. Treat `registry/` as the canonical source of truth and `INDEX.md` as the curated discovery surface only.

When working in this repository:

- Read `README.md`, `INDEX.md`, `COPILOT_CLI_ADAPTER_NOTE.md`, and `registry/catalog-exclusions.json` before making changes.
- Keep `registry/` authoritative. Do not invent alternate catalog or MCP sources.
- Respect `registry/catalog-exclusions.json`; stray items are not official catalog entries.
- Use `local/scripts/bootstrap.py --force` and `local/scripts/verify-bootstrap.py` as the authoritative first-run setup and verification path.
- Use `local/scripts/verify-copilot-session.py --use-project-mcp` when you need repeatable non-interactive Copilot runtime evidence.
- The shared read-only registry MCP server lives at `registry/mcp/claude-project-mcp-seed/server.py`.
- The tracked `.mcp.json` is a template-safe seed. If you need to attach the project MCP baseline in a Copilot session, launch from the repo root with `copilot --additional-mcp-config @.mcp.json`.
- Do not rewrite the seed into machine-specific absolute paths inside the repo.
- Avoid touching unrelated files and do not revert user changes.
- Prefer minimal, evidence-backed edits and add or update tests when the change affects repository behavior.
