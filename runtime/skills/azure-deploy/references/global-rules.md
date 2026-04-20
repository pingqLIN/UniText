---
runtime_projection: true
source_of_truth: registry/skills/azure-deploy/references/global-rules.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/azure-deploy/references/global-rules.md`
> Source of truth: `registry/skills/azure-deploy/references/global-rules.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Global Rules

> **MANDATORY** — These rules apply to ALL skills. Violations are unacceptable.

## Rule 1: Destructive Actions Require User Confirmation

⛔ **ALWAYS use `ask_user`** before ANY destructive action.

### What is Destructive?

| Category | Examples |
|----------|----------|
| **Delete** | `az group delete`, `azd down`, `rm -rf`, delete resource |
| **Overwrite** | Replace existing files, overwrite config, reset settings |
| **Irreversible** | Purge Key Vault, delete storage account, drop database |
| **Cost Impact** | Provision expensive resources, scale up significantly |
| **Security** | Expose secrets, change access policies, modify RBAC |

### How to Confirm

```
ask_user(
  question: "This will permanently delete resource group 'rg-myapp'. Continue?",
  choices: ["Yes, delete it", "No, cancel"]
)
```

### No Exceptions

- Do NOT assume user wants to delete/overwrite
- Do NOT proceed based on "the user asked to deploy" (deploy ≠ delete old)
- Do NOT batch destructive actions without individual confirmation

---

## Rule 2: Never Assume Subscription or Location

⛔ **ALWAYS use `ask_user`** to confirm:
- Azure subscription (show actual name and ID)
- Azure region/location

See [Pre-Deploy Checklist](pre-deploy-checklist.md).
