import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "local" / "scripts" / "report-release-hygiene.py"


def load_module():
    spec = importlib.util.spec_from_file_location("report_release_hygiene", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class ReleaseHygieneTests(unittest.TestCase):
    def test_classify_path_separates_release_scope_from_blockers(self):
        module = load_module()
        self.assertEqual(module.classify_path("README.md")[0], "release_scope")
        self.assertEqual(module.classify_path("local/scripts/bootstrap.py")[0], "release_scope")
        self.assertEqual(module.classify_path(".mcp.json")[0], "machine_specific")
        self.assertEqual(module.classify_path("i18n/de/README.md")[0], "translation_wave")
        self.assertEqual(
            module.classify_path("registry/skills/microsoft-foundry/SKILL.md")[0],
            "stray_registry",
        )
        self.assertEqual(module.classify_path("banner.psd")[0], "binary_asset")
        self.assertEqual(module.classify_path("SECURITY_REVIEW_ADVISORY.md")[0], "review_noise")
        self.assertEqual(module.classify_path("notes/todo.md")[0], "outside_release_scope")

    def test_build_report_counts_categories(self):
        module = load_module()
        entries = [
            module.Entry(status="M", path="README.md"),
            module.Entry(status=" M", path=".mcp.json"),
            module.Entry(status="??", path="i18n/de/README.md"),
            module.Entry(status="??", path="registry/skills/microsoft-foundry/SKILL.md"),
        ]
        report = module.build_report(entries)
        self.assertFalse(report["ok"])
        self.assertEqual(report["summary"]["release_scope"], 1)
        self.assertEqual(report["summary"]["blockers"], 3)
        self.assertEqual(report["summary"]["by_category"]["release_scope"], 1)
        self.assertEqual(report["summary"]["by_category"]["machine_specific"], 1)
        self.assertEqual(report["summary"]["by_category"]["translation_wave"], 1)
        self.assertEqual(report["summary"]["by_category"]["stray_registry"], 1)
        self.assertEqual(report["summary"]["acknowledged"], 0)

    def test_build_report_can_acknowledge_known_exclusions(self):
        module = load_module()
        entries = [
            module.Entry(status=" M", path=".mcp.json"),
            module.Entry(status="??", path="i18n/de/README.md"),
            module.Entry(status="??", path="registry/skills/microsoft-foundry/SKILL.md"),
        ]
        report = module.build_report(
            entries,
            allowed_categories={"translation_wave"},
            allowed_paths={".mcp.json"},
            allowed_prefixes=("registry/skills/microsoft-foundry/",),
        )
        self.assertTrue(report["ok"])
        self.assertEqual(report["summary"]["acknowledged"], 3)
        self.assertEqual(report["summary"]["blockers"], 0)

    def test_cli_reports_blockers_for_dirty_repo(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir) / "repo"
            repo_root.mkdir()
            subprocess.run(["git", "init", "-q"], cwd=repo_root, check=True)
            (repo_root / "README.md").write_text("demo\n", encoding="utf-8")
            (repo_root / ".mcp.json").write_text("{}\n", encoding="utf-8")
            (repo_root / "i18n").mkdir()
            (repo_root / "i18n" / "de").mkdir(parents=True, exist_ok=True)
            (repo_root / "i18n" / "de" / "README.md").write_text("demo\n", encoding="utf-8")
            (repo_root / "registry" / "skills" / "microsoft-foundry").mkdir(parents=True)
            (repo_root / "registry" / "skills" / "microsoft-foundry" / "SKILL.md").write_text(
                "demo\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--repo-root",
                    str(repo_root),
                    "--json",
                ],
                text=True,
                capture_output=True,
                encoding="utf-8",
                errors="replace",
            )

        self.assertNotEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["summary"]["release_scope"], 1)
        self.assertEqual(payload["summary"]["blockers"], 3)

    def test_format_markdown_includes_heading(self):
        module = load_module()
        report = module.build_report([module.Entry(status=" M", path="local/scripts/bootstrap.py")], REPO_ROOT)
        markdown = module.format_markdown(REPO_ROOT, report)
        self.assertIn("# Release Hygiene Report", markdown)
        self.assertIn("## Blockers", markdown)


if __name__ == "__main__":
    unittest.main()
