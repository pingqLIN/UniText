# CLI Compatibility Matrix

> 상태: Working Draft
> 마지막 업데이트: 2026-03-23

| CLI | 버전 기준 | UniText 의존 동작 | 현재 상태 | 마지막 검증 |
|---|---|---|---|---|
| Claude Code | 2.1.63 | `~/.claude/skills`를 읽고 project `.mcp.json`을 지원한다 | delivery path verified | 2026-03-24 |
| Codex CLI | 0.106.0 | `config.toml`의 `skills_path`에서 skills를 읽고 `[mcp_servers.unitext_registry]`를 등록할 수 있다 | bootstrap verified | 2026-03-24 |
| Gemini CLI | 0.31.0 | `~/.gemini/skills`와 `~/.agents/skills`를 읽는다 | delivery path verified | 2026-03-24 |
| GitHub CLI | 2.87.3 | workflow는 참고용이며 native skills를 지원하지 않는다 | 알려진 제한 | 2026-03-02 |
| VS Code | 1.109.5 | 직접적인 resource consumer는 아니며 주로 authoring environment로 사용된다 | 알려진 제한 | 2026-03-02 |
| Windsurf | 1.108.2 | 직접적인 resource consumer는 아니며 주로 authoring environment로 사용된다 | 알려진 제한 | 2026-03-02 |

## Notes

- 이 matrix는 UniText가 현재 의존하는 CLI 동작을 기록하는 것이며, 각 CLI의 전체 기능을 나열하는 것이 아닙니다.
- major version이 바뀔 때마다 skills와 mcp delivery를 최소 1회는 다시 검증해야 합니다.
- `delivery path verified`는 `verify-delivery.ps1`로 canonical skills path 정합성을 확인했다는 뜻이며, end-to-end 상호작용 검증이 완료되었다는 뜻은 아닙니다.
