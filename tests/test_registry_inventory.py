import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / "registry" / "skills"


class RegistryInventoryTests(unittest.TestCase):
    def test_review_shortlist_skills_exist(self):
        expected = {
            "pdf",
            "docx",
            "xlsx",
            "pptx",
            "mcp-builder",
            "skill-creator",
            "webapp-testing",
            "doc-coauthoring",
            "frontend-design",
            "web-artifacts-builder",
            "internal-comms",
            "theme-factory",
        }
        actual = {path.name for path in SKILLS_ROOT.iterdir() if path.is_dir()}
        self.assertTrue(expected.issubset(actual))

    def test_expanded_skill_families_exist(self):
        expected = {
            "cloudflare",
            "cloudflare-governance",
            "microsoft-foundry",
            "azure-prepare",
            "azure-validate",
            "azure-cost",
            "azure-resource-lookup",
            "entra-app-registration",
        }
        actual = {path.name for path in SKILLS_ROOT.iterdir() if path.is_dir()}
        self.assertTrue(expected.issubset(actual))

    def test_skill_inventory_has_not_collapsed_below_current_baseline(self):
        actual = [path for path in SKILLS_ROOT.iterdir() if path.is_dir()]
        self.assertGreaterEqual(len(actual), 44)


if __name__ == "__main__":
    unittest.main()
