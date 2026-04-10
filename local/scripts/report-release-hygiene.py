#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from typing import NamedTuple
from pathlib import Path


RELEASE_SCOPE_EXACT = {
    ".gitignore",
    "LICENSE",
    "README.md",
    "INDEX.md",
    "VISION.md",
    "RESOURCE_SPEC.md",
    "OPERATIONS.md",
    "PROJECT_MODES.md",
    "SECRET_HANDLING_GUIDELINES.md",
    "MILESTONES.md",
    "TEMPLATE_RELEASE_PACKAGE.md",
    "TEMPLATE_RELEASE_CHECKLIST.md",
    "REBUILD_AS_NEW_PROJECT.md",
    "COPILOT_CLI_ADAPTER_NOTE.md",
    "PROJECT_STATUS_REPORT_2026-03-23.md",
    "local/docs/CLI_COMPAT_MATRIX.md",
    "local/scripts/README.md",
    "registry/catalog-exclusions.json",
    ".github/copilot-instructions.md",
}
RELEASE_SCOPE_PREFIXES = (
    "local/scripts/",
    "local/docs/",
    "tests/",
    "template/examples/local/",
    "FINAL_RELEASE_DEVELOPMENT_PLAN_",
    "RELEASE_EVIDENCE_",
    "RELEASE_HYGIENE_REPORT_",
    "I18N_WAVE_REPORT_",
    "COPILOT_SESSION_EVIDENCE_",
)
BLOCKER_SUFFIXES = (".jpg", ".jpeg", ".png", ".psd")


class Entry(NamedTuple):
    status: str
    path: str


def parse_git_status_line(line: str) -> Entry | None:
    if len(line) < 4:
        return None
    status = line[:2]
    path = line[3:]
    if " -> " in path:
        path = path.rsplit(" -> ", 1)[-1]
    return Entry(status=status, path=path)


def collect_git_status(repo_root: Path) -> list[Entry]:
    result = subprocess.run(
        ["git", "-C", str(repo_root), "status", "--short", "--untracked-files=all"],
        check=False,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or result.stdout.strip() or "git status failed")

    entries: list[Entry] = []
    for raw_line in result.stdout.splitlines():
        entry = parse_git_status_line(raw_line)
        if entry is not None:
            entries.append(entry)
    return entries


def read_catalog_exclusions(repo_root: Path) -> set[str]:
    path = repo_root / "registry" / "catalog-exclusions.json"
    if not path.exists():
        return {"microsoft-foundry"}
    body = json.loads(path.read_text(encoding="utf-8"))
    skills = body.get("skills", {})
    if not isinstance(skills, dict):
        return {"microsoft-foundry"}
    return set(skills.keys()) or {"microsoft-foundry"}


def classify_path(path: str, excluded_skills: set[str] | None = None) -> tuple[str, str]:
    excluded_skills = {"microsoft-foundry"} if excluded_skills is None else excluded_skills
    if path in RELEASE_SCOPE_EXACT or any(path.startswith(prefix) for prefix in RELEASE_SCOPE_PREFIXES):
        return "release_scope", "belongs to the current release workstream"
    if path == ".mcp.json":
        return "machine_specific", "local bootstrap output should not be committed as portable source"
    if path.startswith("ops/history/"):
        return "generated_history", "history artifacts are evidence only"
    if any(path.startswith(f"registry/skills/{skill_id}/") for skill_id in excluded_skills):
        return "stray_registry", "explicitly excluded stray registry item"
    if path.startswith("i18n/"):
        return "translation_wave", "translation changes are outside the current release scope"
    if Path(path).suffix.lower() in BLOCKER_SUFFIXES:
        return "binary_asset", "binary or design assets are outside the release scope"
    if path.startswith("SECURITY_") or path.startswith("security/"):
        return "review_noise", "review drafts should be split from the release commit"
    return "outside_release_scope", "not part of the current release workstream"


def is_acknowledged(
    path: str,
    category: str,
    *,
    allowed_categories: set[str],
    allowed_paths: set[str],
    allowed_prefixes: tuple[str, ...],
) -> bool:
    if category in allowed_categories:
        return True
    if path in allowed_paths:
        return True
    return any(path.startswith(prefix) for prefix in allowed_prefixes)


def build_report(
    entries: list[Entry],
    repo_root: Path | None = None,
    *,
    allowed_categories: set[str] | None = None,
    allowed_paths: set[str] | None = None,
    allowed_prefixes: tuple[str, ...] | None = None,
) -> dict[str, object]:
    excluded_skills = read_catalog_exclusions(repo_root or Path(__file__).resolve().parents[2])
    allowed_categories = set() if allowed_categories is None else set(allowed_categories)
    allowed_paths = set() if allowed_paths is None else set(allowed_paths)
    allowed_prefixes = tuple() if allowed_prefixes is None else tuple(allowed_prefixes)
    release_scope: list[dict[str, str]] = []
    acknowledged: list[dict[str, str]] = []
    blockers: list[dict[str, str]] = []
    by_category: dict[str, int] = {}

    for entry in entries:
        category, reason = classify_path(entry.path, excluded_skills)
        by_category[category] = by_category.get(category, 0) + 1
        payload = {"status": entry.status, "path": entry.path, "category": category, "reason": reason}
        if category == "release_scope":
            release_scope.append(payload)
        elif is_acknowledged(
            entry.path,
            category,
            allowed_categories=allowed_categories,
            allowed_paths=allowed_paths,
            allowed_prefixes=allowed_prefixes,
        ):
            acknowledged.append(payload)
        else:
            blockers.append(payload)

    return {
        "release_scope": release_scope,
        "acknowledged": acknowledged,
        "blockers": blockers,
        "summary": {
            "total": len(entries),
            "release_scope": len(release_scope),
            "acknowledged": len(acknowledged),
            "blockers": len(blockers),
            "by_category": by_category,
        },
        "allowed": {
            "categories": sorted(allowed_categories),
            "paths": sorted(allowed_paths),
            "prefixes": list(allowed_prefixes),
        },
        "ok": not blockers,
    }


def format_markdown(repo_root: Path, report: dict[str, object]) -> str:
    summary = report["summary"]
    acknowledged = report["acknowledged"]
    blockers = report["blockers"]
    lines = [
        "# Release Hygiene Report",
        "",
        f"- repo: `{repo_root}`",
        f"- total dirty entries: `{summary['total']}`",
        f"- release scope: `{summary['release_scope']}`",
        f"- acknowledged exclusions: `{summary['acknowledged']}`",
        f"- blockers: `{summary['blockers']}`",
        f"- ok: `{str(report['ok']).lower()}`",
        "",
    ]

    if acknowledged:
        lines.append("## Acknowledged Exclusions")
        for item in acknowledged[:20]:
            lines.append(f"- `{item['status']}` `{item['category']}` `{item['path']}`: {item['reason']}")
        if len(acknowledged) > 20:
            lines.append(f"- ... {len(acknowledged) - 20} more")
        lines.append("")

    lines.extend(
        [
            "## Blockers",
        ]
    )
    if not blockers:
        lines.append("- none")
        return "\n".join(lines)

    for item in blockers[:20]:
        lines.append(f"- `{item['status']}` `{item['category']}` `{item['path']}`: {item['reason']}")
    if len(blockers) > 20:
        lines.append(f"- ... {len(blockers) - 20} more")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Classify dirty worktree entries into release scope and blockers.")
    parser.add_argument("--repo-root", default=str(Path(__file__).resolve().parents[2]))
    parser.add_argument("--json", action="store_true", help="emit JSON instead of markdown")
    parser.add_argument("--markdown", action="store_true", help="emit markdown explicitly")
    parser.add_argument(
        "--allow-category",
        action="append",
        default=[],
        help="treat this blocker category as an acknowledged exclusion",
    )
    parser.add_argument(
        "--allow-path",
        action="append",
        default=[],
        help="treat this exact path as an acknowledged exclusion",
    )
    parser.add_argument(
        "--allow-prefix",
        action="append",
        default=[],
        help="treat any path under this prefix as an acknowledged exclusion",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    entries = collect_git_status(repo_root)
    report = build_report(
        entries,
        repo_root,
        allowed_categories=set(args.allow_category),
        allowed_paths=set(args.allow_path),
        allowed_prefixes=tuple(args.allow_prefix),
    )
    report["repo_root"] = str(repo_root)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(format_markdown(repo_root, report))

    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
