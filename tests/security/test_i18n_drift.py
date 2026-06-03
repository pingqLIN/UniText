import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "local" / "scripts" / "audit-i18n-drift.py"


def run_command(args, cwd=REPO_ROOT):
    return subprocess.run(
        args,
        cwd=cwd,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


def init_git_repo(repo: Path) -> None:
    run_command(["git", "-C", str(repo), "init", "-q"])
    run_command(["git", "-C", str(repo), "config", "user.email", "test@example.com"])
    run_command(["git", "-C", str(repo), "config", "user.name", "Test User"])


def commit_all(repo: Path, message: str) -> None:
    add_result = run_command(["git", "-C", str(repo), "add", "."])
    if add_result.returncode != 0:
        raise AssertionError(add_result.stdout + add_result.stderr)
    commit_result = run_command(["git", "-C", str(repo), "commit", "-m", message])
    if commit_result.returncode != 0:
        raise AssertionError(commit_result.stdout + commit_result.stderr)


def write_manifest(repo: Path) -> None:
    manifest = {
        "default_locale": "en",
        "locales": ["zh-TW"],
        "archived_locales": ["de"],
        "source_docs": ["README.md", "INDEX.md"],
        "required_source_docs": ["README.md"],
    }
    manifest_path = repo / "i18n" / "manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


class I18nDriftTests(unittest.TestCase):
    def test_cli_counts_required_and_optional_i18n_issues(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir) / "repo"
            repo.mkdir()
            init_git_repo(repo)
            write_manifest(repo)
            (repo / "README.md").write_text("# Source\n", encoding="utf-8")
            (repo / "INDEX.md").write_text("# Index\n", encoding="utf-8")
            commit_all(repo, "baseline")

            translated_readme = repo / "i18n" / "zh-TW" / "README.md"
            translated_readme.parent.mkdir(parents=True, exist_ok=True)
            translated_readme.write_text("# Translation\n", encoding="utf-8")

            result = run_command(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--repo-root",
                    str(repo),
                    "--format",
                    "json",
                    "--exit-zero",
                ]
            )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["locale_count"], 1)
        self.assertEqual(payload["archived_locale_count"], 1)
        self.assertEqual(payload["required_source_doc_count"], 1)
        self.assertEqual(payload["required_issues_found"], 1)
        self.assertEqual(payload["optional_issues_found"], 1)
        self.assertEqual(payload["issues_found"], 2)
        self.assertFalse(payload["ok"])

        by_locale = payload["by_locale"]["zh-TW"]
        self.assertEqual(by_locale["required_untracked"], 1)
        self.assertEqual(by_locale["optional_missing"], 1)
        statuses = {(issue["source_doc"], issue["status"], issue["required"]) for issue in payload["sample_issues"]}
        self.assertIn(("README.md", "untracked", True), statuses)
        self.assertIn(("INDEX.md", "missing", False), statuses)

    def test_cli_rejects_archived_locale_as_unknown_active_locale(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir) / "repo"
            repo.mkdir()
            init_git_repo(repo)
            write_manifest(repo)
            (repo / "README.md").write_text("# Source\n", encoding="utf-8")
            (repo / "INDEX.md").write_text("# Index\n", encoding="utf-8")
            commit_all(repo, "baseline")

            result = run_command(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--repo-root",
                    str(repo),
                    "--format",
                    "json",
                    "--locale",
                    "de",
                ]
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Unknown locales: de", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
