# UniText — External Review Package

> 상태: Active Baseline  
> 용도: 외부 리뷰에서 무엇을 봐야 하고, 무엇을 보지 말아야 하며, 어떻게 반복 가능한 review package를 만들지 정의합니다.

## 1. Purpose

`UniText`는 이미 외부 리뷰가 가능한 baseline 단계에 들어왔습니다. 그러나 리뷰는 다음에 집중해야 합니다.

- 핵심 아키텍처가 합리적인가
- canonical registry가 실제로 자리 잡았는가
- operations safety model이 실행 가능한가
- 선택된 shared resources가 프로젝트 방향을 대표하기에 충분한가

이 문서의 목적은 이러한 내용을 반복 가능한 review package로 묶는 것이지, 작성자의 전체 작업 디렉터리를 그대로 넘기는 것이 아닙니다.

## 2. Recommended Reading Order

외부 리뷰어는 다음 순서로 읽는 것이 좋습니다.

1. `EXTERNAL_REVIEW_COVER_NOTE.md`
2. `EXTERNAL_REVIEW_HIGHLIGHTS.md`
3. `README.md`
4. `INDEX.md`
5. `VISION.md`
6. `RESOURCE_SPEC.md`
7. `OPERATIONS.md`
8. `SECRET_HANDLING_GUIDELINES.md`
9. `MILESTONES.md`
10. `PROJECT_STATUS_REPORT_2026-03-23.md`
11. `ESSENTIAL_SKILLS_SHORTLIST.md`

실제 리소스 샘플을 보려면 다음도 확인합니다.

- `registry/skills/`의 `8 + 4` 핵심 집합
- `registry/agents/registry-curator/`
- `registry/mcp/claude-project-mcp-seed/`
- `registry/workflow/claude-plans/`
- `local/scripts/`의 최소 governance scripts와 cross-platform first-run scripts

## 3. Review Scope

현재 review package에는 다음이 포함되어야 합니다.

- 핵심 문서
  - `EXTERNAL_REVIEW_COVER_NOTE.md`
  - `EXTERNAL_REVIEW_HIGHLIGHTS.md`
  - `README.md`
  - `INDEX.md`
  - `VISION.md`
  - `RESOURCE_SPEC.md`
  - `OPERATIONS.md`
  - `SECRET_HANDLING_GUIDELINES.md`
  - `PROJECT_MODES.md`
  - `MILESTONES.md`
  - `PROJECT_STATUS_REPORT_2026-03-23.md`
  - `ESSENTIAL_SKILLS_SHORTLIST.md`
  - `EXTERNAL_REVIEW_PACKAGE.md`
- 최소 governance 문서
  - `local/docs/ADOPTION_CHECKLIST.md`
  - `local/docs/CLI_COMPAT_MATRIX.md`
  - `local/scripts/README.md`
- 최소 governance scripts
  - `bootstrap.py`
  - `verify-bootstrap.py`
  - `create-git-bundle.py`
  - `scan-skills.ps1`
  - `sync-skills.ps1`
  - `verify-delivery.ps1`
  - `health-check.ps1`
  - `batch-adopt-skills.ps1`
  - `generate-index-entries.ps1`
  - `rollback-skills.ps1`
  - `export-review-package.ps1`
- 선택된 shared resources
  - `registry/skills/`의 `8 + 4` 집합
  - `registry/agents/registry-curator/`
  - `registry/mcp/claude-project-mcp-seed/`
  - `registry/workflow/claude-plans/`

## 4. Out Of Scope

다음은 외부 리뷰의 주 대상이 아닙니다.

- `backup/`
- `recovered_*`
- `.bak_*`
- `ops/history/`
- 로컬 특정 path mapping과 개인 환경 잔재
- shortlist에 포함되지 않은 후보 skills
- 추적되지 않았거나 실험 중인 내용

authoring notes and review archives는 작성자 작업 참고 자료이며 canonical review source가 아닙니다.

## 5. Export Command

repo root에서 다음을 실행합니다.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-review-package.ps1
```

기본 출력 위치:

```text
ops/review-package/review_YYYYMMDD_HHMMSS/
```

내용만 미리 확인하고 파일은 쓰지 않으려면:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-review-package.ps1 -DryRun
```

## 6. Validation

export 전에 최소한 한 번은 다음을 실행하는 것이 좋습니다.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\health-check.ps1
```

canonical skills delivery 정렬을 확인하려면:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-delivery.ps1
```

## 7. Current Interpretation

2026-03-24 기준으로 `UniText`는 다음을 갖추었습니다.

- reviewer-facing cover note와 highlights summary
- 외부 리뷰용으로 읽을 수 있는 핵심 문서
- `8 + 4` 핵심 skills 집합
- agent / workflow seed와 실행 가능한 MCP baseline
- review package를 반복 생성하는 정리 흐름
- cross-platform `bootstrap -> verify`
- portable `git bundle` backup 흐름

따라서 현재 가장 적절한 위치는:

**external-review-ready baseline**

입니다.

**fully generalized release template**는 아닙니다.

