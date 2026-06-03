import importlib.util
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_script_module(script_name: str):
    script = REPO_ROOT / "local" / "scripts" / script_name
    module_name = f"unitext_{script.stem.replace('-', '_')}"
    spec = importlib.util.spec_from_file_location(module_name, script)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load script module from {script}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_skill(root: Path, name: str, body: str = "# Skill\n") -> None:
    skill = root / name
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(body, encoding="utf-8")


class RuntimeBundleHiddenEntryTests(unittest.TestCase):
    def test_system_runtime_overlay_is_gitignored(self):
        ignore_lines = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()

        self.assertIn("runtime/skills/.system/", ignore_lines)

    def test_verify_ignores_hidden_runtime_source_entries(self):
        verify = load_script_module("verify-bootstrap.py")

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            runtime_skills = root / "runtime-skills"
            target = root / "codex-skills"
            runtime_skills.mkdir()
            target.mkdir()
            write_skill(runtime_skills, "env")
            write_skill(target, "env")
            write_skill(runtime_skills, ".system", "# system\n")

            contains_baseline, mode, missing, _, aliases = verify.codex_target_contains_runtime_baseline(
                target,
                runtime_skills,
            )

            self.assertTrue(contains_baseline)
            self.assertEqual(mode, "bundle")
            self.assertEqual(missing, [])
            self.assertEqual(aliases, [])

    def test_register_materialized_bundle_ignores_hidden_source_entries(self):
        register = load_script_module("register-codex-skills.py")

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            runtime_skills = root / "runtime-skills"
            target = root / "codex-skills"
            runtime_skills.mkdir()
            target.mkdir()
            write_skill(runtime_skills, "env")
            write_skill(runtime_skills, ".system", "# source system\n")
            write_skill(target, ".system", "# target system\n")

            action, aliases = register.ensure_materialized_runtime_bundle(runtime_skills, target)

            self.assertEqual(action, "refreshed-existing-bundle")
            self.assertEqual(aliases, [])
            self.assertTrue((target / "env" / "SKILL.md").exists())
            self.assertEqual((target / ".system" / "SKILL.md").read_text(encoding="utf-8"), "# target system\n")

    def test_register_missing_target_lists_as_empty(self):
        register = load_script_module("register-codex-skills.py")

        with tempfile.TemporaryDirectory() as temp_dir:
            missing = Path(temp_dir) / "missing-skills"

            self.assertEqual(register.list_skill_names(missing), [])


if __name__ == "__main__":
    unittest.main()
