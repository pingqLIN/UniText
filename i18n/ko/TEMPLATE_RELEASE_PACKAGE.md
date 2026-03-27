# UniText — Template Release Package

> 상태: Active Baseline  
> 용도: template release cleanup의 목표, 범위, 반복 가능한 export 흐름을 정의합니다.

> **동기화 주석 2026-03-27:** 이 번역본은 current-baseline의 일부만 반영합니다. 영어 `TEMPLATE_RELEASE_PACKAGE.md`가 authoritative version입니다. release boundary, exclusions, skills 규칙에 관한 고위험 섹션은 맞춰 두었지만, 나머지는 더 오래되었을 수 있습니다. `5.1 Skills Release Rule` 절은 아직 여기까지 동기화되지 않았으므로 해당 규칙은 영어 원문을 기준으로 봐야 합니다.

## 1. Purpose

`UniText`의 template release는 작성자 작업공간을 그대로 포장하는 것이 아니라 다음을 만족하는 package를 내보내야 합니다.

- 핵심 아키텍처와 규격을 유지
- 최소 사용 예시를 유지
- local-only state를 제외
- 역사적 governance 잔재를 제외
- 다른 사용자가 fork / clone 후 확장하기 적합

이 package의 위치는:

**starter template**

이며 다음은 아닙니다.

**authoring workspace snapshot**

## 2. Include

현재 template package에는 다음이 포함되어야 합니다.

- 핵심 문서
  - `README.md`
  - `INDEX.md`
  - `VISION.md`
  - `RESOURCE_SPEC.md`
  - `OPERATIONS.md`
  - `PROJECT_MODES.md`
  - `SECRET_HANDLING_GUIDELINES.md`
  - `MILESTONES.md`
  - `TEMPLATE_RELEASE_PACKAGE.md`
  - `TEMPLATE_RELEASE_CHECKLIST.md`
- template-safe root config
  - `.gitignore`
- generic examples
  - `registry/skills/example-skill/`
  - `registry/agents/example-agent/`
  - `registry/mcp/example-mcp/`
  - `registry/workflow/example-workflow/`
- starter local overlay skeleton
  - `local/README.md`
  - `local/docs/PATH_MAP.md`
  - `local/scripts/bootstrap.py`
  - `local/scripts/verify-bootstrap.py`
  - `local/scripts/create-git-bundle.py`
  - `local/scripts/sync-skills.ps1`
- release metadata
  - `manifest.json`
  - `release.json`

## 3. Exclude

template package에는 다음이 포함되면 안 됩니다.

- `backup/`
- `recovered_*`
- `.bak_*`
- `ops/history/`
- `ops/review-package/`
- `ops/template-package/`
- authoring notes and review archives
- `local/docs/PATH_MAP.md`
- 실제 사용자 계정, home directory, 절대 경로
- review-specific docs
  - `EXTERNAL_REVIEW_PACKAGE.md`
  - `EXTERNAL_REVIEW_COVER_NOTE.md`
  - `EXTERNAL_REVIEW_HIGHLIGHTS.md`
  - `PROJECT_STATUS_REPORT_2026-03-23.md`

## 4. Export Command

repo root에서 다음을 실행합니다.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-template-package.ps1
```

기본 출력 위치:

```text
ops/template-package/template_YYYYMMDD_HHMMSS/
```

내용만 미리 확인하고 파일은 쓰지 않으려면:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-template-package.ps1 -DryRun
```

export된 package를 검증하려면:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-template-package.ps1 -Path .\ops\template-package\<package-name>
```

export 후 새 사용자의 first-run 권장 경로:

```bash
python local/scripts/bootstrap.py --dry-run
python local/scripts/bootstrap.py --force
python local/scripts/verify-bootstrap.py
python local/scripts/create-git-bundle.py
```

## 5. Export Interpretation

export된 template package는 다음을 의미합니다.

- UniText의 핵심 계약
- 깨끗한 starter layout
- 최소 generic examples 집합

다음을 의미하지는 않습니다.

- 작성자의 전체 작업 상태
- 모든 채택된 skills
- 모든 review / audit 증거
- 완료된 local delivery wiring

## 6. Current Interpretation

2026-03-27 기준으로 `UniText`는 다음을 갖추었습니다.

- 외부 리뷰 package
- reviewer-facing entry docs
- template release cleanup baseline
- 반복 가능한 template package export script
- starter local overlay skeleton
- template package verification script
- release metadata
- cross-platform first-run scripts
- portable bundle backup 흐름

따라서 현재 가장 적절한 해석은:

**template release candidate**

입니다.

**authoring workspace snapshot**는 아닙니다.

