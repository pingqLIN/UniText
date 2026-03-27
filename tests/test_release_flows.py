import json
import os
import tempfile
import shutil
import subprocess
import sys
import unittest
import uuid
import textwrap
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
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


def powershell_literal(value):
    return "'" + str(value).replace("'", "''") + "'"


def powershell_path(path):
    return powershell_literal(translate_path_for_powershell(path))


def run_powershell_json(script_path, *script_args, depth=5):
    script_parts = ["&", powershell_path(script_path)]
    for arg in script_args:
        if isinstance(arg, Path):
            script_parts.append(powershell_path(arg))
        elif isinstance(arg, str) and arg.startswith("-"):
            script_parts.append(arg)
        else:
            script_parts.append(powershell_literal(arg))

    script_parts.extend(["|", "ConvertTo-Json", "-Depth", str(depth), "-Compress"])
    result = run_command([POWERSHELL, "-NoProfile", "-Command", " ".join(script_parts)])
    return result, json.loads(result.stdout)


def run_powershell_file(script_path, *script_args):
    args = [POWERSHELL, "-NoProfile", "-File", translate_path_for_powershell(script_path)]
    for arg in script_args:
        if isinstance(arg, Path):
            args.append(translate_path_for_powershell(arg))
        else:
            args.append(str(arg))
    return run_command(args)


class ReleaseFlowTests(unittest.TestCase):
    def test_bootstrap_dry_run_emits_machine_readable_plan(self):
        result = run_command([sys.executable, "local/scripts/bootstrap.py", "--dry-run"])
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["dry_run"])
        self.assertIn("skills", payload)
        self.assertIn("codex", payload)
        self.assertIn("project_mcp", payload)

    @unittest.skipUnless(HAS_POWERSHELL, f"{POWERSHELL} is required for PowerShell release-flow tests")
    def test_workspace_hygiene_check_reports_ok(self):
        result, payload = run_powershell_json(REPO_ROOT / "local" / "scripts" / "verify-workspace-hygiene.ps1")
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertTrue(payload["ok"])
        self.assertFalse(payload["absolute_path_hits"])

    @unittest.skipUnless(HAS_POWERSHELL, f"{POWERSHELL} is required for PowerShell release-flow tests")
    def test_review_package_dry_run_exposes_ci_and_source_model(self):
        result, payload = run_powershell_json(
            REPO_ROOT / "local" / "scripts" / "export-review-package.ps1",
            "-DryRun",
            depth=6,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertEqual(payload["public_skill_source_model"], "github-backed")
        item_paths = {item["path"] for item in payload["items"] if "path" in item}
        self.assertIn(".github\\\\workflows\\\\ci.yml", item_paths)

    @unittest.skipUnless(HAS_POWERSHELL, f"{POWERSHELL} is required for PowerShell release-flow tests")
    def test_template_package_export_and_verify_smoke(self):
        name = f"testsmoke_{uuid.uuid4().hex[:8]}"
        package_path = REPO_ROOT / "ops" / "template-package" / name
        try:
            export_result = run_powershell_file(
                REPO_ROOT / "local" / "scripts" / "export-template-package.ps1",
                "-Name",
                name,
            )
            self.assertEqual(export_result.returncode, 0, msg=export_result.stdout + export_result.stderr)

            verify_result, payload = run_powershell_json(
                REPO_ROOT / "local" / "scripts" / "verify-template-package.ps1",
                "-Path",
                package_path,
            )
            self.assertEqual(verify_result.returncode, 0, msg=verify_result.stdout + verify_result.stderr)
            self.assertTrue(payload["ok"])
        finally:
            if package_path.exists():
                shutil.rmtree(package_path)

    def test_bootstrap_force_writes_complete_state_in_isolated_repo(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            repo = temp_root / "repo"
            home = temp_root / "home"
            server_source = REPO_ROOT / "registry" / "mcp" / "claude-project-mcp-seed" / "server.py"

            (repo / "registry" / "skills").mkdir(parents=True)
            (repo / "registry" / "mcp" / "claude-project-mcp-seed").mkdir(parents=True)
            (repo / "registry" / "mcp" / "claude-project-mcp-seed" / "server.py").write_text(
                server_source.read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            (repo / "README.md").write_text("# temp\n", encoding="utf-8")
            (repo / "INDEX.md").write_text("# temp\n", encoding="utf-8")
            home.mkdir()

            env = os.environ.copy()
            env["HOME"] = str(home)
            env["USERPROFILE"] = str(home)

            result = subprocess.run(
                [
                    sys.executable,
                    "local/scripts/bootstrap.py",
                    "--repo-root",
                    str(repo),
                    "--allow-external-repo-root",
                    "--force",
                    "--mode",
                    "mirror",
                ],
                cwd=REPO_ROOT,
                env=env,
                text=True,
                capture_output=True,
                encoding="utf-8",
                errors="replace",
            )
            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)

            payload = json.loads(result.stdout)
            self.assertFalse(payload["dry_run"])
            self.assertTrue((repo / ".mcp.json").exists())
            self.assertTrue((home / ".codex" / "config.toml").exists())
            self.assertTrue((home / ".claude" / "skills").exists())
            self.assertTrue((home / ".gemini" / "skills").exists())
            self.assertTrue((home / ".agents" / "skills").exists())

    @unittest.skipUnless(HAS_POWERSHELL, f"{POWERSHELL} is required for PowerShell release-flow tests")
    def test_verify_template_rejects_forbidden_residual(self):
        name = f"residual_{uuid.uuid4().hex[:8]}"
        package_path = REPO_ROOT / "ops" / "template-package" / name
        try:
            export_result = run_powershell_file(
                REPO_ROOT / "local" / "scripts" / "export-template-package.ps1",
                "-Name",
                name,
            )
            self.assertEqual(export_result.returncode, 0, msg=export_result.stdout + export_result.stderr)

            forbidden = package_path / "EXTERNAL_REVIEW_PACKAGE.md"
            forbidden.write_text("forbidden residual", encoding="utf-8")

            verify_result, payload = run_powershell_json(
                REPO_ROOT / "local" / "scripts" / "verify-template-package.ps1",
                "-Path",
                package_path,
            )
            self.assertEqual(verify_result.returncode, 0, msg=verify_result.stdout + verify_result.stderr)
            self.assertFalse(payload["ok"])
            self.assertIn("EXTERNAL_REVIEW_PACKAGE.md", payload["forbidden_present"])
        finally:
            if package_path.exists():
                shutil.rmtree(package_path)

    @unittest.skipUnless(HAS_POWERSHELL, f"{POWERSHELL} is required for PowerShell release-flow tests")
    def test_generate_index_entries_uses_explicit_root(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            skill = root / "registry" / "skills" / "demo-skill"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                "---\nname: demo-skill\ndescription: demo\n---\n\n## Usage\n",
                encoding="utf-8",
            )

            result = run_powershell_file(
                REPO_ROOT / "local" / "scripts" / "generate-index-entries.ps1",
                "-Root",
                root,
            )
            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            self.assertIn("demo-skill", result.stdout)

    @unittest.skipUnless(HAS_POWERSHELL, f"{POWERSHELL} is required for PowerShell release-flow tests")
    def test_scan_skills_uses_shared_frontmatter_parser(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            valid = root / "valid-skill"
            invalid = root / "invalid-skill"
            valid.mkdir()
            invalid.mkdir()

            (valid / "SKILL.md").write_text(
                textwrap.dedent(
                    """\
                    ---
                    name: valid-skill
                    description: >
                      Folded description
                      with multiple lines
                    license: MIT
                    tags:
                      - alpha
                      - beta
                    ---

                    ## Usage
                    """
                ),
                encoding="utf-8",
            )
            (invalid / "SKILL.md").write_text(
                textwrap.dedent(
                    """\
                    ---
                    name: invalid-skill
                    name: duplicate
                    description: broken
                    ---

                    ## Usage
                    """
                ),
                encoding="utf-8",
            )

            result, payload = run_powershell_json(
                REPO_ROOT / "local" / "scripts" / "scan-skills.ps1",
                "-Source",
                root,
                depth=8,
            )

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            self.assertEqual(len(payload), 2)

            records = {item["id"]: item for item in payload}
            self.assertEqual(records["valid-skill"]["name"], "valid-skill")
            self.assertIn("Folded description", records["valid-skill"]["description"])
            self.assertEqual(records["valid-skill"]["license"], "MIT")
            self.assertEqual(records["valid-skill"]["tags"], ["alpha", "beta"])
            self.assertTrue(records["valid-skill"]["validation_ok"])
            self.assertTrue(records["valid-skill"]["adoption_ready"])

            self.assertFalse(records["invalid-skill"]["validation_ok"])
            self.assertIn("Duplicate key", records["invalid-skill"]["validation_message"])
