import json
import os
import shutil
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
PREVIEW_PY = REPO_ROOT / "local" / "scripts" / "preview-renormalize.py"
PREVIEW_PS1 = REPO_ROOT / "local" / "scripts" / "preview-renormalize.ps1"
RUN_PY = REPO_ROOT / "local" / "scripts" / "run-renormalize.py"
RUN_PS1 = REPO_ROOT / "local" / "scripts" / "run-renormalize.ps1"


def get_powershell_executable():
    candidate = os.environ.get("POWERSHELL", "pwsh")
    if shutil.which(candidate):
        return candidate
    return None


def quote_powershell_string(value: Path | str) -> str:
    return "'" + str(value).replace("'", "''") + "'"


def run_command(args):
    return subprocess.run(
        args,
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


def run_json(args) -> dict:
    result = run_command(args)
    if result.returncode != 0:
        raise AssertionError(result.stdout + result.stderr)
    return json.loads(result.stdout)


def normalize_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


class RenormalizeParityTests(unittest.TestCase):
    def setUp(self):
        self.powershell = get_powershell_executable()
        if self.powershell is None:
            self.skipTest("PowerShell executable not available")

    def run_powershell_json(self, command: str) -> dict:
        result = run_command([self.powershell, "-NoProfile", "-Command", command])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def test_preview_wrapper_matches_python_core_summary(self):
        python_payload = run_json([sys.executable, str(PREVIEW_PY), "--sample-size", "8"])
        command = f"& {quote_powershell_string(PREVIEW_PS1)} -SampleSize 8 | ConvertTo-Json -Depth 8"
        powershell_payload = self.run_powershell_json(command)

        self.assertEqual(powershell_payload["ok"], python_payload["ok"])
        self.assertEqual(powershell_payload["line_ending_policy_present"], python_payload["line_ending_policy_present"])
        self.assertEqual(powershell_payload["renormalize_candidate_count"], python_payload["renormalize_candidate_count"])
        self.assertEqual(normalize_list(powershell_payload["sample_paths"]), python_payload["sample_paths"])
        self.assertEqual(normalize_list(powershell_payload["top_level_scopes"]), python_payload["top_level_scopes"])

    def test_run_wrapper_preview_matches_python_core_summary(self):
        python_payload = run_json(
            [
                sys.executable,
                str(RUN_PY),
                "--scope",
                "root",
                "--sample-size",
                "8",
                "--max-files",
                "999999",
            ]
        )
        command = (
            f"& {quote_powershell_string(RUN_PS1)} "
            "-Scope root -SampleSize 8 -MaxFiles 999999 | ConvertTo-Json -Depth 8"
        )
        powershell_payload = self.run_powershell_json(command)

        self.assertEqual(powershell_payload["ok"], python_payload["ok"])
        self.assertFalse(powershell_payload["apply_mode"])
        self.assertEqual(powershell_payload["apply_mode"], python_payload["apply_mode"])
        self.assertEqual(powershell_payload["renormalize_candidate_count"], python_payload["renormalize_candidate_count"])
        self.assertEqual(normalize_list(powershell_payload["scope"]), python_payload["scope"])
        self.assertEqual(normalize_list(powershell_payload["target_paths"]), python_payload["target_paths"])
        self.assertEqual(normalize_list(powershell_payload["sample_paths"]), python_payload["sample_paths"])
        self.assertEqual(normalize_list(powershell_payload["staged_paths"]), python_payload["staged_paths"])


if __name__ == "__main__":
    unittest.main()
