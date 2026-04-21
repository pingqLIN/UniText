#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run bounded UniText self-repair simulations.")
    parser.add_argument("--scenario", default="runtime-target-drift")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--output")
    parser.add_argument("--exit-zero", action="store_true")
    return parser.parse_args()


def run_command(command: list[str]) -> tuple[int, str, str]:
    completed = subprocess.run(
        command,
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return completed.returncode, completed.stdout, completed.stderr


def build_wrong_target(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    (path / "placeholder.txt").write_text("mismatched target\n", encoding="utf-8")


def render_markdown(report: dict[str, object]) -> str:
    before = report["before"]
    after = report["after"]
    lines = [
        f"# Self-Repair Simulation — {report['scenario']}",
        "",
        f"- generated_at: `{report['generated_at']}`",
        f"- classification: `{report['classification']}`",
        f"- recovered: `{str(report['recovered']).lower()}`",
        f"- repo_root: `{report['repo_root']}`",
        f"- simulated_home: `{report['simulated_home']}`",
        "",
        "## Before",
        "",
        f"- verify_exit_code: `{before['verify_exit_code']}`",
        f"- verify_ok: `{before['verify_ok']}`",
        "",
        "## Repair",
        "",
        f"- bootstrap_exit_code: `{report['repair']['bootstrap_exit_code']}`",
        f"- bootstrap_applied: `{str(report['repair']['bootstrap_applied']).lower()}`",
        "",
        "## After",
        "",
        f"- verify_exit_code: `{after['verify_exit_code']}`",
        f"- verify_ok: `{after['verify_ok']}`",
        "",
    ]
    return "\n".join(lines) + "\n"


def write_output(text: str, output: str | None) -> None:
    if output is None:
        print(text)
        return
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")
    print(output_path)


def run_runtime_target_drift() -> dict[str, object]:
    scenario_path = REPO_ROOT / "docs" / "architecture" / "scenarios" / "runtime-target-drift.json"
    scenario = json.loads(scenario_path.read_text(encoding="utf-8"))

    with tempfile.TemporaryDirectory(prefix="unitext-sim-home-") as home_dir_name:
        home_dir = Path(home_dir_name)
        history_root = home_dir / "history"

        for relative in (".claude/skills", ".gemini/skills", ".agents/skills"):
            build_wrong_target(home_dir / relative)

        verify_before_command = [
            "python",
            str(REPO_ROOT / "local" / "scripts" / "verify-bootstrap.py"),
            "--home-dir",
            str(home_dir),
            "--skip-codex",
            "--skip-copilot",
        ]
        before_code, before_stdout, before_stderr = run_command(verify_before_command)
        before_report = json.loads(before_stdout)

        bootstrap_command = [
            "python",
            str(REPO_ROOT / "local" / "scripts" / "bootstrap.py"),
            "--home-dir",
            str(home_dir),
            "--history-root",
            str(history_root),
            "--skip-runtime-build",
            "--skip-codex",
            "--skip-copilot",
            "--skip-project-mcp",
            "--force",
        ]
        bootstrap_code, bootstrap_stdout, bootstrap_stderr = run_command(bootstrap_command)
        bootstrap_report = json.loads(bootstrap_stdout) if bootstrap_stdout.strip() else {}

        verify_after_command = [
            "python",
            str(REPO_ROOT / "local" / "scripts" / "verify-bootstrap.py"),
            "--home-dir",
            str(home_dir),
            "--skip-codex",
            "--skip-copilot",
        ]
        after_code, after_stdout, after_stderr = run_command(verify_after_command)
        after_report = json.loads(after_stdout)

        recovered = (
            before_report.get("ok") is False
            and bootstrap_code == 0
            and after_report.get("ok") is True
        )
        classification = "recovered" if recovered else "blocked-with-escalation"

        return {
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "scenario": scenario["id"],
            "scenario_config": str(scenario_path),
            "repo_root": str(REPO_ROOT),
            "simulated_home": str(home_dir),
            "classification": classification,
            "recovered": recovered,
            "before": {
                "verify_exit_code": before_code,
                "verify_ok": before_report.get("ok"),
                "stdout": before_report,
                "stderr": before_stderr.strip(),
            },
            "repair": {
                "bootstrap_exit_code": bootstrap_code,
                "bootstrap_applied": bootstrap_code == 0,
                "stdout": bootstrap_report,
                "stderr": bootstrap_stderr.strip(),
            },
            "after": {
                "verify_exit_code": after_code,
                "verify_ok": after_report.get("ok"),
                "stdout": after_report,
                "stderr": after_stderr.strip(),
            },
        }


def main() -> int:
    args = parse_args()
    if args.scenario != "runtime-target-drift":
        raise SystemExit(f"unsupported scenario: {args.scenario}")

    report = run_runtime_target_drift()
    output = json.dumps(report, indent=2) if args.format == "json" else render_markdown(report)
    write_output(output, args.output)

    if args.exit_zero:
        return 0
    return 0 if report["recovered"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
