import json
import os
import shutil
import subprocess
import sys
import tempfile
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


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_minimal_repo(repo_root: Path) -> None:
    write_text(repo_root / "README.md", "# Demo\n")
    write_text(repo_root / "INDEX.md", "# Index\n")
    write_text(repo_root / "registry" / "skills" / "demo" / "SKILL.md", "## Demo\n")
    write_text(repo_root / "registry" / "mcp" / "claude-project-mcp-seed" / "server.py", "print('ok')\n")


class InterruptedRunIntegrityTests(unittest.TestCase):
    def test_bootstrap_dry_run_leaves_no_artifacts_in_isolated_repo(self):
        script = REPO_ROOT / "local" / "scripts" / "bootstrap.py"
        with tempfile.TemporaryDirectory() as temp_dir:
            sandbox = Path(temp_dir)
            repo_root = sandbox / "repo"
            home_root = sandbox / "home"
            build_minimal_repo(repo_root)
            env = os.environ.copy()
            env["HOME"] = str(home_root)

            result = run_command(
                [
                    sys.executable,
                    str(script),
                    "--repo-root",
                    str(repo_root),
                    "--allow-external-repo-root",
                    "--dry-run",
                ],
                env=env,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["generation_state"], "dry_run")
            self.assertFalse((repo_root / ".mcp.json").exists())
            self.assertFalse((repo_root / "ops" / "history").exists())
            self.assertFalse((home_root / ".codex" / "config.toml").exists())
            self.assertFalse((home_root / ".copilot" / "mcp-config.json").exists())

    def test_bootstrap_force_writes_complete_state_in_isolated_repo(self):
        script = REPO_ROOT / "local" / "scripts" / "bootstrap.py"
        with tempfile.TemporaryDirectory() as temp_dir:
            sandbox = Path(temp_dir)
            repo_root = sandbox / "repo"
            home_root = sandbox / "home"
            build_minimal_repo(repo_root)
            env = os.environ.copy()
            env["HOME"] = str(home_root)

            result = run_command(
                [
                    sys.executable,
                    str(script),
                    "--repo-root",
                    str(repo_root),
                    "--allow-external-repo-root",
                    "--force",
                    "--mode",
                    "mirror",
                ],
                env=env,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((repo_root / ".mcp.json").exists())
            runs = sorted((repo_root / "ops" / "history").glob("bootstrap_*"))
            self.assertEqual(len(runs), 1)
            state = json.loads((runs[0] / "state.json").read_text(encoding="utf-8"))
            summary = json.loads((runs[0] / "summary.json").read_text(encoding="utf-8"))
            self.assertEqual(state["generation_state"], "complete")
            self.assertEqual(summary["generation_state"], "complete")
            self.assertEqual(state, summary)
            self.assertTrue((home_root / ".codex" / "config.toml").exists())
            self.assertTrue((home_root / ".copilot" / "skills").exists())
            copilot_config = home_root / ".copilot" / "mcp-config.json"
            self.assertTrue(copilot_config.exists())
            copilot_body = json.loads(copilot_config.read_text(encoding="utf-8"))
            self.assertEqual(
                copilot_body["mcpServers"]["unitext-registry"]["args"],
                [str(repo_root / "registry" / "mcp" / "claude-project-mcp-seed" / "server.py"), "--root", str(repo_root)],
            )

    def test_bootstrap_force_merges_existing_copilot_mcp_config(self):
        script = REPO_ROOT / "local" / "scripts" / "bootstrap.py"
        with tempfile.TemporaryDirectory() as temp_dir:
            sandbox = Path(temp_dir)
            repo_root = sandbox / "repo"
            home_root = sandbox / "home"
            build_minimal_repo(repo_root)
            existing_config = home_root / ".copilot" / "mcp-config.json"
            write_text(
                existing_config,
                json.dumps(
                    {
                        "mcpServers": {
                            "existing-server": {
                                "type": "local",
                                "command": "demo",
                                "args": ["--demo"],
                                "env": {},
                                "tools": ["*"],
                            }
                        }
                    }
                ),
            )
            env = os.environ.copy()
            env["HOME"] = str(home_root)

            result = run_command(
                [
                    sys.executable,
                    str(script),
                    "--repo-root",
                    str(repo_root),
                    "--allow-external-repo-root",
                    "--force",
                    "--mode",
                    "mirror",
                ],
                env=env,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            body = json.loads(existing_config.read_text(encoding="utf-8"))
            self.assertIn("existing-server", body["mcpServers"])
            self.assertIn("unitext-registry", body["mcpServers"])

    def test_verify_template_rejects_interrupted_residual(self):
        powershell = get_powershell_executable()
        if powershell is None:
            self.skipTest("PowerShell executable not available")

        script = REPO_ROOT / "local" / "scripts" / "verify-template-package.ps1"
        with tempfile.TemporaryDirectory() as temp_dir:
            package_root = Path(temp_dir) / ".template_run.staging_20260325"
            package_root.mkdir(parents=True)
            write_text(package_root / "manifest.json", "{}\n")
            write_text(package_root / "release.json", "{}\n")
            write_text(package_root / "generation-state.json", json.dumps({"generation_state": "partial"}))

            result = run_command(
                [
                    powershell,
                    "-NoProfile",
                    "-File",
                    str(script),
                    "-Path",
                    str(package_root),
                ]
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertFalse(payload["ok"])
            self.assertTrue(payload["metadata_issues"])

    def test_release_integrity_helper_detects_bad_generation_state(self):
        powershell = get_powershell_executable()
        if powershell is None:
            self.skipTest("PowerShell executable not available")

        helper = REPO_ROOT / "local" / "scripts" / "lib" / "release-integrity.ps1"
        with tempfile.TemporaryDirectory() as temp_dir:
            package_root = Path(temp_dir) / "package"
            package_root.mkdir()
            metadata = {
                "release_target": "template-package",
                "phase_target": "template-release-cleanup",
                "release_channel": "candidate",
                "generation_state": "partial",
            }
            write_text(package_root / "manifest.json", json.dumps(metadata))
            write_text(package_root / "release.json", json.dumps(metadata))
            write_text(package_root / "generation-state.json", json.dumps(metadata))

            command = (
                f". '{helper}'; "
                f"$result = Test-ReleasePackageMetadata "
                f"-PackagePath '{package_root}' "
                f"-ExpectedReleaseTarget 'template-package' "
                f"-ExpectedPhaseTarget 'template-release-cleanup' "
                f"-ExpectedReleaseChannel 'candidate'; "
                "$result | ConvertTo-Json -Depth 8"
            )
            result = run_command([powershell, "-NoProfile", "-Command", command])

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertFalse(payload["ok"])
            self.assertTrue(any("generation_state" in item for item in payload["issues"]))


if __name__ == "__main__":
    unittest.main()
