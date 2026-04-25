from __future__ import annotations

import subprocess
from collections import Counter
from pathlib import Path


SCOPE_MAP: dict[str, list[str]] = {
    "repo": ["."],
    "root": [
        ".gitattributes",
        ".github",
        ".gitignore",
        ".mcp.json",
        ".claude",
        "AGENTS.md",
        "README.md",
        "INDEX.md",
        "VISION.md",
        "RESOURCE_SPEC.md",
        "OPERATIONS.md",
        "PROJECT_MODES.md",
        "WORKSPACE_SENSITIVE_METADATA_RULES.json",
        "WORKSPACE_SENSITIVE_METADATA_RULES.md",
        "DOCUMENT_PLACEMENT_POLICY.md",
        "SECRET_HANDLING_GUIDELINES.md",
        "MILESTONES.md",
        "BOUNDARY_INCIDENT_REVIEW_TEMPLATE.md",
        "TEMPLATE_RELEASE_PACKAGE.md",
        "TEMPLATE_RELEASE_CHECKLIST.md",
        "REBUILD_AS_NEW_PROJECT.md",
        "NO_PUBLISH_POLICY.md",
    ],
    "registry": ["registry"],
    "i18n": ["i18n"],
    "local": ["local"],
    "template": ["template"],
}


def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def run_git(repo: Path, args: list[str]) -> list[str]:
    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    output = completed.stdout.splitlines() + completed.stderr.splitlines()
    if completed.returncode != 0:
        message = "\n".join(line for line in output if line.strip())
        raise RuntimeError(message or f"git {' '.join(args)} failed")
    return output


def parse_preview_paths(output: list[str]) -> list[str]:
    paths: list[str] = []
    for line in output:
        if not line.startswith("add '") or not line.endswith("'"):
            continue
        paths.append(line[5:-1])
    return paths


def unique_targets(scopes: list[str]) -> tuple[list[str], list[str]]:
    selected = list(dict.fromkeys(scopes))
    invalid = [scope for scope in selected if scope not in SCOPE_MAP]
    if invalid:
        raise RuntimeError(f"Unsupported scope: {', '.join(invalid)}")
    targets: list[str] = []
    for scope in selected:
        for target in SCOPE_MAP[scope]:
            if target not in targets:
                targets.append(target)
    return selected, targets


def preview_paths(repo: Path, targets: list[str]) -> list[str]:
    output = run_git(repo, ["add", "-n", "--renormalize", "--", *targets])
    return parse_preview_paths(output)


def apply_paths(repo: Path, targets: list[str]) -> list[str]:
    run_git(repo, ["add", "--renormalize", "--", *targets])
    output = run_git(repo, ["diff", "--cached", "--name-only", "--", *targets])
    return [line for line in output if line.strip()]


def top_level_groups(paths: list[str]) -> list[dict[str, object]]:
    counter: Counter[str] = Counter()
    for path in paths:
        counter[path.split("/", 1)[0].split("\\", 1)[0]] += 1
    return [
        {"scope": name, "count": count}
        for name, count in sorted(counter.items(), key=lambda item: (-item[1], item[0]))
    ]
