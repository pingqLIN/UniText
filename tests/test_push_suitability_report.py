import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "local" / "scripts" / "generate-push-suitability-report.py"


def load_module():
    module_name = "unitext_push_suitability_report"
    spec = importlib.util.spec_from_file_location(module_name, SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load script module from {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class PushSuitabilityReportTests(unittest.TestCase):
    def test_recommendation_lines_require_clean_gates(self):
        module = load_module()
        lines = module.recommendation_lines(
            {
                "bootstrap": {"ok": False},
                "boundary": {"ok": False},
                "publishability": {"structurally_publishable_if_permission_is_granted": False},
                "tracking": {
                    "branch": "main",
                    "tracking": "origin/main",
                    "upstream_configured": True,
                    "tracking_resolved": True,
                    "ahead": 4,
                    "behind": 2,
                },
            }
        )
        self.assertTrue(any("bootstrap" in line for line in lines))
        self.assertTrue(any("workspace boundary" in line for line in lines))
        self.assertTrue(any("publishability blockers" in line for line in lines))
        self.assertTrue(any("`4`-commit batch" in line and "`origin/main`" in line for line in lines))
        self.assertTrue(any("behind by `2`" in line for line in lines))

    def test_recommendation_lines_require_upstream_configuration_when_missing(self):
        module = load_module()
        lines = module.recommendation_lines(
            {
                "bootstrap": {"ok": True},
                "boundary": {"ok": True},
                "publishability": {"structurally_publishable_if_permission_is_granted": True},
                "tracking": {
                    "branch": "feature/push-review",
                    "tracking": None,
                    "upstream_configured": False,
                    "tracking_resolved": False,
                    "ahead": None,
                    "behind": None,
                },
            }
        )
        self.assertTrue(any("upstream tracking branch" in line for line in lines))
        self.assertFalse(any("Structurally ready for push review" in line for line in lines))

    def test_run_json_script_uses_current_interpreter(self):
        module = load_module()
        completed = subprocess.CompletedProcess(args=[], returncode=0, stdout="{}", stderr="")
        with patch.object(module.subprocess, "run", return_value=completed) as mock_run:
            payload = module.run_json_script("verify-bootstrap.py")
        self.assertEqual(payload, {})
        self.assertEqual(mock_run.call_args.args[0][0], sys.executable)

    def test_try_run_git_config_raises_on_unexpected_git_failure(self):
        module = load_module()
        failed = subprocess.CompletedProcess(args=[], returncode=128, stdout="", stderr="fatal: unsafe repository")
        with patch.object(module.subprocess, "run", return_value=failed):
            with self.assertRaisesRegex(RuntimeError, "unsafe repository"):
                module.try_run_git_config(["config", "--get", "branch.main.remote"])

    def test_ahead_behind_status_handles_missing_upstream(self):
        module = load_module()
        with patch.object(module, "branch_head", return_value="feature/push-review"), patch.object(
            module, "try_run_git_config", side_effect=[None, None]
        ):
            status = module.ahead_behind_status()
        self.assertEqual(
            status,
            {
                "branch": "feature/push-review",
                "tracking": None,
                "upstream_configured": False,
                "tracking_resolved": False,
                "ahead": None,
                "behind": None,
            },
        )

    def test_ahead_behind_status_handles_unresolved_upstream_ref(self):
        module = load_module()
        with patch.object(module, "branch_head", return_value="feature/release"), patch.object(
            module, "try_run_git_config", side_effect=["origin", "refs/heads/release/1.0"]
        ), patch.object(module, "git_ref_exists", return_value=False):
            status = module.ahead_behind_status()
        self.assertEqual(
            status,
            {
                "branch": "feature/release",
                "tracking": "origin/release/1.0",
                "upstream_configured": True,
                "tracking_resolved": False,
                "ahead": None,
                "behind": None,
            },
        )

    def test_format_markdown_includes_push_boundary_note(self):
        module = load_module()
        payload = {
            "generated_on": "2026-04-28",
            "repo_root": "Q:\\UniText",
            "branch_status": "## main...origin/main [ahead 64]",
            "tracking": {
                "tracking": "origin/main",
                "upstream_configured": True,
                "tracking_resolved": True,
                "ahead": 64,
                "behind": 0,
            },
            "recent_commits": ["0c83e0c Refine runtime diff gating and sync projections"],
            "bootstrap": {"ok": True},
            "boundary": {"ok": True, "path_violations": {}, "content_violations": {}},
            "publishability": {"working_tree_clean": True, "structurally_publishable_if_permission_is_granted": True},
            "recommendations": ["Structurally ready for push review if the user explicitly grants push permission."],
        }
        rendered = module.format_markdown(payload)
        self.assertIn("# UniText Push Suitability Report — 2026-04-28", rendered)
        self.assertIn("This report does not grant publish or push permission.", rendered)
        self.assertIn("Structurally ready for push review", rendered)
        self.assertIn("Upstream configured: `true`", rendered)
        self.assertIn("Upstream resolved: `true`", rendered)

    def test_format_markdown_marks_commit_distance_unknown_without_upstream(self):
        module = load_module()
        payload = {
            "generated_on": "2026-04-28",
            "repo_root": "Q:\\UniText",
            "branch_status": "## feature/push-review",
            "tracking": {
                "branch": "feature/push-review",
                "tracking": None,
                "upstream_configured": False,
                "tracking_resolved": False,
                "ahead": None,
                "behind": None,
            },
            "recent_commits": [],
            "bootstrap": {"ok": True},
            "boundary": {"ok": True, "path_violations": {}, "content_violations": {}},
            "publishability": {"working_tree_clean": True, "structurally_publishable_if_permission_is_granted": True},
            "recommendations": ["Configure an upstream tracking branch for `feature/push-review` before treating this branch as push-ready."],
        }
        rendered = module.format_markdown(payload)
        self.assertIn("Upstream tracking: `not configured`", rendered)
        self.assertIn("Ahead commits: `unknown`", rendered)
        self.assertIn("Behind commits: `unknown`", rendered)

    def test_recommendation_lines_use_actual_tracking_branch(self):
        module = load_module()
        lines = module.recommendation_lines(
            {
                "bootstrap": {"ok": True},
                "boundary": {"ok": True},
                "publishability": {"structurally_publishable_if_permission_is_granted": True},
                "tracking": {
                    "branch": "release-review",
                    "tracking": "origin/release/1.0",
                    "upstream_configured": True,
                    "tracking_resolved": True,
                    "ahead": 3,
                    "behind": 0,
                },
            }
        )
        self.assertTrue(any("against `origin/release/1.0`" in line for line in lines))

    def test_default_output_path_uses_ignored_ops_reports_directory(self):
        module = load_module()
        relative = module.default_output_path().relative_to(REPO_ROOT)
        self.assertEqual(
            relative.as_posix(),
            f"ops/reports/PUSH_SUITABILITY_REPORT_{module.date.today().isoformat()}.md",
        )


if __name__ == "__main__":
    unittest.main()
