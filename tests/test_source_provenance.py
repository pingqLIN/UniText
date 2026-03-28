import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILES = sorted((REPO_ROOT / "registry" / "skills").glob("*/SOURCE.yaml"))

REQUIRED_KEYS = {
    "registry_name",
    "source_type",
    "source_repo",
    "source_url",
    "source_path",
    "source_license",
    "imported_at",
    "source_revision",
    "license_evidence_path",
    "license_evidence_scope",
    "license_scope_note",
    "provenance_confidence",
    "import_method",
    "notes",
}


def parse_simple_yaml(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


class SourceProvenanceTests(unittest.TestCase):
    def test_active_skill_source_files_have_required_fields(self):
        self.assertGreater(len(SOURCE_FILES), 0)
        for source_file in SOURCE_FILES:
            with self.subTest(source_file=source_file):
                payload = parse_simple_yaml(source_file)
                self.assertEqual(set(payload), REQUIRED_KEYS)
                self.assertEqual(payload["registry_name"], source_file.parent.name)
                self.assertRegex(payload["source_revision"], r"^[0-9a-f]{40}$")

    def test_provenance_confidence_matches_license_scope(self):
        expected_by_scope = {
            "repository-root": "repo-license-relied-upon",
            "skill-subtree": "path-level-evidence-stronger",
            "path-ancestor": "path-level-evidence-stronger",
        }
        allowed_scopes = set(expected_by_scope) | {"not-found"}

        for source_file in SOURCE_FILES:
            with self.subTest(source_file=source_file):
                payload = parse_simple_yaml(source_file)
                scope = payload["license_evidence_scope"]
                confidence = payload["provenance_confidence"]

                self.assertIn(scope, allowed_scopes)
                if scope == "not-found":
                    self.assertEqual(confidence, "repo-license-relied-upon")
                    self.assertEqual(payload["license_evidence_path"], "")
                    continue

                self.assertEqual(confidence, expected_by_scope[scope])
                self.assertNotEqual(payload["license_evidence_path"], "")

    def test_license_scope_note_uses_standardized_wording(self):
        for source_file in SOURCE_FILES:
            with self.subTest(source_file=source_file):
                payload = parse_simple_yaml(source_file)
                note = payload["license_scope_note"]
                evidence_path = payload["license_evidence_path"]
                scope = payload["license_evidence_scope"]

                self.assertIn("source_path and source_revision recorded from the local source clone.", note)
                if scope == "skill-subtree":
                    self.assertIn(f"License evidence discovered at {evidence_path}; scope recorded as skill-subtree.", note)
                elif scope == "path-ancestor":
                    self.assertIn(
                        f"Ancestor-path license evidence discovered at {evidence_path}; scope recorded as path-ancestor.",
                        note,
                    )
                elif scope == "repository-root":
                    self.assertTrue(
                        note.startswith(f"Repository-root license evidence discovered at {evidence_path};")
                        or note.startswith(f"License evidence discovered at {evidence_path}; scope recorded as repository-root."),
                        msg=note,
                    )
                else:
                    self.assertIn("repo-level license relied upon", note)

    def test_refresh_script_uses_same_scope_to_confidence_mapping(self):
        script = (REPO_ROOT / "local" / "scripts" / "refresh-skills-registry.ps1").read_text(encoding="utf-8")
        self.assertIn('"skill-subtree" { "path-level-evidence-stronger" }', script)
        self.assertIn('"path-ancestor" { "path-level-evidence-stronger" }', script)
        self.assertIn('"repository-root" { "repo-license-relied-upon" }', script)
        self.assertIn('default { "repo-license-relied-upon" }', script)


if __name__ == "__main__":
    unittest.main()
