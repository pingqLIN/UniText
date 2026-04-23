# UniText — Template Release Checklist

> 용도: template package를 출력하거나 게시하기 전에 최소 정리가 끝났는지 빠르게 점검합니다.

## 1. Docs

- [ ] `README.md`가 작성자의 개인 배경 없이도 이해 가능함
- [ ] `INDEX.md`가 discovery entry로 동작함
- [ ] `PROJECT_MODES.md`가 template과 authoring workspace를 분명히 구분함
- [ ] `SECRET_HANDLING_GUIDELINES.md`가 secret boundary를 정의하고 실제 credential을 포함하지 않음
- [ ] `TEMPLATE_RELEASE_PACKAGE.md`가 갱신됨
- [ ] `MILESTONES.md`가 현재 phase 상태를 반영함

## 2. Cleanup Boundaries

- [ ] template package에 `backup/`이 포함되지 않음
- [ ] template package에 `recovered_*`가 포함되지 않음
- [ ] template package에 `.bak_*`가 포함되지 않음
- [ ] template package에 `ops/history/`가 포함되지 않음
- [ ] template package에 review-only docs가 포함되지 않음
- [ ] template package에 machine-specific absolute paths가 포함되지 않음

## 3. Examples

- [ ] 최소 1개의 generic skill example
- [ ] 최소 1개의 generic agent example
- [ ] 최소 1개의 generic mcp example
- [ ] 최소 1개의 generic workflow example
- [ ] 최소 1개의 generic local overlay skeleton
- [ ] starter package에 cross-platform `bootstrap -> verify` 경로가 포함됨

## 4. Validation

- [ ] `health-check.ps1`가 통과함
- [ ] `export-template-package.ps1 -DryRun`이 package 내용을 나열함
- [ ] `export-template-package.ps1`가 package를 성공적으로 생성함
- [ ] `verify-template-package.ps1`가 통과함
- [ ] `bootstrap.py --dry-run`가 깨끗한 환경에서 초기화를 미리 보여줌
- [ ] `verify-bootstrap.py`가 first-run wiring을 검증함
- [ ] package에 `manifest.json`이 포함됨
- [ ] package에 `release.json`이 포함됨

## 5. Release Call

위 항목이 모두 완료되면 다음으로 볼 수 있습니다.

**template release candidate에 적합함**

local-only boundary가 불명확하거나, examples가 불완전하거나, CLI 검증이 부족하면 다음으로 봅니다.

**template release cleanup baseline**
