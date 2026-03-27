# UniText — Operations

> 상태: Template Base
> 역할: adapter / operations control plane의 책임, delivery 규칙, 안전 경계를 정의합니다.

> **동기화 주석 2026-03-27:** 이 번역본은 current-baseline의 일부만 반영합니다. 영어 `OPERATIONS.md`가 authoritative version입니다. delivery 규칙, trigger, first-run baseline은 맞춰 두었지만 예시와 표현은 일부 다를 수 있습니다.

모든 delivery와 mutation은 `UniText`의 순수 텍스트 registry / spec 계약을 source of truth로 삼아야 합니다.

password, API key, token, credential 같은 sensitive material이 포함되면 `SECRET_HANDLING_GUIDELINES.md`도 함께 따라야 합니다.

## 1. Scope

이 문서는 다음을 다룹니다.

- adapter responsibilities
- delivery modes
- delivery triggers
- adoption flow
- drift / repair
- logical-to-physical mapping

이 문서는 다음을 다루지 않습니다.

- shared resource metadata schema
- 단일 플랫폼의 유일한 구현 방식
- 로컬 authoring repo의 역사 상태

## 2. Delivery Modes

| Mode | When to use |
|---|---|
| `pointer` | discovery 또는 머신에 등록하지 않는 리소스 |
| `mirror` | CLI가 로컬 복사본을 필요로 하거나 symlink가 불안정할 때 |
| `symlink` | 고정 경로가 필요하고 플랫폼이 안정적 링크를 지원할 때 |
| `native-config` | CLI에 공식 설정 진입점이 있을 때 |

`delivery mode`는 운영 시 adapter가 해석하는 것이며, 리소스의 고정 속성이 아닙니다.

## 3. Delivery Resolution Rules

adapter는 다음 우선순위를 따릅니다.

1. 공식 설정 진입점이 있으면 `native-config` 우선
2. 고정 경로가 필요하고 플랫폼이 안정적 링크를 지원하면 `symlink`
3. symlink를 안전하게 사용할 수 없으면 `mirror`
4. 주 목적이 discovery 또는 entry면 `pointer`

## 4. Delivery Triggers

delivery는 명시적 trigger로만 시작할 수 있습니다.

- `bootstrap`
- `sync`
- `adopt`
- `repair`

## 5. Safety Rules

### Dry-Run First

다음 작업은 먼저 dry-run plan을 생성해야 합니다.

- `adopt`
- `repair`
- 기존 상태를 덮어쓸 수 있는 `sync`

### Backup Before Mutation

모든 파괴적 작업에는 다음이 필요합니다.

- backup 또는 동등한 복구 지점
- 추적 가능한 작업 기록
- 실패 시 중단 조건

### No Silent Canonicalization

동일 이름에 다른 내용이 발견되면:

- review에서 멈출 것
- operator가 canonical source를 명시적으로 결정하게 할 것

## 6. Adoption Flow

1. `SCAN`
   - 후보 출처를 스캔하고 adopt 가능한 리소스와 readiness 상태를 나열
2. `REVIEW`
   - review checklist로 metadata, 내용 품질, canonical source의 정당성을 확인
3. `DRY-RUN`
   - adopt 또는 delivery가 어떤 대상을 수정할지, backup이 필요한지 미리 확인
4. `ADOPT`
   - 출처 내용을 registry canonical location에 쓰되, 기존 내용을 덮어쓰면 먼저 backup
5. `DELIVER`
   - adapter가 registry 내용을 대상 CLI에 전달, 기존 상태를 덮어쓸 수 있으면 log와 backup 유지
   - CLI가 `native-config`를 지원하면 `bootstrap` 단계에서 machine-local config를 쓸 수 있지만, canonical definition은 계속 `registry/`에 남김
6. `VERIFY`
   - 파일 존재, 경로 해석, delivery mode, 대상 CLI 로드 조건을 검증

## 6.1 First-Run Baseline

새 template 사용자가 macOS / Linux / Windows에서 최소 초기화를 끝내도록 하려면 최소한 다음이 필요합니다.

- 크로스 플랫폼 `bootstrap`
- 크로스 플랫폼 `verify`
- portable repo backup 흐름
- 실행 가능한 최소 MCP baseline

## 7. Operations State

다음은 shared resources가 아니라 operations state입니다.

- inventories
- baselines
- backups
- drift reports
- repair plans
- audit trails

이들은 `/operations`에 있어야 하며 `/registry`에 섞이면 안 됩니다.

## 8. Logical-to-Physical Mapping

논리 경로는 안정적인 계약이며, 실경로는 deployment-specific mapping입니다.

| Logical area | Meaning | Physical mapping examples |
|---|---|---|
| `/registry/skills` | canonical skill sources | shared directory, repo subdir, mounted path |
| `/registry/mcp` | canonical MCP definitions | config folder, generated manifest root |
| `/registry/agents` | canonical agent instruction roots | agent profiles directory, shared prompt library |
| `/registry/workflow` | workflow docs / runbooks | workflow folder, project-local docs |
| `/operations` | inventories, backups, drift logs | ops folder, state store, audit directory |
