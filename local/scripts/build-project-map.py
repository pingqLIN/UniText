#!/usr/bin/env python3
from __future__ import annotations

import runpy
from pathlib import Path


PROJECT_ENTRYPOINT = Path(__file__).resolve().parents[2] / "web" / "project-map-ui" / "build-project-map.py"


if __name__ == "__main__":
    runpy.run_path(str(PROJECT_ENTRYPOINT), run_name="__main__")
