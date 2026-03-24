# Local Overlay

이 디렉터리는 **로컬 deployment, scripts, path 대조, 그리고 기타 비핵심 overlay**를 담습니다.

설계 목적은 아주 단순합니다.

- 로컬 설정이 루트의 핵심 개념을 오염시키지 않게 한다
- 로컬 수정본을 집중적으로 관리할 수 있게 한다
- 필요하면 `local/` 전체를 바로 지우고 다시 만들 수 있게 한다

## Contents

- `docs/`
  - 로컬 deployment 관련 설명과 대조 문서
- `scripts/`
  - 로컬 실행용 scripts

## Current Files

- [docs/authoring](../../../local/docs/authoring)
  - 재편 이전에 남겨둔 authoring 강화판 핵심 문서
- [docs/MCP_DEPLOYMENT_NOTES.md](docs/MCP_DEPLOYMENT_NOTES.md)
  - 현재 로컬 MCP deployment와 연결 방식 설명
- [docs/PATH_MAP.md](docs/PATH_MAP.md)
  - 현재 deployment의 path 참조와 역사적 대조
- [docs/WORKFLOW_DEPLOYMENT_NOTES.md](docs/WORKFLOW_DEPLOYMENT_NOTES.md)
  - 현재 로컬 workflow 연결 설명
- [scripts/sync-skills.ps1](../../../local/scripts/sync-skills.ps1)
  - 로컬 동기화 script

## Rule

어떤 내용이 다음 중 무엇을 설명하는지로 판단합니다.

- 이 system이 어떻게 동작해야 하는가
  - 그것은 `local/`에 두면 안 된다
- 이 instance가 지금 어떻게 구성되어 있는가
  - 그것은 `local/`에 두어야 한다
