from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from budget_plan_template import build_budget_plan_artifact
from gcp_budget_api import build_budget_preflight
from gcp_inventory import build_inventory
from gcp_project_readiness import readiness_report
from gcp_shared import SERVICE_CATALOG, recommend_service, resolve_gcloud_command, score_project_fit


def summarize_project_candidate(project: dict[str, Any], service_key: str) -> dict[str, Any]:
    project_id = project["projectId"]
    readiness = readiness_report(project_id, service_key)
    billing_info = readiness["billing"].get("data") or {}
    service_accounts = readiness["serviceAccounts"].get("data") or []
    fit = score_project_fit(
        billing_enabled=bool(billing_info.get("billingEnabled")),
        missing_apis=readiness["readiness"]["missingApis"],
        missing_labels=readiness["readiness"]["missingLabels"],
        service_account_count=len(service_accounts),
    )
    return {
        "projectId": project_id,
        "projectName": project.get("name", project_id),
        "fit": fit,
        "readiness": readiness["readiness"],
    }


def choose_candidate_projects(
    inventory: dict[str, Any], explicit_project: str | None, scan_projects: int
) -> list[dict[str, Any]]:
    projects = inventory["projects"].get("data") or []
    if explicit_project:
        return [project for project in projects if project.get("projectId") == explicit_project]

    current_project = (
        ((inventory.get("config") or {}).get("data") or {}).get("core") or {}
    ).get("project")
    if current_project:
        prioritized = [project for project in projects if project.get("projectId") == current_project]
        if scan_projects <= 0:
            return prioritized
        others = [project for project in projects if project.get("projectId") != current_project]
        return prioritized + others[:scan_projects]

    limit = max(1, scan_projects) if scan_projects > 0 else 1
    return projects[:limit]


def build_setup_checklist(best_candidate: dict[str, Any] | None, chosen_service: str) -> dict[str, Any]:
    service_meta = SERVICE_CATALOG[chosen_service]
    readiness = (best_candidate or {}).get("readiness") or {}
    missing_apis = readiness.get("missingApis") or []
    missing_labels = readiness.get("missingLabels") or []

    return {
        "apis": service_meta["apis"],
        "missingApis": missing_apis,
        "iam": service_meta["iamRoles"],
        "secrets": ["Use Secret Manager for production secrets"] if chosen_service != "secret-manager" else [],
        "networking": service_meta["networking"],
        "observability": service_meta["observability"],
        "labels": service_meta["labels"],
        "missingLabels": missing_labels,
    }


def build_cost_and_budget_plan(
    capability: str,
    chosen_service: str,
    chosen_project: str | None,
    billing_account: str | None,
    billing_owner: str | None,
    technical_owner: str | None,
    monthly_low: float | None,
    monthly_high: float | None,
) -> dict[str, Any]:
    estimate: dict[str, Any] = {
        "currency": "USD",
        "monthlyLow": monthly_low,
        "monthlyHigh": monthly_high,
        "confidence": "directional" if monthly_low is not None or monthly_high is not None else "unknown",
    }

    budget_amount = None
    if monthly_low is not None and monthly_high is not None:
        budget_amount = round(((monthly_low + monthly_high) / 2) * 1.25, 2)

    budget_plan = None
    if (
        billing_owner
        and technical_owner
        and monthly_low is not None
        and monthly_high is not None
    ):
        budget_plan = build_budget_plan_artifact(
            capability=capability,
            service=SERVICE_CATALOG[chosen_service]["displayName"],
            monthly_low=monthly_low,
            monthly_high=monthly_high,
            currency="USD",
            billing_owner=billing_owner,
            technical_owner=technical_owner,
        )

    budget_api_preflight = None
    if billing_account and chosen_project:
        budget_api_preflight = build_budget_preflight(billing_account, chosen_project)

    result = {
        "billingDrivers": SERVICE_CATALOG[chosen_service]["billingDrivers"],
        "estimate": estimate,
        "recommendedBudget": budget_amount,
        "budgetThresholdsPercent": [50, 80, 100],
        "billingOwner": billing_owner,
        "budgetPlanArtifact": budget_plan,
        "budgetApiPreflight": budget_api_preflight,
    }
    if chosen_project:
        result["apiUserProject"] = chosen_project
    if billing_account:
        result["billingAccount"] = billing_account
    return result


def build_tracking_plan(technical_owner: str | None) -> dict[str, Any]:
    return {
        "technicalOwner": technical_owner,
        "reviewCadence": "monthly",
        "metrics": [
            "usage volume",
            "error rate",
            "monthly spend",
            "budget burn percentage",
        ],
        "riskNotes": [],
    }


def build_assessment(
    capability: str,
    service_key: str | None,
    project_id: str | None,
    scan_projects: int,
    billing_owner: str | None,
    technical_owner: str | None,
    monthly_low: float | None,
    monthly_high: float | None,
) -> dict[str, Any]:
    recommendation = recommend_service(capability)
    chosen_service = service_key or recommendation["primaryService"]
    inventory = build_inventory(project_id, include_services=bool(project_id))
    billing_accounts = inventory["billingAccounts"].get("data") or []
    open_billing_accounts = [account["name"] for account in billing_accounts if account.get("open")]
    candidates = choose_candidate_projects(inventory, project_id, scan_projects)
    candidate_reports = [summarize_project_candidate(candidate, chosen_service) for candidate in candidates]
    candidate_reports.sort(key=lambda item: item["fit"]["score"], reverse=True)

    best_candidate = candidate_reports[0] if candidate_reports else None
    if best_candidate:
        reuse_decision = best_candidate["fit"]["decision"]
        chosen_project = best_candidate["projectId"]
    else:
        reuse_decision = "new-project"
        chosen_project = project_id or "new-project-required"

    chosen_billing_account = open_billing_accounts[0] if open_billing_accounts else None

    return {
        "requestedCapability": capability,
        "recommendedService": {
            "service": chosen_service,
            "displayName": SERVICE_CATALOG[chosen_service]["displayName"],
            "alternatives": recommendation["alternatives"],
        },
        "existingProjectFit": {
            "activeAccount": (((inventory.get("config") or {}).get("data") or {}).get("core") or {}).get(
                "account"
            ),
            "activeProject": (((inventory.get("config") or {}).get("data") or {}).get("core") or {}).get(
                "project"
            ),
            "projectCount": len(inventory["projects"].get("data") or []),
            "openBillingAccounts": open_billing_accounts,
            "candidateProjects": candidate_reports,
        },
        "reuseOrNewProjectDecision": {
            "projectId": chosen_project,
            "decision": reuse_decision,
            "notes": (best_candidate or {}).get("fit", {}).get("notes", []),
        },
        "requiredSetupChecklist": build_setup_checklist(best_candidate, chosen_service),
        "costAndBudgetPlan": build_cost_and_budget_plan(
            capability,
            chosen_service,
            chosen_project if chosen_project != "new-project-required" else None,
            chosen_billing_account,
            billing_owner,
            technical_owner,
            monthly_low,
            monthly_high,
        ),
        "ongoingTrackingPlan": build_tracking_plan(technical_owner),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run an end-to-end GCP service-adoption assessment for a project capability."
    )
    parser.add_argument("--capability", required=True, help="Requested business or technical capability.")
    parser.add_argument(
        "--service",
        choices=sorted(SERVICE_CATALOG.keys()),
        help="Optional explicit service override.",
    )
    parser.add_argument("--project", help="Optional project ID to force assessment against.")
    parser.add_argument(
        "--scan-projects",
        type=int,
        default=0,
        help="Number of additional projects to compare beyond the active project. Default is 0.",
    )
    parser.add_argument("--billing-owner", help="Optional billing owner for the output artifact.")
    parser.add_argument("--technical-owner", help="Optional technical owner for the output artifact.")
    parser.add_argument("--monthly-low", type=float, help="Optional low-end monthly estimate.")
    parser.add_argument("--monthly-high", type=float, help="Optional high-end monthly estimate.")
    args = parser.parse_args()

    if resolve_gcloud_command() is None:
        print(json.dumps({"ok": False, "error": "gcloud not found on PATH"}, indent=2))
        return 1

    assessment = build_assessment(
        args.capability,
        args.service,
        args.project,
        args.scan_projects,
        args.billing_owner,
        args.technical_owner,
        args.monthly_low,
        args.monthly_high,
    )
    print(json.dumps(assessment, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
