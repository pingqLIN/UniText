from __future__ import annotations

import argparse
import json
import sys
from gcp_shared import resolve_gcloud_command, run_gcloud, summarize_enabled_services


def build_inventory(project_id: str | None, include_services: bool) -> dict[str, Any]:
    inventory: dict[str, Any] = {
        "auth": run_gcloud(["auth", "list", "--format=json"]),
        "config": run_gcloud(["config", "list", "--format=json"]),
        "projects": run_gcloud(["projects", "list", "--format=json"]),
        "billingAccounts": run_gcloud(["billing", "accounts", "list", "--format=json"]),
    }

    if project_id:
        inventory["targetProject"] = {
            "projectId": project_id,
            "details": run_gcloud(["projects", "describe", project_id, "--format=json"]),
            "billing": run_gcloud(["billing", "projects", "describe", project_id, "--format=json"]),
            "serviceAccounts": run_gcloud(
                ["iam", "service-accounts", "list", f"--project={project_id}", "--format=json"]
            ),
        }
        if include_services:
            services_response = run_gcloud(
                ["services", "list", "--enabled", f"--project={project_id}", "--format=json"]
            )
            inventory["targetProject"]["enabledServices"] = summarize_enabled_services(
                services_response
            )

    return inventory


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inventory the local gcloud context for GCP service-adoption decisions."
    )
    parser.add_argument("--project", help="Target project ID to inspect in more detail.")
    parser.add_argument(
        "--include-services",
        action="store_true",
        help="Include enabled APIs for the target project.",
    )
    args = parser.parse_args()

    if resolve_gcloud_command() is None:
        print(json.dumps({"ok": False, "error": "gcloud not found on PATH"}, indent=2))
        return 1

    inventory = build_inventory(args.project, args.include_services)
    print(json.dumps(inventory, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
