import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
LIB_PATH = REPO_ROOT / "local" / "scripts" / "lib" / "workspace-sensitive-metadata.ps1"
VALIDATE_SCRIPT = REPO_ROOT / "local" / "scripts" / "validate-workspace-sensitive-metadata-rules.ps1"


def get_powershell_executable():
    candidate = os.environ.get("POWERSHELL", "pwsh")
    if shutil.which(candidate):
        return candidate
    return None


def quote_powershell_string(value: Path | str) -> str:
    return "'" + str(value).replace("'", "''") + "'"


def run_command(args, cwd=REPO_ROOT):
    return subprocess.run(
        args,
        cwd=cwd,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


def as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def write_rules(root: Path, overrides: dict | None = None) -> dict:
    rules = {
        "shared_surface_scope": ["README.md", "WORKSPACE_SENSITIVE_METADATA_RULES.json"],
        "path_rules": [
            {"label": "tracked operations state", "regex": "^ops/"},
        ],
        "content_patterns": [
            {
                "label": "machine-specific Windows path",
                "regex": "(?i)\\b[A-Z]:\\\\(Users|Services|Projects)\\\\",
                "skip_script_pattern_lines": False,
            }
        ],
        "self_test_cases": [
            {
                "label": "flag machine-specific path",
                "sample": "Prod runtime: Q:\\Services\\tb2-prod",
                "expected_labels": ["machine-specific Windows path"],
            }
        ],
    }
    if overrides:
        rules.update(overrides)
    (root / "WORKSPACE_SENSITIVE_METADATA_RULES.json").write_text(
        json.dumps(rules, indent=2) + "\n",
        encoding="utf-8",
    )
    return rules


class WorkspaceSensitiveMetadataTests(unittest.TestCase):
    def setUp(self):
        self.powershell = get_powershell_executable()
        if self.powershell is None:
            self.skipTest("PowerShell executable not available")

    def run_powershell_json(self, command: str):
        result = run_command([self.powershell, "-NoProfile", "-Command", command])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def test_current_repo_rules_validate_successfully(self):
        command = f"& {quote_powershell_string(VALIDATE_SCRIPT)} | ConvertTo-Json -Depth 8"
        payload = self.run_powershell_json(command)

        self.assertTrue(payload["ok"], payload)
        self.assertEqual(as_list(payload["errors"]), [])
        self.assertEqual(as_list(payload["missing_shared_surface_scope"]), [])
        self.assertGreater(payload["content_pattern_count"], 0)
        self.assertGreater(payload["self_test_case_count"], 0)

    def test_fixture_rules_validate_positive_contract(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "README.md").write_text("# Fixture\n", encoding="utf-8")
            write_rules(root)

            command = (
                f". {quote_powershell_string(LIB_PATH)}; "
                f"$rules = Get-WorkspaceSensitiveMetadataRules -RootPath {quote_powershell_string(root)}; "
                f"Test-WorkspaceSensitiveMetadataRules -Rules $rules -RootPath {quote_powershell_string(root)} -RequireScopeExists "
                "| ConvertTo-Json -Depth 8"
            )
            payload = self.run_powershell_json(command)

        self.assertTrue(payload["ok"], payload)
        self.assertEqual(as_list(payload["errors"]), [])

    def test_fixture_rules_report_invalid_and_missing_metadata(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "README.md").write_text("# Fixture\n", encoding="utf-8")
            write_rules(
                root,
                {
                    "shared_surface_scope": ["README.md", "MISSING.md"],
                    "path_rules": [
                        {"label": "duplicate", "regex": "^ops/"},
                        {"label": "duplicate", "regex": "["},
                    ],
                    "content_patterns": [
                        {
                            "label": "duplicate content",
                            "regex": "(?i)\\b[A-Z]:\\\\(Users|Services|Projects)\\\\",
                            "skip_script_pattern_lines": False,
                        },
                        {
                            "label": "duplicate content",
                            "regex": "[",
                        },
                    ],
                    "self_test_cases": [
                        {
                            "label": "intentional mismatch",
                            "sample": "Prod runtime: Q:\\Services\\tb2-prod",
                            "expected_labels": [],
                        }
                    ],
                },
            )

            command = (
                f". {quote_powershell_string(LIB_PATH)}; "
                f"$rules = Get-WorkspaceSensitiveMetadataRules -RootPath {quote_powershell_string(root)}; "
                f"Test-WorkspaceSensitiveMetadataRules -Rules $rules -RootPath {quote_powershell_string(root)} -RequireScopeExists "
                "| ConvertTo-Json -Depth 8"
            )
            payload = self.run_powershell_json(command)

        errors = "\n".join(as_list(payload["errors"]))
        self.assertFalse(payload["ok"], payload)
        self.assertIn("path_rules labels must be unique", errors)
        self.assertIn("content_patterns labels must be unique", errors)
        self.assertIn("Invalid path rule regex", errors)
        self.assertIn("Invalid content pattern regex", errors)
        self.assertIn("must define skip_script_pattern_lines", errors)
        self.assertIn("self_test_case 'intentional mismatch' mismatch", errors)
        self.assertIn("shared_surface_scope entry is missing from root: MISSING.md", errors)

    def test_content_scan_ignores_rule_self_test_samples_but_flags_regular_docs(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "README.md").write_text("Prod runtime: Q:\\Services\\tb2-prod\n", encoding="utf-8")
            write_rules(root)

            command = (
                f". {quote_powershell_string(LIB_PATH)}; "
                f"$rules = Get-WorkspaceSensitiveMetadataRules -RootPath {quote_powershell_string(root)}; "
                "$violations = @(Find-WorkspaceSensitiveContentViolations "
                f"-RootPath {quote_powershell_string(root)} "
                "-Files @('WORKSPACE_SENSITIVE_METADATA_RULES.json','README.md') "
                "-ContentPatterns $rules.content_patterns); "
                "[pscustomobject]@{ violations = @($violations) } | ConvertTo-Json -Depth 8"
            )
            payload = self.run_powershell_json(command)

        violations = as_list(payload["violations"])
        self.assertEqual(len(violations), 1, violations)
        self.assertEqual(violations[0]["path"], "README.md")
        self.assertEqual(violations[0]["label"], "machine-specific Windows path")


if __name__ == "__main__":
    unittest.main()
