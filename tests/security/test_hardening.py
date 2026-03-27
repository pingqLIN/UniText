import json
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
def find_powershell_executable():
    candidates = []
    env_value = os.environ.get("POWERSHELL")
    if env_value:
        candidates.append(env_value)
    candidates.extend(["pwsh", "powershell.exe", "powershell"])

    for candidate in candidates:
        resolved = shutil.which(candidate)
        if resolved:
            return resolved

        candidate_path = Path(candidate)
        if candidate_path.is_absolute() and candidate_path.exists():
            return str(candidate_path)

    return None


POWERSHELL = find_powershell_executable()
HAS_POWERSHELL = POWERSHELL is not None
WSL_POWERSHELL = HAS_POWERSHELL and os.name != "nt" and POWERSHELL.lower().endswith(".exe")


def run_command(args, cwd=REPO_ROOT):
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, encoding="utf-8", errors="replace")


def translate_path_for_powershell(path):
    path = str(Path(path))
    if not WSL_POWERSHELL:
        return path

    translated = subprocess.run(
        ["wslpath", "-w", path],
        check=False,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    if translated.returncode != 0:
        return path

    return translated.stdout.strip() or path


def run_powershell_file(script_path, *script_args):
    args = [POWERSHELL, "-NoProfile", "-File", translate_path_for_powershell(script_path)]
    for arg in script_args:
        if isinstance(arg, Path):
            args.append(translate_path_for_powershell(arg))
        else:
            args.append(str(arg))
    return run_command(args)


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
        payload = json.loads(result.stdout)
        self.assertFalse(payload["ok"])
        self.assertIn("Duplicate key", payload["message"])

    @unittest.skipUnless(HAS_POWERSHELL, f"{POWERSHELL} is required for PowerShell security tests")
    def test_export_template_rejects_escape_output_root(self):
        script = REPO_ROOT / "local" / "scripts" / "export-template-package.ps1"
        result = run_powershell_file(script, "-OutputRoot", "../outside", "-DryRun")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ops/template-package", result.stdout + result.stderr)

    @unittest.skipUnless(HAS_POWERSHELL, f"{POWERSHELL} is required for PowerShell security tests")
    def test_batch_adopt_rejects_invalid_skill_id(self):
        script = REPO_ROOT / "local" / "scripts" / "batch-adopt-skills.ps1"
        result = run_powershell_file(script, "-Ids", "bad/skill", "-DryRun")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Id", result.stdout + result.stderr)

    @unittest.skipUnless(HAS_POWERSHELL, f"{POWERSHELL} is required for PowerShell security tests")
    def test_rollback_rejects_invalid_skill_id(self):
        script = REPO_ROOT / "local" / "scripts" / "rollback-skills.ps1"
        adopt_runs = sorted((REPO_ROOT / "ops" / "history").glob("adopt_*"))
        if not adopt_runs:
            self.skipTest("No adopt_* run available for rollback validation")
        result = run_powershell_file(script, "-RunDir", adopt_runs[0], "-Id", "bad/skill", "-DryRun")
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
