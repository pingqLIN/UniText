#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path


def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def run_git(repo: Path, path: str) -> tuple[str | None, int | None]:
    command = [
        "git",
        "-C",
        str(repo),
        "log",
        "-1",
        "--format=%H|%ct",
        "--",
        path,
    ]
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    text = completed.stdout.strip()
    if not text:
        return None, None
    sha, stamp = text.split("|", 1)
    return sha, int(stamp)


def main() -> int:
    repo = get_repo_root()
    manifest_path = repo / "i18n" / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    locales = list(manifest["locales"])
    source_docs = list(manifest["source_docs"])
    issues: list[dict[str, object]] = []
    locale_counts: dict[str, Counter[str]] = {locale: Counter() for locale in locales}

    for source_doc in source_docs:
        source_path = repo / source_doc
        source_exists = source_path.exists()
        source_sha, source_timestamp = run_git(repo, source_doc) if source_exists else (None, None)

        for locale in locales:
            translated_doc = Path("i18n") / locale / source_doc
            translated_path = repo / translated_doc
            if not source_exists:
                locale_counts[locale]["source_missing"] += 1
                issues.append(
                    {
                        "locale": locale,
                        "source_doc": source_doc,
                        "translated_doc": str(translated_doc).replace("\\", "/"),
                        "status": "source-missing",
                    }
                )
                continue

            if not translated_path.exists():
                locale_counts[locale]["missing"] += 1
                issues.append(
                    {
                        "locale": locale,
                        "source_doc": source_doc,
                        "translated_doc": str(translated_doc).replace("\\", "/"),
                        "status": "missing",
                        "source_sha": source_sha,
                    }
                )
                continue

            translated_sha, translated_timestamp = run_git(repo, str(translated_doc).replace("\\", "/"))
            status = "up-to-date"
            if translated_timestamp is None:
                status = "untracked"
            elif source_timestamp is not None and translated_timestamp < source_timestamp:
                status = "stale"

            locale_counts[locale][status] += 1
            if status != "up-to-date":
                issues.append(
                    {
                        "locale": locale,
                        "source_doc": source_doc,
                        "translated_doc": str(translated_doc).replace("\\", "/"),
                        "status": status,
                        "source_sha": source_sha,
                        "translated_sha": translated_sha,
                    }
                )

    summary = {
        "manifest_path": str(manifest_path),
        "default_locale": manifest["default_locale"],
        "locale_count": len(locales),
        "source_doc_count": len(source_docs),
        "issues_found": len(issues),
        "by_locale": {
            locale: {
                "missing": locale_counts[locale]["missing"],
                "stale": locale_counts[locale]["stale"],
                "untracked": locale_counts[locale]["untracked"],
                "source_missing": locale_counts[locale]["source_missing"],
            }
            for locale in locales
        },
        "sample_issues": issues[:40],
        "ok": len(issues) == 0,
    }
    print(json.dumps(summary, indent=2))
    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
