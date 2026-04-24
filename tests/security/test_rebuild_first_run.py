import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
EXPORT_SCRIPT = REPO_ROOT / "local" / "scripts" / "export-rebuild-project.ps1"


def get_powershell_executable():
    candidate = os.environ.get("POWERSHELL", "pwsh")
    if shutil.which(candidate):
        return candidate
    return None


def run_command(args, cwd=REPO_ROOT):
    return subprocess.run(
        args,
        cwd=cwd,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


def can_create_directory_symlink() -> bool:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        source = root / "source"
        link = root / "link"
        source.mkdir()
        try:
            link.symlink_to(source, target_is_directory=True)
        except OSError:
            return False
        return link.is_symlink()


class RebuildFirstRunTests(unittest.TestCase):
    def test_exported_rebuild_package_supports_isolated_bootstrap_first_run(self):
        powershell = get_powershell_executable()
        if powershell is None:
            self.skipTest("PowerShell executable not available")
        if not can_create_directory_symlink():
            self.skipTest("Directory symlink creation is unavailable on this host.")

        output_base = REPO_ROOT / "ops" / "rebuild-project"
        output_base.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=output_base, prefix="unit_") as output_dir:
            package_name = "rebuild-first-run"
            package_path = Path(output_dir) / package_name
            export_result = run_command(
                [
                    powershell,
                    "-NoProfile",
                    "-File",
                    str(EXPORT_SCRIPT),
                    "-OutputRoot",
                    output_dir,
                    "-Name",
                    package_name,
                ]
            )
            self.assertEqual(export_result.returncode, 0, export_result.stdout + export_result.stderr)

            bootstrap = package_path / "local" / "scripts" / "bootstrap.py"
            verify = package_path / "local" / "scripts" / "verify-bootstrap.py"
            self.assertTrue((package_path / "local" / "scripts" / "build-runtime-layer.py").is_file())
            self.assertTrue((package_path / "local" / "scripts" / "lib" / "integration_surfaces.py").is_file())
            self.assertTrue((package_path / "local" / "config" / "integration-surfaces.json").is_file())

            dry_run_result = run_command(
                [
                    sys.executable,
                    str(bootstrap),
                    "--dry-run",
                    "--home-dir",
                    str(package_path / ".first-run-home"),
                    "--skip-copilot",
                    "--skip-project-mcp",
                ],
                cwd=package_path,
            )
            self.assertEqual(dry_run_result.returncode, 0, dry_run_result.stdout + dry_run_result.stderr)
            dry_run_payload = json.loads(dry_run_result.stdout)
            self.assertEqual(dry_run_payload["generation_state"], "dry_run")
            self.assertEqual(dry_run_payload["runtime"]["action"], "planned")

            home_dir = package_path / ".first-run-home"
            history_root = package_path / "ops" / "history"
            home_dir.mkdir(exist_ok=True)
            bootstrap_result = run_command(
                [
                    sys.executable,
                    str(bootstrap),
                    "--force",
                    "--home-dir",
                    str(home_dir),
                    "--history-root",
                    str(history_root),
                    "--skip-copilot",
                    "--skip-project-mcp",
                ],
                cwd=package_path,
            )
            self.assertEqual(bootstrap_result.returncode, 0, bootstrap_result.stdout + bootstrap_result.stderr)
            self.assertTrue((package_path / "runtime" / "skills" / "example-skill" / "SKILL.md").is_file())

            verify_result = run_command(
                [
                    sys.executable,
                    str(verify),
                    "--home-dir",
                    str(home_dir),
                    "--skip-copilot",
                    "--skip-project-mcp",
                ],
                cwd=package_path,
            )
            self.assertEqual(verify_result.returncode, 0, verify_result.stdout + verify_result.stderr)
            verify_payload = json.loads(verify_result.stdout)
            self.assertTrue(verify_payload["ok"], verify_result.stdout)
            self.assertTrue(verify_payload["codex"]["runtime_target_contains_runtime_baseline"])


if __name__ == "__main__":
    unittest.main()
