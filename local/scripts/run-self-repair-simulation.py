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


def run_command(command: list[str], cwd: Path | None = None) -> tuple[int, str, str]:
    completed = subprocess.run(
        command,
        cwd=str(cwd or REPO_ROOT),
        text=True,
        encoding="utf-8",
        errors="replace",
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


def load_external_review_contract(repo_root: Path) -> dict[str, object]:
    contract_path = repo_root / "docs" / "reviews" / "external-review-bundle.contract.json"
    return json.loads(contract_path.read_text(encoding="utf-8"))


def copy_path(source_root: Path, target_root: Path, relative_path: str) -> None:
    source = source_root / relative_path
    target = target_root / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    if source.is_dir():
        shutil.copytree(source, target, dirs_exist_ok=True)
        return
    shutil.copy2(source, target)


def build_external_review_fixture(target_root: Path) -> None:
    contract = load_external_review_contract(REPO_ROOT)

    fixture_paths = {
        "docs/reviews/external-review-bundle.contract.json",
        "local/scripts/export-review-package.ps1",
        "local/scripts/lib/path-safety.ps1",
        "local/scripts/repair-external-review-bundle-contract.py",
    }
    fixture_paths.update(str(item) for item in contract.get("files", []))
    fixture_paths.update(str(item) for item in contract.get("directories", []))

    skills = contract.get("skills", {})
    if isinstance(skills, dict):
        for name in [str(item) for item in skills.get("core", []) + skills.get("expansion", [])]:
            fixture_paths.add(f"registry/skills/{name}")

    for relative_path in sorted(fixture_paths):
        copy_path(REPO_ROOT, target_root, relative_path)


def mutate_review_bundle_contract(repo_root: Path) -> None:
    contract_path = repo_root / "docs" / "reviews" / "external-review-bundle.contract.json"
    contract = json.loads(contract_path.read_text(encoding="utf-8"))

    legacy_map = {
        "docs/reviews/EXTERNAL_REVIEW_COVER_NOTE.md": "EXTERNAL_REVIEW_COVER_NOTE.md",
        "docs/reviews/EXTERNAL_REVIEW_HIGHLIGHTS.md": "EXTERNAL_REVIEW_HIGHLIGHTS.md",
        "docs/reviews/EXTERNAL_REVIEW_PACKAGE.md": "EXTERNAL_REVIEW_PACKAGE.md",
        "docs/reviews/ESSENTIAL_SKILLS_SHORTLIST.md": "ESSENTIAL_SKILLS_SHORTLIST.md",
        "docs/reports/status/PROJECT_STATUS_REPORT_2026-03-23.md": "../reports/status/PROJECT_STATUS_REPORT_2026-03-23.md",
    }

    def rewrite(entries: list[str]) -> list[str]:
        return [legacy_map.get(item, item) for item in entries]

    contract["reading_order"] = rewrite([str(item) for item in contract.get("reading_order", [])])
    contract["files"] = rewrite([str(item) for item in contract.get("files", [])])
    contract_path.write_text(json.dumps(contract, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def build_workspace_sensitive_fixture(target_root: Path) -> None:
    fixture_paths = {
        "AGENTS.md",
        "WORKSPACE_SENSITIVE_METADATA_RULES.json",
        "WORKSPACE_SENSITIVE_METADATA_RULES.md",
        "README.md",
        "INDEX.md",
        "VISION.md",
        "RESOURCE_SPEC.md",
        "OPERATIONS.md",
        "PROJECT_MODES.md",
        "SECRET_HANDLING_GUIDELINES.md",
        "TEMPLATE_RELEASE_PACKAGE.md",
        "TEMPLATE_RELEASE_CHECKLIST.md",
        "REBUILD_AS_NEW_PROJECT.md",
        "MILESTONES.md",
        "NO_PUBLISH_POLICY.md",
        "DOCUMENT_PLACEMENT_POLICY.md",
        "BOUNDARY_INCIDENT_REVIEW_TEMPLATE.md",
        ".github/pull_request_template.md",
        ".mcp.json",
        ".claude/settings.json",
        "docs/adapters/COPILOT_CLI_ADAPTER_NOTE.md",
        "docs/concepts/SKILL0_COLLABORATION_VISION.md",
        "docs/reviews/external-review-bundle.contract.json",
        "docs/reviews/ESSENTIAL_SKILLS_SHORTLIST.md",
        "docs/reviews/EXTERNAL_REVIEW_PACKAGE.md",
        "docs/reviews/EXTERNAL_REVIEW_COVER_NOTE.md",
        "docs/reviews/EXTERNAL_REVIEW_HIGHLIGHTS.md",
        "local/scripts/bootstrap.py",
        "local/scripts/git-startup.ps1",
        "local/scripts/health-check.ps1",
        "local/scripts/export-template-package.ps1",
        "local/scripts/preview-renormalize.ps1",
        "local/scripts/preview-renormalize.py",
        "local/scripts/run-renormalize.ps1",
        "local/scripts/run-renormalize.py",
        "local/scripts/verify-template-package.ps1",
        "local/scripts/export-rebuild-project.ps1",
        "local/scripts/verify-rebuild-project.ps1",
        "local/scripts/validate-workspace-sensitive-metadata-rules.ps1",
        "local/scripts/validate-workspace-sensitive-metadata-rules.py",
        "local/scripts/verify-workspace-boundaries.ps1",
        "local/scripts/verify-workspace-boundaries.py",
        "local/scripts/get-publishability-report.ps1",
        "local/scripts/get-publishability-report.py",
        "local/scripts/get-document-placement-recommendation.ps1",
        "local/scripts/lib/renormalize_core.py",
        "local/scripts/lib/workspace-sensitive-metadata.ps1",
        "local/scripts/lib/workspace_sensitive_metadata.py",
        "local/scripts/lib/workspace_boundaries.py",
        "local/scripts/repair-workspace-sensitive-rules.py",
        "local/scripts/repair-workspace-sensitive-content-patterns.py",
        "registry/README.md",
        "registry/skills/conversation-memo/SKILL.md",
        "registry/skills/conversation-memo/references/memo-lifecycle.md",
        "registry/skills/azure-compute/workflows/vm-troubleshooter/references/credential-auth-errors.md",
        "registry/skills/azure-compute/workflows/vm-troubleshooter/references/vm-agent-not-responding.md",
        "registry/skills/azure-deploy/references/recipes/azcli/verify.md",
        "registry/skills/azure-deploy/references/recipes/azd/verify.md",
        "registry/skills/azure-deploy/references/recipes/bicep/verify.md",
        "registry/skills/azure-deploy/references/recipes/cicd/verify.md",
        "registry/skills/azure-deploy/references/recipes/terraform/verify.md",
        "registry/skills/azure-diagnostics/SKILL.md",
        "registry/skills/azure-diagnostics/aks-troubleshooting/aks-troubleshooting.md",
        "registry/skills/azure-diagnostics/aks-troubleshooting/networking.md",
        "registry/skills/azure-diagnostics/references/container-apps/README.md",
    }

    for relative_path in sorted(fixture_paths):
        copy_path(REPO_ROOT, target_root, relative_path)

    for relative_dir in (".github", "registry"):
        (target_root / relative_dir).mkdir(parents=True, exist_ok=True)


def initialize_git_fixture(target_root: Path) -> None:
    run_command(["git", "init", "-q"], cwd=target_root)
    run_command(["git", "config", "user.name", "Simulation Bot"], cwd=target_root)
    run_command(["git", "config", "user.email", "simulation@example.com"], cwd=target_root)
    run_command(["git", "add", "-A"], cwd=target_root)


def mutate_workspace_sensitive_rules(repo_root: Path) -> None:
    rules_path = repo_root / "WORKSPACE_SENSITIVE_METADATA_RULES.json"
    rules = json.loads(rules_path.read_text(encoding="utf-8"))

    legacy_map = {
        "docs/adapters/COPILOT_CLI_ADAPTER_NOTE.md": "COPILOT_CLI_ADAPTER_NOTE.md",
        "docs/concepts/SKILL0_COLLABORATION_VISION.md": "SKILL0_COLLABORATION_VISION.md",
        "docs/reviews/EXTERNAL_REVIEW_PACKAGE.md": "EXTERNAL_REVIEW_PACKAGE.md",
        "docs/reviews/EXTERNAL_REVIEW_COVER_NOTE.md": "EXTERNAL_REVIEW_COVER_NOTE.md",
        "docs/reviews/EXTERNAL_REVIEW_HIGHLIGHTS.md": "EXTERNAL_REVIEW_HIGHLIGHTS.md",
        "docs/reviews/ESSENTIAL_SKILLS_SHORTLIST.md": "ESSENTIAL_SKILLS_SHORTLIST.md",
    }

    rules["shared_surface_scope"] = [
        legacy_map.get(str(item), str(item))
        for item in rules.get("shared_surface_scope", [])
    ]
    rules_path.write_text(json.dumps(rules, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def mutate_workspace_sensitive_content_patterns(repo_root: Path) -> None:
    rules_path = repo_root / "WORKSPACE_SENSITIVE_METADATA_RULES.json"
    rules = json.loads(rules_path.read_text(encoding="utf-8"))

    for pattern in rules.get("content_patterns", []):
        if pattern.get("label") != "live workspace hostname":
            continue
        pattern["regex"] = (
            r"(?i)\b(?:zone hostname|ingress|hostnames?|domain)\b[^\r\n]*\b"
            r"(?!workspace\.example\.com\b)(?!example\.com\b)(?:[a-z0-9-]+\.)+[a-z]{2,}\b"
        )
        pattern["skip_script_pattern_lines"] = True

    rules_path.write_text(json.dumps(rules, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


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


def run_review_bundle_contract_drift() -> dict[str, object]:
    scenario_path = REPO_ROOT / "docs" / "architecture" / "scenarios" / "review-bundle-contract-drift.json"
    scenario = json.loads(scenario_path.read_text(encoding="utf-8"))

    with tempfile.TemporaryDirectory(prefix="unitext-sim-repo-") as repo_dir_name:
        fixture_root = Path(repo_dir_name)
        build_external_review_fixture(fixture_root)
        mutate_review_bundle_contract(fixture_root)

        export_script = fixture_root / "local" / "scripts" / "export-review-package.ps1"
        export_before_command = [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            f"& '{export_script}' -DryRun | ConvertTo-Json -Depth 8",
        ]
        before_code, before_stdout, before_stderr = run_command(export_before_command)

        repair_command = [
            "python",
            str(fixture_root / "local" / "scripts" / "repair-external-review-bundle-contract.py"),
            "--repo-root",
            str(fixture_root),
            "--write",
        ]
        repair_code, repair_stdout, repair_stderr = run_command(repair_command)
        repair_report = json.loads(repair_stdout) if repair_stdout.strip() else {}

        export_after_command = [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            f"& '{export_script}' -DryRun | ConvertTo-Json -Depth 8",
        ]
        after_code, after_stdout, after_stderr = run_command(export_after_command)
        after_report = json.loads(after_stdout) if after_stdout.strip() else {}

        recovered = before_code != 0 and repair_code == 0 and after_code == 0
        classification = "recovered" if recovered else "blocked-with-escalation"

        return {
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "scenario": scenario["id"],
            "scenario_config": str(scenario_path),
            "repo_root": str(REPO_ROOT),
            "simulated_repo": str(fixture_root),
            "classification": classification,
            "recovered": recovered,
            "before": {
                "export_exit_code": before_code,
                "export_ok": before_code == 0,
                "stdout": before_stdout.strip(),
                "stderr": before_stderr.strip(),
            },
            "repair": {
                "repair_exit_code": repair_code,
                "repair_ok": repair_code == 0,
                "stdout": repair_report,
                "stderr": repair_stderr.strip(),
            },
            "after": {
                "export_exit_code": after_code,
                "export_ok": after_code == 0,
                "stdout": after_report,
                "stderr": after_stderr.strip(),
            },
        }


def run_workspace_sensitive_boundary_drift() -> dict[str, object]:
    scenario_path = REPO_ROOT / "docs" / "architecture" / "scenarios" / "workspace-sensitive-boundary-drift.json"
    scenario = json.loads(scenario_path.read_text(encoding="utf-8"))

    with tempfile.TemporaryDirectory(prefix="unitext-sim-boundary-") as repo_dir_name:
        fixture_root = Path(repo_dir_name)
        build_workspace_sensitive_fixture(fixture_root)
        mutate_workspace_sensitive_rules(fixture_root)

        validate_script = fixture_root / "local" / "scripts" / "validate-workspace-sensitive-metadata-rules.ps1"
        validate_before_command = [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            f"& '{validate_script}' | ConvertTo-Json -Depth 8",
        ]
        before_code, before_stdout, before_stderr = run_command(validate_before_command)
        before_report = json.loads(before_stdout) if before_stdout.strip() else {}

        repair_command = [
            "python",
            str(fixture_root / "local" / "scripts" / "repair-workspace-sensitive-rules.py"),
            "--repo-root",
            str(fixture_root),
            "--write",
        ]
        repair_code, repair_stdout, repair_stderr = run_command(repair_command)
        repair_report = json.loads(repair_stdout) if repair_stdout.strip() else {}

        validate_after_command = [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            f"& '{validate_script}' | ConvertTo-Json -Depth 8",
        ]
        after_code, after_stdout, after_stderr = run_command(validate_after_command)
        after_report = json.loads(after_stdout) if after_stdout.strip() else {}

        recovered = (
            before_report.get("ok") is False
            and repair_code == 0
            and after_report.get("ok") is True
        )
        classification = "recovered" if recovered else "blocked-with-escalation"

        return {
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "scenario": scenario["id"],
            "scenario_config": str(scenario_path),
            "repo_root": str(REPO_ROOT),
            "simulated_repo": str(fixture_root),
            "classification": classification,
            "recovered": recovered,
            "before": {
                "validate_exit_code": before_code,
                "validate_ok": before_report.get("ok"),
                "stdout": before_report,
                "stderr": before_stderr.strip(),
            },
            "repair": {
                "repair_exit_code": repair_code,
                "repair_ok": repair_code == 0,
                "stdout": repair_report,
                "stderr": repair_stderr.strip(),
            },
            "after": {
                "validate_exit_code": after_code,
                "validate_ok": after_report.get("ok"),
                "stdout": after_report,
                "stderr": after_stderr.strip(),
            },
        }


def run_workspace_sensitive_content_pattern_drift() -> dict[str, object]:
    scenario_path = REPO_ROOT / "docs" / "architecture" / "scenarios" / "workspace-sensitive-content-pattern-drift.json"
    scenario = json.loads(scenario_path.read_text(encoding="utf-8"))

    with tempfile.TemporaryDirectory(prefix="unitext-sim-content-pattern-") as repo_dir_name:
        fixture_root = Path(repo_dir_name)
        build_workspace_sensitive_fixture(fixture_root)
        initialize_git_fixture(fixture_root)
        mutate_workspace_sensitive_content_patterns(fixture_root)

        validate_script = fixture_root / "local" / "scripts" / "validate-workspace-sensitive-metadata-rules.ps1"
        verify_script = fixture_root / "local" / "scripts" / "verify-workspace-boundaries.ps1"

        validate_before_command = [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            f"& '{validate_script}' | ConvertTo-Json -Depth 10",
        ]
        before_validate_code, before_validate_stdout, before_validate_stderr = run_command(validate_before_command)
        before_validate_report = json.loads(before_validate_stdout) if before_validate_stdout.strip() else {}

        verify_before_command = [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            f"& '{verify_script}' | ConvertTo-Json -Depth 10",
        ]
        before_verify_code, before_verify_stdout, before_verify_stderr = run_command(verify_before_command)
        before_verify_report = json.loads(before_verify_stdout) if before_verify_stdout.strip() else {}

        repair_command = [
            "python",
            str(fixture_root / "local" / "scripts" / "repair-workspace-sensitive-content-patterns.py"),
            "--repo-root",
            str(fixture_root),
            "--write",
        ]
        repair_code, repair_stdout, repair_stderr = run_command(repair_command)
        repair_report = json.loads(repair_stdout) if repair_stdout.strip() else {}

        validate_after_command = [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            f"& '{validate_script}' | ConvertTo-Json -Depth 10",
        ]
        after_validate_code, after_validate_stdout, after_validate_stderr = run_command(validate_after_command)
        after_validate_report = json.loads(after_validate_stdout) if after_validate_stdout.strip() else {}

        verify_after_command = [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            f"& '{verify_script}' | ConvertTo-Json -Depth 10",
        ]
        after_verify_code, after_verify_stdout, after_verify_stderr = run_command(verify_after_command)
        after_verify_report = json.loads(after_verify_stdout) if after_verify_stdout.strip() else {}

        recovered = (
            before_validate_report.get("ok") is False
            and before_verify_report.get("ok") is False
            and repair_code == 0
            and after_validate_report.get("ok") is True
            and after_verify_report.get("ok") is True
        )
        classification = "recovered" if recovered else "blocked-with-escalation"

        return {
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "scenario": scenario["id"],
            "scenario_config": str(scenario_path),
            "repo_root": str(REPO_ROOT),
            "simulated_repo": str(fixture_root),
            "classification": classification,
            "recovered": recovered,
            "before": {
                "validate_exit_code": before_validate_code,
                "validate_ok": before_validate_report.get("ok"),
                "validate_stdout": before_validate_report,
                "validate_stderr": before_validate_stderr.strip(),
                "verify_exit_code": before_verify_code,
                "verify_ok": before_verify_report.get("ok"),
                "verify_stdout": before_verify_report,
                "verify_stderr": before_verify_stderr.strip(),
            },
            "repair": {
                "repair_exit_code": repair_code,
                "repair_ok": repair_code == 0,
                "stdout": repair_report,
                "stderr": repair_stderr.strip(),
            },
            "after": {
                "validate_exit_code": after_validate_code,
                "validate_ok": after_validate_report.get("ok"),
                "validate_stdout": after_validate_report,
                "validate_stderr": after_validate_stderr.strip(),
                "verify_exit_code": after_verify_code,
                "verify_ok": after_verify_report.get("ok"),
                "verify_stdout": after_verify_report,
                "verify_stderr": after_verify_stderr.strip(),
            },
        }


def main() -> int:
    args = parse_args()
    if args.scenario == "runtime-target-drift":
        report = run_runtime_target_drift()
    elif args.scenario == "review-bundle-contract-drift":
        report = run_review_bundle_contract_drift()
    elif args.scenario == "workspace-sensitive-boundary-drift":
        report = run_workspace_sensitive_boundary_drift()
    elif args.scenario == "workspace-sensitive-content-pattern-drift":
        report = run_workspace_sensitive_content_pattern_drift()
    else:
        raise SystemExit(f"unsupported scenario: {args.scenario}")
    output = json.dumps(report, indent=2) if args.format == "json" else render_markdown(report)
    write_output(output, args.output)

    if args.exit_zero:
        return 0
    return 0 if report["recovered"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
