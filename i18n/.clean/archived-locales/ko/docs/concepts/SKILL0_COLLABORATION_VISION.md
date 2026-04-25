# UniText × skill-0 — Collaboration Vision

> 상태: Concept Draft
> 목적: `UniText`와 `skill-0`의 관계, 협업 공간, 가능한 경로, 그리고 현재 부족한 메커니즘을 정의합니다.

## 1. Executive Summary

`UniText`와 `skill-0`는 서로 배타적이거나 중복된 프로젝트가 아니라, 상하류 관계를 만들 수 있는 두 층입니다.

- `UniText`는 shared resources의 **registry / delivery / governance**를 담당합니다
- `skill-0`는 높은 수준의 skill을 흡수하고, 분해하고, 정규화해서 더 범용적인 **atomic operation set**으로 바꿉니다

따라서 가장 합리적인 협업 방식은 "누가 누구를 대체하는가"가 아니라 다음입니다.

**UniText는 canonical inputs와 governance 가능한 수용면을 제공하고, skill-0는 decomposition / normalization / recomposition 능력을 제공한다.**

## 2. Each Project Solves a Different Problem

### UniText

`UniText`가 푸는 문제는 다음입니다.

- shared resource를 어떻게 canonical화할 것인가
- 여러 AI CLI 사이에서 어떻게 delivery할 것인가
- `SCAN -> REVIEW -> DRY-RUN -> ADOPT -> DELIVER -> VERIFY`로 변경을 어떻게 관리할 것인가

즉,

**distribution / governance problem**

### skill-0

`skill-0`가 푸는 문제는 다음입니다.

- 어떤 높은 수준의 skill이 실제로 어떤 최소 operation unit으로 구성되는가
- 어떤 step이 재사용 가능한 primitive인가
- 어떤 설명은 surface wording이고, 어떤 것이 core operation인가
- 높은 수준의 skill을 더 작고, 더 일반적이며, 더 이식하기 쉬운 능력 집합으로 다시 조합할 수 있는가

즉,

**abstraction / compiler / normalization problem**

## 3. Relationship Between the Two

`skill-0`의 목표 관점에서 보면, `UniText`의 가장 가치 있는 역할은 "배포되는 결과"가 아니라 다음과 같습니다.

- 안정적인 high-level skill source
- 논리적 identity와 metadata를 가진 canonical corpus
- 계속 분석, 비교, 추적할 수 있는 skills data set

이 관점에서 두 프로젝트의 관계는 다음처럼 설명할 수 있습니다.

| Project | Primary role |
|---|---|
| `UniText` | shared resources의 canonical source of truth |
| `skill-0` | high-level skills를 분석하고 분해하고 컴파일하는 analyzer / decomposer / compiler |

한 문장으로 말하면,

**UniText는 skill을 저장하고, skill-0는 skill을 해체한다.**

## 4. Current Collaboration Space

`UniText`의 core schema를 아직 바꾸지 않아도 이미 협업 공간은 있습니다.

### 4.1 Use UniText as input corpus

`skill-0`는 다음을 직접 입력으로 사용할 수 있습니다.

- `registry/skills/*/SKILL.md`
- `INDEX.md`의 catalog metadata
- `RESOURCE_SPEC.md`가 제공하는 identity / canonical location 계약

이렇게 하면 `skill-0`가 분석하는 것은 흩어진 복사본이 아니라 더 정리된 canonical skill corpus가 됩니다.

### 4.2 Use UniText as a governed staging ground

`skill-0`의 분석 출력은 현재 canonical registry로 바로 돌려보내지 않고 다음 같은 위치에 둘 수 있습니다.

- `/operations`
- 예: `ops/analysis/skill-0/`

이 방법의 장점은 다음과 같습니다.

- shared resource schema를 성급하게 오염시키지 않는다
- 분석 형식이 안정적인지 먼저 관찰할 수 있다
- `skill-0`를 analysis pipeline으로 취급하고, 바로 canonical source로 승격하지 않아도 된다

### 4.3 Use UniText review flow to evaluate derived outputs

`skill-0`가 다음과 같은 출력을 만들면,

- atom maps
- normalized step sets
- shared subroutine clusters
- recomposition candidates

이 결과물은 `UniText`의 review mindset으로 검사할 수 있습니다.

- identity가 안정적인가
- naming이 명확한가
- 원래 skill로의 대응 관계를 추적할 수 있는가
- canonical form은 사람이 결정해야 하는가

## 5. Most Likely Collaboration Modes

### Mode A — skill-0 as external analyzer

`skill-0`가 `UniText`를 data source로 삼아 analysis report를 만들지만 registry에는 다시 쓰지 않습니다.

적합한 용도:

- decomposition method의 빠른 검증
- skill overlap analysis
- reusable primitives 탐색

장점:

- 도입 비용이 가장 낮음
- `UniText` schema를 거의 바꾸지 않아도 됨

단점:

- 결과가 sidecar artifacts에 머문다
- shared canonical resource로 자리 잡기 어렵다

### Mode B — skill-0 as sidecar generator

`skill-0`가 `registry/skills`를 읽고, machine-readable sidecar를 옆에 생성합니다.

- `skill.atoms.json`
- `skill.graph.json`
- `skill.coverage.json`

장점:

- skill과 atom의 대응을 명확하게 만들 수 있다
- 단순 report보다 tooling에 싣기 쉽다

단점:

- `UniText` schema의 경계 문제에 닿기 시작한다
- 무엇이 canonical이고 무엇이 generated인지 정의해야 한다

### Mode C — primitives become a first-class resource type

협업이 성숙하면 `UniText`에 공식 resource type을 추가할 수 있습니다.

- `/registry/primitives`
- 또는 `/registry/operations`

이렇게 하면 `skill-0`의 출력은 분석 부속물이 아니라 registry가 공식 관리하는 shared resources가 됩니다.

장점:

- 진짜 공동 어휘층을 만든다
- cross-skill recomposition을 뒷받침할 수 있다

단점:

- `UniText`의 resource model을 바꿔야 한다
- 새로운 metadata spec, adoption flow, verification rules가 필요하다

## 6. What Is Missing Today

현재 두 프로젝트가 자연스럽게 깊게 통합되지 못하는 가장 큰 이유는 다음 메커니즘이 아직 없기 때문입니다.

### 6.1 Missing canonical type for primitives

`UniText`의 현재 1차 resource type은 다음 4가지입니다.

- `skills`
- `mcp`
- `agents`
- `workflow`

아직 다음은 없습니다.

- `primitives`
- `operations`
- `atoms`

즉 `skill-0`가 가장 중요하게 여기는 산출물을 받아줄 1차 수용면이 아직 `UniText`에 없습니다.

### 6.2 Missing metadata spec for atomic units

현재 `RESOURCE_SPEC.md`는 높은 수준의 shared resources를 설명하는 데 적합하지만, 다음은 아직 정의하지 않았습니다.

- atom id
- operation signature
- preconditions / postconditions
- composition rules
- source skill로의 provenance

### 6.3 Missing adoption flow for derived artifacts

`UniText`에는 skills adoption flow가 있지만, 다음과 같은 경우를 다루는 전용 흐름은 없습니다.

- 같은 skill에서 서로 다른 atom set이 분해되는 경우
- 여러 skill이 비슷하지만 완전히 같지는 않은 primitive에 대응되는 경우
- 어떤 atom이 canonicalize할 만큼 안정적인지 판단하는 경우

### 6.4 Missing verification model

`skill-0`의 출력을 더 공식적인 협업 단계로 옮기려면 최소한 다음에 답해야 합니다.

- decomposition이 안정적인가
- round-trip recomposition이 가능한가
- cross-skill reuse를 실제로 높이는가
- 그냥 기존 설명을 다시 말한 것뿐은 아닌가

### 6.5 Missing boundary between analysis and canon

아직 다음 경계 규칙이 필요합니다.

- 어떤 `skill-0` 산출물이 단순 analysis인지
- 어떤 산출물이 canonical shared resource로 볼 수 있는지

이 경계가 불분명한 동안에는 가장 안전한 곳은 `ops/analysis/skill-0/`입니다.

## 7. Recommended Near-Term Direction

단기적으로는 `UniText`의 core schema를 바로 바꾸기보다 다음처럼 점진적으로 가는 것이 가장 합리적입니다.

**Mode A -> Mode B의 점진적 협업**

### Phase A — Analysis Only

먼저 다음을 합니다.

- `registry/skills/*/SKILL.md`를 입력으로 사용
- decomposition report를 출력
- `ops/analysis/skill-0/`에 저장

이 단계의 목표는 canonicalize가 아니라 다음을 확인하는 것입니다.

- atom extraction이 안정적인가
- skill overlap이 실제로 관찰되는가
- 어떤 primitive를 남길 가치가 있는가

### Phase B — Stable Sidecars

형식이 안정되면 다음을 도입합니다.

- sidecar schemas
- naming rules
- source-skill linkage
- basic verification

이 시점에는 아직 resource type을 늘리지 않아도 다음 관계를 만들 수 있습니다.

- `skill -> atoms`
- `atom -> source skills`

### Phase C — First-Class Primitives

analysis가 가치를 증명하면 다음 중 하나를 `UniText`에 공식 도입하는 것을 검토합니다.

- `/registry/primitives`
- `/registry/operations`

그 시점에만 다음 문서를 공식적으로 갱신하면 됩니다.

- `VISION.md`
- `RESOURCE_SPEC.md`
- `INDEX.md`
- `OPERATIONS.md`

## 8. Concrete First Deliverables

두 프로젝트가 협업을 시작하기 위한 첫 결과물로 가장 가치 있는 것은 다음 4가지입니다.

1. `skill-0`의 analysis output draft schema를 정의한다
2. `UniText`의 `Core 8` skills 중 1~2개를 골라 decomposition sample을 만든다
3. 출력을 `ops/analysis/skill-0/`에 둔다
4. 다음을 비교한다
   - 서로 다른 skills 사이에서 공유되는 atom
   - skill 문장과 atom 층 사이의 차이
   - 최소 workflow로 역재구성할 수 있는지

## 9. Strategic Interpretation

협업이 성공하면 장기적인 역할 분담은 분명해집니다.

- `UniText`는 shared AI resources의 canonical hub가 된다
- `skill-0`는 skill normalization과 primitive extraction engine이 된다

system layer로 보면 다음과 같습니다.

| Layer | Project |
|---|---|
| Canonical resource governance | `UniText` |
| Skill decomposition / normalization | `skill-0` |
| Future primitive vocabulary layer | `UniText × skill-0`의 공동 결과 |

## 10. Final Position

현재 가장 정확한 결론은 다음입니다.

**`UniText`와 `skill-0`는 높은 관련성을 가지지만, 중복 개발은 아니다.**

하나는 governance와 배포를, 다른 하나는 분해와 추상화를 맡습니다.

따라서 단기적으로 가장 합리적인 협업은 `skill-0`를 `UniText`의 기존 4종 resource에 바로 밀어 넣는 것이 아닙니다.

**`skill-0`가 먼저 `UniText`를 canonical input corpus로 다루게 하고, 그 analysis 결과를 우선 `ops/analysis/skill-0/`에 두는 것**입니다.

출력 형식, 가치, 검증 방법이 안정되면 그때 primitive / operation 계층을 새로운 canonical resource type으로 공식 승격할지 결정하면 됩니다.
