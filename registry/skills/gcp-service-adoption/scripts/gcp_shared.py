from __future__ import annotations

import json
import re
import shutil
import subprocess
from typing import Any


SERVICE_CATALOG: dict[str, dict[str, Any]] = {
    "cloud-run": {
        "displayName": "Cloud Run",
        "apis": [
            "run.googleapis.com",
            "artifactregistry.googleapis.com",
            "logging.googleapis.com",
            "monitoring.googleapis.com",
            "secretmanager.googleapis.com",
        ],
        "iamRoles": [
            "roles/run.developer",
            "roles/iam.serviceAccountUser",
            "roles/artifactregistry.reader",
        ],
        "labels": ["owner", "environment", "cost-center"],
        "networking": [
            "Decide ingress mode",
            "Decide whether Serverless VPC Access is needed",
        ],
        "observability": [
            "Cloud Logging retention confirmed",
            "Cloud Monitoring alert policy defined",
        ],
        "billingDrivers": [
            "request count",
            "CPU time",
            "memory time",
            "network egress",
        ],
    },
    "vertex-ai": {
        "displayName": "Vertex AI",
        "apis": [
            "aiplatform.googleapis.com",
            "logging.googleapis.com",
            "monitoring.googleapis.com",
            "secretmanager.googleapis.com",
        ],
        "iamRoles": [
            "roles/aiplatform.user",
            "roles/iam.serviceAccountUser",
        ],
        "labels": ["owner", "environment", "cost-center"],
        "networking": [
            "Confirm region and data residency",
            "Decide whether private connectivity is required",
        ],
        "observability": [
            "Model usage metrics reviewed",
            "Quota and alerting plan defined",
        ],
        "billingDrivers": [
            "model inference volume",
            "training or tuning jobs",
            "stored artifacts",
            "network egress",
        ],
    },
    "cloud-storage": {
        "displayName": "Cloud Storage",
        "apis": [
            "storage.googleapis.com",
            "logging.googleapis.com",
            "monitoring.googleapis.com",
        ],
        "iamRoles": [
            "roles/storage.objectAdmin",
        ],
        "labels": ["owner", "environment", "cost-center"],
        "networking": [
            "Confirm public versus private access model",
        ],
        "observability": [
            "Audit logging policy confirmed",
        ],
        "billingDrivers": [
            "storage volume",
            "operations count",
            "retrieval class",
            "network egress",
        ],
    },
    "secret-manager": {
        "displayName": "Secret Manager",
        "apis": [
            "secretmanager.googleapis.com",
            "logging.googleapis.com",
        ],
        "iamRoles": [
            "roles/secretmanager.secretAccessor",
        ],
        "labels": ["owner", "environment", "cost-center"],
        "networking": [
            "Confirm whether workloads access secrets over private paths",
        ],
        "observability": [
            "Access audit logging confirmed",
        ],
        "billingDrivers": [
            "stored secret versions",
            "access operations",
        ],
    },
}

SERVICE_HINTS: list[dict[str, Any]] = [
    {
        "service": "vertex-ai",
        "patterns": [
            r"\bai\b",
            r"\bllm\b",
            r"\bmodel\b",
            r"\binference\b",
            r"\bprompt\b",
            r"\bgemini\b",
            r"\bembedding\b",
            r"\btraining\b",
        ],
        "alternatives": ["cloud-run"],
    },
    {
        "service": "secret-manager",
        "patterns": [
            r"\bsecrets?\b",
            r"\btokens?\b",
            r"\bcredentials?\b",
            r"\bapi keys?\b",
            r"\bpasswords?\b",
        ],
        "alternatives": ["cloud-run"],
    },
    {
        "service": "cloud-storage",
        "patterns": [
            r"\bfiles?\b",
            r"\buploads?\b",
            r"\bobjects?\b",
            r"\bstorage\b",
            r"\barchives?\b",
            r"\bassets?\b",
            r"\bblobs?\b",
        ],
        "alternatives": ["cloud-run"],
    },
    {
        "service": "cloud-run",
        "patterns": [
            r"\bhttp\b",
            r"\bapi\b",
            r"\bservice\b",
            r"\bcontainer\b",
            r"\bwebhook\b",
            r"\bstateless\b",
            r"\bbackend\b",
        ],
        "alternatives": ["cloud-storage"],
    },
]


def resolve_gcloud_command() -> str | None:
    for candidate in ("gcloud.cmd", "gcloud"):
        resolved = shutil.which(candidate)
        if resolved:
            return resolved
    return None


def run_gcloud(args: list[str]) -> dict[str, Any]:
    gcloud_command = resolve_gcloud_command()
    if gcloud_command is None:
        return {"ok": False, "command": ["gcloud", *args], "stderr": "gcloud not found on PATH"}

    completed = subprocess.run(
        [gcloud_command, *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        return {
            "ok": False,
            "command": ["gcloud", *args],
            "stderr": completed.stderr.strip(),
        }

    stdout = completed.stdout.strip()
    if not stdout:
        return {"ok": True, "data": None}

    try:
        return {"ok": True, "data": json.loads(stdout)}
    except json.JSONDecodeError:
        return {"ok": True, "data": stdout}


def summarize_enabled_services(response: dict[str, Any]) -> dict[str, Any]:
    if not response.get("ok"):
        return response

    services = response.get("data") or []
    summary: list[dict[str, str]] = []
    for item in services:
        config = item.get("config") or {}
        name = config.get("name")
        title = config.get("title")
        if isinstance(name, str):
            row: dict[str, str] = {"name": name}
            if isinstance(title, str):
                row["title"] = title
            summary.append(row)

    summary.sort(key=lambda item: item["name"])
    return {"ok": True, "data": summary}


def extract_enabled_service_names(response: dict[str, Any]) -> set[str]:
    if not response.get("ok"):
        return set()

    raw = response.get("data") or []
    names: set[str] = set()
    for item in raw:
        config = item.get("config") or {}
        name = config.get("name")
        if isinstance(name, str):
            names.add(name)
    return names


def extract_labels(project_response: dict[str, Any]) -> dict[str, str]:
    if not project_response.get("ok"):
        return {}
    data = project_response.get("data") or {}
    labels = data.get("labels") or {}
    if isinstance(labels, dict):
        return {str(key): str(value) for key, value in labels.items()}
    return {}


def recommend_service(capability: str) -> dict[str, Any]:
    lowered = capability.lower()
    scores: dict[str, int] = {key: 0 for key in SERVICE_CATALOG}

    for rule in SERVICE_HINTS:
        for pattern in rule["patterns"]:
            if re.search(pattern, lowered):
                scores[rule["service"]] += 1

    ranked = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    primary, primary_score = ranked[0]
    if primary_score == 0:
        primary = "cloud-run"

    alternatives = [key for key, score in ranked if key != primary and score > 0][:2]
    if not alternatives:
        alternatives = next(
            (rule["alternatives"] for rule in SERVICE_HINTS if rule["service"] == primary),
            [],
        )

    return {
        "primaryService": primary,
        "primaryDisplayName": SERVICE_CATALOG[primary]["displayName"],
        "alternatives": alternatives[:2],
    }


def score_project_fit(
    *,
    billing_enabled: bool,
    missing_apis: list[str],
    missing_labels: list[str],
    service_account_count: int,
) -> dict[str, Any]:
    score = 0
    notes: list[str] = []

    if billing_enabled:
        score += 3
    else:
        notes.append("billing is not enabled")

    if not missing_apis:
        score += 3
    else:
        score += max(0, 3 - len(missing_apis))
        notes.append(f"missing APIs: {', '.join(missing_apis)}")

    if not missing_labels:
        score += 2
    else:
        score += max(0, 2 - len(missing_labels))
        notes.append(f"missing labels: {', '.join(missing_labels)}")

    if service_account_count > 0:
        score += 1
    else:
        notes.append("no service accounts found")

    decision = "reuse-existing" if billing_enabled and len(missing_apis) <= 1 else "new-project"
    return {"score": score, "decision": decision, "notes": notes}
