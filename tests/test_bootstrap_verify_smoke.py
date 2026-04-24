import json
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


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


def load_bootstrap_module():
    bootstrap = REPO_ROOT / "local" / "scripts" / "bootstrap.py"
    spec = importlib.util.spec_from_file_location("unitext_bootstrap", bootstrap)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load bootstrap module from {bootstrap}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class BootstrapVerifySmokeTests(unittest.TestCase):
    def test_runtime_bundle_sync_excludes_hidden_source_entries(self):
        bootstrap = load_bootstrap_module()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "runtime-skills"
            source.mkdir()
            (source / "env").mkdir()
            (source / "env" / "SKILL.md").write_text("# env\n", encoding="utf-8")
            (source / ".system").mkdir()
            (source / ".system" / "marker.txt").write_text("local overlay\n", encoding="utf-8")

            target = root / "codex-skills"
            result = bootstrap.set_skills_target(source, target, "mirror", dry_run=False)

            self.assertEqual(result["action"], "created")
            self.assertTrue((target / "env" / "SKILL.md").exists())
            self.assertFalse((target / ".system").exists())

    def test_runtime_bundle_sync_preserves_target_hidden_extras(self):
        bootstrap = load_bootstrap_module()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "runtime-skills"
            source.mkdir()
            (source / "env").mkdir()
            (source / "env" / "SKILL.md").write_text("# env\n", encoding="utf-8")
            (source / ".system").mkdir()
            (source / ".system" / "marker.txt").write_text("source overlay\n", encoding="utf-8")

            target = root / "codex-skills"
            target.mkdir()
            (target / ".system").mkdir()
            (target / ".system" / "marker.txt").write_text("target overlay\n", encoding="utf-8")

            dry_run = bootstrap.set_skills_target(
                source,
                target,
                "mirror",
                dry_run=True,
                preserve_local_extras=True,
            )
            self.assertEqual(dry_run["baseline_entries"], ["env"])

            result = bootstrap.set_skills_target(
                source,
                target,
                "mirror",
                dry_run=False,
                preserve_local_extras=True,
            )

            self.assertEqual(result["action"], "synced")
            self.assertTrue((target / "env" / "SKILL.md").exists())
            self.assertEqual((target / ".system" / "marker.txt").read_text(encoding="utf-8"), "target overlay\n")

    def test_bootstrap_force_to_temp_home_passes_verify(self):
        if not can_create_directory_symlink():
            self.skipTest("Directory symlink creation is unavailable on this host.")

        bootstrap = REPO_ROOT / "local" / "scripts" / "bootstrap.py"
        verify = REPO_ROOT / "local" / "scripts" / "verify-bootstrap.py"

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            home_dir = root / "home"
            history_root = root / "history"
            home_dir.mkdir()

            bootstrap_result = run_command(
                [
                    sys.executable,
                    str(bootstrap),
                    "--force",
                    "--home-dir",
                    str(home_dir),
                    "--history-root",
                    str(history_root),
                    "--skip-runtime-build",
                    "--skip-copilot",
                    "--skip-project-mcp",
                ]
            )
            self.assertEqual(bootstrap_result.returncode, 0, bootstrap_result.stdout + bootstrap_result.stderr)

            verify_result = run_command(
                [
                    sys.executable,
                    str(verify),
                    "--home-dir",
                    str(home_dir),
                    "--skip-copilot",
                    "--skip-project-mcp",
                ]
            )
            self.assertEqual(verify_result.returncode, 0, verify_result.stdout + verify_result.stderr)

            payload = json.loads(verify_result.stdout)
            self.assertTrue(payload["ok"])
            self.assertTrue(all(item["matches_expected"] for item in payload["targets"]))
            self.assertTrue(payload["codex"]["skills_path_matches"])
            self.assertTrue(payload["codex"]["runtime_target_contains_runtime_baseline"])
            self.assertEqual(payload["codex"]["runtime_target_missing_baseline"], [])


if __name__ == "__main__":
    unittest.main()
