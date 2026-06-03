from __future__ import annotations

import argparse
import json
import math
import sys
from typing import Any


def build_budget_plan_artifact(
    *,
    capability: str,
    service: str,
    monthly_low: float,
    monthly_high: float,
    currency: str,
    billing_owner: str,
    technical_owner: str,
) -> dict[str, Any]:
    midpoint = (monthly_low + monthly_high) / 2
    recommended_budget = math.ceil(midpoint * 1.25)
    return {
        "capability": capability,
        "service": service,
        "estimate": {
            "currency": currency,
            "monthlyLow": monthly_low,
            "monthlyHigh": monthly_high,
            "monthlyMidpoint": round(midpoint, 2),
        },
        "budgetPolicy": {
            "recommendedBudget": recommended_budget,
            "thresholdsPercent": [50, 80, 100],
            "billingOwner": billing_owner,
            "technicalOwner": technical_owner,
            "reviewCadence": "monthly",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a starter budget-governance artifact for a GCP feature rollout."
    )
    parser.add_argument("--capability", required=True, help="Business capability or feature name.")
    parser.add_argument("--service", required=True, help="Chosen Google Cloud service.")
    parser.add_argument("--monthly-low", type=float, required=True, help="Lower monthly estimate.")
    parser.add_argument("--monthly-high", type=float, required=True, help="Upper monthly estimate.")
    parser.add_argument("--currency", default="USD")
    parser.add_argument("--billing-owner", required=True)
    parser.add_argument("--technical-owner", required=True)
    args = parser.parse_args()

    payload = build_budget_plan_artifact(
        capability=args.capability,
        service=args.service,
        monthly_low=args.monthly_low,
        monthly_high=args.monthly_high,
        currency=args.currency,
        billing_owner=args.billing_owner,
        technical_owner=args.technical_owner,
    )

    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
