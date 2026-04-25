#!/usr/bin/env python3
from __future__ import annotations

import argparse
import stat
import getpass
import json
import os
import re
import shutil
import subprocess
import sys
import textwrap
from copy import deepcopy
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from lib.integration_surfaces import find_surface, load_integration_surfaces, surfaces_by_kind


REPO_MARKERS = [
    Path("registry") / "skills",
    Path("registry") / "mcp" / "claude-project-mcp-seed" / "server.py",
    Path("README.md"),
    Path("INDEX.md"),
]

UNITEXT_REGISTRY_STARTUP_TIMEOUT_SEC = 60.0


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


def safe_name(path: Path) -> str:
    parts = [part for part in (path.parent.name, path.name) if part]
    if parts:
        return "-".join(parts)
    return "target"


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
        try:
            path.chmod(stat.S_IWRITE)
        except OSError:
            pass
        path.unlink()
        return

    def onerror(func, failed_path, exc_info) -> None:
        failed = Path(failed_path)
        try:
            failed.chmod(stat.S_IWRITE)
        except OSError:
            pass
        func(failed_path)

    shutil.rmtree(path, onerror=onerror)


def copy_path(source: Path, destination: Path) -> None:
    if source.is_dir():
        shutil.copytree(source, destination, symlinks=True)
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def find_noncanonical_alias_entries(source: Path, target: Path) -> list[dict[str, str]]:
    if not source.exists() or not source.is_dir():
        return []
    if not target.exists() or not target.is_dir():
        return []

    canonical_by_key = {item.name.casefold(): item.name for item in sorted(source.iterdir())}
    aliases: list[dict[str, str]] = []
    for item in sorted(target.iterdir()):
        canonical_name = canonical_by_key.get(item.name.casefold())
        if canonical_name and item.name != canonical_name:
            aliases.append({"path": str(item), "canonical_name": canonical_name})
    return aliases


def sync_runtime_baseline(source: Path, target: Path, dry_run: bool) -> dict[str, object]:
    baseline_entries = [item.name for item in sorted(source.iterdir())]
    alias_entries = find_noncanonical_alias_entries(source, target)
    if dry_run:
        return {
            "target": str(target),
            "action": "sync-baseline",
            "mode": "bundle",
            "preserve_local_extras": True,
            "baseline_entries": baseline_entries,
            "pruned_alias_entries": alias_entries,
        }

    target.parent.mkdir(parents=True, exist_ok=True)
    target.mkdir(parents=True, exist_ok=True)
    for alias_entry in alias_entries:
        remove_path(Path(alias_entry["path"]))
    for item in sorted(source.iterdir()):
        destination = target / item.name
        if destination.exists() or destination.is_symlink():
            remove_path(destination)
        copy_path(item, destination)
    return {
        "target": str(target),
        "action": "synced",
        "mode": "bundle",
        "preserve_local_extras": True,
        "baseline_entries": baseline_entries,
        "pruned_alias_entries": alias_entries,
    }


def ensure_runtime_layer(repo: Path, dry_run: bool) -> dict[str, object]:
    builder = repo / "local" / "scripts" / "build-runtime-layer.py"
    if not builder.exists():
        raise SystemExit(f"runtime builder not found: {builder}")

    command = [sys.executable, str(builder)]
    if not dry_run:
        command.append("--write")

    completed = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
        cwd=repo,
    )
    details = json.loads(completed.stdout) if completed.stdout.strip() else {}
    if not dry_run:
        details["action"] = "rebuilt"
    else:
        details["action"] = "planned"
    details["command"] = command
    return details


def set_skills_target(
    source: Path,
    target: Path,
    mode: str,
    dry_run: bool,
    *,
    preserve_local_extras: bool = False,
) -> dict[str, object]:
    if target.is_symlink():
        resolved = target.readlink()
        if target.resolve() == source.resolve():
            return {"target": str(target), "action": "skip", "mode": "symlink", "reason": "already aligned"}
        if dry_run:
            return {"target": str(target), "action": "replace", "mode": "symlink", "reason": f"points to {resolved}"}
        remove_path(target)
    elif target.exists():
        if preserve_local_extras and target.is_dir():
            return sync_runtime_baseline(source, target, dry_run)
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


def render_codex_wrapper() -> str:
    return textwrap.dedent(
        """\
        #!/usr/bin/env python3
        from __future__ import annotations

        import argparse
        import importlib.util
        import sys
        import time
        import traceback
        from pathlib import Path


        def append_log(log_path: Path, message: str) -> None:
            log_path.parent.mkdir(parents=True, exist_ok=True)
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            with log_path.open("a", encoding="utf-8") as handle:
                handle.write(f"[{timestamp}] {message}\\n")


        def load_module(target: Path):
            spec = importlib.util.spec_from_file_location("unitext_registry_server", target)
            if spec is None or spec.loader is None:
                raise RuntimeError(f"unable to load module from {target}")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module


        def main() -> int:
            parser = argparse.ArgumentParser(add_help=False)
            parser.add_argument("--target", required=True)
            parser.add_argument("--log", required=True)
            args, passthrough = parser.parse_known_args()

            log_path = Path(args.log)
            target = Path(args.target)
            start = time.perf_counter()

            append_log(log_path, f"wrapper start argv={sys.argv!r}")
            append_log(log_path, f"cwd={Path.cwd()} target={target}")

            try:
                module = load_module(target)
                import_ms = round((time.perf_counter() - start) * 1000, 2)
                append_log(log_path, f"target imported in {import_ms} ms")

                sys.argv = [str(target), *passthrough]
                append_log(log_path, f"delegating with argv={sys.argv!r}")

                run_start = time.perf_counter()
                exit_code = int(module.main())
                run_ms = round((time.perf_counter() - run_start) * 1000, 2)
                append_log(log_path, f"target main exited code={exit_code} run_ms={run_ms}")
                return exit_code
            except SystemExit as exc:
                code = exc.code if isinstance(exc.code, int) else 0
                total_ms = round((time.perf_counter() - start) * 1000, 2)
                append_log(log_path, f"SystemExit code={code} total_ms={total_ms}")
                raise
            except Exception:
                total_ms = round((time.perf_counter() - start) * 1000, 2)
                append_log(log_path, f"exception after {total_ms} ms:\\n{traceback.format_exc()}")
                raise


        if __name__ == "__main__":
            raise SystemExit(main())
        """
    )


def render_codex_mcp_block(server: Path, root: Path, wrapper_path: Path, log_path: Path) -> str:
    args = ", ".join(
        toml_string(item)
        for item in [str(wrapper_path), "--target", str(server), "--log", str(log_path), "--root", str(root)]
    )
    return "\n".join(
        [
            "[mcp_servers.unitext_registry]",
            f"startup_timeout_sec = {UNITEXT_REGISTRY_STARTUP_TIMEOUT_SEC}",
            f"command = {toml_string(sys.executable)}",
            f"args = [{args}]",
            "",
        ]
    )


def upsert_codex_mcp_block(text: str, server: Path, root: Path, wrapper_path: Path, log_path: Path) -> str:
    block = render_codex_mcp_block(server, root, wrapper_path, log_path)
    pattern = r"(?ms)^\[mcp_servers\.unitext_registry\]\n.*?(?=^\[|\Z)"
    if re.search(pattern, text):
        return re.sub(pattern, lambda _: block, text)
    if not text.endswith("\n"):
        text += "\n"
    return text + "\n" + block


def render_project_mcp() -> dict[str, object]:
    return {
        "mcpServers": {
            "unitext-registry": {
                "transport": "stdio",
                "command": "python",
                "args": ["registry/mcp/claude-project-mcp-seed/server.py", "--root", "."],
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
    parser.add_argument("--home-dir")
    parser.add_argument("--history-root")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--mode", choices=["auto", "symlink", "mirror"], default="auto")
    parser.add_argument("--skip-runtime-build", action="store_true")
    parser.add_argument("--skip-skills", action="store_true")
    parser.add_argument("--skip-codex", action="store_true")
    parser.add_argument("--skip-copilot", action="store_true")
    parser.add_argument("--skip-project-mcp", action="store_true")
    args = parser.parse_args()

    if not args.dry_run and not args.force:
        raise SystemExit("non-dry-run bootstrap requires --force")

    repo = Path(args.repo_root).resolve()
    home_dir = Path(args.home_dir).resolve() if args.home_dir else get_home_dir()
    validate_repo_root(repo, root, args.allow_external_repo_root)
    runtime_root = repo / "runtime"
    runtime_skills = runtime_root / "skills"
    server = repo / "registry" / "mcp" / "claude-project-mcp-seed" / "server.py"
    manifest_path, integration_surfaces = load_integration_surfaces(repo)
    project_mcp_surface = find_surface(integration_surfaces, "project-mcp-seed")
    codex_config_surface = find_surface(integration_surfaces, "codex-native-config")
    codex_skills_surface = find_surface(integration_surfaces, "codex-skills")
    copilot_surface = find_surface(integration_surfaces, "copilot-global-mcp")
    project_mcp = project_mcp_surface.resolve_path(repo_root=repo, home_dir=home_dir)
    codex_config = codex_config_surface.resolve_path(repo_root=repo, home_dir=home_dir)
    codex_skills_target = codex_skills_surface.resolve_path(repo_root=repo, home_dir=home_dir)
    copilot_mcp_config = copilot_surface.resolve_path(repo_root=repo, home_dir=home_dir)
    skills_target_surfaces = [
        surface
        for surface in surfaces_by_kind(integration_surfaces, "skills-target")
        if surface.surface_id != codex_skills_surface.surface_id
    ]
    skills_targets = [
        {
            "surface_id": surface.surface_id,
            "path": surface.resolve_path(repo_root=repo, home_dir=home_dir),
        }
        for surface in skills_target_surfaces
    ]
    mode = "symlink" if args.mode == "auto" else args.mode
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    history_root = Path(args.history_root).resolve() if args.history_root else repo / "ops" / "history"
    run_dir = history_root / f"bootstrap_{stamp}"
    summary: dict[str, object] = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "generation_state": "dry_run" if args.dry_run else "apply",
        "repo_root": str(repo),
        "script_repo_root": str(root),
        "external_repo_root": repo != root,
        "home_dir": str(home_dir),
        "integration_surfaces_manifest": str(manifest_path),
        "dry_run": args.dry_run,
        "mode": args.mode,
        "runtime": {},
        "skills_source": str(runtime_skills),
        "skills": [],
        "codex": {},
        "copilot": {},
        "project_mcp": {},
    }

    if args.skip_runtime_build:
        summary["runtime"] = {
            "action": "skipped",
            "reason": "--skip-runtime-build",
            "target": str(runtime_root),
        }
    else:
        summary["runtime"] = ensure_runtime_layer(repo, args.dry_run)
    if not runtime_skills.exists():
        raise SystemExit(f"runtime skills source not found after build: {runtime_skills}")
    if not server.exists():
        raise SystemExit(f"mcp server not found: {server}")

    if not args.dry_run:
        run_dir.mkdir(parents=True, exist_ok=False)

    if not args.skip_skills:
        for target_info in skills_targets:
            target = target_info["path"]
            if not args.dry_run and (target.exists() or target.is_symlink()):
                backup_path(target, run_dir / "skills" / safe_name(target))
            result = set_skills_target(runtime_skills, target, mode, args.dry_run)
            result["surface_id"] = target_info["surface_id"]
            summary["skills"].append(result)

    if not args.skip_codex:
        wrapper_path = codex_config.parent / "diagnostics" / "unitext_registry_wrapper.py"
        log_path = codex_config.parent / "diagnostics" / "unitext_registry_startup.log"
        wrapper = render_codex_wrapper()
        if not args.dry_run and (codex_skills_target.exists() or codex_skills_target.is_symlink()):
            backup_path(codex_skills_target, run_dir / "codex" / "skills")
        codex_skills_result = set_skills_target(
            runtime_skills,
            codex_skills_target,
            mode,
            args.dry_run,
            preserve_local_extras=codex_skills_surface.preserve_local_extras,
        )
        original = codex_config.read_text(encoding="utf-8") if codex_config.exists() else ""
        wrapper_original = wrapper_path.read_text(encoding="utf-8") if wrapper_path.exists() else ""
        updated = update_line(original, r"^skills_path\s*=.*$", f"skills_path = {toml_string(str(codex_skills_target))}")
        updated = upsert_codex_mcp_block(updated, server, repo, wrapper_path, log_path)
        changed = updated != original or wrapper != wrapper_original
        summary["codex"] = {
            "path": str(codex_config),
            "surface_id": codex_config_surface.surface_id,
            "changed": changed,
            "skills_path": str(codex_skills_target),
            "skills_target": codex_skills_result,
            "mcp_server": "unitext_registry",
            "wrapper_path": str(wrapper_path),
            "log_path": str(log_path),
        }
        if changed and not args.dry_run:
            codex_config.parent.mkdir(parents=True, exist_ok=True)
            if codex_config.exists():
                backup_path(codex_config, run_dir / "codex" / "config.toml")
            wrapper_path.parent.mkdir(parents=True, exist_ok=True)
            if wrapper_path.exists():
                backup_path(wrapper_path, run_dir / "codex" / "unitext_registry_wrapper.py")
            wrapper_path.write_text(wrapper, encoding="utf-8")
            codex_config.write_text(updated, encoding="utf-8")

    if not args.skip_copilot:
        original = copilot_mcp_config.read_text(encoding="utf-8") if copilot_mcp_config.exists() else ""
        original_body = parse_json_object(original) if original else {}
        updated_body = upsert_copilot_mcp_config(original, server, repo)
        updated = json.dumps(updated_body, indent=2)
        changed = updated_body != original_body
        summary["copilot"] = {
            "path": str(copilot_mcp_config),
            "surface_id": copilot_surface.surface_id,
            "changed": changed,
            "mcp_server": "unitext-registry",
        }
        if changed and not args.dry_run:
            copilot_mcp_config.parent.mkdir(parents=True, exist_ok=True)
            if copilot_mcp_config.exists():
                backup_path(copilot_mcp_config, run_dir / "copilot" / "mcp-config.json")
            copilot_mcp_config.write_text(updated + "\n", encoding="utf-8")

    if not args.skip_project_mcp:
        body = render_project_mcp()
        existing = project_mcp.read_text(encoding="utf-8") if project_mcp.exists() else ""
        existing_body = parse_json_object(existing) if existing else {}
        updated = json.dumps(body, indent=2)
        changed = body != existing_body
        summary["project_mcp"] = {
            "path": str(project_mcp),
            "surface_id": project_mcp_surface.surface_id,
            "changed": changed,
            "mode": "template-seed",
        }
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
