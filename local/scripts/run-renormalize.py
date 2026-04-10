#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))

from renormalize_core import SCOPE_MAP, apply_paths, get_repo_root, preview_paths, unique_targets  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scope", action="append", choices=sorted(SCOPE_MAP), dest="scopes")
    parser.add_argument("--sample-size", type=int, default=40)
    parser.add_argument("--max-files", type=int, default=200)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = get_repo_root()
    selected, targets = unique_targets(args.scopes or ["repo"])
    paths = preview_paths(repo, targets)

    if args.apply and len(paths) > args.max_files and not args.force:
        raise RuntimeError(
            f"Renormalize would touch {len(paths)} files, which exceeds MaxFiles={args.max_files}. "
            "Re-run with --force or narrow --scope."
        )

    staged_paths = apply_paths(repo, targets) if args.apply and paths else []
    summary = {
        "repo_root": str(repo),
        "scope": selected,
        "target_paths": targets,
        "line_ending_policy_present": (repo / ".gitattributes").exists(),
        "apply_mode": args.apply,
        "forced": args.force,
        "max_files_guard": args.max_files,
        "renormalize_candidate_count": len(paths),
        "sample_paths": paths[: args.sample_size],
        "staged_paths": staged_paths,
        "ok": True,
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
