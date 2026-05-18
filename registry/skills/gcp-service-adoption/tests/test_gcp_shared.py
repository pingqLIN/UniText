from __future__ import annotations

import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from gcp_shared import recommend_service, score_project_fit


def test_recommend_service_cloud_run() -> None:
    result = recommend_service("stateless HTTP API for webhook backend")
    assert result["primaryService"] == "cloud-run"


def test_recommend_service_cloud_storage() -> None:
    result = recommend_service("store uploaded files and generated assets")
    assert result["primaryService"] == "cloud-storage"


def test_recommend_service_secret_manager() -> None:
    result = recommend_service("manage API keys and secrets securely")
    assert result["primaryService"] == "secret-manager"


def test_score_project_fit_reuse_existing() -> None:
    result = score_project_fit(
        billing_enabled=True,
        missing_apis=[],
        missing_labels=[],
        service_account_count=2,
    )
    assert result["decision"] == "reuse-existing"
    assert result["score"] >= 8


def test_score_project_fit_new_project() -> None:
    result = score_project_fit(
        billing_enabled=False,
        missing_apis=["run.googleapis.com", "secretmanager.googleapis.com"],
        missing_labels=["owner", "environment"],
        service_account_count=0,
    )
    assert result["decision"] == "new-project"
    assert result["notes"]
