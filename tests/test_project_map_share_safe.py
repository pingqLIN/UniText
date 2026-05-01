import importlib.util
import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "web" / "project-map-ui" / "build-project-map.py"
RUNTIME_PATH = REPO_ROOT / "web" / "project-map-ui" / "project-map-runtime.js"
TEMPLATE_PATH = REPO_ROOT / "web" / "project-map-ui" / "project-map-template.html"


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

    def test_interactive_payload_includes_global_workspace_and_repo_sources(self):
        payload = BUILD_PROJECT_MAP.build_payload(REPO_ROOT)
        sources = payload["governance"]["sources"]
        scopes = [source["scope"] for source in sources]

        self.assertEqual(scopes, ["global-home", "workspace", "repo"])
        self.assertTrue(sources[0]["project_external"])
        self.assertTrue(sources[1]["project_external"])
        self.assertFalse(sources[2]["project_external"])
        self.assertIn(".codex", sources[0]["path"])
        self.assertEqual(payload["governance"]["effective_hard_rules"][0]["rule_category"], "hard_rule")

    def test_share_safe_html_omits_native_paths_and_governance_sources(self):
        payload = BUILD_PROJECT_MAP.build_payload(REPO_ROOT)
        share_html = BUILD_PROJECT_MAP.render_html(payload, page_mode="share-safe")

        self.assertIn('"page_mode": "share-safe"', share_html)
        self.assertIn('"governance_resolver": false', share_html)
        self.assertIn("window.AGENT_GOVERNANCE_POLICY = null;", share_html)
        self.assertNotIn("Q:\\\\UniText", share_html)
        self.assertNotIn("Q:\\\\AGENTS.md", share_html)
        self.assertNotIn("C:\\\\Users\\\\miles", share_html)
        self.assertNotIn(".codex\\\\AGENTS.md", share_html)
        self.assertNotIn('"effective_file_rules"', share_html)
        self.assertNotIn('id="export-card"', share_html)
        self.assertNotIn('id="workspace-tab-governance"', share_html)
        self.assertNotIn('id="workspace-panel-governance"', share_html)
        self.assertNotIn('id="maintenance-controls"', share_html)
        self.assertNotIn('class="governance-panel"', share_html)
        self.assertNotIn('id="governance-resolve"', share_html)
        self.assertNotIn('id="governance-write"', share_html)
        self.assertNotIn('id="governance-funnel"', share_html)

    def test_interactive_html_keeps_operator_surface_data(self):
        payload = BUILD_PROJECT_MAP.build_payload(REPO_ROOT)
        interactive_html = BUILD_PROJECT_MAP.render_html(payload, page_mode="interactive")

        self.assertIn("Q:\\\\UniText", interactive_html)
        self.assertIn('"effective_file_rules"', interactive_html)
        self.assertIn("window.AGENT_GOVERNANCE_POLICY = {", interactive_html)
        self.assertIn('"governance_resolver": true', interactive_html)
        self.assertIn('id="export-card"', interactive_html)
        self.assertIn('id="maintenance-controls"', interactive_html)
        self.assertIn('class="governance-panel"', interactive_html)
        self.assertIn('id="masthead-toggle"', interactive_html)
        self.assertIn('id="map-fit"', interactive_html)
        self.assertIn('id="governance-analysis-path"', interactive_html)
        self.assertIn('id="governance-funnel"', interactive_html)
        self.assertNotIn('id="masthead-quick-filters"', interactive_html)
        self.assertNotIn('class="workspace-preview-rail"', interactive_html)

    def test_runtime_contains_latched_masthead_drag_pan_and_expanded_text_scale(self):
        runtime_source = RUNTIME_PATH.read_text(encoding="utf-8")

        self.assertIn("autoCollapsedLatch", runtime_source)
        self.assertIn("setupMapDragPan", runtime_source)
        self.assertIn("suppressNextMapClick", runtime_source)
        self.assertIn('TEXT_SCALE_ORDER = ["xs", "sm", "md", "lg", "xl"]', runtime_source)
        self.assertIn("getConfiguredGovernanceSources", runtime_source)
        self.assertIn("manual-path-only", runtime_source)
        self.assertIn("Configured source is manual, unreadable, or path-mismatched", runtime_source)
        self.assertIn("unverified_path_classification", runtime_source)

    def test_tour_first_visit_prompts_without_auto_opening_and_highlights_operation_focus(self):
        runtime_source = RUNTIME_PATH.read_text(encoding="utf-8")
        template_source = TEMPLATE_PATH.read_text(encoding="utf-8")

        self.assertIn('selector: ".masthead-aside"', runtime_source)
        self.assertIn("syncTourEntryCue", runtime_source)
        self.assertIn('document.body.classList.toggle("tour-entry-cue", shouldPrompt)', runtime_source)
        self.assertNotIn("if (!state.tourOpen) startTour();", runtime_source)
        self.assertIn("tour-cta-cue", template_source)
        self.assertIn("body.tour-active .masthead-aside", template_source)
        self.assertIn("--tour-entry-glow", template_source)

    def test_handoff_payload_describes_surface_contract(self):
        payload = BUILD_PROJECT_MAP.build_payload(REPO_ROOT)
        handoff_payload = BUILD_PROJECT_MAP.build_handoff_payload(payload)
        rendered_handoff = json.dumps(handoff_payload, ensure_ascii=False)

        self.assertFalse(handoff_payload["surface_contract"]["share_safe"]["browser_scan"])
        self.assertFalse(handoff_payload["surface_contract"]["share_safe"]["governance_resolver"])
        self.assertFalse(handoff_payload["surface_contract"]["share_safe"]["native_repo_paths"])
        self.assertIn("native repo path", handoff_payload["handoff_notes"][1])
        self.assertNotIn("C:\\Users\\miles", rendered_handoff)
        self.assertNotIn(".codex\\AGENTS.md", rendered_handoff)

    def test_runtime_marks_static_export_artifacts_as_stale_after_browser_refresh(self):
        runtime_source = RUNTIME_PATH.read_text(encoding="utf-8")

        self.assertIn('state.lastRefreshSource !== "bootstrap"', runtime_source)
        self.assertIn("Static artifacts:", runtime_source)
        self.assertIn("python local/scripts/build-project-map.py", runtime_source)

    def test_runtime_governance_note_points_to_current_policy_file(self):
        runtime_source = RUNTIME_PATH.read_text(encoding="utf-8")

        self.assertIn("local/config/agent-governance-layers.json", runtime_source)
        self.assertNotIn("local/config/agent-file-governance-rules.json", runtime_source)


if __name__ == "__main__":
    unittest.main()
