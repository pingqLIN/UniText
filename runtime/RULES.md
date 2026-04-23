# Runtime Rules

這份文件整併 consumer agent 最常查的低噪音規則。需要 deeper source-of-truth 時，再跟著這裡的指向回到 `registry/` 或 root docs。

## 1. Source Hygiene

- 一般任務先讀 `runtime/*`，不是 `registry/*`
- `registry/*` 只作 canonical source、adoption、template、rebuild、或 runtime debug
- `local/*` 只用來理解 machine-local wiring，不作 shared truth
- `ops/*` 只看 evidence / reports / generated state，不作 canonical answer

## 2. Publish Boundary

- 未經使用者明確要求，不可 push、upload、post、publish repo 內容
- private repo 不等於自動可發布
- 若要先判斷 push suitability，走 publishability / boundary verify 路線

Deeper source:

- `../AGENTS.md`
- `../NO_PUBLISH_POLICY.md`

## 3. Secret And Env Boundary

- shared surface 不得包含 secret value
- shared env baseline 不得包含 local-only environment habit
- local-only habit 包含 `localhost`、本機 callback URL、作者機器路徑、debug override、測試 fallback
- 若文件同時需要 shared guidance 與 live local baseline，必須拆成 sanitized/shared 與 local/live pair

Deeper source:

- `../SECRET_HANDLING_GUIDELINES.md`
- `../WORKSPACE_SENSITIVE_METADATA_RULES.md`

## 4. Placement Rule

- 描述 shared truth 的內容放 tracked shared layer
- 描述單一作者工作區現況的內容放 `local/docs/`
- generated state、audit evidence、export output 放 `ops/`

Deeper source:

- `../DOCUMENT_PLACEMENT_POLICY.md`

## 5. Delivery Contract

- `registry/` 是 canonical source，不是 consumer runtime surface
- `runtime/` 是 tracked runtime read model
- `bootstrap.py` 應把 consumer targets 對齊到 `runtime/skills`
- Codex 的 `skills_path` 應指向 machine-local target，而不是 repo 內 `registry/skills`

Deeper source:

- `../OPERATIONS.md`
- `../local/scripts/bootstrap.py`
- `../local/scripts/verify-bootstrap.py`

## 6. Bootstrap And Verify

first-run 建議順序：

1. `python local/scripts/bootstrap.py --dry-run`
2. `python local/scripts/bootstrap.py --force`
3. `python local/scripts/verify-bootstrap.py`

若要重建 `runtime/`：

1. `python local/scripts/build-runtime-layer.py --write`

## 7. Release Hygiene

- template package 不得夾帶 machine-specific absolute paths
- template package 不得夾帶 live Cloudflare baseline refs、真實 hostnames、真實 IDs、runtime 路徑
- shared env baseline 不得夾帶 local-only environment habit

Deeper source:

- `../TEMPLATE_RELEASE_CHECKLIST.md`
- `../TEMPLATE_RELEASE_PACKAGE.md`
