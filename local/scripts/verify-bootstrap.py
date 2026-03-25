#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
import tomllib
from pathlib import Path


def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict[str, object] | None:
    if not path.exists():
        return None
    try:
        body = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return body if isinstance(body, dict) else None


def read_toml(path: Path) -> dict[str, object] | None:
    if not path.exists():
        return None
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError):
        return None


def safe_contains_all(items: list[object], expected: list[str]) -> bool:
    return all(item in items for item in expected)


def snapshot_tree(root: Path) -> dict[str, dict[str, str]]:
    snapshot: dict[str, dict[str, str]] = {}
    for path in sorted(root.rglob("*")):
        rel = str(path.relative_to(root))
        if path.is_symlink():
            snapshot[rel] = {"kind": "symlink", "target": str(path.readlink())}
        elif path.is_dir():
            snapshot[rel] = {"kind": "dir"}
        elif path.is_file():
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            snapshot[rel] = {"kind": "file", "sha256": digest}
    return snapshot


def target_matches_source(target: Path, source: Path) -> tuple[bool, str | None]:
    if not target.exists() and not target.is_symlink():
        return False, None
    try:
        if target.is_symlink():
            return target.resolve() == source.resolve(), "symlink"
        if target.is_dir():
            return snapshot_tree(target) == snapshot_tree(source), "mirror"
        return False, "file"
    except OSError:
        return False, None


def latest_bootstrap_run(repo: Path) -> Path | None:
    history = repo / "ops" / "history"
    candidates = [path for path in history.glob("bootstrap_*") if path.is_dir()]
    if not candidates:
        return None
    return max(candidates, key=lambda path: path.name)


def report_bootstrap_run(run_dir: Path) -> dict[str, object]:
    state_path = run_dir / "state.json"
    summary_path = run_dir / "summary.json"
    state = read_json(state_path)
    summary = read_json(summary_path)
    ok = False
    reason = None
    if state is None or summary is None:
        reason = "missing state or summary"
    elif state != summary:
        reason = "state and summary diverge"
    elif state.get("generation_state") != "complete":
        reason = f"generation_state={state.get('generation_state')!r}"
    elif summary.get("completed_at") is None:
        reason = "missing completed_at"
    elif state.get("current_step") != "finalize":
        reason = f"current_step={state.get('current_step')!r}"
    else:
        step_statuses = [step.get("status") for step in state.get("steps", []) if isinstance(step, dict)]
        ok = bool(step_statuses) and all(status in {"complete", "skipped"} for status in step_statuses)
        if not ok:
            reason = "unfinished step status detected"
    return {
        "checked": True,
        "path": str(run_dir),
        "state_path": str(state_path),
        "summary_path": str(summary_path),
        "exists": run_dir.exists(),
        "state_exists": state_path.exists(),
        "summary_exists": summary_path.exists(),
        "generation_state": None if state is None else state.get("generation_state"),
        "current_step": None if state is None else state.get("current_step"),
        "ok": ok,
        "reason": reason,
    }


def main() -> int:
    repo = get_repo_root()
    source = repo / "registry" / "skills"
    server = repo / "registry" / "mcp" / "claude-project-mcp-seed" / "server.py"
    codex_config = Path.home() / ".codex" / "config.toml"
    copilot_config = Path.home() / ".copilot" / "mcp-config.json"
    claude_settings = repo / ".claude" / "settings.json"
    project_mcp = repo / ".mcp.json"
    targets = [
        Path.home() / ".claude" / "skills",
        Path.home() / ".gemini" / "skills",
        Path.home() / ".agents" / "skills",
        Path.home() / ".copilot" / "skills",
    ]

    target_report = []
    target_ok = True
    for target in targets:
        matches, mode = target_matches_source(target, source)
        target_ok = target_ok and matches
        target_report.append(
            {
                "path": str(target),
                "exists": target.exists() or target.is_symlink(),
                "is_symlink": target.is_symlink(),
                "mode": mode,
                "matches_expected": matches,
            }
        )

    codex_body = read_toml(codex_config)
    codex_report = {
        "path": str(codex_config),
        "exists": codex_config.exists(),
        "parsed": codex_body is not None,
        "skills_path_matches": False,
        "mcp_command_matches": False,
        "mcp_args_match": False,
    }
    if codex_body is not None:
        codex_report["skills_path_matches"] = codex_body.get("skills_path") == str(source)
        mcp_servers = codex_body.get("mcp_servers")
        if isinstance(mcp_servers, dict):
            unitext_registry = mcp_servers.get("unitext_registry")
            if isinstance(unitext_registry, dict):
                codex_report["mcp_command_matches"] = unitext_registry.get("command") == sys.executable
                codex_report["mcp_args_match"] = unitext_registry.get("args") == [str(server), "--root", str(repo)]

    copilot_body = read_json(copilot_config)
    copilot_report = {
        "path": str(copilot_config),
        "exists": copilot_config.exists(),
        "parsed": copilot_body is not None,
        "server_present": False,
        "type_matches": False,
        "command_matches": False,
        "args_match": False,
        "tools_match": False,
    }
    if copilot_body is not None:
        mcp_servers = copilot_body.get("mcpServers")
        if isinstance(mcp_servers, dict):
            unitext_registry = mcp_servers.get("unitext-registry")
            if isinstance(unitext_registry, dict):
                copilot_report["server_present"] = True
                copilot_report["type_matches"] = unitext_registry.get("type") == "local"
                copilot_report["command_matches"] = unitext_registry.get("command") == sys.executable
                copilot_report["args_match"] = unitext_registry.get("args") == [str(server), "--root", str(repo)]
                copilot_report["tools_match"] = unitext_registry.get("tools") == ["*"]

    claude_body = read_json(claude_settings)
    claude_report = {
        "path": str(claude_settings),
        "exists": claude_settings.exists(),
        "parsed": claude_body is not None,
        "registry_permissions_match": False,
    }
    if claude_body is not None:
        permissions = claude_body.get("permissions")
        if isinstance(permissions, dict):
            allow = permissions.get("allow")
            if isinstance(allow, list):
                claude_report["registry_permissions_match"] = safe_contains_all(
                    allow,
                    [
                        "Bash(find . -type f -name *.json -o -name *.toml -o -name *.yaml -o -name *.yml)",
                        "Bash(find . -type f \\(-name *.py -o -name *.js -o -name *.ts -o -name *.sh -o -name *.ps1 \\))",
                        "mcp__unitext-registry__registry_summary",
                        "mcp__unitext-registry__list_registry_entries",
                        "mcp__unitext-registry__read_registry_file",
                    ],
                )

    project_mcp_body = read_json(project_mcp)
    project_mcp_report = {
        "path": str(project_mcp),
        "exists": project_mcp.exists(),
        "parsed": project_mcp_body is not None,
        "matches_expected": False,
    }
    if project_mcp_body is not None:
        mcp_servers = project_mcp_body.get("mcpServers")
        if isinstance(mcp_servers, dict):
            server_config = mcp_servers.get("unitext-registry")
            if isinstance(server_config, dict):
                project_mcp_report["matches_expected"] = (
                    server_config.get("command") == sys.executable
                    and server_config.get("args") == [str(server), "--root", str(repo)]
                )

    bootstrap_run = {"checked": False, "exists": False, "ok": True}
    latest_run = latest_bootstrap_run(repo)
    if latest_run is not None:
        bootstrap_run = report_bootstrap_run(latest_run)

    report = {
        "repo_root": str(repo),
        "skills_source": str(source),
        "targets": target_report,
        "codex": codex_report,
        "copilot": copilot_report,
        "claude_project": claude_report,
        "project_mcp": project_mcp_report,
        "bootstrap_run": bootstrap_run,
    }
    report["ok"] = (
        target_ok
        and codex_report["skills_path_matches"]
        and codex_report["mcp_command_matches"]
        and codex_report["mcp_args_match"]
        and copilot_report["server_present"]
        and copilot_report["type_matches"]
        and copilot_report["command_matches"]
        and copilot_report["args_match"]
        and copilot_report["tools_match"]
        and claude_report["registry_permissions_match"]
        and project_mcp_report["matches_expected"]
        and bootstrap_run["ok"]
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
