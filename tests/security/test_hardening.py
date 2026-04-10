import json
import importlib.util
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
POWERSHELL = os.environ.get("POWERSHELL", "pwsh")


def run_command(args, cwd=REPO_ROOT):
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, encoding="utf-8", errors="replace")


class SecurityHardeningTests(unittest.TestCase):
    def test_with_server_rejects_shell_string_by_default(self):
        script = REPO_ROOT / "registry" / "skills" / "webapp-testing" / "scripts" / "with_server.py"
        result = run_command(
            [
                sys.executable,
                str(script),
                "--server",
                "npm run dev && echo MARKER",
                "--port",
                "5173",
                "--",
                sys.executable,
                "-c",
                "print('ok')",
            ]
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must be JSON unless --allow-shell", result.stdout + result.stderr)

    def test_quick_validate_rejects_duplicate_frontmatter_keys(self):
        if importlib.util.find_spec("yaml") is None:
            self.skipTest("PyYAML is not installed in the current test environment")
        script = REPO_ROOT / "registry" / "skills" / "skill-creator" / "scripts" / "quick_validate.py"
        with tempfile.TemporaryDirectory() as temp_dir:
            skill_dir = Path(temp_dir) / "demo-skill"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text(
                textwrap.dedent(
                    """\
                    ---
                    name: demo-skill
                    name: evil
                    description: ok
                    ---

                    ## Usage
                    """
                ),
                encoding="utf-8",
            )
            result = run_command([sys.executable, str(script), str(skill_dir), "--json"])
        self.assertEqual(result.returncode, 1)
        combined_output = result.stdout + result.stderr
        if result.stdout.strip():
            payload = json.loads(result.stdout)
            self.assertFalse(payload["ok"])
            self.assertIn("Duplicate key", payload["message"])
        else:
            self.assertIn("Duplicate key", combined_output)

    def test_export_template_rejects_escape_output_root(self):
        script = REPO_ROOT / "local" / "scripts" / "export-template-package.ps1"
        result = run_command(
            [
                POWERSHELL,
                "-NoProfile",
                "-File",
                str(script),
                "-OutputRoot",
                "..\\outside",
                "-DryRun",
            ]
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ops/template-package", result.stdout + result.stderr)

    def test_batch_adopt_rejects_invalid_skill_id(self):
        script = REPO_ROOT / "local" / "scripts" / "batch-adopt-skills.ps1"
        result = run_command(
            [
                POWERSHELL,
                "-NoProfile",
                "-File",
                str(script),
                "-Source",
                "registry\\skills",
                "-Ids",
                "..\\..",
                "-DryRun",
            ]
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Id", result.stdout + result.stderr)

    def test_rollback_rejects_invalid_skill_id(self):
        script = REPO_ROOT / "local" / "scripts" / "rollback-skills.ps1"
        adopt_runs = sorted((REPO_ROOT / "ops" / "history").glob("adopt_*"))
        if not adopt_runs:
            self.skipTest("No adopt_* run available for rollback validation")
        result = run_command(
            [
                POWERSHELL,
                "-NoProfile",
                "-File",
                str(script),
                "-RunDir",
                str(adopt_runs[0]),
                "-Id",
                "..\\..",
                "-DryRun",
            ]
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Id", result.stdout + result.stderr)

    def test_bootstrap_rejects_external_repo_root_by_default(self):
        script = REPO_ROOT / "local" / "scripts" / "bootstrap.py"
        result = run_command(
            [
                sys.executable,
                str(script),
                "--repo-root",
                "..",
                "--dry-run",
            ]
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("external --repo-root is disabled by default", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
