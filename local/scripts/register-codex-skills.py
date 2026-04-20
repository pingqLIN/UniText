#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import stat
from datetime import datetime
from pathlib import Path


EXCLUDED_SKILL_NAMES = {".clean", "_backup"}


def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def get_home_dir() -> Path:
    return Path.home()


def write_json(path: Path, body: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(body, indent=2), encoding="utf-8")


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


def backup_path(path: Path, destination: Path) -> None:
    if not path.exists() and not path.is_symlink():
        return
    if path.is_symlink():
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


def copy_path(source: Path, destination: Path) -> None:
    if source.is_dir():
        shutil.copytree(source, destination, symlinks=True)
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def list_skill_names(root: Path) -> list[str]:
    return [
        item.name
        for item in sorted(root.iterdir())
        if item.is_dir() and item.name not in EXCLUDED_SKILL_NAMES
    ]


def ensure_materialized_runtime_bundle(runtime_skills: Path, codex_target: Path) -> str:
    if codex_target.is_symlink() and codex_target.resolve() == runtime_skills.resolve():
        remove_path(codex_target)
        shutil.copytree(runtime_skills, codex_target, symlinks=True)
        return "converted-symlink-to-bundle"

    codex_target.mkdir(parents=True, exist_ok=True)
    for item in sorted(runtime_skills.iterdir()):
        destination = codex_target / item.name
        if destination.exists() or destination.is_symlink():
            remove_path(destination)
        copy_path(item, destination)
    return "refreshed-existing-bundle"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Restore missing legacy Codex skills into the machine-local Codex bundle."
    )
    parser.add_argument(
        "--source",
        required=True,
        help="Source directory containing the legacy Codex skills tree to restore from.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Report the restore plan without mutating the target.")
    parser.add_argument("--write", action="store_true", help="Apply the restore plan.")
    args = parser.parse_args()

    if args.dry_run and args.write:
        raise SystemExit("choose either --dry-run or --write, not both")
    if not args.dry_run and not args.write:
        raise SystemExit("specify --dry-run or --write")

    repo = get_repo_root()
    home_dir = get_home_dir()
    runtime_skills = repo / "runtime" / "skills"
    source_root = Path(args.source).expanduser().resolve()
    codex_target = home_dir / ".codex" / "skills"

    if not source_root.exists():
        raise SystemExit(f"skills source not found: {source_root}")
    if not runtime_skills.exists():
        raise SystemExit(f"runtime skills not found: {runtime_skills}")

    source_skill_names = list_skill_names(source_root)
    current_skill_names = list_skill_names(codex_target)
    missing = [name for name in source_skill_names if name not in current_skill_names]
    existing_overlap = [name for name in source_skill_names if name in current_skill_names]

    summary: dict[str, object] = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(repo),
        "source_root": str(source_root),
        "runtime_skills": str(runtime_skills),
        "codex_target": str(codex_target),
        "source_skill_count": len(source_skill_names),
        "current_skill_count": len(current_skill_names),
        "missing_skill_count": len(missing),
        "missing_skills": missing,
        "existing_overlap": existing_overlap,
        "mode": "dry-run" if args.dry_run else "write",
    }

    if args.dry_run:
        print(json.dumps(summary, indent=2))
        return 0

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = repo / "ops" / "history" / f"register_codex_skills_{stamp}"
    run_dir.mkdir(parents=True, exist_ok=False)

    if codex_target.exists() or codex_target.is_symlink():
        backup_path(codex_target, run_dir / "codex" / "skills")

    summary["codex_target_prepare"] = ensure_materialized_runtime_bundle(runtime_skills, codex_target)

    restored: list[str] = []
    for skill_name in missing:
        source_skill = source_root / skill_name
        destination_skill = codex_target / skill_name
        if destination_skill.exists() or destination_skill.is_symlink():
            continue
        copy_path(source_skill, destination_skill)
        restored.append(skill_name)

    summary["restored_skills"] = restored
    summary["restored_skill_count"] = len(restored)
    summary["resulting_skill_count"] = len(list_skill_names(codex_target))

    write_json(run_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
