# UniText — Vision

> 상태: Template Base
> 원칙: 어떤 단일 운영체제, 디렉터리 구조, 배포 방식도 규격의 전제로 삼지 않습니다.

## 1. What UniText Is

`UniText`는 text-native, registry-first, AI-first shared resource hub로서, 여러 AI CLI / agent 시스템이 동일한 순수 텍스트 계약으로 자원 정의와 채택 방식을 공유하게 합니다.

이 구조는 두 층으로 이루어집니다.

1. `Registry`
   - shared resources, canonical identity, 최소 계약을 정의
2. `Adapter / Operations Control Plane`
   - registry 내용을 다양한 CLI에 연결하고 install, sync, adopt, repair를 처리

## 2. Problem It Solves

`UniText`가 해결하려는 문제는 여러 도구 사이에서 리소스가 조각나는 현상입니다.

- skills가 여러 위치에 흩어짐
- MCP 정의가 다른 설정 형식으로 분산됨
- agent instructions를 공유하기 어려움
- workflow 관행이 도구 간에 이어지지 않음
- AI가 읽기 쉽고 버전 관리에 친화적인 공통 텍스트 인터페이스가 부족함

## 3. Architecture Position

공식 위치:

**Registry-first, adapter-enabled, operations-governed**

핵심 원칙:

- registry가 없으면 공통 출처와 공통 의미가 없음
- adapter가 없으면 registry를 각 CLI에 실제로 보낼 수 없음
- AI는 중요한 consumer이자 협력자지만, 유일하게 신뢰할 수 있는 통합 메커니즘은 아님

## 4. Resource Types

기본 shared resource types는 다음과 같습니다.

- `skills`
- `mcp`
- `agents`
- `workflow`

`operations state`는 shared resource type이 아니며 `/operations`에 독립적으로 존재해야 합니다.

## 5. Discovery and Delivery

`INDEX.md`는 discovery를 담당하며 다음에 답합니다.

- 어떤 리소스가 있는가
- 각 리소스의 논리적 위치는 어디인가
- 어떤 CLI가 지원되는가

`OPERATIONS.md`는 delivery를 담당하며 다음에 답합니다.

- 특정 CLI가 리소스를 어떻게 가져가는가
- 언제 install, sync, adopt, repair를 실행하는가
- delivery mode를 어떻게 해석하는가

사용 가능한 delivery modes:

- `pointer`
- `mirror`
- `symlink`
- `native-config`

## 6. Delivery Triggers

delivery는 명시적 trigger로만 시작할 수 있습니다.

- `bootstrap`
- `sync`
- `adopt`
- `repair`

모든 파괴적 작업은 다음을 따라야 합니다.

- 먼저 dry-run
- 먼저 backup
- canonical source를 조용히 결정하지 않음

## 7. Adoption Model

### Soft Adoption

- 먼저 discovery를 도입
- 기존 리소스를 즉시 강제 이전하지 않음

### Formal Adoption

공식 채택 절차:

1. `SCAN`
2. `REVIEW`
3. `DRY-RUN`
4. `ADOPT`
5. `DELIVER`
6. `VERIFY`

동일한 이름에 내용이 다른 리소스가 있으면 절차는 `REVIEW / DRY-RUN`에서 멈춰야 합니다.

## 8. Documentation Set

핵심 문서:

- `VISION.md`
- `INDEX.md`
- `RESOURCE_SPEC.md`
- `OPERATIONS.md`
- `PROJECT_MODES.md`

## 9. Path Strategy

주 문서는 다음과 같은 logical canonical path를 사용합니다.

- `/registry/skills`
- `/registry/mcp`
- `/registry/agents`
- `/registry/workflow`
- `/operations`

절대 경로와 플랫폼 전용 설정은 deployment mapping에 속할 뿐, vision-level contract는 아닙니다.

## 10. Design Principles

- `Registry first`
- `Discovery before automation`
- `Explicit triggers`
- `Minimum viable metadata`
- `Canonical source of truth`
- `CLI-specific delivery`
- `Platform-agnostic contract`
- `Safe mutation`

## 11. One-Sentence Positioning

> UniText는 text-native, registry-first, AI-first shared resource hub로서, 명확한 adapter와 operations control plane을 통해 여러 AI CLI가 동일한 canonical resources를 안전하게 발견, 채택, 공유하도록 합니다.
