[English](../../WORKSPACE_SENSITIVE_METADATA_RULES.md) | [繁體中文](../zh-TW/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [简体中文](../zh-CN/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [日本語](../ja/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [Deutsch](../de/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [Français](../fr/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [Español](../es/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [한국어](WORKSPACE_SENSITIVE_METADATA_RULES.md) | [Italiano](../it/WORKSPACE_SENSITIVE_METADATA_RULES.md)

# Workspace Sensitive Metadata Rules

> 상태: Active Baseline
> 용도: shared surface 위의 workspace-sensitive metadata 에 대한 탐지 규칙, 유지보수 규칙, 검증 경계를 정의한다.

## 1. Purpose

`WORKSPACE_SENSITIVE_METADATA_RULES.json` 은 authoring repo 와 exported starter package 가 공유하는 규칙 소스다. 이 파일은 다음과 같은 drift 를 줄이기 위해 존재한다.

- shared docs 에 로컬 절대 경로가 섞이는 경우
- shared scripts 에 live workspace hostname 이 섞이는 경우
- shared governance files 에 live redirect URI 나 Cloudflare IDs 가 섞이는 경우
- boundary verify 와 template verify 가 서로 다른 규칙 집합을 쓰는 경우

이 문서는 다음을 설명한다.

- 규칙 파일 각 구역이 무엇을 뜻하는지
- 언제 새로운 규칙을 추가해야 하는지
- sanitized placeholder 를 live metadata 로 오인하지 않도록 어떻게 막는지
- 규칙을 바꾼 뒤 어떤 검증을 다시 돌려야 하는지

## 2. Schema

`WORKSPACE_SENSITIVE_METADATA_RULES.json` 에는 현재 네 개의 최상위 구역이 있다.

- `shared_surface_scope`
  - repo-side boundary verify 가 기본적으로 스캔할 tracked shared surfaces 를 정의한다
- `path_rules`
  - shared surface 안에 나타나면 안 되는 tracked path 자체를 정의한다
- `content_patterns`
  - 어떤 텍스트 내용을 workspace-sensitive metadata 로 볼지 정의한다
- `self_test_cases`
  - regex 수정 후 조용한 회귀가 생기지 않도록 긍정/부정 내장 사례를 정의한다

## 3. Maintenance Rules

- 새로운 shared governance doc 또는 shared control script 를 추가했고 그것이 repo-side boundary review 범위에 속한다면 `shared_surface_scope` 에도 함께 추가해야 한다
- 새로운 live metadata 유형이 생기면 먼저 `content_patterns`, 그다음 대응하는 `self_test_cases` 를 추가한다
- 어떤 placeholder 를 안전한 예시로 간주해야 한다면 `expected_labels = []` 인 self-test case 를 반드시 추가한다
- 어떤 regex 가 script 안에서 규칙 문자열로만 나타난다면 `skip_script_pattern_lines` 를 명시해야 한다
- 오탐을 피하려고 authoring-only 또는 operations-only path 를 `shared_surface_scope` 에 넣어서는 안 된다. 먼저 문서 배치가 잘못된 것은 아닌지 확인해야 한다

## 4. Required Validation

`WORKSPACE_SENSITIVE_METADATA_RULES.json` 을 조정할 때마다 최소한 다음을 다시 실행해야 한다.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\validate-workspace-sensitive-metadata-rules.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-workspace-boundaries.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\health-check.ps1
```

이번 변경이 starter baseline 에 영향을 준다면 다음도 추가로 실행해야 한다.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-template-package.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-template-package.ps1 -Path .\ops\template-package\<package-name>
```

## 5. Design Boundary

이 규칙 세트의 목표는 다음과 같다.

- shared surface 위에 안정적이고 유지보수 가능하며 검증 가능한 heuristic controls 를 제공하는 것

이것은 다음이 아니다.

- 모든 secret 유형을 위한 완전한 schema validator
- 모든 infrastructure provider 를 위한 범용 DLP 시스템
- local-only / ops-only 영역을 전부 스캔하는 도구

앞으로 metadata 유형이 계속 늘어난다면, 다음 단계는 규칙 소스와 테스트 사례를 확장하는 것이지 live references 를 다시 shared registry 로 되돌리는 것이 아니다.
