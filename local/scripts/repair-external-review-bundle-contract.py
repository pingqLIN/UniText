#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath


REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_RELATIVE_PATH = "docs/reviews/external-review-bundle.contract.json"

LEGACY_PATH_MAP = {
    "EXTERNAL_REVIEW_COVER_NOTE.md": "docs/reviews/EXTERNAL_REVIEW_COVER_NOTE.md",
    "EXTERNAL_REVIEW_HIGHLIGHTS.md": "docs/reviews/EXTERNAL_REVIEW_HIGHLIGHTS.md",
    "EXTERNAL_REVIEW_PACKAGE.md": "docs/reviews/EXTERNAL_REVIEW_PACKAGE.md",
    "ESSENTIAL_SKILLS_SHORTLIST.md": "docs/reviews/ESSENTIAL_SKILLS_SHORTLIST.md",
    "PROJECT_STATUS_REPORT_2026-03-23.md": "docs/reports/status/PROJECT_STATUS_REPORT_2026-03-23.md",
    "../reports/status/PROJECT_STATUS_REPORT_2026-03-23.md": "docs/reports/status/PROJECT_STATUS_REPORT_2026-03-23.md",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Normalize external review bundle contract paths.")
    parser.add_argument("--repo-root", default=str(REPO_ROOT))
    parser.add_argument("--write", action="store_true")
    return parser.parse_args()


def normalize_path(value: str) -> str:
    raw = value.replace("\\", "/")
    if raw in LEGACY_PATH_MAP:
        return LEGACY_PATH_MAP[raw]

    basename = PurePosixPath(raw).name
    if basename in LEGACY_PATH_MAP:
        return LEGACY_PATH_MAP[basename]

    return raw


def normalize_list(entries: list[str]) -> tuple[list[str], list[dict[str, str]]]:
    normalized: list[str] = []
    changes: list[dict[str, str]] = []
    seen: set[str] = set()

    for original in entries:
        repaired = normalize_path(original)
        if repaired != original:
            changes.append({"from": original, "to": repaired, "reason": "legacy-path"})
        if repaired in seen:
            changes.append({"from": original, "to": repaired, "reason": "deduplicated"})
            continue
        normalized.append(repaired)
        seen.add(repaired)

    return normalized, changes


def validate_contract(repo_root: Path, contract: dict[str, object]) -> dict[str, object]:
    files = [str(item) for item in contract.get("files", [])]
    directories = [str(item) for item in contract.get("directories", [])]
    reading_order = [str(item) for item in contract.get("reading_order", [])]
    skills = contract.get("skills", {})
    skill_names = []
    if isinstance(skills, dict):
        skill_names.extend(str(item) for item in skills.get("core", []))
        skill_names.extend(str(item) for item in skills.get("expansion", []))

    missing_paths = [
        path
        for path in files + directories
        if not (repo_root / path).exists()
    ]
    missing_skill_dirs = [
        name
        for name in skill_names
        if not (repo_root / "registry" / "skills" / name).exists()
    ]
    missing_reading_order_entries = [path for path in reading_order if path not in files]

    return {
        "missing_paths": missing_paths,
        "missing_skill_dirs": missing_skill_dirs,
        "missing_reading_order_entries": missing_reading_order_entries,
        "ok": not (missing_paths or missing_skill_dirs or missing_reading_order_entries),
    }


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    contract_path = repo_root / CONTRACT_RELATIVE_PATH
    contract = json.loads(contract_path.read_text(encoding="utf-8"))

    files, file_changes = normalize_list([str(item) for item in contract.get("files", [])])
    reading_order, reading_changes = normalize_list([str(item) for item in contract.get("reading_order", [])])

    added_to_files: list[str] = []
    for item in reading_order:
        if item not in files:
            files.append(item)
            added_to_files.append(item)

    contract["files"] = files
    contract["reading_order"] = reading_order

    validation = validate_contract(repo_root, contract)
    changed = bool(file_changes or reading_changes or added_to_files)

    if args.write and changed:
        contract_path.write_text(json.dumps(contract, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    report = {
        "repo_root": str(repo_root),
        "contract_path": str(contract_path),
        "changed": changed,
        "write_applied": bool(args.write and changed),
        "file_changes": file_changes,
        "reading_order_changes": reading_changes,
        "added_to_files": added_to_files,
        "validation": validation,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if validation["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
