import ast
import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "local" / "scripts" / "run-self-repair-simulation.py"


class SelfRepairSimulationTests(unittest.TestCase):
    def test_runner_does_not_hardcode_python_executable(self):
        tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
        command_literals = [
            node.value
            for node in ast.walk(tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
        ]
        self.assertNotIn("python", command_literals)

    def run_scenario(self, scenario: str) -> dict[str, object]:
        if shutil.which("powershell") is None:
            self.skipTest("Windows PowerShell executable not available")

        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--scenario", scenario, "--format", "json"],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["recovered"], payload)
        self.assertEqual(payload["classification"], "recovered")
        return payload

    def test_runtime_target_drift_recovers(self):
        payload = self.run_scenario("runtime-target-drift")
        self.assertFalse(payload["before"]["verify_ok"])
        self.assertTrue(payload["after"]["verify_ok"])

    def test_review_bundle_contract_drift_recovers(self):
        payload = self.run_scenario("review-bundle-contract-drift")
        self.assertFalse(payload["before"]["export_ok"])
        self.assertTrue(payload["after"]["export_ok"])

    def test_workspace_sensitive_boundary_drift_recovers(self):
        payload = self.run_scenario("workspace-sensitive-boundary-drift")
        self.assertFalse(payload["before"]["validate_ok"])
        self.assertTrue(payload["after"]["validate_ok"])

    def test_workspace_sensitive_content_pattern_drift_recovers(self):
        payload = self.run_scenario("workspace-sensitive-content-pattern-drift")
        self.assertFalse(payload["before"]["validate_ok"])
        self.assertFalse(payload["before"]["verify_ok"])
        self.assertTrue(payload["after"]["validate_ok"])
        self.assertTrue(payload["after"]["verify_ok"])


if __name__ == "__main__":
    unittest.main()
