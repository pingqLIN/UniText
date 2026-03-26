#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import tempfile
import sys
from datetime import datetime
from pathlib import Path


REPO_MARKERS = [
    Path("registry") / "skills",
    Path("registry") / "mcp" / "claude-project-mcp-seed" / "server.py",
    Path("README.md"),
    Path("INDEX.md"),
]
PLANNED_STEPS = [
    "prepare_run_directory",
    "protect_existing_inputs",
    "sync_skills_targets",
    "update_codex_config",
    "update_copilot_config",
    "update_project_mcp",
    "write_summary",
    "finalize",
]


def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def get_home_dir() -> Path:
    override = os.environ.get("UNITEXT_HOME") or os.environ.get("HOME")
    if override:
        return Path(override).expanduser().resolve()
    return Path.home()


def safe_name(path: Path) -> str:
    text = str(path).strip()
    if not text:
        return "target"
    normalized = re.sub(r"[\\/:]+", "_", text)
    return re.sub(r"[^A-Za-z0-9._-]", "_", normalized).strip("._") or "target"


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def atomic_write_json(path: Path, body: object) -> None:
    atomic_write_text(path, json.dumps(body, indent=2, ensure_ascii=False) + "\n")


def read_json_object(path: Path) -> dict[str, object] | None:
    if not path.exists():
        return None
    try:
        body = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(body, dict):
        raise RuntimeError(f"expected JSON object in {path}")
    return body


def backup_path(path: Path, destination: Path) -> None:
    if not path.exists() and not path.is_symlink():
        return
    if path.is_symlink():
        destination.parent.mkdir(parents=True, exist_ok=True)
        atomic_write_json(
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


def make_step_log() -> list[dict[str, str]]:
    return [{"name": step, "status": "pending"} for step in PLANNED_STEPS]


def set_step_status(report: dict[str, object], step_name: str, status: str, detail: str | None = None) -> None:
    steps = report["steps"]
    for step in steps:
        if step["name"] == step_name:
            step["status"] = status
            if detail is None:
                step.pop("detail", None)
            else:
                step["detail"] = detail
            break
    else:
        raise KeyError(step_name)
    report["current_step"] = step_name
    report["updated_at"] = datetime.now().isoformat(timespec="seconds")


def update_line(text: str, pattern: str, replacement: str) -> str:
    if re.search(pattern, text, flags=re.MULTILINE):
        return re.sub(pattern, lambda _: replacement, text, flags=re.MULTILINE)
    return text + ("\n" if text and not text.endswith("\n") else "") + replacement + "\n"


def upsert_top_level_toml_key(text: str, key: str, replacement: str) -> str:
    pattern = rf"(?m)^{re.escape(key)}\s*=.*$"
    stripped = re.sub(pattern, "", text)
    lines = [line for line in stripped.splitlines() if line.strip() != "" or line == ""]
    insert_at = len(lines)
    for index, line in enumerate(lines):
        if line.startswith("["):
            insert_at = index
            break

    lines.insert(insert_at, replacement)
    updated = "\n".join(lines)
    if text.endswith("\n") or not text:
        return updated + "\n"
    return updated


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


def render_copilot_mcp_config(existing: dict[str, object] | None, server: Path, root: Path) -> dict[str, object]:
    body = {} if existing is None else dict(existing)
    raw_servers = body.get("mcpServers")
    if raw_servers is None:
        mcp_servers: dict[str, object] = {}
    elif isinstance(raw_servers, dict):
        mcp_servers = dict(raw_servers)
    else:
        raise RuntimeError("expected mcpServers to be an object in Copilot MCP config")
    mcp_servers["unitext-registry"] = render_copilot_mcp_server(server, root)
    body["mcpServers"] = mcp_servers
    return body


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
    home_dir = get_home_dir()
    codex_config = home_dir / ".codex" / "config.toml"
    copilot_mcp_config = home_dir / ".copilot" / "mcp-config.json"
    skills_targets = [
        home_dir / ".claude" / "skills",
        home_dir / ".gemini" / "skills",
        home_dir / ".agents" / "skills",
        home_dir / ".copilot" / "skills",
    ]
    mode = "symlink" if args.mode == "auto" else args.mode
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    run_dir = repo / "ops" / "history" / f"bootstrap_{stamp}"
    state_path = run_dir / "state.json"
    summary_path = run_dir / "summary.json"
    summary: dict[str, object] = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "updated_at": datetime.now().isoformat(timespec="seconds"),
        "completed_at": None,
        "generation_state": "dry_run" if args.dry_run else "in_progress",
        "current_step": "validate_inputs",
        "repo_root": str(repo),
        "script_repo_root": str(root),
        "external_repo_root": repo != root,
        "dry_run": args.dry_run,
        "mode": args.mode,
        "run_dir": str(run_dir),
        "state_path": str(state_path),
        "summary_path": str(summary_path),
        "steps": make_step_log(),
        "skills": [],
        "codex": {},
        "copilot": {},
        "project_mcp": {},
    }

    if not source.exists():
        raise SystemExit(f"skills source not found: {source}")
    if not server.exists():
        raise SystemExit(f"mcp server not found: {server}")

    if args.dry_run:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        return 0

    try:
        run_dir.mkdir(parents=True, exist_ok=False)
        set_step_status(summary, "prepare_run_directory", "complete")
        atomic_write_json(state_path, summary)

        set_step_status(summary, "protect_existing_inputs", "in_progress")
        if not args.skip_skills:
            for target in skills_targets:
                if target.exists() or target.is_symlink():
                    backup_path(target, run_dir / "skills" / safe_name(target))
        if not args.skip_codex and codex_config.exists():
            backup_path(codex_config, run_dir / "codex" / "config.toml")
        if not args.skip_copilot and copilot_mcp_config.exists():
            backup_path(copilot_mcp_config, run_dir / "copilot" / "mcp-config.json")
        if not args.skip_project_mcp and project_mcp.exists():
            backup_path(project_mcp, run_dir / "project-mcp" / ".mcp.json")
        set_step_status(summary, "protect_existing_inputs", "complete")
        atomic_write_json(state_path, summary)

        if not args.skip_skills:
            set_step_status(summary, "sync_skills_targets", "in_progress")
            for target in skills_targets:
                summary["skills"].append(set_skills_target(source, target, mode, args.dry_run))
            set_step_status(summary, "sync_skills_targets", "complete")
        else:
            set_step_status(summary, "sync_skills_targets", "skipped", "requested by --skip-skills")
        atomic_write_json(state_path, summary)

        if not args.skip_codex:
            set_step_status(summary, "update_codex_config", "in_progress")
            original = codex_config.read_text(encoding="utf-8") if codex_config.exists() else ""
            updated = upsert_top_level_toml_key(original, "skills_path", f"skills_path = {toml_string(str(source))}")
            updated = upsert_codex_mcp_block(updated, server, repo)
            changed = updated != original
            summary["codex"] = {
                "path": str(codex_config),
                "changed": changed,
                "skills_path": str(source),
                "mcp_server": "unitext_registry",
            }
            if changed:
                codex_config.parent.mkdir(parents=True, exist_ok=True)
                atomic_write_text(codex_config, updated)
            set_step_status(summary, "update_codex_config", "complete")
        else:
            set_step_status(summary, "update_codex_config", "skipped", "requested by --skip-codex")
        atomic_write_json(state_path, summary)

        if not args.skip_copilot:
            set_step_status(summary, "update_copilot_config", "in_progress")
            existing = read_json_object(copilot_mcp_config)
            updated_body = render_copilot_mcp_config(existing, server, repo)
            existing_text = copilot_mcp_config.read_text(encoding="utf-8") if copilot_mcp_config.exists() else ""
            updated = json.dumps(updated_body, indent=2, ensure_ascii=False) + "\n"
            changed = updated != existing_text
            summary["copilot"] = {
                "path": str(copilot_mcp_config),
                "changed": changed,
                "skills_path": str(home_dir / ".copilot" / "skills"),
                "mcp_server": "unitext-registry",
            }
            if changed:
                copilot_mcp_config.parent.mkdir(parents=True, exist_ok=True)
                atomic_write_text(copilot_mcp_config, updated)
            set_step_status(summary, "update_copilot_config", "complete")
        else:
            set_step_status(summary, "update_copilot_config", "skipped", "requested by --skip-copilot")
        atomic_write_json(state_path, summary)

        if not args.skip_project_mcp:
            set_step_status(summary, "update_project_mcp", "in_progress")
            body = render_project_mcp(server, repo)
            existing = project_mcp.read_text(encoding="utf-8") if project_mcp.exists() else ""
            updated = json.dumps(body, indent=2)
            changed = updated != existing
            summary["project_mcp"] = {"path": str(project_mcp), "changed": changed}
            if changed:
                atomic_write_text(project_mcp, updated + "\n")
            set_step_status(summary, "update_project_mcp", "complete")
        else:
            set_step_status(summary, "update_project_mcp", "skipped", "requested by --skip-project-mcp")
        atomic_write_json(state_path, summary)

        set_step_status(summary, "write_summary", "complete")
        set_step_status(summary, "finalize", "complete")
        summary["generation_state"] = "complete"
        summary["completed_at"] = datetime.now().isoformat(timespec="seconds")
        atomic_write_json(summary_path, summary)
        atomic_write_json(state_path, summary)
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        return 0
    except Exception as exc:
        summary["generation_state"] = "failed"
        summary["completed_at"] = datetime.now().isoformat(timespec="seconds")
        summary["error"] = {"type": type(exc).__name__, "message": str(exc)}
        summary["updated_at"] = datetime.now().isoformat(timespec="seconds")
        if not args.dry_run:
            try:
                atomic_write_json(state_path, summary)
            except Exception:
                pass
        raise


if __name__ == "__main__":
    raise SystemExit(main())
