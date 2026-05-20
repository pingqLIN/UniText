from __future__ import annotations

import argparse
import json
import sys


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a starter output artifact that matches the skill output contract."
    )
    parser.add_argument("--capability", required=True)
    parser.add_argument("--service", required=True)
    parser.add_argument("--project", required=True)
    parser.add_argument("--decision", required=True, choices=["reuse-existing", "new-project"])
    parser.add_argument("--billing-owner", required=True)
    parser.add_argument("--technical-owner", required=True)
    parser.add_argument("--monthly-low", type=float, default=0.0)
    parser.add_argument("--monthly-high", type=float, default=0.0)
    parser.add_argument("--currency", default="USD")
    args = parser.parse_args()

    report = {
        "requestedCapability": args.capability,
        "recommendedService": args.service,
        "existingProjectFit": {
            "projectId": args.project,
            "decision": args.decision,
            "notes": [],
        },
        "requiredSetupChecklist": {
            "apis": [],
            "iam": [],
            "secrets": [],
            "networking": [],
            "observability": [],
            "labels": [],
        },
        "costAndBudgetPlan": {
            "estimate": {
                "currency": args.currency,
                "monthlyLow": args.monthly_low,
                "monthlyHigh": args.monthly_high,
            },
            "budgetThresholdsPercent": [50, 80, 100],
            "billingOwner": args.billing_owner,
        },
        "ongoingTrackingPlan": {
            "technicalOwner": args.technical_owner,
            "reviewCadence": "monthly",
            "metrics": [],
            "riskNotes": [],
        },
    }

    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
