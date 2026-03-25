import json
import os
import subprocess
import sys
import shutil
import importlib.util
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def run_command(args, cwd=REPO_ROOT, env=None):
    return subprocess.run(
        args,
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


def get_powershell_executable():
    candidate = os.environ.get("POWERSHELL", "pwsh")
    if shutil.which(candidate):
        return candidate
    return None


def load_with_server_module():
    script = REPO_ROOT / "registry" / "skills" / "webapp-testing" / "scripts" / "with_server.py"
    spec = importlib.util.spec_from_file_location("with_server", script)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


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
        self.assertIn("Server spec must be JSON", result.stdout + result.stderr)

    def test_with_server_rejects_allow_shell_flag(self):
        script = REPO_ROOT / "registry" / "skills" / "webapp-testing" / "scripts" / "with_server.py"
        result = run_command(
            [
                sys.executable,
                str(script),
                "--allow-shell",
                "--server",
                '{"cmd":["python","-c","print(1)"]}',
                "--port",
                "5173",
                "--",
                sys.executable,
                "-c",
                "print('ok')",
            ]
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Legacy shell mode has been disabled", result.stdout + result.stderr)

    def test_with_server_json_spec_uses_non_shell_process_launch(self):
        module = load_with_server_module()
        server = module.parse_server_spec('{"cmd":["python","server.py"],"cwd":"frontend"}', allow_shell=False)
        self.assertEqual(server["cmd"], ["python", "server.py"])
        self.assertEqual(server["cwd"], "frontend")

    def test_with_server_parse_rejects_allow_shell_mode(self):
        module = load_with_server_module()
        with self.assertRaisesRegex(ValueError, "Legacy shell mode has been disabled"):
            module.parse_server_spec('{"cmd":["python","server.py"]}', allow_shell=True)

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

    def test_quick_validate_json_includes_canonical_metadata(self):
        script = REPO_ROOT / "registry" / "skills" / "skill-creator" / "scripts" / "quick_validate.py"
        with tempfile.TemporaryDirectory() as temp_dir:
            skill_dir = Path(temp_dir) / "demo-skill"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text(
                textwrap.dedent(
                    """\
                    ---
                    name: demo-skill
                    description: Demo description
                    ---

                    ## Usage
                    """
                ),
                encoding="utf-8",
            )
            result = run_command([sys.executable, str(script), str(skill_dir), "--json"])
        self.assertEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["id"], "demo-skill")
        self.assertEqual(payload["name"], "demo-skill")
        self.assertEqual(payload["description"], "Demo description")
        self.assertEqual(payload["canonical_location"], "/registry/skills/demo-skill")
        self.assertTrue(payload["has_skill_md"])
        self.assertTrue(payload["has_frontmatter"])

    def test_catalog_exclusions_marks_microsoft_foundry_as_non_catalog_surface(self):
        policy = REPO_ROOT / "registry" / "catalog-exclusions.json"
        payload = json.loads(policy.read_text(encoding="utf-8"))
        entry = payload["skills"]["microsoft-foundry"]
        self.assertIn(entry["status"], {"stray", "excluded"})
        self.assertIn("excluded", entry["reason"].lower())

    def test_export_template_rejects_escape_output_root(self):
        script = REPO_ROOT / "local" / "scripts" / "export-template-package.ps1"
        powershell = get_powershell_executable()
        if powershell is None:
            self.skipTest("PowerShell executable not available")
        result = run_command(
            [
                powershell,
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
        powershell = get_powershell_executable()
        if powershell is None:
            self.skipTest("PowerShell executable not available")
        result = run_command(
            [
                powershell,
                "-NoProfile",
                "-File",
                str(script),
                "-Ids",
                "..\\..",
                "-DryRun",
            ]
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Id", result.stdout + result.stderr)

    def test_rollback_rejects_invalid_skill_id(self):
        script = REPO_ROOT / "local" / "scripts" / "rollback-skills.ps1"
        powershell = get_powershell_executable()
        if powershell is None:
            self.skipTest("PowerShell executable not available")
        adopt_runs = sorted((REPO_ROOT / "ops" / "history").glob("adopt_*"))
        if not adopt_runs:
            self.skipTest("No adopt_* run available for rollback validation")
        result = run_command(
            [
                powershell,
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

    def test_bootstrap_dry_run_reports_dry_run_generation_state(self):
        script = REPO_ROOT / "local" / "scripts" / "bootstrap.py"
        result = run_command([sys.executable, str(script), "--dry-run"])
        self.assertEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["generation_state"], "dry_run")

    def test_scan_skills_uses_validator_and_controlled_parse_source(self):
        powershell = get_powershell_executable()
        if powershell is None:
            self.skipTest("PowerShell executable not available")

        script = REPO_ROOT / "local" / "scripts" / "scan-skills.ps1"
        with tempfile.TemporaryDirectory() as temp_dir:
            source_root = Path(temp_dir) / "skills"
            valid_skill = source_root / "good-skill"
            invalid_skill = source_root / "bad-skill"
            valid_skill.mkdir(parents=True)
            invalid_skill.mkdir(parents=True)

            (valid_skill / "SKILL.md").write_text(
                textwrap.dedent(
                    """\
                    ---
                    name: good-skill
                    description: A valid skill
                    ---

                    ## Usage
                    """
                ),
                encoding="utf-8",
            )
            (invalid_skill / "SKILL.md").write_text(
                textwrap.dedent(
                    """\
                    ---
                    name: bad-skill
                    name: evil
                    description: Broken on purpose
                    ---
                    """
                ),
                encoding="utf-8",
            )

            command = f"& '{script}' -Source '{source_root}' | ConvertTo-Json -Depth 6"
            result = run_command([powershell, "-NoProfile", "-Command", command], cwd=REPO_ROOT)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(len(payload), 2)
        good = next(item for item in payload if item["id"] == "good-skill")
        bad = next(item for item in payload if item["id"] == "bad-skill")
        self.assertTrue(good["validation_ok"])
        self.assertEqual(good["name"], "good-skill")
        self.assertFalse(bad["validation_ok"])
        self.assertIn("Duplicate key", bad["validation_message"])

    def test_generate_index_entries_uses_explicit_root(self):
        powershell = get_powershell_executable()
        if powershell is None:
            self.skipTest("PowerShell executable not available")

        script = REPO_ROOT / "local" / "scripts" / "generate-index-entries.ps1"
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir) / "repo"
            skill_root = repo_root / "registry" / "skills" / "demo-skill"
            skill_root.mkdir(parents=True)
            (skill_root / "SKILL.md").write_text(
                textwrap.dedent(
                    """\
                    ---
                    name: demo-skill
                    description: Demo skill
                    ---

                    ## Usage
                    """
                ),
                encoding="utf-8",
            )

            command = f"& '{script}' -Root '{repo_root}' -AsJson"
            result = run_command([powershell, "-NoProfile", "-Command", command], cwd=REPO_ROOT)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload[0]["id"], "demo-skill")
        self.assertEqual(payload[0]["canonical_location"], "/registry/skills/demo-skill")
        self.assertEqual(payload[0]["source_of_truth"], "/registry/skills/demo-skill/SKILL.md")


if __name__ == "__main__":
    unittest.main()
