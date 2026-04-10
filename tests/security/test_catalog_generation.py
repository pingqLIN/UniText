import json
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def run_command(args, cwd=REPO_ROOT):
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, encoding="utf-8", errors="replace")


def get_powershell_executable():
    candidate = os.environ.get("POWERSHELL", "pwsh")
    if shutil.which(candidate):
        return candidate
    return None


class CatalogGenerationTests(unittest.TestCase):
    def test_catalog_exclusions_marks_microsoft_foundry_as_non_catalog_surface(self):
        policy = REPO_ROOT / "registry" / "catalog-exclusions.json"
        payload = json.loads(policy.read_text(encoding="utf-8"))
        entry = payload["skills"]["microsoft-foundry"]
        self.assertIn(entry["status"], {"stray", "excluded"})
        self.assertIn("excluded", entry["reason"].lower())

    def test_generate_index_entries_uses_explicit_root(self):
        powershell = get_powershell_executable()
        if powershell is None:
            self.skipTest("PowerShell executable not available")

        script = REPO_ROOT / "local" / "scripts" / "generate-index-entries.ps1"
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir) / "repo"
            skill_root = repo_root / "registry" / "skills" / "demo-skill"
            skill_root.mkdir(parents=True)
            (skill_root / "SKILL.md").write_text(
                textwrap.dedent(
                    """\
                    ---
                    name: demo-skill
                    description: Demo skill
                    ---

                    ## Usage
                    """
                ),
                encoding="utf-8",
            )

            command = f"& '{script}' -Root '{repo_root}' -AsJson"
            result = run_command([powershell, "-NoProfile", "-Command", command], cwd=REPO_ROOT)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload[0]["id"], "demo-skill")
        self.assertEqual(payload[0]["canonical_location"], "/registry/skills/demo-skill")
        self.assertEqual(payload[0]["source_of_truth"], "/registry/skills/demo-skill/SKILL.md")

    def test_generate_index_entries_respects_catalog_exclusions(self):
        powershell = get_powershell_executable()
        if powershell is None:
            self.skipTest("PowerShell executable not available")

        script = REPO_ROOT / "local" / "scripts" / "generate-index-entries.ps1"
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir) / "repo"
            skills_root = repo_root / "registry" / "skills"
            included_root = skills_root / "demo-skill"
            excluded_root = skills_root / "microsoft-foundry"
            included_root.mkdir(parents=True)
            excluded_root.mkdir(parents=True)
            (included_root / "SKILL.md").write_text(
                textwrap.dedent(
                    """\
                    ---
                    name: demo-skill
                    description: Demo skill
                    ---

                    ## Usage
                    """
                ),
                encoding="utf-8",
            )
            (excluded_root / "SKILL.md").write_text(
                textwrap.dedent(
                    """\
                    ---
                    name: microsoft-foundry
                    description: Stray item
                    ---

                    ## Usage
                    """
                ),
                encoding="utf-8",
            )
            exclusions_path = repo_root / "registry" / "catalog-exclusions.json"
            exclusions_path.parent.mkdir(parents=True, exist_ok=True)
            exclusions_path.write_text(
                json.dumps(
                    {
                        "skills": {
                            "microsoft-foundry": {
                                "status": "stray",
                                "reason": "Excluded from official catalog",
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            command = f"& '{script}' -Root '{repo_root}' -AsJson"
            result = run_command([powershell, "-NoProfile", "-Command", command], cwd=REPO_ROOT)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        ids = {entry["id"] for entry in payload}
        self.assertIn("demo-skill", ids)
        self.assertNotIn("microsoft-foundry", ids)


if __name__ == "__main__":
    unittest.main()
