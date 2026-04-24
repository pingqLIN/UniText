from __future__ import annotations

import argparse
import json
from pathlib import Path

from lib.workspace_sensitive_metadata import as_list, load_rules, validate_rules


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate UniText workspace-sensitive metadata rules.")
    parser.add_argument("--format", choices=("json",), default="json")
    args = parser.parse_args()

    root = repo_root()
    rules = load_rules(root)
    result = validate_rules(rules, root=root, require_scope_exists=True)
    missing_scope_entries = [
        error.removeprefix("shared_surface_scope entry is missing from root: ")
        for error in as_list(result["errors"])
        if error.startswith("shared_surface_scope entry is missing from root: ")
    ]

    payload = {
        "rules_path": str(root / "WORKSPACE_SENSITIVE_METADATA_RULES.json"),
        "shared_surface_scope_count": len(as_list(rules.get("shared_surface_scope"))),
        "path_rule_count": len(as_list(rules.get("path_rules"))),
        "content_pattern_count": len(as_list(rules.get("content_patterns"))),
        "self_test_case_count": len(as_list(rules.get("self_test_cases"))),
        "missing_shared_surface_scope": missing_scope_entries,
        "errors": as_list(result["errors"]),
        "ok": bool(result["ok"]),
    }
    print(json.dumps(payload, indent=2))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
