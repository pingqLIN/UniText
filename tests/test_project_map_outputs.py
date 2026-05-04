import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "local" / "scripts" / "build-project-map.py"
PROJECT_SCRIPT_PATH = REPO_ROOT / "web" / "project-map-ui" / "build-project-map.py"


def run_command(args):
    return subprocess.run(
        args,
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


class ProjectMapOutputTests(unittest.TestCase):
    def test_project_entrypoint_writes_artifacts(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result = run_command([sys.executable, str(PROJECT_SCRIPT_PATH), "--output-dir", temp_dir])
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            summary = json.loads(result.stdout)

            self.assertEqual(Path(summary["html_path"]), Path(temp_dir) / "site" / "project-map.html")
            self.assertTrue((Path(temp_dir) / "site" / "project-map-share.html").is_file())

    def test_project_entrypoint_accepts_non_unitext_governance_root_with_markers(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir) / "governance-root"
            output_root = Path(temp_dir) / "out"
            temp_root.mkdir()
            (temp_root / "README.md").write_text("# Demo Governance Root\n", encoding="utf-8")
            (temp_root / "AGENTS.md").write_text("# AGENTS.md\n\n- Keep changes local.\n", encoding="utf-8")

            result = run_command([
                sys.executable,
                str(PROJECT_SCRIPT_PATH),
                "--repo-root",
                str(temp_root),
                "--output-dir",
                str(output_root),
            ])

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            summary = json.loads(result.stdout)
            payload = json.loads((output_root / "project-map.json").read_text(encoding="utf-8"))
            interactive_html = (output_root / "site" / "project-map.html").read_text(encoding="utf-8")
            validation = payload["meta"]["root_validation"]
            adapter = payload["meta"]["project_map_adapter"]

            self.assertEqual(Path(summary["repo_root"]), temp_root.resolve())
            self.assertTrue(validation["valid"])
            self.assertEqual(validation["selected_adapter"], "governance-folder")
            self.assertEqual(adapter["adapter_id"], "governance-folder")
            self.assertIn("AGENTS.md", adapter["root_markers"])
            self.assertIn("AGENTS.md", validation["governance_markers_present"])
            self.assertEqual(payload["governance"]["path_classification"]["scope_hint"], "repo")
            self.assertIn('"policy_loaded": false', interactive_html)
            self.assertIn('"adapter_id": "governance-folder"', interactive_html)
            self.assertGreaterEqual(summary["node_count"], 2)

    def test_project_entrypoint_rejects_root_without_governance_markers(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir) / "not-governance"
            temp_root.mkdir()

            result = run_command([
                sys.executable,
                str(PROJECT_SCRIPT_PATH),
                "--repo-root",
                str(temp_root),
                "--output-dir",
                str(Path(temp_dir) / "out"),
            ])

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing recognized governance markers", result.stdout + result.stderr)

    def test_project_entrypoint_rejects_explicit_missing_governance_policy(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir) / "governance-root"
            temp_root.mkdir()
            (temp_root / "AGENTS.md").write_text("# AGENTS.md\n", encoding="utf-8")

            output_dir = Path(temp_dir) / "out"
            result = run_command([
                sys.executable,
                str(PROJECT_SCRIPT_PATH),
                "--repo-root",
                str(temp_root),
                "--output-dir",
                str(output_dir),
                "--governance-policy",
                "missing-policy.json",
            ])

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("governance policy file does not exist", result.stdout + result.stderr)
            self.assertFalse(output_dir.exists())

    def test_cli_writes_self_contained_interactive_share_and_handoff_artifacts(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result = run_command([sys.executable, str(SCRIPT_PATH), "--output-dir", temp_dir])
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            summary = json.loads(result.stdout)

            output_root = Path(temp_dir)
            json_path = output_root / "project-map.json"
            html_path = output_root / "site" / "project-map.html"
            share_html_path = output_root / "site" / "project-map-share.html"
            handoff_json_path = output_root / "site" / "project-map-handoff.json"
            handoff_md_path = output_root / "site" / "project-map-handoff.md"

            self.assertEqual(Path(summary["json_path"]), json_path)
            self.assertEqual(Path(summary["html_path"]), html_path)
            self.assertEqual(Path(summary["share_html_path"]), share_html_path)
            self.assertEqual(Path(summary["handoff_json_path"]), handoff_json_path)
            self.assertEqual(Path(summary["handoff_md_path"]), handoff_md_path)

            for path in (json_path, html_path, share_html_path, handoff_json_path, handoff_md_path):
                self.assertTrue(path.is_file(), f"Missing generated artifact: {path}")

            payload = json.loads(json_path.read_text(encoding="utf-8"))
            interactive_html = html_path.read_text(encoding="utf-8")
            share_html = share_html_path.read_text(encoding="utf-8")
            handoff = json.loads(handoff_json_path.read_text(encoding="utf-8"))
            handoff_markdown = handoff_md_path.read_text(encoding="utf-8")

        self.assertGreater(summary["node_count"], 0)
        self.assertGreater(summary["edge_count"], 0)
        self.assertEqual(summary["node_count"], len(payload["nodes"]))
        self.assertEqual(summary["edge_count"], len(payload["edges"]))

        for placeholder in (
            "__BOOTSTRAP_DATA__",
            "__PAGE_MODE__",
            "__GOVERNANCE_POLICY__",
            "__RUNTIME_SOURCE__",
        ):
            self.assertNotIn(placeholder, interactive_html)
            self.assertNotIn(placeholder, share_html)

        self.assertIn('window.PROJECT_MAP_PAGE_MODE = "interactive";', interactive_html)
        self.assertIn('window.PROJECT_MAP_PAGE_MODE = "share-safe";', share_html)
        self.assertIn("window.PROJECT_MAP_BOOTSTRAP =", interactive_html)
        self.assertIn("window.PROJECT_MAP_BOOTSTRAP =", share_html)
        self.assertIn("window.AGENT_GOVERNANCE_POLICY = {", interactive_html)
        self.assertIn("window.AGENT_GOVERNANCE_POLICY = null;", share_html)
        self.assertIn('id="link-repo"', interactive_html)
        self.assertNotIn('id="link-repo"', share_html)
        self.assertNotIn('id="workspace-tab-governance"', share_html)
        self.assertNotIn('id="workspace-panel-governance"', share_html)
        self.assertNotIn('id="maintenance-controls"', share_html)
        self.assertNotIn('class="governance-panel"', share_html)
        self.assertNotIn('id="governance-write"', share_html)

        self.assertFalse(handoff["surface_contract"]["share_safe"]["browser_scan"])
        self.assertFalse(handoff["surface_contract"]["share_safe"]["governance_resolver"])
        self.assertFalse(handoff["surface_contract"]["share_safe"]["native_repo_paths"])
        self.assertIn("Share-safe page", handoff_markdown)


if __name__ == "__main__":
    unittest.main()
