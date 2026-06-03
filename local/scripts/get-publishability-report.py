from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any

from lib.workspace_boundaries import build_boundary_payload


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def run_git(root: Path, args: list[str]) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return [line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip()]


def infer_document_placement(candidate_path: str) -> dict[str, Any]:
    normalized = candidate_path.replace("\\", "/").lstrip("./")

    def recommendation(
        classification: str,
        recommended_location: str,
        tracked: bool | None,
        share_safe: bool | None,
        rationale: str,
        notes: list[str],
        shared_form: str | None = None,
    ) -> dict[str, Any]:
        matches = None
        if classification != "manual-review" and recommended_location:
            matches = normalized.lower().startswith(recommended_location.replace("\\", "/").lstrip("./").lower())
        return {
            "topic": "document",
            "authorship_window_is_primary_rule": False,
            "classification": classification,
            "shared_form": shared_form if classification == "shared-canonical" else None,
            "recommended_location": recommended_location,
            "tracked": tracked,
            "share_safe": share_safe,
            "candidate_path": normalized,
            "candidate_path_matches_recommendation": matches,
            "rationale": rationale,
            "notes": notes,
        }

    common_notes = ["Classify by document role and audience, not by the window where the file was edited."]
    if normalized.startswith("ops/"):
        return recommendation(
            "generated-state",
            "ops/",
            False,
            False,
            "Paths under ops/ are treated as generated state, audit evidence, or export artifacts rather than canonical source.",
            common_notes,
        )
    if normalized.startswith("local/docs/authoring/"):
        return recommendation(
            "authoring-draft",
            "local/docs/authoring/",
            False,
            False,
            "Paths under local/docs/authoring/ are ignored authoring drafts, review notes, or workboards.",
            common_notes,
        )
    if re.search(r"^local/docs/.+_(LIVE|WORKSPACE_BASELINE)\.md$", normalized, re.IGNORECASE):
        return recommendation(
            "single-workspace-live",
            "local/docs/",
            False,
            False,
            "LIVE and WORKSPACE_BASELINE documents describe one workspace or machine-local state and should stay local-only.",
            common_notes,
        )
    if re.search(r"^registry/.+/references/", normalized):
        return recommendation(
            "shared-canonical",
            "registry/.../references/",
            True,
            True,
            "Sanitized shared references belong under registry references and should remain template-safe.",
            common_notes,
            "registry-reference",
        )
    if normalized.startswith("registry/workflow/"):
        return recommendation(
            "shared-canonical",
            "registry/workflow/",
            True,
            True,
            "Shared workflow and runbook material belongs in the tracked workflow layer.",
            common_notes,
            "registry-workflow",
        )
    if re.search(r"^[^/]+\.md$", normalized):
        return recommendation(
            "shared-canonical",
            normalized,
            True,
            True,
            "Root markdown docs are treated as repo-wide canonical policy, spec, or guidance unless evidence says otherwise.",
            common_notes + ["Tracked shared placement still does not imply publish permission."],
            "root-doc",
        )
    return recommendation(
        "manual-review",
        "manual-review",
        None,
        None,
        "Path alone is not enough to classify this file. Review the document role and audience before deciding placement.",
        common_notes,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Report local publishability signals without granting publish permission.")
    parser.add_argument("--format", choices=("json",), default="json")
    args = parser.parse_args()

    root = repo_root()
    branch_lines = run_git(root, ["branch", "--show-current"])
    branch = branch_lines[0] if branch_lines else ""
    unstaged = run_git(root, ["diff", "--name-only"])
    staged = run_git(root, ["diff", "--cached", "--name-only"])
    untracked = run_git(root, ["ls-files", "--others", "--exclude-standard"])
    changed = sorted(set(unstaged + staged + untracked))
    boundary = build_boundary_payload(root)

    local_only_changes = [
        path
        for path in changed
        if re.search(r"^local/docs/authoring/", path)
        or re.search(r"^local/docs/.+_LIVE\.md$", path)
        or re.search(r"^local/docs/.+_WORKSPACE_BASELINE\.md$", path)
    ]
    ops_changes = [path for path in changed if path.startswith("ops/")]
    shared_changes = [
        path
        for path in changed
        if not path.startswith("ops/")
        and not re.search(r"^local/docs/authoring/", path)
        and not re.search(r"^local/docs/.+_LIVE\.md$", path)
        and not re.search(r"^local/docs/.+_WORKSPACE_BASELINE\.md$", path)
    ]
    document_placement_observations = [infer_document_placement(path) for path in changed if path.endswith(".md")]
    document_placement_manual_review = [
        item for item in document_placement_observations if item["classification"] == "manual-review"
    ]
    document_placement_mismatches = [
        item
        for item in document_placement_observations
        if item["candidate_path_matches_recommendation"] is False
    ]

    payload = {
        "branch": branch,
        "no_publish_permission_required": True,
        "working_tree_clean": len(changed) == 0,
        "changed_paths": changed,
        "local_only_changes": local_only_changes,
        "ops_changes": ops_changes,
        "shared_surface_changes": shared_changes,
        "document_placement_observations": document_placement_observations,
        "document_placement_manual_review": document_placement_manual_review,
        "document_placement_mismatches": document_placement_mismatches,
        "boundary_ok": bool(boundary["ok"]),
        "boundary_rules_ok": bool(boundary["rules_ok"]),
        "boundary_rule_errors": boundary["rules_errors"],
        "boundary_path_violations": boundary["path_violations"],
        "boundary_content_violations": boundary["content_violations"],
        "structurally_publishable_if_permission_is_granted": bool(boundary["ok"])
        and len(changed) == 0
        and len(local_only_changes) == 0
        and len(ops_changes) == 0,
    }
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
