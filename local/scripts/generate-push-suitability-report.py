from __future__ import annotations

import argparse
import json
import subprocess
from datetime import date
from pathlib import Path
from typing import Any


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def run_json_script(script_name: str) -> dict[str, Any]:
    script = Path(__file__).resolve().parent / script_name
    result = subprocess.run(
        ["python", str(script)],
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or f"{script_name} failed")
    return json.loads(result.stdout)


def run_git(args: list[str]) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo_root()), *args],
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or f"git {' '.join(args)} failed")
    return result.stdout.strip()


def branch_head() -> str:
    return run_git(["branch", "--show-current"])


def branch_status() -> str:
    return run_git(["status", "--short", "--branch"]).splitlines()[0]


def ahead_behind_status() -> dict[str, int | str]:
    branch = branch_head()
    if not branch:
        return {"branch": "", "tracking": "", "ahead": 0, "behind": 0}
    upstream = run_git(["rev-parse", "--abbrev-ref", f"{branch}@{{upstream}}"])
    counts = run_git(["rev-list", "--left-right", "--count", f"{branch}...{upstream}"]).split()
    ahead = int(counts[0]) if len(counts) >= 1 else 0
    behind = int(counts[1]) if len(counts) >= 2 else 0
    return {"branch": branch, "tracking": upstream, "ahead": ahead, "behind": behind}


def recent_commits(limit: int = 5) -> list[str]:
    output = run_git(["log", "--oneline", f"-{limit}"])
    return [line for line in output.splitlines() if line.strip()]


def recommendation_lines(payload: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    publishability = payload["publishability"]
    bootstrap = payload["bootstrap"]
    boundary = payload["boundary"]
    tracking = payload["tracking"]

    if not bootstrap["ok"]:
        lines.append("Do not push until bootstrap verification returns `ok = true`.")
    if not boundary["ok"]:
        lines.append("Do not push until workspace boundary violations are resolved.")
    if not publishability["structurally_publishable_if_permission_is_granted"]:
        lines.append("Do not push until publishability blockers are cleared.")
    if tracking["ahead"] > 0:
        lines.append(
            f"Review the local `{tracking['ahead']}`-commit batch against `origin/main` before any push discussion."
        )
    if tracking["behind"] > 0:
        lines.append(
            f"Reconcile the local branch with `{tracking['tracking']}` before any push, because it is behind by `{tracking['behind']}`."
        )
    if (
        bootstrap["ok"]
        and boundary["ok"]
        and publishability["structurally_publishable_if_permission_is_granted"]
        and tracking["behind"] == 0
    ):
        lines.append("Structurally ready for push review if the user explicitly grants push permission.")
    return lines


def build_payload() -> dict[str, Any]:
    bootstrap = run_json_script("verify-bootstrap.py")
    boundary = run_json_script("verify-workspace-boundaries.py")
    publishability = run_json_script("get-publishability-report.py")
    tracking = ahead_behind_status()
    return {
        "generated_on": str(date.today()),
        "repo_root": str(repo_root()),
        "branch_status": branch_status(),
        "tracking": tracking,
        "recent_commits": recent_commits(),
        "bootstrap": bootstrap,
        "boundary": boundary,
        "publishability": publishability,
        "recommendations": recommendation_lines(
            {
                "bootstrap": bootstrap,
                "boundary": boundary,
                "publishability": publishability,
                "tracking": tracking,
            }
        ),
    }


def format_markdown(payload: dict[str, Any]) -> str:
    tracking = payload["tracking"]
    bootstrap = payload["bootstrap"]
    boundary = payload["boundary"]
    publishability = payload["publishability"]
    commits = payload["recent_commits"]
    recommendations = payload["recommendations"]

    lines = [
        f"# UniText Push Suitability Report — {payload['generated_on']}",
        "",
        "> Scope: local push-readiness signals only.",
        "> Publication: local-only until explicitly approved by the user.",
        "",
        "## Current Repo State",
        "",
        f"- Repo: `{payload['repo_root']}`",
        f"- Branch status: `{payload['branch_status']}`",
        f"- Upstream tracking: `{tracking['tracking']}`",
        f"- Ahead commits: `{tracking['ahead']}`",
        f"- Behind commits: `{tracking['behind']}`",
        f"- Working tree clean: `{str(publishability['working_tree_clean']).lower()}`",
        "",
        "## Verification Summary",
        "",
        f"- `verify-bootstrap.py`: `ok = {str(bootstrap['ok']).lower()}`",
        f"- `verify-workspace-boundaries.py`: `ok = {str(boundary['ok']).lower()}`",
        f"- `get-publishability-report.py`: `structurally_publishable_if_permission_is_granted = {str(publishability['structurally_publishable_if_permission_is_granted']).lower()}`",
        f"- Boundary path violations: `{len(boundary['path_violations'])}`",
        f"- Boundary content violations: `{len(boundary['content_violations'])}`",
        "",
        "## Recent Commits",
        "",
    ]
    for commit in commits:
        lines.append(f"- `{commit}`")
    lines.extend(["", "## Recommendations", ""])
    for item in recommendations or ["No additional recommendation."]:
        lines.append(f"- {item}")
    lines.extend(["", "## Publish Boundary", ""])
    lines.append("- This report does not grant publish or push permission.")
    lines.append("- Even if structurally publishable, pushing still requires explicit user approval under the repo no-publish rule.")
    return "\n".join(lines) + "\n"


def default_output_path() -> Path:
    return repo_root() / "docs" / "reports" / "status" / f"PUSH_SUITABILITY_REPORT_{date.today().isoformat()}.md"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a local-only push suitability report.")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of markdown")
    parser.add_argument("--output", type=Path, default=None, help="write markdown or JSON output to a file")
    args = parser.parse_args()

    payload = build_payload()
    rendered = json.dumps(payload, indent=2, ensure_ascii=False) if args.json else format_markdown(payload)

    if args.output is not None:
        output_path = args.output
    elif args.json:
        output_path = None
    else:
        output_path = default_output_path()

    if output_path is not None:
        if not output_path.is_absolute():
            output_path = (repo_root() / output_path).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8", newline="\n")

    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
