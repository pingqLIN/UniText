from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from gcp_billing_rest import append_query, billing_request


def normalize_billing_account(billing_account: str) -> str:
    if billing_account.startswith("billingAccounts/"):
        return billing_account
    return f"billingAccounts/{billing_account}"


def extract_service_disabled_context(
    result: dict[str, Any], expected_service: str
) -> dict[str, str] | None:
    error = result.get("error")
    if not isinstance(error, dict):
        return None

    nested_error = error.get("error")
    if not isinstance(nested_error, dict):
        return None

    details = nested_error.get("details")
    if not isinstance(details, list):
        return None

    for detail in details:
        if not isinstance(detail, dict):
            continue
        metadata = detail.get("metadata")
        if not isinstance(metadata, dict):
            continue
        service_name = metadata.get("service")
        reason = detail.get("reason")
        if reason == "SERVICE_DISABLED" and service_name == expected_service:
            return {
                "service": expected_service,
                "activationUrl": str(metadata.get("activationUrl", "")),
                "consumer": str(metadata.get("consumer", "")),
            }

    return None


def build_budget_payload(
    *,
    display_name: str,
    budget_scope_project: str,
    amount_units: float | None,
    calendar_period: str,
    thresholds: list[float],
    billing_account: str,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "displayName": display_name,
        "budgetFilter": {
            "projects": [f"projects/{budget_scope_project}"],
            "calendarPeriod": calendar_period,
        },
        "thresholdRules": [
            {"thresholdPercent": threshold, "spendBasis": "CURRENT_SPEND"} for threshold in thresholds
        ],
        "allUpdatesRule": {},
    }

    if amount_units is None:
        payload["amount"] = {"lastPeriodAmount": {}}
    else:
        units = int(amount_units)
        nanos = int(round((amount_units - units) * 1_000_000_000))
        payload["amount"] = {"specifiedAmount": {"currencyCode": "USD", "units": units, "nanos": nanos}}

    payload["_meta"] = {"billingAccount": normalize_billing_account(billing_account)}
    return payload


def list_budgets(billing_account: str, api_user_project: str) -> dict[str, Any]:
    account_name = normalize_billing_account(billing_account)
    url = f"https://billingbudgets.googleapis.com/v1/{account_name}/budgets"
    return billing_request(method="GET", url=url, api_user_project=api_user_project)


def create_budget(
    billing_account: str, api_user_project: str, payload: dict[str, Any], apply: bool
) -> dict[str, Any]:
    account_name = normalize_billing_account(billing_account)
    sanitized_payload = {key: value for key, value in payload.items() if key != "_meta"}
    if not apply:
        return {"ok": True, "mode": "dry-run", "url": f"https://billingbudgets.googleapis.com/v1/{account_name}/budgets", "payload": sanitized_payload}

    url = f"https://billingbudgets.googleapis.com/v1/{account_name}/budgets"
    return billing_request(
        method="POST",
        url=url,
        api_user_project=api_user_project,
        body=sanitized_payload,
    )


def build_budget_preflight(billing_account: str, api_user_project: str) -> dict[str, Any]:
    result = list_budgets(billing_account, api_user_project)
    disabled_context = extract_service_disabled_context(result, "billingbudgets.googleapis.com")
    if result.get("ok"):
        return {
            "ok": True,
            "ready": True,
            "billingAccount": normalize_billing_account(billing_account),
            "apiUserProject": api_user_project,
            "checks": {"budgetApiEnabled": True},
            "budgetsVisible": len(result.get("data", {}).get("budgets", [])),
        }

    if disabled_context is not None:
        return {
            "ok": False,
            "ready": False,
            "billingAccount": normalize_billing_account(billing_account),
            "apiUserProject": api_user_project,
            "checks": {"budgetApiEnabled": False},
            "remediation": {
                "enableApiCommand": (
                    f"gcloud services enable billingbudgets.googleapis.com --project {api_user_project}"
                ),
                "activationUrl": disabled_context["activationUrl"],
            },
            "originalError": result,
        }

    return {
        "ok": False,
        "ready": False,
        "billingAccount": normalize_billing_account(billing_account),
        "apiUserProject": api_user_project,
        "checks": {"budgetApiEnabled": None},
        "originalError": result,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="List budgets or build/create Cloud Billing Budget API payloads."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List budgets for a billing account.")
    list_parser.add_argument("--billing-account", required=True)
    list_parser.add_argument("--api-user-project", required=True)

    preflight_parser = subparsers.add_parser(
        "preflight",
        help="Check whether the Budget API is ready for the chosen api-user-project.",
    )
    preflight_parser.add_argument("--billing-account", required=True)
    preflight_parser.add_argument("--api-user-project", required=True)

    payload_parser = subparsers.add_parser("payload", help="Generate a budget payload.")
    payload_parser.add_argument("--billing-account", required=True)
    payload_parser.add_argument("--display-name", required=True)
    payload_parser.add_argument("--budget-scope-project", required=True)
    payload_parser.add_argument("--amount-units", type=float)
    payload_parser.add_argument("--calendar-period", default="MONTH")
    payload_parser.add_argument("--thresholds", default="0.5,0.8,1.0")

    create_parser = subparsers.add_parser("create", help="Create a budget or print the request body.")
    create_parser.add_argument("--billing-account", required=True)
    create_parser.add_argument("--api-user-project", required=True)
    create_parser.add_argument("--display-name", required=True)
    create_parser.add_argument("--budget-scope-project", required=True)
    create_parser.add_argument("--amount-units", type=float)
    create_parser.add_argument("--calendar-period", default="MONTH")
    create_parser.add_argument("--thresholds", default="0.5,0.8,1.0")
    create_parser.add_argument("--apply", action="store_true", help="Actually call the Budget API.")

    args = parser.parse_args()

    if args.command == "list":
        result = list_budgets(args.billing_account, args.api_user_project)
        print(json.dumps(result, indent=2))
        return 0 if result.get("ok") else 1

    if args.command == "preflight":
        result = build_budget_preflight(args.billing_account, args.api_user_project)
        print(json.dumps(result, indent=2))
        return 0 if result.get("ready") else 1

    thresholds = [float(item.strip()) for item in args.thresholds.split(",") if item.strip()]
    payload = build_budget_payload(
        display_name=args.display_name,
        budget_scope_project=args.budget_scope_project,
        amount_units=args.amount_units,
        calendar_period=args.calendar_period,
        thresholds=thresholds,
        billing_account=args.billing_account,
    )

    if args.command == "payload":
        print(json.dumps(payload, indent=2))
        return 0

    result = create_budget(args.billing_account, args.api_user_project, payload, args.apply)
    print(json.dumps(result, indent=2))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
