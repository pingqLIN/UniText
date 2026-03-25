#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from typing import NamedTuple
from pathlib import Path


RELEASE_SCOPE_EXACT = {
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
    "RELEASE_EVIDENCE_2026-03-25.md",
    "FINAL_RELEASE_DEVELOPMENT_PLAN_2026-03-25.md",
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


def classify_path(path: str) -> tuple[str, str]:
    if path in RELEASE_SCOPE_EXACT or any(path.startswith(prefix) for prefix in RELEASE_SCOPE_PREFIXES):
        return "release_scope", "belongs to the current release workstream"
    if path == ".mcp.json":
        return "machine_specific", "local bootstrap output should not be committed as portable source"
    if path.startswith("ops/history/"):
        return "generated_history", "history artifacts are evidence only"
    if path.startswith("registry/skills/microsoft-foundry/"):
        return "stray_registry", "explicitly excluded stray registry item"
    if path.startswith("i18n/"):
        return "translation_wave", "translation changes are outside the current release scope"
    if Path(path).suffix.lower() in BLOCKER_SUFFIXES:
        return "binary_asset", "binary or design assets are outside the release scope"
    if path.startswith("SECURITY_") or path.startswith("security/"):
        return "review_noise", "review drafts should be split from the release commit"
    return "outside_release_scope", "not part of the current release workstream"


def build_report(entries: list[Entry]) -> dict[str, object]:
    release_scope: list[dict[str, str]] = []
    blockers: list[dict[str, str]] = []
    by_category: dict[str, int] = {}

    for entry in entries:
        category, reason = classify_path(entry.path)
        by_category[category] = by_category.get(category, 0) + 1
        payload = {"status": entry.status, "path": entry.path, "category": category, "reason": reason}
        if category == "release_scope":
            release_scope.append(payload)
        else:
            blockers.append(payload)

    return {
        "release_scope": release_scope,
        "blockers": blockers,
        "summary": {
            "total": len(entries),
            "release_scope": len(release_scope),
            "blockers": len(blockers),
            "by_category": by_category,
        },
        "ok": not blockers,
    }


def format_markdown(repo_root: Path, report: dict[str, object]) -> str:
    summary = report["summary"]
    blockers = report["blockers"]
    lines = [
        "# Release Hygiene Report",
        "",
        f"- repo: `{repo_root}`",
        f"- total dirty entries: `{summary['total']}`",
        f"- release scope: `{summary['release_scope']}`",
        f"- blockers: `{summary['blockers']}`",
        f"- ok: `{str(report['ok']).lower()}`",
        "",
        "## Blockers",
    ]
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
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    entries = collect_git_status(repo_root)
    report = build_report(entries)
    report["repo_root"] = str(repo_root)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(format_markdown(repo_root, report))

    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
