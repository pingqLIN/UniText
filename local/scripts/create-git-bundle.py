#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> str:
    completed = subprocess.run(
        cmd,
        cwd=cwd,
        check=True,
        text=True,
        capture_output=True,
    )
    return completed.stdout.strip()


def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def parse_remotes(output: str) -> list[dict[str, str]]:
    remotes: list[dict[str, str]] = []
    for line in output.splitlines():
        parts = line.split()
        if len(parts) != 3:
            continue
        remotes.append({"name": parts[0], "url": parts[1], "direction": parts[2]})
    return remotes


def main() -> int:
    root = get_repo_root()
    parser = argparse.ArgumentParser(description="Create a portable git bundle backup.")
    parser.add_argument("--repo-root", default=str(root))
    parser.add_argument("--output-root", default="")
    parser.add_argument("--name", default="")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    repo = Path(args.repo_root).resolve()
    output_root = Path(args.output_root).resolve() if args.output_root else repo / "ops" / "git-bundles"
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder = args.name or f"bundle_{stamp}"
    bundle_dir = output_root / folder
    bundle_path = bundle_dir / "unitext.bundle"

    head = run(["git", "rev-parse", "HEAD"], repo)
    branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], repo)
    remotes = parse_remotes(run(["git", "remote", "-v"], repo))

    manifest: dict[str, object] = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(repo),
        "bundle_dir": str(bundle_dir),
        "bundle_path": str(bundle_path),
        "head": head,
        "branch": branch,
        "remote_count": len(remotes),
        "remotes": remotes,
        "command": ["git", "bundle", "create", str(bundle_path), "--all"],
    }

    if args.dry_run:
        print(json.dumps(manifest, indent=2))
        return 0

    bundle_dir.mkdir(parents=True, exist_ok=False)
    subprocess.run(
        ["git", "bundle", "create", str(bundle_path), "--all"],
        cwd=repo,
        check=True,
    )
    manifest["bundle_size_bytes"] = bundle_path.stat().st_size
    (bundle_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
