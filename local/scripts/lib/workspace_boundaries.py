from __future__ import annotations

from pathlib import Path

from .workspace_sensitive_metadata import (
    as_list,
    find_content_violations,
    find_path_violations,
    get_text_files,
    get_tracked_files,
    load_rules,
    validate_rules,
)


def build_boundary_payload(root: Path, scope: list[str] | None = None) -> dict[str, object]:
    rules = load_rules(root)
    rules_check = validate_rules(rules, root=root, require_scope_exists=True)
    effective_scope = scope if scope else [str(entry) for entry in as_list(rules.get("shared_surface_scope"))]
    tracked_files = get_tracked_files(root, effective_scope)
    path_violations = find_path_violations(tracked_files, as_list(rules.get("path_rules")))
    content_violations = find_content_violations(root, get_text_files(tracked_files), as_list(rules.get("content_patterns")))

    return {
        "scanned_scope": effective_scope,
        "scanned_file_count": len(tracked_files),
        "rules_ok": bool(rules_check["ok"]),
        "rules_errors": as_list(rules_check["errors"]),
        "path_violations": path_violations,
        "content_violations": content_violations,
        "ok": bool(rules_check["ok"]) and not path_violations and not content_violations,
    }
