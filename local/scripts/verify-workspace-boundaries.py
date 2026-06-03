from __future__ import annotations

import argparse
import json
from pathlib import Path

from lib.workspace_boundaries import build_boundary_payload


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def build_payload(scope: list[str] | None = None) -> dict[str, object]:
    return build_boundary_payload(repo_root(), scope)


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify tracked shared surfaces for workspace-sensitive metadata.")
    parser.add_argument("--scope", action="append", default=[])
    parser.add_argument("--format", choices=("json",), default="json")
    args = parser.parse_args()

    payload = build_payload(args.scope)
    print(json.dumps(payload, indent=2))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
