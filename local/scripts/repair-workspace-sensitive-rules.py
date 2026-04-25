#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath


REPO_ROOT = Path(__file__).resolve().parents[2]
RULES_RELATIVE_PATH = "WORKSPACE_SENSITIVE_METADATA_RULES.json"

LEGACY_SCOPE_PATH_MAP = {
    "EXTERNAL_REVIEW_COVER_NOTE.md": "docs/reviews/EXTERNAL_REVIEW_COVER_NOTE.md",
    "EXTERNAL_REVIEW_HIGHLIGHTS.md": "docs/reviews/EXTERNAL_REVIEW_HIGHLIGHTS.md",
    "EXTERNAL_REVIEW_PACKAGE.md": "docs/reviews/EXTERNAL_REVIEW_PACKAGE.md",
    "ESSENTIAL_SKILLS_SHORTLIST.md": "docs/reviews/ESSENTIAL_SKILLS_SHORTLIST.md",
    "COPILOT_CLI_ADAPTER_NOTE.md": "docs/adapters/COPILOT_CLI_ADAPTER_NOTE.md",
    "SKILL0_COLLABORATION_VISION.md": "docs/concepts/SKILL0_COLLABORATION_VISION.md",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Normalize workspace-sensitive boundary rule references.")
    parser.add_argument("--repo-root", default=str(REPO_ROOT))
    parser.add_argument("--write", action="store_true")
    return parser.parse_args()


def normalize_scope_path(value: str) -> str:
    raw = value.replace("\\", "/")
    if raw in LEGACY_SCOPE_PATH_MAP:
        return LEGACY_SCOPE_PATH_MAP[raw]

    basename = PurePosixPath(raw).name
    if basename in LEGACY_SCOPE_PATH_MAP:
        return LEGACY_SCOPE_PATH_MAP[basename]

    return raw


def normalize_scope(entries: list[str]) -> tuple[list[str], list[dict[str, str]]]:
    normalized: list[str] = []
    changes: list[dict[str, str]] = []
    seen: set[str] = set()

    for original in entries:
        repaired = normalize_scope_path(original)
        if repaired != original:
            changes.append({"from": original, "to": repaired, "reason": "legacy-path"})
        if repaired in seen:
            changes.append({"from": original, "to": repaired, "reason": "deduplicated"})
            continue
        normalized.append(repaired)
        seen.add(repaired)

    return normalized, changes


def validate_scope(repo_root: Path, scope: list[str]) -> dict[str, object]:
    missing_paths = [path for path in scope if not (repo_root / path).exists()]
    return {
        "missing_paths": missing_paths,
        "ok": not missing_paths,
    }


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    rules_path = repo_root / RULES_RELATIVE_PATH
    rules = json.loads(rules_path.read_text(encoding="utf-8"))

    shared_surface_scope = [str(item) for item in rules.get("shared_surface_scope", [])]
    normalized_scope, scope_changes = normalize_scope(shared_surface_scope)
    rules["shared_surface_scope"] = normalized_scope

    validation = validate_scope(repo_root, normalized_scope)
    changed = bool(scope_changes)

    if args.write and changed:
        rules_path.write_text(json.dumps(rules, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    report = {
        "repo_root": str(repo_root),
        "rules_path": str(rules_path),
        "changed": changed,
        "write_applied": bool(args.write and changed),
        "scope_changes": scope_changes,
        "validation": validation,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if validation["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
