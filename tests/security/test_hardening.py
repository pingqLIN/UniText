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


def load_bootstrap_module():
    script = REPO_ROOT / "local" / "scripts" / "bootstrap.py"
    spec = importlib.util.spec_from_file_location("bootstrap", script)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def normalize_manifest_path(value: str) -> str:
    return "/".join(part for part in value.replace("\\", "/").split("/") if part)


def quote_powershell_string(value: Path | str) -> str:
    return "'" + str(value).replace("'", "''") + "'"


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

    def test_bootstrap_home_dir_falls_back_to_windows_username(self):
        module = load_bootstrap_module()
        original_home = module.Path.home
        original_environ = os.environ.copy()
        try:
            module.Path.home = classmethod(lambda cls: (_ for _ in ()).throw(RuntimeError("no home")))
            for key in ("HOME", "USERPROFILE", "HOMEDRIVE", "HOMEPATH"):
                os.environ.pop(key, None)
            os.environ["USERNAME"] = "miles"
            home_dir = module.get_home_dir()
        finally:
            module.Path.home = original_home
            os.environ.clear()
            os.environ.update(original_environ)

        self.assertEqual(home_dir, Path("C:/Users/miles"))

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

    def test_export_template_dry_run_lists_required_starter_members(self):
        script = REPO_ROOT / "local" / "scripts" / "export-template-package.ps1"
        powershell = get_powershell_executable()
        if powershell is None:
            self.skipTest("PowerShell executable not available")
        result = run_command(
            [
                powershell,
                "-NoProfile",
                "-Command",
                f"& '{script}' -DryRun | ConvertTo-Json -Depth 6",
            ]
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        sources = {normalize_manifest_path(item["source"]) for item in payload["items"]}
        targets = {normalize_manifest_path(item["target"]) for item in payload["items"]}

        self.assertIn("README.md", sources)
        self.assertIn("registry/mcp/claude-project-mcp-seed", sources)
        self.assertIn("local/scripts/bootstrap.py", sources)
        self.assertIn("local/scripts/build-runtime-layer.py", sources)
        self.assertIn("local/scripts/lib/integration_surfaces.py", sources)
        self.assertIn("local/scripts/validate-workspace-sensitive-metadata-rules.py", sources)
        self.assertIn("local/scripts/verify-workspace-boundaries.py", sources)
        self.assertIn("local/scripts/get-publishability-report.py", sources)
        self.assertIn("local/scripts/lib/workspace_sensitive_metadata.py", sources)
        self.assertIn("local/scripts/lib/workspace_boundaries.py", sources)
        self.assertIn("local/config/integration-surfaces.json", sources)
        self.assertIn("registry/skills/example-skill", targets)
        self.assertIn("machine-local runtime state", payload["excluded"])

    def test_export_template_actual_write_verifies_package(self):
        script = REPO_ROOT / "local" / "scripts" / "export-template-package.ps1"
        verify_script = REPO_ROOT / "local" / "scripts" / "verify-template-package.ps1"
        powershell = get_powershell_executable()
        if powershell is None:
            self.skipTest("PowerShell executable not available")

        output_base = REPO_ROOT / "ops" / "template-package"
        output_base.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=output_base, prefix="unit_") as temp_dir:
            output_root = Path(temp_dir)
            package_name = "template-test"
            package_path = output_root / package_name
            export_result = run_command(
                [
                    powershell,
                    "-NoProfile",
                    "-File",
                    str(script),
                    "-OutputRoot",
                    str(output_root),
                    "-Name",
                    package_name,
                ]
            )
            self.assertEqual(export_result.returncode, 0, export_result.stdout + export_result.stderr)
            self.assertTrue((package_path / "manifest.json").is_file())
            self.assertTrue((package_path / "release.json").is_file())

            command = f"& {quote_powershell_string(verify_script)} -Path {quote_powershell_string(package_path)} | ConvertTo-Json -Depth 6"
            verify_result = run_command([powershell, "-NoProfile", "-Command", command])

        self.assertEqual(verify_result.returncode, 0, verify_result.stdout + verify_result.stderr)
        payload = json.loads(verify_result.stdout)
        self.assertTrue(payload["ok"], verify_result.stdout)
        self.assertEqual(payload["missing"], [])
        self.assertEqual(payload["forbidden_present"], [])
        self.assertEqual(payload["content_violations"], [])

    def test_external_review_contract_validates_and_export_uses_contract(self):
        contract_path = REPO_ROOT / "docs" / "reviews" / "external-review-bundle.contract.json"
        repair_script = REPO_ROOT / "local" / "scripts" / "repair-external-review-bundle-contract.py"
        result = run_command([sys.executable, str(repair_script)])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["validation"]["ok"], payload)
        self.assertFalse(payload["changed"], payload)
        contract = json.loads(contract_path.read_text(encoding="utf-8"))

        powershell = get_powershell_executable()
        if powershell is None:
            self.skipTest("PowerShell executable not available")

        export_script = REPO_ROOT / "local" / "scripts" / "export-review-package.ps1"
        export_result = run_command(
            [
                powershell,
                "-NoProfile",
                "-Command",
                f"& {quote_powershell_string(export_script)} -DryRun | ConvertTo-Json -Depth 8",
            ]
        )
        self.assertEqual(export_result.returncode, 0, export_result.stdout + export_result.stderr)
        export_payload = json.loads(export_result.stdout)

        expected_items = (
            [("file", normalize_manifest_path(path)) for path in contract["files"]]
            + [("dir", normalize_manifest_path(path)) for path in contract["directories"]]
            + [("dir", f"registry/skills/{skill}") for skill in contract["skills"]["core"]]
            + [("dir", f"registry/skills/{skill}") for skill in contract["skills"]["expansion"]]
        )
        actual_items = [
            (item["kind"], normalize_manifest_path(item["path"]))
            for item in export_payload["items"]
        ]

        self.assertEqual(actual_items, expected_items)
        self.assertEqual(export_payload["item_count"], len(expected_items))

    def test_export_rebuild_rejects_escape_output_root(self):
        script = REPO_ROOT / "local" / "scripts" / "export-rebuild-project.ps1"
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
        self.assertIn("ops/rebuild-project", result.stdout + result.stderr)

    def test_export_rebuild_actual_write_verifies_package(self):
        script = REPO_ROOT / "local" / "scripts" / "export-rebuild-project.ps1"
        verify_script = REPO_ROOT / "local" / "scripts" / "verify-rebuild-project.ps1"
        powershell = get_powershell_executable()
        if powershell is None:
            self.skipTest("PowerShell executable not available")

        output_base = REPO_ROOT / "ops" / "rebuild-project"
        output_base.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=output_base, prefix="unit_") as temp_dir:
            output_root = Path(temp_dir)
            package_name = f"rebuild-test-{output_root.name}"
            package_path = output_root / package_name
            export_result = run_command(
                [
                    powershell,
                    "-NoProfile",
                    "-File",
                    str(script),
                    "-OutputRoot",
                    str(output_root),
                    "-Name",
                    package_name,
                ]
            )
            self.assertEqual(export_result.returncode, 0, export_result.stdout + export_result.stderr)
            self.assertTrue((package_path / "REBUILD_AS_NEW_PROJECT.md").is_file())

            command = f"& {quote_powershell_string(verify_script)} -Path {quote_powershell_string(package_path)} | ConvertTo-Json -Depth 6"
            verify_result = run_command([powershell, "-NoProfile", "-Command", command])

        self.assertEqual(verify_result.returncode, 0, verify_result.stdout + verify_result.stderr)
        payload = json.loads(verify_result.stdout)
        self.assertTrue(payload["ok"], verify_result.stdout)
        self.assertTrue(payload["template_ok"], verify_result.stdout)
        self.assertEqual(payload["missing"], [])
        self.assertEqual(payload["forbidden_present"], [])

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
        self.assertIsNone(bad["name"])
        self.assertFalse(bad["has_description"])
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
