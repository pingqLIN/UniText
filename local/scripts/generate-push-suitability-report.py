from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Any


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def run_json_script(script_name: str) -> dict[str, Any]:
    script = Path(__file__).resolve().parent / script_name
    result = subprocess.run(
        [sys.executable, str(script)],
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


def try_run_git_config(args: list[str]) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(repo_root()), *args],
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode == 1:
        return None
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or f"git {' '.join(args)} failed")
    return result.stdout.strip()


def tracking_branch_name(merge_ref: str) -> str:
    if merge_ref.startswith("refs/heads/"):
        return merge_ref.removeprefix("refs/heads/")
    return merge_ref


def tracking_ref_name(remote: str, merge_ref: str) -> str:
    return f"{remote}/{tracking_branch_name(merge_ref)}"


def tracking_remote_ref(remote: str, merge_ref: str) -> str:
    return f"refs/remotes/{remote}/{tracking_branch_name(merge_ref)}"


def git_ref_exists(ref: str) -> bool:
    result = subprocess.run(
        ["git", "-C", str(repo_root()), "show-ref", "--verify", "--quiet", ref],
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode == 0:
        return True
    if result.returncode == 1:
        return False
    raise RuntimeError(result.stderr.strip() or result.stdout.strip() or f"git show-ref --verify {ref} failed")


def branch_head() -> str:
    return run_git(["branch", "--show-current"])


def branch_status() -> str:
    return run_git(["status", "--short", "--branch"]).splitlines()[0]


def ahead_behind_status() -> dict[str, int | str | bool | None]:
    branch = branch_head()
    if not branch:
        return {
            "branch": "",
            "tracking": None,
            "upstream_configured": False,
            "tracking_resolved": False,
            "ahead": None,
            "behind": None,
        }
    remote = try_run_git_config(["config", "--get", f"branch.{branch}.remote"])
    merge_ref = try_run_git_config(["config", "--get", f"branch.{branch}.merge"])
    if not remote or not merge_ref:
        return {
            "branch": branch,
            "tracking": None,
            "upstream_configured": False,
            "tracking_resolved": False,
            "ahead": None,
            "behind": None,
        }
    tracking = tracking_ref_name(remote, merge_ref)
    if not git_ref_exists(tracking_remote_ref(remote, merge_ref)):
        return {
            "branch": branch,
            "tracking": tracking,
            "upstream_configured": True,
            "tracking_resolved": False,
            "ahead": None,
            "behind": None,
        }
    counts = run_git(["rev-list", "--left-right", "--count", f"{branch}...{tracking}"]).split()
    ahead = int(counts[0]) if len(counts) >= 1 else 0
    behind = int(counts[1]) if len(counts) >= 2 else 0
    return {
        "branch": branch,
        "tracking": tracking,
        "upstream_configured": True,
        "tracking_resolved": True,
        "ahead": ahead,
        "behind": behind,
    }


def recent_commits(limit: int = 5) -> list[str]:
    output = run_git(["log", "--oneline", f"-{limit}"])
    return [line for line in output.splitlines() if line.strip()]


def recommendation_lines(payload: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    publishability = payload["publishability"]
    bootstrap = payload["bootstrap"]
    boundary = payload["boundary"]
    tracking = payload["tracking"]
    tracking_branch = tracking.get("branch", "")
    upstream_configured = bool(tracking.get("upstream_configured", tracking.get("tracking")))
    tracking_resolved = bool(tracking.get("tracking_resolved", upstream_configured and tracking.get("tracking")))
    ahead = tracking.get("ahead")
    behind = tracking.get("behind")

    if not bootstrap["ok"]:
        lines.append("Do not push until bootstrap verification returns `ok = true`.")
    if not boundary["ok"]:
        lines.append("Do not push until workspace boundary violations are resolved.")
    if not publishability["structurally_publishable_if_permission_is_granted"]:
        lines.append("Do not push until publishability blockers are cleared.")
    if not tracking_branch:
        lines.append("Push suitability review is incomplete because HEAD is detached; switch to a branch before any push review.")
    elif not upstream_configured:
        lines.append(
            f"Configure an upstream tracking branch for `{tracking_branch}` before treating this branch as push-ready."
        )
    elif not tracking_resolved:
        lines.append(
            f"Fetch or repair the upstream tracking ref `{tracking['tracking']}` before treating commit distance as authoritative."
        )
    if isinstance(ahead, int) and ahead > 0:
        lines.append(
            f"Review the local `{ahead}`-commit batch against `{tracking['tracking']}` before any push discussion."
        )
    if isinstance(behind, int) and behind > 0:
        lines.append(
            f"Reconcile the local branch with `{tracking['tracking']}` before any push, because it is behind by `{behind}`."
        )
    if (
        tracking_branch
        and upstream_configured
        and tracking_resolved
        and bootstrap["ok"]
        and boundary["ok"]
        and publishability["structurally_publishable_if_permission_is_granted"]
        and behind == 0
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
    upstream_configured = bool(tracking.get("upstream_configured", tracking.get("tracking")))
    tracking_resolved = bool(tracking.get("tracking_resolved", upstream_configured and tracking.get("tracking")))
    ahead = tracking.get("ahead")
    behind = tracking.get("behind")
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
        f"- Upstream tracking: `{tracking['tracking'] or 'not configured'}`",
        f"- Upstream configured: `{str(upstream_configured).lower()}`",
        f"- Upstream resolved: `{str(tracking_resolved).lower()}`",
        f"- Ahead commits: `{ahead if ahead is not None else 'unknown'}`",
        f"- Behind commits: `{behind if behind is not None else 'unknown'}`",
        f"- Working tree clean: `{str(publishability['working_tree_clean']).lower()}`",
        "- Note: commit distance is captured at report generation time. If this report is committed afterward, the actual local ahead count increases by that report commit.",
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
    return repo_root() / "ops" / "reports" / f"PUSH_SUITABILITY_REPORT_{date.today().isoformat()}.md"


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
