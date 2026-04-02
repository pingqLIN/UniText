#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from copy import deepcopy
from datetime import datetime
from pathlib import Path


REPO_MARKERS = [
    Path("registry") / "skills",
    Path("registry") / "mcp" / "claude-project-mcp-seed" / "server.py",
    Path("README.md"),
    Path("INDEX.md"),
]


def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def safe_name(path: Path) -> str:
    return path.name or path.parent.name or "target"


def write_json(path: Path, body: object) -> None:
    path.write_text(json.dumps(body, indent=2), encoding="utf-8")


def backup_path(path: Path, destination: Path) -> None:
    if not path.exists() and not path.is_symlink():
        return
    if path.is_symlink():
        destination.parent.mkdir(parents=True, exist_ok=True)
        write_json(
            destination.with_suffix(destination.suffix + ".symlink.json"),
            {"path": str(path), "target": str(path.readlink())},
        )
        return
    if path.is_dir():
        shutil.copytree(path, destination, symlinks=True)
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, destination)


def remove_path(path: Path) -> None:
    if not path.exists() and not path.is_symlink():
        return
    if path.is_symlink() or path.is_file():
        path.unlink()
        return
    shutil.rmtree(path)


def set_skills_target(source: Path, target: Path, mode: str, dry_run: bool) -> dict[str, object]:
    if target.is_symlink():
        resolved = target.readlink()
        if target.resolve() == source.resolve():
            return {"target": str(target), "action": "skip", "mode": "symlink", "reason": "already aligned"}
        if dry_run:
            return {"target": str(target), "action": "replace", "mode": "symlink", "reason": f"points to {resolved}"}
        remove_path(target)
    elif target.exists():
        if dry_run:
            return {"target": str(target), "action": "replace", "mode": "mirror", "reason": "existing directory or file"}
        remove_path(target)

    if dry_run:
        return {"target": str(target), "action": "create", "mode": mode}

    target.parent.mkdir(parents=True, exist_ok=True)
    if mode != "mirror":
        try:
            target.symlink_to(source, target_is_directory=True)
            return {"target": str(target), "action": "created", "mode": "symlink"}
        except OSError as exc:
            if mode == "symlink":
                raise RuntimeError(f"symlink creation failed for {target}: {exc}") from exc
    shutil.copytree(source, target)
    return {"target": str(target), "action": "created", "mode": "mirror"}


def update_line(text: str, pattern: str, replacement: str) -> str:
    if re.search(pattern, text, flags=re.MULTILINE):
        return re.sub(pattern, lambda _: replacement, text, flags=re.MULTILINE)
    return text + ("\n" if text and not text.endswith("\n") else "") + replacement + "\n"


def toml_string(value: str) -> str:
    if "'" not in value:
        return f"'{value}'"
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def render_codex_mcp_block(server: Path, root: Path) -> str:
    args = ", ".join(toml_string(item) for item in [str(server), "--root", str(root)])
    return "\n".join(
        [
            "[mcp_servers.unitext_registry]",
            "startup_timeout_sec = 60",
            f"command = {toml_string(sys.executable)}",
            f"args = [{args}]",
            "",
        ]
    )


def upsert_codex_mcp_block(text: str, server: Path, root: Path) -> str:
    block = render_codex_mcp_block(server, root)
    pattern = r"(?ms)^\[mcp_servers\.unitext_registry\]\n.*?(?=^\[|\Z)"
    if re.search(pattern, text):
        return re.sub(pattern, lambda _: block, text)
    if not text.endswith("\n"):
        text += "\n"
    return text + "\n" + block


def render_project_mcp(server: Path, root: Path) -> dict[str, object]:
    return {
        "mcpServers": {
            "unitext-registry": {
                "transport": "stdio",
                "command": sys.executable,
                "args": [str(server), "--root", str(root)],
            }
        }
    }


def render_copilot_mcp_server(server: Path, root: Path) -> dict[str, object]:
    return {
        "type": "local",
        "command": sys.executable,
        "args": [str(server), "--root", str(root)],
        "env": {},
        "tools": ["*"],
    }


def parse_json_object(text: str) -> dict[str, object]:
    if not text.strip():
        return {}
    body = json.loads(text)
    if not isinstance(body, dict):
        raise RuntimeError("JSON content must contain a top-level object.")
    return body


def upsert_copilot_mcp_config(text: str, server: Path, root: Path) -> dict[str, object]:
    body = parse_json_object(text)
    servers = body.get("mcpServers", {})
    if not isinstance(servers, dict):
        raise RuntimeError("~/.copilot/mcp-config.json must contain an object at mcpServers.")
    updated = deepcopy(body)
    updated.setdefault("mcpServers", {})
    updated["mcpServers"]["unitext-registry"] = render_copilot_mcp_server(server, root)
    return updated


def validate_repo_surface(repo: Path) -> None:
    missing = [str(marker) for marker in REPO_MARKERS if not (repo / marker).exists()]
    if missing:
        raise SystemExit(f"repo root is missing required markers: {', '.join(missing)}")


def validate_repo_root(candidate: Path, script_root: Path, allow_external: bool) -> None:
    if candidate == script_root:
        validate_repo_surface(candidate)
        return
    if not allow_external:
        raise SystemExit(
            "external --repo-root is disabled by default; rerun with --allow-external-repo-root if intentional"
        )
    validate_repo_surface(candidate)


def main() -> int:
    root = get_repo_root()
    parser = argparse.ArgumentParser(description="Bootstrap UniText delivery for local CLI runtimes.")
    parser.add_argument("--repo-root", default=str(root))
    parser.add_argument("--allow-external-repo-root", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--mode", choices=["auto", "symlink", "mirror"], default="auto")
    parser.add_argument("--skip-skills", action="store_true")
    parser.add_argument("--skip-codex", action="store_true")
    parser.add_argument("--skip-copilot", action="store_true")
    parser.add_argument("--skip-project-mcp", action="store_true")
    args = parser.parse_args()

    if not args.dry_run and not args.force:
        raise SystemExit("non-dry-run bootstrap requires --force")

    repo = Path(args.repo_root).resolve()
    validate_repo_root(repo, root, args.allow_external_repo_root)
    source = repo / "registry" / "skills"
    server = repo / "registry" / "mcp" / "claude-project-mcp-seed" / "server.py"
    project_mcp = repo / ".mcp.json"
    codex_config = Path.home() / ".codex" / "config.toml"
    copilot_mcp_config = Path.home() / ".copilot" / "mcp-config.json"
    skills_targets = [
        Path.home() / ".claude" / "skills",
        Path.home() / ".gemini" / "skills",
        Path.home() / ".agents" / "skills",
    ]
    mode = "symlink" if args.mode == "auto" else args.mode
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = repo / "ops" / "history" / f"bootstrap_{stamp}"
    summary: dict[str, object] = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(repo),
        "script_repo_root": str(root),
        "external_repo_root": repo != root,
        "dry_run": args.dry_run,
        "mode": args.mode,
        "skills": [],
        "codex": {},
        "copilot": {},
        "project_mcp": {},
    }

    if not source.exists():
        raise SystemExit(f"skills source not found: {source}")
    if not server.exists():
        raise SystemExit(f"mcp server not found: {server}")

    if not args.dry_run:
        run_dir.mkdir(parents=True, exist_ok=False)

    if not args.skip_skills:
        for target in skills_targets:
            if not args.dry_run and (target.exists() or target.is_symlink()):
                backup_path(target, run_dir / "skills" / safe_name(target))
            summary["skills"].append(set_skills_target(source, target, mode, args.dry_run))

    if not args.skip_codex:
        original = codex_config.read_text(encoding="utf-8") if codex_config.exists() else ""
        updated = update_line(original, r"^skills_path\s*=.*$", f"skills_path = {toml_string(str(source))}")
        updated = upsert_codex_mcp_block(updated, server, repo)
        changed = updated != original
        summary["codex"] = {
            "path": str(codex_config),
            "changed": changed,
            "skills_path": str(source),
            "mcp_server": "unitext_registry",
        }
        if changed and not args.dry_run:
            codex_config.parent.mkdir(parents=True, exist_ok=True)
            if codex_config.exists():
                backup_path(codex_config, run_dir / "codex" / "config.toml")
            codex_config.write_text(updated, encoding="utf-8")

    if not args.skip_copilot:
        original = copilot_mcp_config.read_text(encoding="utf-8") if copilot_mcp_config.exists() else ""
        original_body = parse_json_object(original) if original else {}
        updated_body = upsert_copilot_mcp_config(original, server, repo)
        updated = json.dumps(updated_body, indent=2)
        changed = updated_body != original_body
        summary["copilot"] = {
            "path": str(copilot_mcp_config),
            "changed": changed,
            "mcp_server": "unitext-registry",
        }
        if changed and not args.dry_run:
            copilot_mcp_config.parent.mkdir(parents=True, exist_ok=True)
            if copilot_mcp_config.exists():
                backup_path(copilot_mcp_config, run_dir / "copilot" / "mcp-config.json")
            copilot_mcp_config.write_text(updated + "\n", encoding="utf-8")

    if not args.skip_project_mcp:
        body = render_project_mcp(server, repo)
        existing = project_mcp.read_text(encoding="utf-8") if project_mcp.exists() else ""
        updated = json.dumps(body, indent=2)
        changed = updated != existing
        summary["project_mcp"] = {"path": str(project_mcp), "changed": changed}
        if changed and not args.dry_run:
            if project_mcp.exists():
                backup_path(project_mcp, run_dir / "project-mcp" / ".mcp.json")
            project_mcp.write_text(updated + "\n", encoding="utf-8")

    if not args.dry_run:
        write_json(run_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
