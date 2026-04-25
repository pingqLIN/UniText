# Runtime Routes

這份文件把常見 intent 映射到最短讀取路徑。

| Intent | First Read | Allowed Next Reads | Do Not Start With |
|---|---|---|---|
| 查簡單治理規則 | `runtime/RULES.md` | 對應 root governance doc | `INDEX.md`, `registry/*` |
| 找技能入口 | `runtime/catalog.json` | `runtime/skills/<id>/SKILL.md` | `registry/skills/*` |
| 找 agent persona | `runtime/catalog.json` | `runtime/agents/<id>/AGENT.md` | `registry/agents/*` |
| 找 workflow 入口 | `runtime/catalog.json` | `runtime/workflow/<id>/WORKFLOW.md` | `registry/workflow/*` |
| 判斷文件放哪一層 | `runtime/RULES.md` | `DOCUMENT_PLACEMENT_POLICY.md` | `ops/*` |
| 判斷 secret / env 邊界 | `runtime/RULES.md` | `SECRET_HANDLING_GUIDELINES.md` | 任意 `.env` 樣板全文 |
| 查 bootstrap / verify | `runtime/RULES.md` | `local/scripts/bootstrap.py`, `local/scripts/verify-bootstrap.py` | `README.md` |
| 查 push / publish boundary | `runtime/RULES.md` | `AGENTS.md`, `NO_PUBLISH_POLICY.md` | `EXTERNAL_REVIEW_*` |
| curator / adopt 任務 | `runtime/agents/registry-curator/AGENT.md` | linked registry refs | `runtime/skills/*` |
| template / rebuild | `runtime/RULES.md` | `TEMPLATE_RELEASE_PACKAGE.md`, `REBUILD_AS_NEW_PROJECT.md` | `ops/template-package/*` |

## Hot Paths

常用高頻入口：

- `runtime/RULES.md`
- `runtime/catalog.json`
- `runtime/skills/env/SKILL.md`
- `runtime/skills/cloudflare-governance/SKILL.md`
- `runtime/skills/doc-coauthoring/SKILL.md`
- `runtime/agents/registry-curator/AGENT.md`
- `runtime/validation/tasks.md`

## Fallback Rule

如果 `runtime/*` 無法回答：

1. 先確認是不是 routing 缺口
2. 再依 `source_of_truth` 或 rewritten link 進 `registry/*`
3. 若是 runtime projection 缺漏，記錄到 `runtime/validation/` 或 `ops/reports/`
