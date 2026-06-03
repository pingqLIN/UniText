#!/usr/bin/env python3
from __future__ import annotations

import argparse
import getpass
import json
import os
import re
import shutil
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from lib.integration_surfaces import find_surface, load_integration_surfaces, surfaces_by_kind


CODEX_UNITEXT_REGISTRY_BLOCK_PATTERN = r"(?ms)^\[mcp_servers\.unitext_registry\]\n.*?(?=^\[|\Z)"


def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def get_home_dir() -> Path:
    try:
        return Path.home()
    except RuntimeError:
        candidates: list[Path] = []

        for variable in ("HOME", "USERPROFILE"):
            fallback = os.environ.get(variable)
            if fallback:
                candidates.append(Path(fallback))

        home_drive = os.environ.get("HOMEDRIVE")
        home_path = os.environ.get("HOMEPATH")
        if home_drive and home_path:
            candidates.append(Path(f"{home_drive}{home_path}"))

        if os.name == "nt":
            username = os.environ.get("USERNAME")
            if username:
                candidates.append(Path("C:/Users") / username)
            try:
                candidates.append(Path("C:/Users") / getpass.getuser())
            except Exception:
                pass

        unique_candidates: list[Path] = []
        seen: set[str] = set()
        for candidate in candidates:
            key = str(candidate)
            if key in seen:
                continue
            seen.add(key)
            unique_candidates.append(candidate)

        for candidate in unique_candidates:
            if candidate.exists():
                return candidate
        if unique_candidates:
            return unique_candidates[0]

        raise RuntimeError(
            "Could not determine home directory from Path.home(), HOME, USERPROFILE, HOMEDRIVE/HOMEPATH, or Windows username fallbacks."
        )


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def contains_path(text: str, value: str) -> bool:
    return value in text or value.replace("\\", "\\\\") in text


def contains_codex_mcp_block(text: str) -> bool:
    return re.search(CODEX_UNITEXT_REGISTRY_BLOCK_PATTERN, text) is not None


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify UniText bootstrap state for local CLI runtimes.")
    parser.add_argument("--home-dir")
    parser.add_argument("--skip-codex", action="store_true")
    parser.add_argument("--skip-copilot", action="store_true")
    parser.add_argument("--skip-project-mcp", action="store_true")
    return parser.parse_args()


def find_noncanonical_alias_entries(target: Path, runtime_skills: Path) -> list[dict[str, str]]:
    if not target.exists() or not target.is_dir():
        return []
    if not runtime_skills.exists() or not runtime_skills.is_dir():
        return []

    canonical_by_key = {item.name.casefold(): item.name for item in runtime_bundle_entries(runtime_skills)}
    aliases: list[dict[str, str]] = []
    for item in sorted(target.iterdir()):
        canonical_name = canonical_by_key.get(item.name.casefold())
        if canonical_name and item.name != canonical_name:
            aliases.append({"path": str(item), "canonical_name": canonical_name})
    return aliases


def runtime_bundle_entries(runtime_skills: Path) -> list[Path]:
    return [item for item in sorted(runtime_skills.iterdir()) if not item.name.startswith(".")]


def codex_target_contains_runtime_baseline(
    target: Path, runtime_skills: Path
) -> tuple[bool, str, list[str], str | None, list[dict[str, str]]]:
    exists = target.exists() or target.is_symlink()
    if not exists:
        return False, "missing", [], None, []

    if target.is_symlink():
        try:
            resolved = str(target.resolve())
            matches = Path(resolved) == runtime_skills.resolve()
        except OSError:
            resolved = None
            matches = False
        return matches, "symlink", [], resolved, []

    if not target.is_dir():
        return False, "file", [], str(target), []

    missing: list[str] = []
    for item in runtime_bundle_entries(runtime_skills):
        candidate = target / item.name
        if not candidate.exists() and not candidate.is_symlink():
            missing.append(item.name)
    duplicate_aliases = find_noncanonical_alias_entries(target, runtime_skills)
    return len(missing) == 0 and not duplicate_aliases, "bundle", missing, str(target), duplicate_aliases


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
    args = parse_args()
    repo = get_repo_root()
    home_dir = Path(args.home_dir).resolve() if args.home_dir else get_home_dir()
    runtime_skills = repo / "runtime" / "skills"
    registry_skills = repo / "registry" / "skills"
    server = repo / "registry" / "mcp" / "claude-project-mcp-seed" / "server.py"
    manifest_path, integration_surfaces = load_integration_surfaces(repo)
    codex_config_surface = find_surface(integration_surfaces, "codex-native-config")
    codex_skills_surface = find_surface(integration_surfaces, "codex-skills")
    copilot_surface = find_surface(integration_surfaces, "copilot-global-mcp")
    project_mcp_surface = find_surface(integration_surfaces, "project-mcp-seed")
    codex_config = codex_config_surface.resolve_path(repo_root=repo, home_dir=home_dir)
    codex_skills_target = codex_skills_surface.resolve_path(repo_root=repo, home_dir=home_dir)
    copilot_mcp_config = copilot_surface.resolve_path(repo_root=repo, home_dir=home_dir)
    claude_settings = repo / ".claude" / "settings.json"
    project_mcp = project_mcp_surface.resolve_path(repo_root=repo, home_dir=home_dir)
    targets = [
        {
            "surface_id": surface.surface_id,
            "path": surface.resolve_path(repo_root=repo, home_dir=home_dir),
        }
        for surface in surfaces_by_kind(integration_surfaces, "skills-target")
        if surface.surface_id != codex_skills_surface.surface_id
    ]

    codex_text = read_text(codex_config)
    (
        codex_target_contains_baseline,
        codex_target_mode,
        codex_target_missing,
        codex_target_resolved,
        codex_target_duplicate_aliases,
    ) = (
        codex_target_contains_runtime_baseline(codex_skills_target, runtime_skills)
    )
    target_report = []
    for target_info in targets:
        target = target_info["path"]
        exists = target.exists() or target.is_symlink()
        is_symlink = target.is_symlink()
        matches = False
        resolved = ""
        if exists:
            try:
                resolved = str(target.resolve())
                matches = Path(resolved) == runtime_skills.resolve()
            except OSError:
                resolved = ""
        target_report.append(
            {
                "surface_id": target_info["surface_id"],
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
        "integration_surfaces_manifest": str(manifest_path),
        "skills_source": str(runtime_skills),
        "targets": target_report,
        "codex": {
            "path": str(codex_config),
            "surface_id": codex_config_surface.surface_id,
            "exists": codex_config.exists(),
            "skills_path_matches": contains_path(codex_text, str(codex_skills_target)),
            "skills_path_points_to_registry": contains_path(codex_text, str(registry_skills)),
            "legacy_global_mcp_present": contains_codex_mcp_block(codex_text),
            "runtime_target_exists": codex_skills_target.exists() or codex_skills_target.is_symlink(),
            "runtime_target_mode": codex_target_mode,
            "runtime_target_resolved": codex_target_resolved,
            "runtime_target_contains_runtime_baseline": codex_target_contains_baseline,
            "runtime_target_missing_baseline": codex_target_missing,
            "runtime_target_duplicate_aliases": codex_target_duplicate_aliases,
        },
        "copilot": copilot_report,
        "claude_project": {
            "path": str(claude_settings),
            "exists": claude_settings.exists(),
            "registry_permissions_match": has_claude_registry_permissions(claude_text),
        },
        "project_mcp": project_mcp_report,
    }
    codex_ok = True if args.skip_codex else (
        report["codex"]["skills_path_matches"]
        and not report["codex"]["skills_path_points_to_registry"]
        and not report["codex"]["legacy_global_mcp_present"]
        and report["codex"]["runtime_target_exists"]
        and report["codex"]["runtime_target_contains_runtime_baseline"]
    )
    copilot_ok = True if args.skip_copilot else (
        not report["copilot"]["cli_present"] or report["copilot"]["mcp_server_matches"]
    )
    project_mcp_ok = True if args.skip_project_mcp else report["project_mcp"]["matches_expected"]
    report["ok"] = (
        all(item["matches_expected"] for item in target_report)
        and codex_ok
        and copilot_ok
        and report["claude_project"]["registry_permissions_match"]
        and project_mcp_ok
    )
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
