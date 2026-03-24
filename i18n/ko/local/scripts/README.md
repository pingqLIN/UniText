# Local Scripts

여기에는 **로컬 작업용 scripts**를 둡니다.

- `*.ps1`은 Windows-first reference implementation으로 유지합니다
- `*.py`는 cross-platform bootstrap / verify / backup path를 제공합니다

## Current Scripts

- `bootstrap.py`
  - cross-platform으로 skills delivery, Codex native-config, project `.mcp.json`을 초기화합니다
- `verify-bootstrap.py`
  - first-run 결과가 현재 repo와 맞는지 cross-platform으로 확인합니다
- `create-git-bundle.py`
  - 휴대 가능한 `git bundle` backup을 만들어 로컬 workspace 하나에만 의존하는 single point of failure를 줄입니다
- `sync-skills.ps1`
  - `registry/skills/`를 로컬 skills target에 동기화합니다
- `scan-skills.ps1`
  - candidate skills를 스캔하고 adoption 체크 결과를 출력합니다
- `verify-delivery.ps1`
  - source와 일반적인 skills target이 존재하는지, link인지, 해결 가능한지 검증합니다
- `health-check.ps1`
  - registry와 scripts에 대해 최소 health check를 수행합니다
- `batch-adopt-skills.ps1`
  - candidate skills를 일괄로 `registry/skills/`로 옮깁니다
- `generate-index-entries.ps1`
  - `registry/skills/`에서 INDEX용 catalog 구역을 생성합니다
- `rollback-skills.ps1`
  - `ops/history/adopt_*`의 backup에서 지정한 skill을 복구합니다
- `export-review-package.ps1`
  - 외부 리뷰에 필요한 cover note, highlights, 핵심 문서, 선택된 registry entries, 최소 scripts를 `ops/review-package/`로 내보냅니다
- `export-template-package.ps1`
  - template-safe docs, generic examples, starter layout을 `ops/template-package/`로 내보냅니다
- `verify-template-package.ps1`
  - 출력된 template package가 필요한 starter structure를 포함하고 review-only / local-only 내용을 포함하지 않는지 검증합니다

## Governance Note

- `sync-skills.ps1`와 `batch-adopt-skills.ps1`는 다음을 따라야 합니다.
  - dry-run first
  - backup before mutation
  - 추적 가능한 log 생성

## Platform Note

- 새 first-run path에서는 `bootstrap.py`와 `verify-bootstrap.py`를 우선 사용합니다.
- `sync-skills.ps1`는 Windows PowerShell reference implementation이자 governance sample로 유지합니다.
