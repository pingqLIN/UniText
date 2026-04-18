# Cloudflare Script Catalog

This file is the discovery layer for reusable Cloudflare scripts in this workspace.

| Script | Owner skill | Purpose | Inputs | Output | Notes |
| --- | --- | --- | --- | --- | --- |
| `cloudflare-governance/scripts/inventory-cloudflare-scope.ps1` | `cloudflare-governance` | Inventory visible Cloudflare account, zone, tunnel, Access app, and DNS scope before routing deeper | API token or Global API Key plus email, optional account/zone hints | JSON inventory plus markdown summary | Read-only discovery layer for the single-entry workflow. |
| `cloudflare-zerotrust-device/scripts/verify-cloudflare-auth.ps1` | `cloudflare-zerotrust-device` | Verify API token, Global API Key, or tunnel-only fallback capability | Optional token, Global API Key, email, account ID | Console summary of auth mode, capability class, and optional tunnel list | Never prints full secrets. |
| `cloudflare-zerotrust-device/scripts/collect-cloudflare-zerotrust-baseline.ps1` | `cloudflare-zerotrust-device` | Collect local WARP, routing, WSL, trace, and account-correlation evidence | Optional account ID, output paths, skip network probes | JSON baseline plus markdown summary | Use before making policy claims. |
| `cloudflare-tunnel-dns/scripts/check-tunnel-runtime-alignment.ps1` | `cloudflare-tunnel-dns` | Compare authoring, prod, staging tunnel configs and runtime metadata, then optionally match them against DNS tunnel records from governance inventory | Optional config paths, release metadata paths, optional governance inventory JSON | JSON alignment report plus markdown summary | Read-only drift check for tunnel, ingress, and runtime target alignment. |
| `cloudflare-tunnel-dns/scripts/plan-staging-public-host-activation.ps1` | `cloudflare-tunnel-dns` | Build a read-only activation plan for `tb2-health-staging.colorgeek.co` using release targets and Cloudflare inventory | Governance inventory JSON, release targets path, optional output paths | JSON plan plus markdown summary | Dry-run only. Surfaces DNS mutation need and whether Access requires a policy decision. |

## Catalog Rules

- Keep scripts under the specialist skill that owns the operational knowledge.
- Add the script here only after it has a stable purpose and smoke-test behavior.
- Governance should link to scripts; it should not become the owner of specialist procedures.
