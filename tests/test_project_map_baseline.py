import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROJECT_MAP_SCRIPT = REPO_ROOT / "web" / "project-map-ui" / "build-project-map.py"


class ProjectMapBaselineTests(unittest.TestCase):
    def test_project_map_core_assets_exist(self):
        expected = [
            PROJECT_MAP_SCRIPT,
            REPO_ROOT / "web" / "project-map-ui" / "project-map-runtime.js",
            REPO_ROOT / "web" / "project-map-ui" / "project-map-template.html",
            REPO_ROOT / "web" / "project-map-ui" / "project_map_contract.py",
            REPO_ROOT / "web" / "project-map-ui" / "CONTRACT.md",
            REPO_ROOT / "web" / "project-map-ui" / "README.md",
            REPO_ROOT / "web" / "project-map-ui" / "RELEASE_CHECKLIST.md",
        ]
        for path in expected:
            self.assertTrue(path.is_file(), f"Missing required project-map asset: {path}")

    def test_project_map_cli_exposes_contract_arguments(self):
        result = subprocess.run(
            [sys.executable, str(PROJECT_MAP_SCRIPT), "--help"],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("--repo-root", result.stdout)
        self.assertIn("--output-dir", result.stdout)
        self.assertIn("--governance-policy", result.stdout)

    def test_project_map_legacy_entrypoints_exist(self):
        expected = [
            REPO_ROOT / "local" / "scripts" / "build-project-map.py",
            REPO_ROOT / "local" / "scripts" / "project-map-runtime.js",
            REPO_ROOT / "local" / "scripts" / "project-map-template.html",
        ]
        for path in expected:
            self.assertTrue(path.is_file(), f"Missing project-map compatibility entrypoint: {path}")

    def test_governance_baseline_assets_exist(self):
        expected = [
            REPO_ROOT / "AGENT_GOVERNANCE_LAYERING.md",
            REPO_ROOT / "local" / "config" / "agent-governance-layers.json",
            REPO_ROOT / "local" / "scripts" / "resolve-agent-governance.py",
        ]
        for path in expected:
            self.assertTrue(path.is_file(), f"Missing required governance asset: {path}")


if __name__ == "__main__":
    unittest.main()
