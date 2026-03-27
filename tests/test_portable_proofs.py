import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def run_command(args, cwd=REPO_ROOT, env=None):
    return subprocess.run(args, cwd=cwd, env=env, text=True, capture_output=True, encoding="utf-8", errors="replace")


def load_mcp_server_module():
    path = REPO_ROOT / "registry" / "mcp" / "claude-project-mcp-seed" / "server.py"
    spec = importlib.util.spec_from_file_location("unitext_mcp_server", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class PortableProofTests(unittest.TestCase):
    def test_bootstrap_dry_run_remains_machine_readable(self):
        result = run_command([sys.executable, "local/scripts/bootstrap.py", "--dry-run"])
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["dry_run"])
        self.assertIn("skills", payload)
        self.assertIn("codex", payload)
        self.assertIn("project_mcp", payload)

    def test_bootstrap_force_delivers_public_skills_in_isolated_home(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            repo = temp_root / "repo"
            home = temp_root / "home"

            (repo / "registry" / "skills").mkdir(parents=True)
            (repo / "registry" / "mcp" / "claude-project-mcp-seed").mkdir(parents=True)
            shutil.copy2(
                REPO_ROOT / "registry" / "mcp" / "claude-project-mcp-seed" / "server.py",
                repo / "registry" / "mcp" / "claude-project-mcp-seed" / "server.py",
            )
            shutil.copytree(REPO_ROOT / "registry" / "skills" / "mcp-builder", repo / "registry" / "skills" / "mcp-builder")
            shutil.copytree(
                REPO_ROOT / "registry" / "skills" / "skill-creator",
                repo / "registry" / "skills" / "skill-creator",
            )
            shutil.copytree(
                REPO_ROOT / "registry" / "skills" / "webapp-testing",
                repo / "registry" / "skills" / "webapp-testing",
            )
            (repo / "README.md").write_text("# temp\n", encoding="utf-8")
            (repo / "INDEX.md").write_text("# temp\n", encoding="utf-8")
            home.mkdir()

            env = os.environ.copy()
            env["HOME"] = str(home)
            env["USERPROFILE"] = str(home)

            result = run_command(
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
                env=env,
            )
            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)

            for parent in [".claude", ".gemini", ".agents"]:
                skills_dir = home / parent / "skills"
                self.assertTrue((skills_dir / "mcp-builder" / "SKILL.md").exists())
                self.assertTrue((skills_dir / "skill-creator" / "SKILL.md").exists())
                self.assertTrue((skills_dir / "webapp-testing" / "SKILL.md").exists())

            config = home / ".codex" / "config.toml"
            project_mcp = repo / ".mcp.json"
            self.assertTrue(config.exists())
            self.assertTrue(project_mcp.exists())
            self.assertIn("skills_path", config.read_text(encoding="utf-8"))

    def test_mcp_seed_registry_summary_tool_returns_counts(self):
        module = load_mcp_server_module()
        server = module.Server(REPO_ROOT)
        response = server.call_tool({"name": "registry_summary", "arguments": {}})
        payload = json.loads(response["content"][0]["text"])
        self.assertEqual(payload["repo_root"], str(REPO_ROOT.resolve()))
        self.assertGreater(payload["skills"], 0)
        self.assertGreater(payload["mcp"], 0)

    def test_mcp_seed_can_read_core_docs_and_registry_files(self):
        module = load_mcp_server_module()
        server = module.Server(REPO_ROOT)

        readme = server.call_tool({"name": "read_registry_file", "arguments": {"path": "README.md"}})
        readme_payload = json.loads(readme["content"][0]["text"])
        self.assertEqual(readme_payload["path"], "README.md")
        self.assertIn("UniText", readme_payload["content"])

        skill = server.call_tool(
            {"name": "read_registry_file", "arguments": {"path": "registry/skills/mcp-builder/SKILL.md"}}
        )
        skill_payload = json.loads(skill["content"][0]["text"])
        self.assertEqual(Path(skill_payload["path"]).as_posix(), "registry/skills/mcp-builder/SKILL.md")
        self.assertIn("mcp-builder", skill_payload["content"])
