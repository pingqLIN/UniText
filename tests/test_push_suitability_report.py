import importlib.util
import sys
import unittest
from pathlib import Path


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
                "tracking": {"ahead": 4, "behind": 2, "tracking": "origin/main"},
            }
        )
        self.assertTrue(any("bootstrap" in line for line in lines))
        self.assertTrue(any("workspace boundary" in line for line in lines))
        self.assertTrue(any("publishability blockers" in line for line in lines))
        self.assertTrue(any("`4`-commit batch" in line for line in lines))
        self.assertTrue(any("behind by `2`" in line for line in lines))

    def test_format_markdown_includes_push_boundary_note(self):
        module = load_module()
        payload = {
            "generated_on": "2026-04-28",
            "repo_root": "Q:\\UniText",
            "branch_status": "## main...origin/main [ahead 64]",
            "tracking": {"tracking": "origin/main", "ahead": 64, "behind": 0},
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


if __name__ == "__main__":
    unittest.main()
