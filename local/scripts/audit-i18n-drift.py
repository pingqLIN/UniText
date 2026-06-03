#!/usr/bin/env python3
from __future__ import annotations

import argparse
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--sample-size", type=int, default=40)
    parser.add_argument("--locale", action="append", dest="locales")
    parser.add_argument("--source-doc", action="append", dest="source_docs")
    parser.add_argument("--output")
    parser.add_argument("--exit-zero", action="store_true")
    return parser.parse_args()


def render_markdown(summary: dict[str, object]) -> str:
    lines = [
        "# UniText i18n Drift Report",
        "",
        f"- manifest: `{summary['manifest_path']}`",
        f"- default locale: `{summary['default_locale']}`",
        f"- active locale count: `{summary['locale_count']}`",
        f"- archived locale count: `{summary['archived_locale_count']}`",
        f"- source doc count: `{summary['source_doc_count']}`",
        f"- required source doc count: `{summary['required_source_doc_count']}`",
        f"- required issues found: `{summary['required_issues_found']}`",
        f"- optional issues found: `{summary['optional_issues_found']}`",
        f"- issues found: `{summary['issues_found']}`",
        "",
        "## By Locale",
        "",
        "| locale | required missing | required stale | required untracked | optional missing | optional stale | optional untracked | source missing |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for locale, counts in summary["by_locale"].items():
        lines.append(
            f"| `{locale}` | {counts['required_missing']} | {counts['required_stale']} | {counts['required_untracked']} | {counts['optional_missing']} | {counts['optional_stale']} | {counts['optional_untracked']} | {counts['source_missing']} |"
        )

    lines.extend(
        [
            "",
            "## By Source Doc",
            "",
            "| source doc | required | missing | stale | untracked | source missing |",
            "|---|---|---:|---:|---:|---:|",
        ]
    )

    for source_doc, counts in summary["by_source_doc"].items():
        lines.append(
            f"| `{source_doc}` | {str(counts['required']).lower()} | {counts['missing']} | {counts['stale']} | {counts['untracked']} | {counts['source_missing']} |"
        )

    sample_issues = summary["sample_issues"]
    if sample_issues:
        lines.extend(
            [
                "",
                "## Sample Issues",
                "",
                "| locale | source doc | status | translated doc |",
                "|---|---|---|---|",
            ]
        )
        for issue in sample_issues:
            lines.append(
                f"| `{issue['locale']}` | `{issue['source_doc']}` | `{issue['status']}` | `{issue['translated_doc']}` |"
            )

    return "\n".join(lines) + "\n"


def write_output(text: str, output: str | None) -> None:
    if output is None:
        print(text)
        return

    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(path)


def main() -> int:
    args = parse_args()
    repo = Path(args.repo_root).resolve() if args.repo_root else get_repo_root()
    manifest_path = repo / "i18n" / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest_locales = list(manifest["locales"])
    archived_locales = list(manifest.get("archived_locales", []))
    manifest_source_docs = list(manifest["source_docs"])
    required_source_docs = set(manifest.get("required_source_docs", manifest_source_docs))
    locales = args.locales or manifest_locales
    source_docs = args.source_docs or manifest_source_docs
    unknown_locales = sorted(set(locales) - set(manifest_locales))
    unknown_source_docs = sorted(set(source_docs) - set(manifest_source_docs))
    if unknown_locales:
        raise SystemExit(f"Unknown locales: {', '.join(unknown_locales)}")
    if unknown_source_docs:
        raise SystemExit(f"Unknown source docs: {', '.join(unknown_source_docs)}")

    issues: list[dict[str, object]] = []
    required_issues = 0
    optional_issues = 0
    locale_counts: dict[str, Counter[str]] = {locale: Counter() for locale in locales}
    source_counts: dict[str, Counter[str]] = {source_doc: Counter() for source_doc in source_docs}

    for source_doc in source_docs:
        source_path = repo / source_doc
        source_exists = source_path.exists()
        source_sha, source_timestamp = run_git(repo, source_doc) if source_exists else (None, None)
        is_required = source_doc in required_source_docs

        for locale in locales:
            translated_doc = Path("i18n") / locale / source_doc
            translated_path = repo / translated_doc
            if not source_exists:
                locale_counts[locale]["source_missing"] += 1
                source_counts[source_doc]["source_missing"] += 1
                issues.append(
                    {
                        "locale": locale,
                        "source_doc": source_doc,
                        "translated_doc": str(translated_doc).replace("\\", "/"),
                        "status": "source-missing",
                        "required": is_required,
                    }
                )
                continue

            if not translated_path.exists():
                locale_counts[locale]["missing"] += 1
                source_counts[source_doc]["missing"] += 1
                issues.append(
                    {
                        "locale": locale,
                        "source_doc": source_doc,
                        "translated_doc": str(translated_doc).replace("\\", "/"),
                        "status": "missing",
                        "source_sha": source_sha,
                        "required": is_required,
                    }
                )
                if is_required:
                    locale_counts[locale]["required_missing"] += 1
                    required_issues += 1
                else:
                    locale_counts[locale]["optional_missing"] += 1
                    optional_issues += 1
                continue

            translated_sha, translated_timestamp = run_git(repo, str(translated_doc).replace("\\", "/"))
            status = "up-to-date"
            if translated_timestamp is None:
                status = "untracked"
            elif source_timestamp is not None and translated_timestamp < source_timestamp:
                status = "stale"

            locale_counts[locale][status] += 1
            source_counts[source_doc][status] += 1
            if status != "up-to-date":
                if is_required:
                    locale_counts[locale][f"required_{status}"] += 1
                    required_issues += 1
                else:
                    locale_counts[locale][f"optional_{status}"] += 1
                    optional_issues += 1
                issues.append(
                    {
                        "locale": locale,
                        "source_doc": source_doc,
                        "translated_doc": str(translated_doc).replace("\\", "/"),
                        "status": status,
                        "source_sha": source_sha,
                        "translated_sha": translated_sha,
                        "required": is_required,
                    }
                )

    summary = {
        "manifest_path": str(manifest_path),
        "default_locale": manifest["default_locale"],
        "locale_count": len(locales),
        "archived_locale_count": len(archived_locales),
        "source_doc_count": len(source_docs),
        "required_source_doc_count": len([doc for doc in source_docs if doc in required_source_docs]),
        "selected_locales": locales,
        "archived_locales": archived_locales,
        "selected_source_docs": source_docs,
        "required_source_docs": [doc for doc in source_docs if doc in required_source_docs],
        "required_issues_found": required_issues,
        "optional_issues_found": optional_issues,
        "issues_found": len(issues),
        "by_locale": {
            locale: {
                "missing": locale_counts[locale]["missing"],
                "stale": locale_counts[locale]["stale"],
                "untracked": locale_counts[locale]["untracked"],
                "required_missing": locale_counts[locale]["required_missing"],
                "required_stale": locale_counts[locale]["required_stale"],
                "required_untracked": locale_counts[locale]["required_untracked"],
                "optional_missing": locale_counts[locale]["optional_missing"],
                "optional_stale": locale_counts[locale]["optional_stale"],
                "optional_untracked": locale_counts[locale]["optional_untracked"],
                "source_missing": locale_counts[locale]["source_missing"],
            }
            for locale in locales
        },
        "by_source_doc": {
            source_doc: {
                "required": source_doc in required_source_docs,
                "missing": source_counts[source_doc]["missing"],
                "stale": source_counts[source_doc]["stale"],
                "untracked": source_counts[source_doc]["untracked"],
                "source_missing": source_counts[source_doc]["source_missing"],
            }
            for source_doc in source_docs
        },
        "sample_issues": issues[: args.sample_size],
        "ok": required_issues == 0,
    }
    output = json.dumps(summary, indent=2) if args.format == "json" else render_markdown(summary)
    write_output(output, args.output)
    if args.exit_zero:
        return 0
    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
