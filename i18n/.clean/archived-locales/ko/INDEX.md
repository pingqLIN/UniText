# UniText — Index

> 상태: `Template Base`
> 역할: 모든 human / AI 가 가장 먼저 읽는 문서이자 discovery 진입점.

`UniText` 는 순수 텍스트를 공유 인터페이스로 사용하며, cross-CLI 통합 호환성과 AI-first discovery 를 강조합니다.

## 1. Core Docs

권장 읽기 순서:

1. `INDEX.md`
2. `VISION.md`
3. `RESOURCE_SPEC.md`
4. `OPERATIONS.md`
5. `PROJECT_MODES.md`
6. `DOCUMENT_PLACEMENT_POLICY.md`
7. `WORKSPACE_SENSITIVE_METADATA_RULES.md`
8. `TEMPLATE_RELEASE_PACKAGE.md`
9. `TEMPLATE_RELEASE_CHECKLIST.md`
10. `REBUILD_AS_NEW_PROJECT.md`
11. `SECRET_HANDLING_GUIDELINES.md`
12. `NO_PUBLISH_POLICY.md`
13. `docs/adapters/COPILOT_CLI_ADAPTER_NOTE.md`
14. `docs/concepts/SKILL0_COLLABORATION_VISION.md`

## 2. Resource Catalog

현재 registry 는 다음 shared resource types 를 다룹니다:

| Type | Logical root | Purpose |
|---|---|---|
| `skills` | `/registry/skills` | 여러 CLI 가 함께 쓸 수 있는 skill 정의 |
| `mcp` | `/registry/mcp` | canonical MCP definitions |
| `agents` | `/registry/agents` | 공용 agent 지침과 persona 정의 |
| `workflow` | `/registry/workflow` | 공용 흐름, runbook, planning guidance |

다음 항목은 shared resource type 이 아닙니다:

| Area | Logical root | Role |
|---|---|---|
| `operations state` | `/operations` | inventories, backups, drift logs, history records |

## 3. Starter Catalog Shape

최소 catalog entry 에는 적어도 다음이 있어야 합니다:

- `id`
- `type`
- `canonical_location`
- `status`

추가 권장 항목:

- `source_of_truth`
- `supported_clis`
- `delivery_guidance`

전체 필드 규칙은 `RESOURCE_SPEC.md` 를 참고하세요.

## 4. Current Catalog Entries

### Review Shortlist

현재 외부 review 주 집합은 전체 후보군이 아니라 [docs/reviews/ESSENTIAL_SKILLS_SHORTLIST.md](docs/reviews/ESSENTIAL_SKILLS_SHORTLIST.md) 의 `8 + 4` 선별 skills 를 기준으로 합니다.

`2026-04-18` 기준으로 authoring tree 내부의 `registry/skills/` 에는 `48` 개의 skill 디렉터리가 있습니다. 아래 표는 review-facing catalog excerpt 이며 전체 inventory dump 는 아닙니다.

### Review Package

외부 reviewer 용 자료를 준비하려면 [docs/reviews/EXTERNAL_REVIEW_PACKAGE.md](docs/reviews/EXTERNAL_REVIEW_PACKAGE.md) 를 진입점으로 사용하고, `local/scripts/export-review-package.ps1` 로 재생성 가능한 review package 를 만드세요.

reviewer 에게 가장 짧은 진입점을 바로 주고 싶다면 먼저 다음을 보세요:

- [docs/reviews/EXTERNAL_REVIEW_COVER_NOTE.md](docs/reviews/EXTERNAL_REVIEW_COVER_NOTE.md)
- [docs/reviews/EXTERNAL_REVIEW_HIGHLIGHTS.md](docs/reviews/EXTERNAL_REVIEW_HIGHLIGHTS.md)

### Template Release

깨끗한 starter package 를 만들려면 [TEMPLATE_RELEASE_PACKAGE.md](TEMPLATE_RELEASE_PACKAGE.md) 를 읽고 `local/scripts/export-template-package.ps1` 를 사용하세요.

export 된 starter package 를 검증하려면 `local/scripts/verify-template-package.ps1` 를 사용하세요.

authoring repo 의 tracked shared surfaces 에 live workspace metadata 가 섞이지 않았는지 먼저 확인하려면 `local/scripts/verify-workspace-boundaries.ps1` 를 사용하세요.

향후 push suitability 논의 전에 로컬 보고서를 만들려면 `local/scripts/get-publishability-report.ps1` 를 사용하세요.

shared metadata 탐지 규칙을 조정하거나 규칙 사례를 이해하려면 먼저 [WORKSPACE_SENSITIVE_METADATA_RULES.md](WORKSPACE_SENSITIVE_METADATA_RULES.md) 를 읽고, 그 다음 `local/scripts/validate-workspace-sensitive-metadata-rules.ps1` 를 사용하세요.

현재 repo 를 바로 새로운 starter project 로 재구성하려면 [REBUILD_AS_NEW_PROJECT.md](REBUILD_AS_NEW_PROJECT.md) 를 읽고 다음을 사용하세요:

- `local/scripts/export-rebuild-project.ps1`
- `local/scripts/verify-rebuild-project.ps1`

새 머신에서 첫 initialize → verify 를 완료하려면 다음을 우선 사용하세요:

- `local/scripts/bootstrap.py`
- `local/scripts/verify-bootstrap.py`

### Related Concept Notes

`Copilot CLI` 의 현재 repo-level bootstrap baseline, 제약, 이후 cross-platform 검증 방향을 이해하려면 [docs/adapters/COPILOT_CLI_ADAPTER_NOTE.md](docs/adapters/COPILOT_CLI_ADAPTER_NOTE.md) 를 보세요.

`UniText` 가 `skill-0` 와 어떻게 협력할 수 있는지 평가하려면 [docs/concepts/SKILL0_COLLABORATION_VISION.md](docs/concepts/SKILL0_COLLABORATION_VISION.md) 를 보세요.

### Skills

| `id` | Tier | `canonical_location` | `status` |
|---|---|---|---|
| `pdf` | Core 8 | `/registry/skills/pdf` | `active` |
| `docx` | Core 8 | `/registry/skills/docx` | `active` |
| `xlsx` | Core 8 | `/registry/skills/xlsx` | `active` |
| `pptx` | Core 8 | `/registry/skills/pptx` | `active` |
| `mcp-builder` | Core 8 | `/registry/skills/mcp-builder` | `active` |
| `skill-creator` | Core 8 | `/registry/skills/skill-creator` | `active` |
| `webapp-testing` | Core 8 | `/registry/skills/webapp-testing` | `active` |
| `doc-coauthoring` | Core 8 | `/registry/skills/doc-coauthoring` | `active` |
| `frontend-design` | Expansion 4 | `/registry/skills/frontend-design` | `active` |
| `web-artifacts-builder` | Expansion 4 | `/registry/skills/web-artifacts-builder` | `active` |
| `internal-comms` | Expansion 4 | `/registry/skills/internal-comms` | `active` |
| `theme-factory` | Expansion 4 | `/registry/skills/theme-factory` | `active` |

### Workspace-Specific Skills

다음 skills 는 shared registry 에 존재하지만 현재 외부 review 의 `8 + 4` shortlist 에는 포함되지 않습니다.

| `id` | Tier | `canonical_location` | `status` |
|---|---|---|---|
| `cloudflare` | Workspace | `/registry/skills/cloudflare` | `active` |
| `wrangler` | Workspace | `/registry/skills/wrangler` | `active` |
| `building-mcp-server-on-cloudflare` | Workspace | `/registry/skills/building-mcp-server-on-cloudflare` | `active` |
| `cloudflare-governance` | Workspace | `/registry/skills/cloudflare-governance` | `active` |
| `cloudflare-access-mcp` | Workspace | `/registry/skills/cloudflare-access-mcp` | `active` |
| `cloudflare-edge-security` | Workspace | `/registry/skills/cloudflare-edge-security` | `active` |
| `cloudflare-runtime-sync` | Workspace | `/registry/skills/cloudflare-runtime-sync` | `active` |
| `cloudflare-tunnel-dns` | Workspace | `/registry/skills/cloudflare-tunnel-dns` | `active` |
| `cloudflare-zerotrust-device` | Workspace | `/registry/skills/cloudflare-zerotrust-device` | `active` |

### Workflow

| Field | Value |
|---|---|
| `id` | `claude-plans` |
| `type` | `workflow` |
| `canonical_location` | `/registry/workflow/claude-plans` |
| `status` | `draft` |
| `source_of_truth` | `/registry/workflow/claude-plans` |
| `supported_clis` | `claude` |
| `delivery_guidance` | Use workflow adapter or project-local plan mapping depending on CLI capability. |

### MCP

| Field | Value |
|---|---|
| `id` | `claude-project-mcp-seed` |
| `type` | `mcp` |
| `canonical_location` | `/registry/mcp/claude-project-mcp-seed` |
| `status` | `active-baseline` |
| `source_of_truth` | `/registry/mcp/claude-project-mcp-seed/definition.json` |
| `supported_clis` | `claude, codex, copilot` |
| `delivery_guidance` | Bootstrap writes a project `.mcp.json`, a Codex native-config entry, and a Copilot `~/.copilot/mcp-config.json` entry pointing to the bundled read-only MCP server. |

### Agents

| Field | Value |
|---|---|
| `id` | `registry-curator` |
| `type` | `agents` |
| `canonical_location` | `/registry/agents/registry-curator` |
| `status` | `active` |
| `source_of_truth` | `/registry/agents/registry-curator/AGENT.md` |
| `supported_clis` | `claude, codex, gemini` |
| `delivery_guidance` | Use as a shared agent persona for review and adoption tasks; actual wiring depends on CLI capability. |

## 5. Example Catalog Entries

### Example: Skill

| Field | Value |
|---|---|
| `id` | `example-skill` |
| `type` | `skills` |
| `canonical_location` | `/registry/skills/example-skill` |
| `status` | `draft` |
| `source_of_truth` | `/registry/skills/example-skill/SKILL.md` |
| `supported_clis` | `undocumented` |
| `delivery_guidance` | Use the skills adapter; resolved mode depends on CLI capabilities and local environment. |

### Example: MCP Definition

| Field | Value |
|---|---|
| `id` | `example-mcp` |
| `type` | `mcp` |
| `canonical_location` | `/registry/mcp/example-mcp` |
| `status` | `draft` |
| `source_of_truth` | `/registry/mcp/example-mcp/definition` |
| `supported_clis` | `undocumented` |
| `delivery_guidance` | Register through the MCP adapter; the final delivery mode depends on CLI capabilities and local environment. |

## 6. Discovery Rules

`INDEX.md` 가 답하는 것은:

- 여기 어떤 resource 가 있는가
- 각 resource 의 논리 위치는 어디인가
- 어떤 규격서나 운영 문서를 봐야 하는가

`INDEX.md` 가 직접 답하지 않는 것은:

- 특정 플랫폼의 절대 경로
- 최종적으로 해석된 delivery mode
- 특정 author workspace 의 로컬 설정
- local authoring plans, review notes, live workspace baselines 를 어디에 두는가; 이 부분은 `DOCUMENT_PLACEMENT_POLICY.md` 를 참고하세요

## 7. How To Use This Baseline

### For Humans

1. 먼저 `VISION.md` 를 읽기
2. `INDEX.md` 로 자신의 starter catalog 만들기
3. `RESOURCE_SPEC.md` 로 resource 필드 정의하기
4. `OPERATIONS.md` 로 플랫폼 / CLI 연결 방식 정의하기

### For AI Agents

1. `INDEX.md` 를 discovery 진입점으로 사용하기
2. schema 가 필요하면 `RESOURCE_SPEC.md` 읽기
3. delivery / mutation 이 필요하면 `OPERATIONS.md` 읽기
4. 단일 배포 환경의 경로를 규격 진실로 취급하지 않기
