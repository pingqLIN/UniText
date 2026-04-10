# Local Scripts

여기에는 **로컬 운영 스크립트** 가 들어갑니다.

- `*.ps1` 는 Windows-first 참조 구현으로 유지합니다
- `*.py` 는 `bootstrap` / `verify` / `backup` 을 위한 cross-platform 경로를 제공합니다

## Current Scripts

- `bootstrap.py`
  - skills delivery, Codex native-config, Copilot MCP config, project `.mcp.json` 을 cross-platform 으로 초기화합니다
- `verify-bootstrap.py`
  - first-run 결과가 현재 repo 와 일치하는지 cross-platform 으로 검증하고, template-safe `.mcp.json` seed 와 이미 bootstrapped 된 로컬 wiring 둘 다 허용합니다
- `create-git-bundle.py`
  - 휴대 가능한 `git bundle` backup 을 만들어 로컬 worktree 에만 의존하는 single-point-of-failure 위험을 낮춥니다
- `git-startup.ps1`
  - 새 session 에 대해 canonical base branch 를 해석하고, 깨끗한 worktree 를 요구하며, 명시적인 fast-forward 업데이트를 수행하고, 새 feature branch 를 만듭니다
- `sync-skills.ps1`
  - `registry/skills/` 를 로컬 skills targets 로 동기화합니다
- `scan-skills.ps1`
  - 후보 skills 를 스캔하고 adoption 점검 결과를 출력합니다
- `verify-delivery.ps1`
  - source 와 일반적인 skills targets 가 존재하는지, 링크인지, 해석 가능한지 검증합니다
- `health-check.ps1`
  - registry 와 scripts 에 대한 최소 health check 를 수행합니다
- `batch-adopt-skills.ps1`
  - 후보 skills 를 일괄로 `registry/skills/` 로 옮깁니다
- `generate-index-entries.ps1`
  - `registry/skills/` 로부터 INDEX 에 필요한 catalog 블록을 생성합니다
- `rollback-skills.ps1`
  - `ops/history/adopt_*` backup 으로부터 지정한 skill 을 복구합니다
- `export-review-package.ps1`
  - 외부 review 에 필요한 cover note, highlights, 핵심 문서, 선별된 registry entries, 최소 scripts 를 `ops/review-package/` 로 export 합니다
- `export-template-package.ps1`
  - template-safe docs, generic examples, starter layout 을 `ops/template-package/` 로 export 합니다
- `verify-template-package.ps1`
  - export 된 template package 에 필요한 starter 구조가 있는지, review-only / local-only 내용이 섞이지 않았는지 검증합니다
- `verify-workspace-boundaries.ps1`
  - 현재 authoring repo 의 tracked shared surfaces 에 live workspace metadata, authoring-only docs, operations state 가 섞이지 않았는지 검증합니다
- `get-publishability-report.ps1`
  - 현재 branch 의 local-only / ops / shared-surface 변경과 boundary verify 결과를 모아 push suitability 를 위한 로컬 보고서를 만듭니다
- `lib/workspace-sensitive-metadata.ps1`
  - shared `WORKSPACE_SENSITIVE_METADATA_RULES.json` 을 불러와 boundary / template / publishability 검증이 같은 규칙 세트를 쓰도록 합니다
- `validate-workspace-sensitive-metadata-rules.ps1`
  - shared `WORKSPACE_SENSITIVE_METADATA_RULES.json` 의 구조, regex 컴파일 가능 여부, 내장 사례 통과 여부를 검증합니다
- `preview-renormalize.ps1`
  - dry-run 만 수행하여 `git add --renormalize .` 가 몇 개의 tracked files 를 건드릴지 미리 보여 주므로, line-ending cleanup 의 blast radius 를 먼저 확인할 수 있습니다
- `run-renormalize.ps1`
  - `repo / root / registry / i18n / local / template` scope 기준의 제어된 renormalize 를 실행합니다. 기본값은 dry-run 이고, `-Apply` 를 명시했을 때만 변경을 stage 하며, `MaxFiles` guard 로 배치 크기를 제한합니다
- `audit-i18n-drift.py`
  - `i18n/manifest.json` 을 읽어 locale 별로 어떤 공식 문서가 누락됐는지, 오래됐는지, 아직 Git 에 추적되지 않았는지 나열하고, `json / markdown`, `locale / source-doc` 필터, workboard 출력도 지원합니다
- `export-rebuild-project.ps1`
  - 현재 repo 를 이름 변경과 재초기화가 가능한 fresh-project baseline 으로 재구성해 `ops/rebuild-project/` 로 export 합니다
- `verify-rebuild-project.ps1`
  - template package 검증에 더해 rebuild guide 와 fresh-project 진입점의 존재도 확인합니다

## Governance Note

- `sync-skills.ps1` 와 `batch-adopt-skills.ps1` 는 모두 다음을 지켜야 합니다:
  - dry-run first
  - mutation 전에 backup
  - 추적 가능한 log 생성

## Platform Note

- 새로운 first-run 경로는 `bootstrap.py` 와 `verify-bootstrap.py` 를 우선 사용합니다.
- `sync-skills.ps1` 는 계속 Windows PowerShell 참조 구현이자 governance 템플릿으로 남겨 둡니다.
