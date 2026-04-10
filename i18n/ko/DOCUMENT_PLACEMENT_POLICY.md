[English](../../DOCUMENT_PLACEMENT_POLICY.md) | [繁體中文](../zh-TW/DOCUMENT_PLACEMENT_POLICY.md) | [简体中文](../zh-CN/DOCUMENT_PLACEMENT_POLICY.md) | [日本語](../ja/DOCUMENT_PLACEMENT_POLICY.md) | [Deutsch](../de/DOCUMENT_PLACEMENT_POLICY.md) | [Français](../fr/DOCUMENT_PLACEMENT_POLICY.md) | [Español](../es/DOCUMENT_PLACEMENT_POLICY.md) | [한국어](DOCUMENT_PLACEMENT_POLICY.md) | [Italiano](../it/DOCUMENT_PLACEMENT_POLICY.md)

# UniText — 문서 배치 정책

> 상태: Active Baseline
> 용도: governance, reference, authoring, operations 문서를 어느 레이어에 두어야 하는지 정의하여 shared 내용과 live workspace 내용이 섞이지 않도록 한다.

## 1. Purpose

UniText 는 동시에 다음과 같다.

- authoring workspace
- shared registry baseline
- template / rebuild export source

그래서 문서를 단지 “주제가 관련 있어 보이는가”만으로 판단하면 잘못된 레이어에 두기 쉽다.

이 규칙이 답하는 것은 다음과 같다.

- 어떤 종류의 문서를 `registry/` 에 둬야 하는가
- 어떤 종류의 문서를 `local/` 에 둬야 하는가
- 어떤 종류의 문서를 `ops/` 에 둬야 하는가
- 어떤 문서는 tracked 될 수 있는가
- 어떤 문서는 ignored local authoring 공간에만 남아야 하는가

## 2. Core Rule

문서 위치를 판단할 때는 주제 분야보다 내용의 성격을 우선한다.

- 문서가 shared canonical truth 를 설명하면 shared layer 에 둔다
- 문서가 단일 작성자 workspace 의 현재 상태를 설명하면 local layer 에 둔다
- 문서가 작업 이력, export 결과, audit evidence, generated state 를 설명하면 operations layer 에 둔다

## 3. Placement Matrix

| Content type | Canonical location | Tracked | Share-safe | Notes |
|---|---|---|---|---|
| 아키텍처 원칙, governance 규칙, template-safe spec | root docs 또는 `registry/` | Yes | Yes | live workspace values 를 피해야 한다 |
| shared sanitized reference | `registry/.../references/` | Yes | Yes | 필드 구조는 설명할 수 있지만 값은 redacted 또는 placeholder 여야 한다 |
| shared workflow / runbook / template | `registry/workflow/` | Yes | Yes | 단일 작성자 머신에 묶이면 안 된다 |
| machine-local path map / wiring notes | `local/docs/` | Case-by-case | Usually no | location / state 는 기록 가능하지만 plaintext secret 는 불가 |
| live workspace baseline | `local/docs/*_WORKSPACE_BASELINE.md` | No | No | 반드시 ignore |
| live operational checklist | `local/docs/*_LIVE.md` | No | No | 반드시 ignore |
| authoring plans / drafts / review notes | `local/docs/authoring/` | No | No | 반드시 ignore |
| generated audit trail / export output / drift report | `ops/` | No | No | state 이며 canonical source 가 아니다 |

## 4. Naming Rules

하나의 주제에 shared 버전과 live 버전이 모두 필요하면 기본적으로 짝을 이루는 이름을 사용한다.

- shared sanitized doc
  - `registry/.../references/<topic>.md`
- live workspace doc
  - `local/docs/<TOPIC>_WORKSPACE_BASELINE.md`
  - 또는 `local/docs/<TOPIC>_LIVE.md`

## 5. Pair Rule

shared sanitized doc 와 live workspace doc 가 동시에 존재하면 다음을 지켜야 한다.

1. shared 버전은 template-safe 구조와 redacted placeholder 만 남긴다
2. live 버전은 `local/docs/` 또는 `local/docs/authoring/` 에만 둔다
3. shared 버전은 live 버전의 위치를 명시한다
4. live 버전도 대응되는 shared sanitized reference 를 가리킨다

## 6. Publishing Rule

다음 표현들은 같은 뜻이 아니다.

- template export passes
- rebuild export passes
- branch is publish-safe

template / rebuild export 가 안전하다는 것은 export 산출물의 경계가 비교적 깨끗하다는 뜻일 뿐, authoring repo 안의 모든 tracked content 가 push 에 적합하다는 뜻은 아니다.

## 7. Quick Decisions

문서를 어디에 둘지 모르겠다면 먼저 이 세 가지를 묻는다.

1. 이 문서는 단일 작성자 workspace 가 지금 어떤 상태인지 설명하는가
   - 예: `local/docs/` 를 우선 검토
2. 이 문서는 작업 결과, audit 산출물, export package, 또는 drift report 인가
   - 예: `ops/` 를 우선 검토
3. 이 문서는 앞으로 template / rebuild / shared registry 에서 안전하게 참조되어야 하는가
   - 예: root docs, `registry/`, 또는 shared workflow layer 를 우선 검토

## 8. Common Misplacements

- live Cloudflare baseline 을 `registry/.../references/` 에 두는 것
- strategy / review plan 을 root 에 두는 것
- export output 또는 audit evidence 를 canonical reference 로 취급하는 것
- machine-specific path 를 shared governance docs 에 직접 쓰는 것

## 9. Review Gate

새 governance / reference 문서를 추가하기 전에 최소한 다음을 확인해야 한다.

- 그것이 live workspace state 가 아니라 shared truth 를 설명하는가
- push 되더라도 `NO_PUBLISH_POLICY.md` 와 template-safe 기대를 계속 만족하는가
- 하나의 파일에 둘 다 넣는 대신 sanitized/live pair 가 필요한 것은 아닌가

## 10. Related Docs

- `README.md`
- `INDEX.md`
- `OPERATIONS.md`
- `PROJECT_MODES.md`
- `SECRET_HANDLING_GUIDELINES.md`
- `NO_PUBLISH_POLICY.md`
