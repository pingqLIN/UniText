from __future__ import annotations

import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from gcp_budget_api import build_budget_payload, extract_service_disabled_context


def test_build_budget_payload_specified_amount() -> None:
    payload = build_budget_payload(
        display_name="Example Budget",
        budget_scope_project="sample-project",
        amount_units=125.5,
        calendar_period="MONTH",
        thresholds=[0.5, 0.8, 1.0],
        billing_account="010E2C-B13825-AE66CC",
    )

    assert payload["displayName"] == "Example Budget"
    assert payload["budgetFilter"]["projects"] == ["projects/sample-project"]
    assert payload["amount"]["specifiedAmount"]["units"] == 125
    assert payload["amount"]["specifiedAmount"]["nanos"] == 500000000
    assert len(payload["thresholdRules"]) == 3
    assert payload["_meta"]["billingAccount"] == "billingAccounts/010E2C-B13825-AE66CC"


def test_build_budget_payload_last_period_amount() -> None:
    payload = build_budget_payload(
        display_name="Example Budget",
        budget_scope_project="sample-project",
        amount_units=None,
        calendar_period="QUARTER",
        thresholds=[0.8],
        billing_account="billingAccounts/010E2C-B13825-AE66CC",
    )

    assert payload["amount"] == {"lastPeriodAmount": {}}
    assert payload["budgetFilter"]["calendarPeriod"] == "QUARTER"


def test_extract_service_disabled_context() -> None:
    result = {
        "ok": False,
        "status": 403,
        "error": {
            "error": {
                "details": [
                    {
                        "reason": "SERVICE_DISABLED",
                        "metadata": {
                            "service": "billingbudgets.googleapis.com",
                            "activationUrl": "https://example.test/enable",
                            "consumer": "projects/sample-project",
                        },
                    }
                ]
            }
        },
    }

    context = extract_service_disabled_context(result, "billingbudgets.googleapis.com")

    assert context == {
        "service": "billingbudgets.googleapis.com",
        "activationUrl": "https://example.test/enable",
        "consumer": "projects/sample-project",
    }
