from __future__ import annotations

import argparse
import json
import sys
from gcp_shared import (
    SERVICE_CATALOG,
    extract_enabled_service_names,
    extract_labels,
    resolve_gcloud_command,
    run_gcloud,
)


def readiness_report(project_id: str, service_key: str) -> dict[str, Any]:
    catalog_entry = SERVICE_CATALOG[service_key]
    project = run_gcloud(["projects", "describe", project_id, "--format=json"])
    billing = run_gcloud(["billing", "projects", "describe", project_id, "--format=json"])
    services = run_gcloud(["services", "list", "--enabled", f"--project={project_id}", "--format=json"])
    service_accounts = run_gcloud(
        ["iam", "service-accounts", "list", f"--project={project_id}", "--format=json"]
    )

    enabled_services = extract_enabled_service_names(services)
    labels = extract_labels(project)
    required_labels = catalog_entry["labels"]
    missing_labels = [label for label in required_labels if label not in labels]
    missing_apis = [api for api in catalog_entry["apis"] if api not in enabled_services]

    report = {
        "projectId": project_id,
        "service": {
            "key": service_key,
            "displayName": catalog_entry["displayName"],
        },
        "project": project,
        "billing": billing,
        "serviceAccounts": service_accounts,
        "readiness": {
            "missingApis": missing_apis,
            "presentLabels": labels,
            "missingLabels": missing_labels,
            "requiredIamRoles": catalog_entry["iamRoles"],
            "networkingChecks": catalog_entry["networking"],
            "observabilityChecks": catalog_entry["observability"],
            "billingDrivers": catalog_entry["billingDrivers"],
        },
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check whether a target GCP project is ready to host a chosen managed service."
    )
    parser.add_argument("--project", required=True, help="GCP project ID to inspect.")
    parser.add_argument(
        "--service",
        required=True,
        choices=sorted(SERVICE_CATALOG.keys()),
        help="Managed service profile to evaluate.",
    )
    args = parser.parse_args()

    if resolve_gcloud_command() is None:
        print(json.dumps({"ok": False, "error": "gcloud not found on PATH"}, indent=2))
        return 1

    report = readiness_report(args.project, args.service)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
