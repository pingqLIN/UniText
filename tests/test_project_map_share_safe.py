import importlib.util
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "local" / "scripts" / "build-project-map.py"
RUNTIME_PATH = REPO_ROOT / "local" / "scripts" / "project-map-runtime.js"


def load_builder_module():
    spec = importlib.util.spec_from_file_location("build_project_map", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


BUILD_PROJECT_MAP = load_builder_module()


class ProjectMapShareSafeTests(unittest.TestCase):
    def test_share_safe_payload_strips_operator_only_metadata(self):
        payload = BUILD_PROJECT_MAP.build_payload(REPO_ROOT)
        share_payload = BUILD_PROJECT_MAP.build_page_payload(payload, "share-safe")

        self.assertEqual(share_payload["meta"]["page_mode"], "share-safe")
        self.assertNotIn("repo_root_native", share_payload["meta"])
        self.assertEqual(
            share_payload["capabilities"],
            {
                "browser_scan": False,
                "governance_resolver": False,
                "native_repo_paths": False,
            },
        )
        self.assertNotIn("governance", share_payload)

    def test_share_safe_html_omits_native_paths_and_governance_sources(self):
        payload = BUILD_PROJECT_MAP.build_payload(REPO_ROOT)
        share_html = BUILD_PROJECT_MAP.render_html(payload, page_mode="share-safe")

        self.assertIn('"page_mode": "share-safe"', share_html)
        self.assertIn('"governance_resolver": false', share_html)
        self.assertIn("window.AGENT_GOVERNANCE_POLICY = null;", share_html)
        self.assertNotIn("Q:\\\\UniText", share_html)
        self.assertNotIn("Q:\\\\AGENTS.md", share_html)
        self.assertNotIn('"effective_file_rules"', share_html)
        self.assertNotIn("Maintenance Controls", share_html)
        self.assertNotIn("Governance Layering", share_html)
        self.assertNotIn('id="export-card"', share_html)

    def test_interactive_html_keeps_operator_surface_data(self):
        payload = BUILD_PROJECT_MAP.build_payload(REPO_ROOT)
        interactive_html = BUILD_PROJECT_MAP.render_html(payload, page_mode="interactive")

        self.assertIn("Q:\\\\UniText", interactive_html)
        self.assertIn('"effective_file_rules"', interactive_html)
        self.assertIn("window.AGENT_GOVERNANCE_POLICY = {", interactive_html)
        self.assertIn('"governance_resolver": true', interactive_html)
        self.assertIn("Maintenance Controls", interactive_html)
        self.assertIn("Governance Layering", interactive_html)

    def test_handoff_payload_describes_surface_contract(self):
        payload = BUILD_PROJECT_MAP.build_payload(REPO_ROOT)
        handoff_payload = BUILD_PROJECT_MAP.build_handoff_payload(payload)

        self.assertFalse(handoff_payload["surface_contract"]["share_safe"]["browser_scan"])
        self.assertFalse(handoff_payload["surface_contract"]["share_safe"]["governance_resolver"])
        self.assertFalse(handoff_payload["surface_contract"]["share_safe"]["native_repo_paths"])
        self.assertIn("native repo path", handoff_payload["handoff_notes"][1])

    def test_runtime_marks_static_export_artifacts_as_stale_after_browser_refresh(self):
        runtime_source = RUNTIME_PATH.read_text(encoding="utf-8")

        self.assertIn('state.lastRefreshSource !== "bootstrap"', runtime_source)
        self.assertIn("Static artifacts:", runtime_source)
        self.assertIn("python local/scripts/build-project-map.py", runtime_source)


if __name__ == "__main__":
    unittest.main()
