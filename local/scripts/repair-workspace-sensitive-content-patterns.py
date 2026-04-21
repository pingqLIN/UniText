#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
RULES_RELATIVE_PATH = "WORKSPACE_SENSITIVE_METADATA_RULES.json"

CANONICAL_CONTENT_PATTERNS = {
    "live workspace hostname": {
        "label": "live workspace hostname",
        "regex": r"(?i)\b(?:zone hostnames?|public hostnames?|custom hostnames?|mcp hostnames?|health hostnames?)\b[^\r\n]*\b(?!workspace\.example\.com\b)(?!example\.com\b)(?:[a-z0-9-]+\.)+[a-z]{2,}\b",
        "skip_script_pattern_lines": True,
    }
}

CANONICAL_SELF_TEST_CASES = {
    "allow sanitized placeholder hostname": {
        "label": "allow sanitized placeholder hostname",
        "sample": "Zone hostname: workspace.example.com",
        "expected_labels": [],
    },
    "flag live hostname in governance text": {
        "label": "flag live hostname in governance text",
        "sample": "Zone hostname: colorgeek.co",
        "expected_labels": ["live workspace hostname"],
    },
    "flag live mcp hostname in governance text": {
        "label": "flag live mcp hostname in governance text",
        "sample": "MCP hostname: mcp.colorgeek.co",
        "expected_labels": ["live workspace hostname"],
    },
    "allow azure bare hostname guidance": {
        "label": "allow azure bare hostname guidance",
        "sample": "Always prepend https:// when presenting URLs to the user. For example, report https://myapp.azurewebsites.net, never myapp.azurewebsites.net.",
        "expected_labels": [],
    },
    "allow domain account guidance": {
        "label": "allow domain account guidance",
        "sample": r"Use VMNAME\\user for local, DOMAIN\\user for domain accounts.",
        "expected_labels": [],
    },
    "allow domain controller guidance": {
        "label": "allow domain controller guidance",
        "sample": "VMAccess extension error on domain controller",
        "expected_labels": [],
    },
    "allow ingress placeholder command": {
        "label": "allow ingress placeholder command",
        "sample": "kubectl get pods -n <ingress-ns> -l app.kubernetes.io/name=ingress-nginx",
        "expected_labels": [],
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Restore canonical workspace-sensitive content pattern definitions.")
    parser.add_argument("--repo-root", default=str(REPO_ROOT))
    parser.add_argument("--write", action="store_true")
    return parser.parse_args()


def normalize_content_patterns(rules: dict[str, object]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    changes: list[dict[str, object]] = []
    normalized: list[dict[str, object]] = []

    for pattern in rules.get("content_patterns", []):
        entry = dict(pattern)
        canonical = CANONICAL_CONTENT_PATTERNS.get(str(entry.get("label")))
        if canonical is None:
            normalized.append(entry)
            continue

        if entry != canonical:
            changes.append(
                {
                    "label": canonical["label"],
                    "from": entry,
                    "to": canonical,
                    "reason": "restore-canonical-content-pattern",
                }
            )
        normalized.append(dict(canonical))

    return normalized, changes


def normalize_self_tests(rules: dict[str, object]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    existing_cases = [dict(case) for case in rules.get("self_test_cases", [])]
    by_label = {str(case.get("label")): case for case in existing_cases}
    changes: list[dict[str, object]] = []

    for label, canonical in CANONICAL_SELF_TEST_CASES.items():
        current = by_label.get(label)
        if current != canonical:
            changes.append(
                {
                    "label": label,
                    "from": current,
                    "to": canonical,
                    "reason": "restore-canonical-self-test",
                }
            )
        by_label[label] = dict(canonical)

    ordered_labels = [str(case.get("label")) for case in existing_cases]
    for label in CANONICAL_SELF_TEST_CASES:
        if label not in ordered_labels:
            ordered_labels.append(label)

    normalized = [by_label[label] for label in ordered_labels]
    return normalized, changes


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    rules_path = repo_root / RULES_RELATIVE_PATH
    rules = json.loads(rules_path.read_text(encoding="utf-8"))

    normalized_patterns, pattern_changes = normalize_content_patterns(rules)
    normalized_self_tests, self_test_changes = normalize_self_tests(rules)

    rules["content_patterns"] = normalized_patterns
    rules["self_test_cases"] = normalized_self_tests

    changed = bool(pattern_changes or self_test_changes)
    if args.write and changed:
        rules_path.write_text(json.dumps(rules, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    report = {
        "repo_root": str(repo_root),
        "rules_path": str(rules_path),
        "changed": changed,
        "write_applied": bool(args.write and changed),
        "content_pattern_changes": pattern_changes,
        "self_test_changes": self_test_changes,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
