from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any


TEXT_EXTENSIONS = {".md", ".json", ".jsonc", ".txt", ".ps1", ".py", ".toml", ".yml", ".yaml"}


def normalize_repo_path(path: str) -> str:
    return path.replace("\\", "/").lstrip("./")


def load_rules(root: Path) -> dict[str, Any]:
    rules_path = root / "WORKSPACE_SENSITIVE_METADATA_RULES.json"
    if not rules_path.exists():
        raise FileNotFoundError(f"Workspace-sensitive metadata rules file not found: {rules_path}")

    rules = json.loads(rules_path.read_text(encoding="utf-8"))
    for key in ("shared_surface_scope", "path_rules", "content_patterns", "self_test_cases"):
        if not rules.get(key):
            raise ValueError(f"Rules file is missing {key}.")
    return rules


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def validate_rules(rules: dict[str, Any], root: Path | None = None, require_scope_exists: bool = False) -> dict[str, Any]:
    errors: list[str] = []

    shared_surface_scope = as_list(rules.get("shared_surface_scope"))
    if not shared_surface_scope:
        errors.append("shared_surface_scope must not be empty.")

    if require_scope_exists and root is None:
        errors.append("RootPath is required when RequireScopeExists is enabled.")

    path_rules = as_list(rules.get("path_rules"))
    path_labels = [str(rule.get("label", "")) for rule in path_rules]
    if len(set(path_labels)) != len(path_labels):
        errors.append("path_rules labels must be unique.")

    content_patterns = as_list(rules.get("content_patterns"))
    content_labels = [str(pattern.get("label", "")) for pattern in content_patterns]
    if len(set(content_labels)) != len(content_labels):
        errors.append("content_patterns labels must be unique.")

    for rule in path_rules:
        try:
            re.compile(str(rule.get("regex", "")))
        except re.error:
            errors.append(f"Invalid path rule regex for '{rule.get('label')}': {rule.get('regex')}")

    for pattern in content_patterns:
        try:
            re.compile(str(pattern.get("regex", "")))
        except re.error:
            errors.append(f"Invalid content pattern regex for '{pattern.get('label')}': {pattern.get('regex')}")

        if "skip_script_pattern_lines" not in pattern:
            errors.append(f"content pattern '{pattern.get('label')}' must define skip_script_pattern_lines.")

    for test_case in as_list(rules.get("self_test_cases")):
        expected = sorted(set(as_list(test_case.get("expected_labels"))))
        actual = sorted(
            {
                str(pattern.get("label"))
                for pattern in content_patterns
                if _regex_search(str(pattern.get("regex", "")), str(test_case.get("sample", "")))
            }
        )
        if expected != actual:
            errors.append(
                f"self_test_case '{test_case.get('label')}' mismatch. "
                f"expected=[{', '.join(expected)}] actual=[{', '.join(actual)}]"
            )

    if require_scope_exists and root is not None:
        for entry in shared_surface_scope:
            if not (root / str(entry)).exists():
                errors.append(f"shared_surface_scope entry is missing from root: {entry}")

    return {"ok": len(errors) == 0, "errors": errors}


def find_path_violations(tracked_files: list[str], path_rules: list[dict[str, Any]]) -> list[dict[str, str]]:
    violations: list[dict[str, str]] = []
    for file_path in tracked_files:
        normalized = normalize_repo_path(file_path)
        for rule in path_rules:
            if _regex_search(str(rule.get("regex", "")), normalized):
                violations.append({"path": normalized, "label": str(rule.get("label", ""))})
    return violations


def find_content_violations(root: Path, files: list[str], content_patterns: list[dict[str, Any]]) -> list[dict[str, Any]]:
    violations: list[dict[str, Any]] = []
    compiled_patterns = [(pattern, re.compile(str(pattern.get("regex", "")))) for pattern in content_patterns]

    for file_path in files:
        normalized = normalize_repo_path(file_path)
        absolute_path = root / normalized
        if not absolute_path.exists():
            continue

        for line_number, line in enumerate(absolute_path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
            for pattern, compiled in compiled_patterns:
                if not compiled.search(line):
                    continue

                if normalized.endswith("WORKSPACE_SENSITIVE_METADATA_RULES.json") and re.search(
                    r'(?i)"sample"\s*:', line
                ):
                    continue

                if (
                    pattern.get("skip_script_pattern_lines")
                    and Path(normalized).suffix.lower() in {".ps1", ".py"}
                    and re.search(r"(?i)\b(regex|pattern|contentpatterns?)\b", line)
                ):
                    continue

                violations.append(
                    {
                        "path": normalized,
                        "label": str(pattern.get("label", "")),
                        "line": line_number,
                        "text": line.strip(),
                    }
                )
    return violations


def get_tracked_files(root: Path, scope: list[str]) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--cached", "--others", "--exclude-standard", "--", *scope],
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        raise RuntimeError("git ls-files failed while resolving tracked files for boundary verification.")
    return [normalize_repo_path(line) for line in result.stdout.splitlines() if line.strip()]


def get_text_files(files: list[str]) -> list[str]:
    return [file_path for file_path in files if Path(file_path).suffix.lower() in TEXT_EXTENSIONS]


def _regex_search(pattern: str, text: str) -> bool:
    try:
        return re.search(pattern, text) is not None
    except re.error:
        return False
