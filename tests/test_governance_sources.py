import unittest
from pathlib import Path

from local.scripts.lib.governance_sources import build_governance_sources, is_within_path


REPO_ROOT = Path(__file__).resolve().parents[1]


class GovernanceSourceTests(unittest.TestCase):
    def test_build_governance_sources_reports_three_file_layers(self):
        governance = build_governance_sources(REPO_ROOT)
        sources = governance["sources"]

        self.assertIn("path_classification", governance)
        self.assertEqual(governance["path_classification"]["scope_hint"], "repo")
        self.assertEqual([source["scope"] for source in sources], ["global-home", "workspace", "repo"])
        self.assertEqual([source["precedence"] for source in sources], [0, 1, 2])
        self.assertTrue(sources[0]["project_external"])
        self.assertTrue(sources[1]["project_external"])
        self.assertFalse(sources[2]["project_external"])
        self.assertTrue(all("exists" in source for source in sources))
        self.assertTrue(all("readable" in source for source in sources))
        self.assertTrue(all(not rule["evidence_only"] for rule in governance["effective_file_rules"]))

    def test_path_boundary_check_rejects_sibling_prefixes(self):
        self.assertTrue(is_within_path(REPO_ROOT / "local", REPO_ROOT))
        self.assertFalse(is_within_path(REPO_ROOT.parent / f"{REPO_ROOT.name}-other", REPO_ROOT))

    def test_external_analysis_path_marks_project_sources_as_evidence_only(self):
        governance = build_governance_sources(REPO_ROOT, Path("C:/external-project"))

        self.assertEqual(governance["path_classification"]["scope_hint"], "external")
        applies = {source["scope"]: source["applies_to_path"] for source in governance["sources"]}
        self.assertTrue(applies["global-home"])
        self.assertFalse(applies["workspace"])
        self.assertFalse(applies["repo"])


if __name__ == "__main__":
    unittest.main()
