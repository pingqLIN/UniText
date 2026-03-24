# AI CLI Path Map

> 상태: Current Authoring Reference
> 주의: 이 문서는 이 repo의 현재 실제 deployment mapping을 기록해 검증과 리뷰를 돕습니다. 규격의 진실은 여전히 `registry/`와 `local/scripts/`의 상대 경로 논리를 따릅니다.

## Canonical Sources

- Skills: `Q:\UniText\registry\skills`
- MCP: `Q:\UniText\registry\mcp`
- Agents: `Q:\UniText\registry\agents`
- Workflow: `Q:\UniText\registry\workflow`

## Runtime Targets

### Claude Code

- Skills: `%USERPROFILE%\.claude\skills`
- Project MCP: `<repo>\.mcp.json`
- Notes:
  - skills target은 `registry\skills`를 가리켜야 한다
  - project-level MCP는 `local/scripts/bootstrap.py`가 생성한다

### Gemini CLI

- Skills: `%USERPROFILE%\.gemini\skills`
- Secondary skills mirror: `%USERPROFILE%\.agents\skills`
- MCP setting location: `%USERPROFILE%\.gemini\settings.json`의 `mcpServers`

### Codex

- Config file: `%USERPROFILE%\.codex\config.toml`
- Skills setting: `skills_path = "Q:\\UniText\\registry\\skills"`
- MCP setting location: `[mcp_servers.unitext_registry]`
- Notes:
  - skills와 MCP wiring은 둘 다 `local/scripts/bootstrap.py`가 쓴다
  - 예전 `C:\Dev\UniText\skills` path는 더 이상 쓰지 않는다

### Workflow Notes

- Claude workflow source: `registry\workflow\claude-plans`
- Gemini workflow temp state: CLI internal state
- Codex: standalone workflow directory setting 없음

## Verification

- repo baseline: `local/scripts/health-check.ps1`
- delivery paths: `local/scripts/verify-delivery.ps1`
- first-run bootstrap: `local/scripts/verify-bootstrap.py`
