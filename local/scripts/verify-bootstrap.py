#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path


UNITEXT_REGISTRY_STARTUP_TIMEOUT_SEC = 360


def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def contains_path(text: str, value: str) -> bool:
    return value in text or value.replace("\\", "\\\\") in text


def contains_timeout_value(text: str, seconds: int) -> bool:
    pattern = rf"(?m)^\s*startup_timeout_sec\s*=\s*{seconds}(?:\.0)?\s*$"
    return re.search(pattern, text) is not None


def has_claude_registry_permissions(text: str) -> bool:
    required = [
        r"Bash(find . -type f \\(-name *.py -o -name *.js -o -name *.ts -o -name *.sh -o -name *.ps1 \\))",
        "mcp__unitext-registry__registry_summary",
        "mcp__unitext-registry__list_registry_entries",
        "mcp__unitext-registry__read_registry_file",
    ]
    return all(item in text for item in required)


def read_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def project_mcp_matches_bootstrap(server_config: dict[str, object], server: Path, repo: Path) -> bool:
    return (
        server_config.get("command") == sys.executable
        and server_config.get("args") == [str(server), "--root", str(repo)]
    )


def project_mcp_matches_template_seed(server_config: dict[str, object]) -> bool:
    return (
        server_config.get("command") == "python"
        and server_config.get("args") == ["registry/mcp/claude-project-mcp-seed/server.py", "--root", "."]
    )


def main() -> int:
    repo = get_repo_root()
    source = repo / "registry" / "skills"
    server = repo / "registry" / "mcp" / "claude-project-mcp-seed" / "server.py"
    codex_config = Path.home() / ".codex" / "config.toml"
    copilot_mcp_config = Path.home() / ".copilot" / "mcp-config.json"
    claude_settings = repo / ".claude" / "settings.json"
    project_mcp = repo / ".mcp.json"
    targets = [
        Path.home() / ".claude" / "skills",
        Path.home() / ".gemini" / "skills",
        Path.home() / ".agents" / "skills",
    ]

    codex_text = read_text(codex_config)
    target_report = []
    for target in targets:
        exists = target.exists() or target.is_symlink()
        is_symlink = target.is_symlink()
        matches = False
        resolved = ""
        if exists:
            try:
                resolved = str(target.resolve())
                matches = Path(resolved) == source.resolve()
            except OSError:
                resolved = ""
        target_report.append(
            {
                "path": str(target),
                "exists": exists,
                "is_symlink": is_symlink,
                "resolved_target": resolved or None,
                "matches_expected": matches,
            }
        )

    project_mcp_report = {
        "path": str(project_mcp),
        "exists": project_mcp.exists(),
        "mode": "missing",
        "bootstrap_matches": False,
        "template_seed_matches": False,
        "matches_expected": False,
    }
    if project_mcp.exists():
        body = read_json(project_mcp)
        server_config = body.get("mcpServers", {}).get("unitext-registry", {})
        bootstrap_matches = project_mcp_matches_bootstrap(server_config, server, repo)
        template_seed_matches = project_mcp_matches_template_seed(server_config)
        mode = "mismatch"
        if bootstrap_matches:
            mode = "bootstrap"
        elif template_seed_matches:
            mode = "template-seed"
        project_mcp_report = {
            "path": str(project_mcp),
            "exists": True,
            "mode": mode,
            "bootstrap_matches": bootstrap_matches,
            "template_seed_matches": template_seed_matches,
            "matches_expected": bootstrap_matches or template_seed_matches,
        }
    claude_text = read_text(claude_settings)
    copilot_installed = shutil.which("copilot") is not None
    copilot_body = read_json(copilot_mcp_config)
    copilot_server = copilot_body.get("mcpServers", {}).get("unitext-registry", {}) if copilot_body else {}
    copilot_report = {
        "path": str(copilot_mcp_config),
        "cli_present": copilot_installed,
        "config_exists": copilot_mcp_config.exists(),
        "mcp_server_matches": (
            copilot_server.get("command") == sys.executable
            and copilot_server.get("args") == [str(server), "--root", str(repo)]
            and copilot_server.get("type") == "local"
        ),
    }

    report = {
        "repo_root": str(repo),
        "skills_source": str(source),
        "targets": target_report,
        "codex": {
            "path": str(codex_config),
            "exists": codex_config.exists(),
            "skills_path_matches": contains_path(codex_text, str(source)),
            "startup_timeout_matches": contains_timeout_value(codex_text, UNITEXT_REGISTRY_STARTUP_TIMEOUT_SEC),
            "mcp_command_matches": contains_path(codex_text, str(sys.executable)),
            "mcp_args_match": contains_path(codex_text, str(server)),
        },
        "copilot": copilot_report,
        "claude_project": {
            "path": str(claude_settings),
            "exists": claude_settings.exists(),
            "registry_permissions_match": has_claude_registry_permissions(claude_text),
        },
        "project_mcp": project_mcp_report,
    }
    report["ok"] = (
        all(item["matches_expected"] for item in target_report)
        and report["codex"]["skills_path_matches"]
        and report["codex"]["startup_timeout_matches"]
        and report["codex"]["mcp_command_matches"]
        and report["codex"]["mcp_args_match"]
        and (not report["copilot"]["cli_present"] or report["copilot"]["mcp_server_matches"])
        and report["claude_project"]["registry_permissions_match"]
        and report["project_mcp"]["matches_expected"]
    )
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
