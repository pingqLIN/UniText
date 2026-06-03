from __future__ import annotations

import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import gcp_adoption_assess


def test_build_assessment_includes_budget_artifact_and_preflight(monkeypatch) -> None:
    def fake_build_inventory(project_id: str | None, include_services: bool) -> dict:
        assert project_id is None
        assert include_services is False
        return {
            "config": {
                "data": {
                    "core": {
                        "account": "user@example.com",
                        "project": "active-project",
                    }
                }
            },
            "projects": {
                "data": [
                    {
                        "projectId": "active-project",
                        "name": "Active Project",
                    }
                ]
            },
            "billingAccounts": {
                "data": [
                    {
                        "name": "billingAccounts/ABC-DEF-GHI",
                        "open": True,
                    }
                ]
            },
        }

    def fake_readiness_report(project_id: str, service_key: str) -> dict:
        assert project_id == "active-project"
        assert service_key == "cloud-run"
        return {
            "billing": {"data": {"billingEnabled": True}},
            "serviceAccounts": {"data": [{"email": "svc@example.com"}]},
            "readiness": {
                "missingApis": ["secretmanager.googleapis.com"],
                "missingLabels": ["owner"],
            },
        }

    def fake_budget_preflight(billing_account: str, api_user_project: str) -> dict:
        assert billing_account == "billingAccounts/ABC-DEF-GHI"
        assert api_user_project == "active-project"
        return {
            "ok": True,
            "ready": True,
            "checks": {"budgetApiEnabled": True},
        }

    monkeypatch.setattr(gcp_adoption_assess, "build_inventory", fake_build_inventory)
    monkeypatch.setattr(gcp_adoption_assess, "readiness_report", fake_readiness_report)
    monkeypatch.setattr(gcp_adoption_assess, "build_budget_preflight", fake_budget_preflight)

    assessment = gcp_adoption_assess.build_assessment(
        capability="stateless HTTP API for webhook backend",
        service_key="cloud-run",
        project_id=None,
        scan_projects=0,
        billing_owner="billing@example.com",
        technical_owner="tech@example.com",
        monthly_low=20.0,
        monthly_high=60.0,
    )

    budget_plan = assessment["costAndBudgetPlan"]
    assert budget_plan["billingAccount"] == "billingAccounts/ABC-DEF-GHI"
    assert budget_plan["apiUserProject"] == "active-project"
    assert budget_plan["budgetApiPreflight"]["ready"] is True
    assert budget_plan["budgetPlanArtifact"]["budgetPolicy"]["recommendedBudget"] == 50
    assert assessment["reuseOrNewProjectDecision"]["decision"] == "reuse-existing"
