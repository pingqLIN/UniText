import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "local" / "scripts" / "report-i18n-wave.py"


def load_module():
    spec = importlib.util.spec_from_file_location("report_i18n_wave", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class I18nWaveTests(unittest.TestCase):
    def test_classify_paths_detects_eol_only_and_substantive(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir) / "repo"
            repo.mkdir()
            baseline = repo / "i18n" / "zh-TW" / "README.md"
            baseline.parent.mkdir(parents=True)
            second = repo / "i18n" / "zh-TW" / "INDEX.md"
            second.parent.mkdir(parents=True, exist_ok=True)
            baseline.write_bytes(b"line one\nline two\n")
            second.write_text("line one\nline two\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "init", "-q"], check=True)
            subprocess.run(["git", "-C", str(repo), "config", "user.email", "test@example.com"], check=True)
            subprocess.run(["git", "-C", str(repo), "config", "user.name", "Test User"], check=True)
            subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-m", "init"], check=True, capture_output=True)

            baseline.write_bytes(b"line one\r\nline two\r\n")
            second.write_text("line one\nchanged text\n", encoding="utf-8")

            report = module.classify_paths(
                repo,
                [
                    {"status": " M", "path": "i18n/zh-TW/README.md"},
                    {"status": " M", "path": "i18n/zh-TW/INDEX.md"},
                ],
            )
            self.assertEqual(report["summary"]["eol_only"], 1)
            self.assertEqual(report["summary"]["substantive"], 1)
            self.assertFalse(report["safe_to_split"])

    def test_cli_reports_safe_split_for_eol_only_changes(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir) / "repo"
            repo.mkdir()
            file_path = repo / "i18n" / "de" / "README.md"
            file_path.parent.mkdir(parents=True)
            file_path.write_bytes(b"alpha\nbeta\n")
            subprocess.run(["git", "-C", str(repo), "init", "-q"], check=True)
            subprocess.run(["git", "-C", str(repo), "config", "user.email", "test@example.com"], check=True)
            subprocess.run(["git", "-C", str(repo), "config", "user.name", "Test User"], check=True)
            subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-m", "init"], check=True, capture_output=True)

            file_path.write_bytes(b"alpha\r\nbeta\r\n")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--repo-root", str(repo), "--json"],
                text=True,
                capture_output=True,
                encoding="utf-8",
                errors="replace",
            )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["safe_to_split"])
        self.assertEqual(payload["summary"]["eol_only"], 1)
        self.assertEqual(payload["summary"]["substantive"], 0)


if __name__ == "__main__":
    unittest.main()
