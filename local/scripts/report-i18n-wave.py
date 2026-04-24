#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def collect_entries(repo_root: Path) -> list[dict[str, str]]:
    result = subprocess.run(
        ["git", "-C", str(repo_root), "status", "--porcelain=v1", "--untracked-files=all", "-z", "--", "i18n"],
        check=True,
        capture_output=True,
        text=False,
    )
    entries: list[dict[str, str]] = []
    for raw in result.stdout.split(b"\0"):
        if not raw:
            continue
        status = raw[:2].decode("utf-8", errors="replace")
        payload = raw[3:].decode("utf-8", errors="replace")
        path = payload.split(" -> ", 1)[-1]
        if path.startswith("i18n/"):
            entries.append({"status": status, "path": path})
    return entries


def is_eol_only(repo_root: Path, path: str) -> bool:
    result = subprocess.run(
        [
            "git",
            "-C",
            str(repo_root),
            "diff",
            "--ignore-cr-at-eol",
            "--ignore-space-at-eol",
            "--exit-code",
            "--",
            path,
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result.returncode == 0


def classify_paths(repo_root: Path, input_entries: list[dict[str, str]]) -> dict[str, object]:
    classified_entries: list[dict[str, str]] = []
    by_category = {"eol_only": 0, "substantive": 0, "new_file": 0}
    for entry in input_entries:
        status = entry["status"]
        path = entry["path"]
        if status == "??":
            category = "new_file"
            reason = "untracked i18n file"
        elif is_eol_only(repo_root, path):
            category = "eol_only"
            reason = "no substantive diff after ignoring CR and trailing-space EOL changes"
        else:
            category = "substantive"
            reason = "content differs after ignoring line-ending-only changes"
        by_category[category] += 1
        classified_entries.append({"status": status, "path": path, "category": category, "reason": reason})

    substantive_count = by_category["substantive"] + by_category["new_file"]
    return {
        "repo_root": str(repo_root),
        "entry_count": len(classified_entries),
        "safe_to_split": substantive_count == 0 and len(classified_entries) > 0,
        "summary": by_category,
        "entries": classified_entries,
    }


def format_markdown(report: dict[str, object]) -> str:
    lines = [
        "# I18n Wave Report",
        "",
        f"- repo: `{report['repo_root']}`",
        f"- dirty entries: `{report['entry_count']}`",
        f"- safe_to_split: `{str(report['safe_to_split']).lower()}`",
        "",
        "## Summary",
    ]
    summary = report["summary"]
    for key in ["eol_only", "substantive", "new_file"]:
        lines.append(f"- `{key}`: {summary.get(key, 0)}")
    lines.append("")
    lines.append("## Entries")
    for entry in report["entries"][:50]:
        lines.append(f"- `{entry['category']}` `{entry['path']}`: {entry['reason']}")
    if len(report["entries"]) > 50:
        lines.append(f"- ... {len(report['entries']) - 50} more")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Classify i18n dirty files as eol-only or substantive changes.")
    parser.add_argument("--repo-root", default=str(get_repo_root()))
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--markdown", action="store_true")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = classify_paths(repo_root, collect_entries(repo_root))

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(format_markdown(report))

    return 0 if report["safe_to_split"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
