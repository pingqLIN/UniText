# UniText — Milestones

> 상태: Active
> 목적: 외부 리뷰와 내부 실행이 함께 사용할 수 있는 정량적 완료 조건을 정의합니다.

## Phase 1 — Skills Registry Online

- `registry/skills/`가 생성됨
- 최소 5개의 skills가 canonical adoption을 완료함
- `INDEX.md`에 해당 catalog entries가 존재함
- `local/scripts/sync-skills.ps1`가 `registry/skills`를 가리킴
- `local/scripts/verify-delivery.ps1`가 skills source와 target 상태를 검증할 수 있음
- `local/scripts/health-check.ps1`가 기본 검사를 통과할 수 있음

## Phase 2 — Full Registry Baseline

- `registry/agents/`가 생성됨
- `registry/mcp/`에 최소 1개의 비어 있지 않은 예시가 읽기 가능하게 유지됨
- `registry/workflow/`에 최소 1개의 catalog entry가 공식적으로 나열됨
- `scan` / `verify` / `sync` 세 가지 작업에 최소 도구가 있음
- `CLI_COMPAT_MATRIX.md`가 현재 의존하는 CLI 동작과 마지막 검증 날짜를 기록함

## Phase 3 — External Review Ready

- Git repository가 초기화됨
- `.gitignore`가 local-only 및 대형 역사 산출물을 제외함
- `README.md`, `INDEX.md`, `docs/reports/status/PROJECT_STATUS_REPORT_2026-03-23.md` 세 문서의 상태가 일치함
- `EXTERNAL_REVIEW_PACKAGE.md`가 리뷰 범위, 읽기 순서, 제외 항목을 정의함
- `EXTERNAL_REVIEW_COVER_NOTE.md`와 `EXTERNAL_REVIEW_HIGHLIGHTS.md`가 reviewer-facing entry docs로 사용 가능함
- `SECRET_HANDLING_GUIDELINES.md`가 governance boundary를 만들고 핵심 읽기 순서에 포함됨
- `local/scripts/export-review-package.ps1`로 review package를 반복 생성할 수 있음
- 크로스 플랫폼 `bootstrap -> verify` first-run 경로가 제공됨
- 외부 리뷰자가 다음을 바로 확인할 수 있음:
  - 핵심 아키텍처 문서
  - adoption된 canonical skills
  - 최소 operations scripts
  - 다음 단계 milestone

## Phase 4 — Template Release Ready

- local-only artifacts가 배포 패키지에 포함되지 않음
- template export 흐름이 문서화됨
- `TEMPLATE_RELEASE_PACKAGE.md`와 `TEMPLATE_RELEASE_CHECKLIST.md`가 존재함
- `local/scripts/export-template-package.ps1`로 starter package를 반복 생성할 수 있음
- `local/scripts/verify-template-package.ps1`로 starter package 구조를 검증할 수 있음
- `SECRET_HANDLING_GUIDELINES.md`가 starter package에 포함됨
- `local/scripts/create-git-bundle.py`로 portable backup artifact를 만들 수 있음
- `skills`, `mcp`, `agents`, `workflow`를 덮는 template-safe generic examples가 있음
- template-safe `local/` skeleton이 있음
- `mcp`에 최소 1개의 실제 실행 가능한 baseline이 있음
- canonical resource coverage가 `skills`, `mcp`, `agents`, `workflow`로 계속 확장됨
- 최소 2개의 CLI가 실제 delivery 검증을 통과함
