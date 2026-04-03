#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))

from renormalize_core import get_repo_root, preview_paths, top_level_groups  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample-size", type=int, default=40)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = get_repo_root()
    paths = preview_paths(repo, ["."])
    summary = {
        "repo_root": str(repo),
        "line_ending_policy_present": (repo / ".gitattributes").exists(),
        "renormalize_candidate_count": len(paths),
        "top_level_scopes": top_level_groups(paths),
        "sample_paths": paths[: args.sample_size],
        "ok": True,
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
