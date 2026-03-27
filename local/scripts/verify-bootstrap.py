#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def contains_path(text: str, value: str) -> bool:
    return value in text or value.replace("\\", "\\\\") in text


def has_claude_registry_permissions(text: str) -> bool:
    required = [
        r"Bash(find . -type f \\(-name *.py -o -name *.js -o -name *.ts -o -name *.sh -o -name *.ps1 \\))",
        "mcp__unitext-registry__registry_summary",
        "mcp__unitext-registry__list_registry_entries",
        "mcp__unitext-registry__read_registry_file",
    ]
    return all(item in text for item in required)


def main() -> int:
    repo = get_repo_root()
    source = repo / "registry" / "skills"
    server = repo / "registry" / "mcp" / "claude-project-mcp-seed" / "server.py"
    codex_config = Path.home() / ".codex" / "config.toml"
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

    project_mcp_report = {"path": str(project_mcp), "exists": project_mcp.exists(), "matches_expected": False}
    if project_mcp.exists():
        body = json.loads(project_mcp.read_text(encoding="utf-8"))
        server_config = body.get("mcpServers", {}).get("unitext-registry", {})
        project_mcp_report["matches_expected"] = (
            server_config.get("command") == sys.executable
            and server_config.get("args") == [str(server), "--root", str(repo)]
        )
    claude_text = read_text(claude_settings)

    report = {
        "repo_root": str(repo),
        "skills_source": str(source),
        "targets": target_report,
        "codex": {
            "path": str(codex_config),
            "exists": codex_config.exists(),
            "skills_path_matches": contains_path(codex_text, str(source)),
            "mcp_command_matches": contains_path(codex_text, str(sys.executable)),
            "mcp_args_match": contains_path(codex_text, str(server)),
        },
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
        and report["codex"]["mcp_command_matches"]
        and report["codex"]["mcp_args_match"]
        and report["claude_project"]["registry_permissions_match"]
        and report["project_mcp"]["matches_expected"]
    )
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
