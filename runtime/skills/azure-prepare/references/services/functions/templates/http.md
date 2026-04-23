---
runtime_projection: true
source_of_truth: registry/skills/azure-prepare/references/services/functions/templates/http.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/azure-prepare/references/services/functions/templates/http.md`
> Source of truth: `registry/skills/azure-prepare/references/services/functions/templates/http.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# HTTP Function Templates

Default templates for HTTP-triggered Azure Functions. Use when no specific integration is detected.

## Templates by Runtime

| Runtime | Template |
|---------|----------|
| C# (.NET) | `azd init -t functions-quickstart-dotnet-azd` |
| JavaScript | `azd init -t functions-quickstart-javascript-azd` |
| TypeScript | `azd init -t functions-quickstart-typescript-azd` |
| Python | `azd init -t functions-quickstart-python-http-azd` |
| Java | `azd init -t azure-functions-java-flex-consumption-azd` |
| PowerShell | `azd init -t functions-quickstart-powershell-azd` |

**Browse all:** [Awesome AZD Functions](https://azure.github.io/awesome-azd/?tags=functions)

## Evaluation Results

| Path | Description |
|------|-------------|
| [base/eval/summary.md](base/eval/summary.md) | Base HTTP template evaluation summary |
| [base/eval/python.md](base/eval/python.md) | Python evaluation results |
