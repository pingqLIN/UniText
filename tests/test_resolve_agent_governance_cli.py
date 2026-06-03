import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "local" / "scripts" / "resolve-agent-governance.py"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--model",
            "gpt-5.4",
            "--environment",
            "codex-local-dev",
            "--instruction-profile",
            "mapping",
            *args,
        ],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


class ResolveAgentGovernanceCliTests(unittest.TestCase):
    def test_cli_reports_path_classification_for_analysis_path(self):
        result = run_cli("--analysis-path", "C:/external-project")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        resolution = json.loads(result.stdout)["resolution"]
        self.assertEqual(resolution["path_classification"]["scope_hint"], "external")
        self.assertIn("analysis_path", resolution)

    def test_cli_rejects_external_output_dir(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result = run_cli("--write-report", "--output-dir", temp_dir)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Refusing to write governance reports outside repository", result.stderr + result.stdout)


if __name__ == "__main__":
    unittest.main()
