import json
import subprocess
import sys
import tempfile
import unittest
from importlib.util import find_spec
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "local" / "scripts" / "build-project-map.py"


@unittest.skipUnless(find_spec("playwright"), "playwright package is not installed")
class ProjectMapBrowserSmokeTests(unittest.TestCase):
    def test_generated_project_map_pages_render_without_browser_errors(self):
        from playwright.sync_api import Error as PlaywrightError
        from playwright.sync_api import sync_playwright

        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run(
                [sys.executable, str(SCRIPT_PATH), "--output-dir", temp_dir],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                encoding="utf-8",
                errors="replace",
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            summary = json.loads(result.stdout)

            with sync_playwright() as playwright:
                try:
                    browser = playwright.chromium.launch(headless=True)
                except PlaywrightError as error:
                    self.skipTest(f"chromium browser is unavailable: {error}")

                try:
                    for path_key in ("html_path", "share_html_path"):
                        page = browser.new_page(viewport={"width": 1280, "height": 900})
                        errors: list[str] = []
                        page.on(
                            "console",
                            lambda message: errors.append(message.text)
                            if message.type == "error"
                            else None,
                        )
                        page.on("pageerror", lambda error: errors.append(str(error)))
                        page.goto(Path(summary[path_key]).resolve().as_uri(), wait_until="networkidle")

                        self.assertEqual(page.title(), "UniText 執行面專案地圖")
                        self.assertGreater(page.locator("svg").count(), 0)
                        self.assertIn("UniText", page.locator("body").inner_text(timeout=5000))
                        node_locator = page.locator("#map [data-map-node]")
                        self.assertGreater(node_locator.count(), 1)
                        target_node_id = node_locator.nth(1).get_attribute("data-map-node")
                        self.assertIsNotNone(target_node_id)
                        node_locator.nth(1).click()
                        page.wait_for_function(
                            """nodeId => {
                                const node = document.querySelector(`#map [data-map-node="${CSS.escape(nodeId)}"]`);
                                const rect = node?.querySelector("rect");
                                return rect?.getAttribute("stroke-width") === "2.1";
                            }""",
                            arg=target_node_id,
                        )
                        self.assertEqual(errors, [], f"{path_key} browser errors: {errors}")
                        page.close()
                finally:
                    browser.close()


if __name__ == "__main__":
    unittest.main()
