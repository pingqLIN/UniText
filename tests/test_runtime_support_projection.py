import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "local" / "scripts" / "build-runtime-layer.py"
SKIPPED_LINK_PREFIXES = ("#", "http://", "https://", "mailto:", "file:", "vscode:")


def load_runtime_builder_module():
    module_name = "unitext_build_runtime_layer_support_projection"
    spec = importlib.util.spec_from_file_location(module_name, SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load script module from {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def runtime_markdown_link_targets(builder, markdown_file: Path):
    content = markdown_file.read_text(encoding="utf-8")
    for match in builder.LINK_PATTERN.finditer(content):
        raw_target = match.group(2).strip()
        if not raw_target or raw_target.startswith(SKIPPED_LINK_PREFIXES):
            continue

        target = raw_target.split("#", 1)[0]
        if not target:
            continue

        yield (markdown_file.parent / target).resolve()


class RuntimeSupportProjectionTests(unittest.TestCase):
    def test_skill_support_projection_copies_scripts_and_json_but_keeps_markdown_rendering(self):
        builder = load_runtime_builder_module()

        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir)
            skill = repo / "registry" / "skills" / "demo-skill"
            (skill / "references").mkdir(parents=True)
            (skill / "scripts").mkdir()
            (skill / "assets" / "nested").mkdir(parents=True)
            (skill / ".cache").mkdir()
            (skill / "TEMP").mkdir()

            (skill / "SKILL.md").write_text(
                "\n".join(
                    [
                        "---",
                        "name: demo-skill",
                        "runtime_support_files: true",
                        "---",
                        "# Demo",
                        "",
                        "[Guide](references/guide.md)",
                        "[Script](scripts/run.ps1)",
                        "[Config](assets/nested/config.json)",
                    ]
                ),
                encoding="utf-8",
            )
            (skill / "references" / "guide.md").write_text(
                "# Guide\n\n[Config](../assets/nested/config.json)\n",
                encoding="utf-8",
            )
            (skill / "scripts" / "run.ps1").write_text("Write-Output 'ok'\n", encoding="utf-8")
            (skill / "assets" / "nested" / "config.json").write_text('{"ok": true}\n', encoding="utf-8")
            (skill / "desktop.ini").write_text("metadata\n", encoding="utf-8")
            (skill / ".cache" / "state.json").write_text('{"state": true}\n', encoding="utf-8")
            (skill / "TEMP" / "state.json").write_text('{"state": true}\n', encoding="utf-8")
            (skill / "debug.LOG").write_text("debug\n", encoding="utf-8")
            (skill / ".cache" / "note.md").write_text("# Hidden note\n", encoding="utf-8")

            runtime = repo / "runtime"
            entries = builder.build_skill_wrappers(repo, runtime, [])

            runtime_skill = runtime / "skills" / "demo-skill"
            runtime_entrypoint = runtime_skill / "SKILL.md"
            runtime_guide = runtime_skill / "references" / "guide.md"

            self.assertEqual(len(entries), 1)
            self.assertTrue((runtime_skill / "scripts" / "run.ps1").is_file())
            self.assertTrue((runtime_skill / "assets" / "nested" / "config.json").is_file())
            self.assertFalse((runtime_skill / "desktop.ini").exists())
            self.assertFalse((runtime_skill / ".cache" / "state.json").exists())
            self.assertFalse((runtime_skill / "TEMP" / "state.json").exists())
            self.assertFalse((runtime_skill / "debug.LOG").exists())
            self.assertFalse((runtime_skill / ".cache" / "note.md").exists())

            self.assertIn("runtime_projection: true", runtime_entrypoint.read_text(encoding="utf-8"))
            guide_content = runtime_guide.read_text(encoding="utf-8")
            self.assertIn("runtime_projection: true", guide_content)
            self.assertIn("[Config](../assets/nested/config.json)", guide_content)

    def test_skill_support_projection_accepts_metadata_runtime_support_files(self):
        builder = load_runtime_builder_module()

        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir)
            skill = repo / "registry" / "skills" / "demo-skill"
            (skill / "scripts").mkdir(parents=True)

            (skill / "SKILL.md").write_text(
                "\n".join(
                    [
                        "---",
                        "name: demo-skill",
                        "description: Demo skill.",
                        "metadata:",
                        "  runtime_support_files: true",
                        "  status: metadata-only",
                        "---",
                        "# Demo",
                        "",
                        "[Script](scripts/run.ps1)",
                    ]
                ),
                encoding="utf-8",
            )
            (skill / "scripts" / "run.ps1").write_text("Write-Output 'ok'\n", encoding="utf-8")

            runtime = repo / "runtime"
            entries = builder.build_skill_wrappers(repo, runtime, [])

            runtime_skill = runtime / "skills" / "demo-skill"
            self.assertTrue((runtime_skill / "scripts" / "run.ps1").is_file())
            self.assertIsNone(entries[0].status)

    def test_runtime_markdown_relative_links_resolve_to_projected_files(self):
        builder = load_runtime_builder_module()

        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir)
            skill = repo / "registry" / "skills" / "demo-skill"
            (skill / "references").mkdir(parents=True)
            (skill / "scripts").mkdir()
            (skill / "assets" / "nested").mkdir(parents=True)

            (skill / "SKILL.md").write_text(
                "\n".join(
                    [
                        "---",
                        "runtime_support_files: true",
                        "---",
                        "# Demo",
                        "",
                        "[Guide](references/guide.md)",
                        "[Script](scripts/run.ps1)",
                        "[Config](assets/nested/config.json)",
                        "[External](https://example.test/docs)",
                        "[Anchor](#local-section)",
                    ]
                ),
                encoding="utf-8",
            )
            (skill / "references" / "guide.md").write_text(
                "\n".join(
                    [
                        "# Guide",
                        "",
                        "[Entrypoint](../SKILL.md)",
                        "[Script](../scripts/run.ps1)",
                        "[Config](../assets/nested/config.json)",
                    ]
                ),
                encoding="utf-8",
            )
            (skill / "scripts" / "run.ps1").write_text("Write-Output 'ok'\n", encoding="utf-8")
            (skill / "assets" / "nested" / "config.json").write_text('{"ok": true}\n', encoding="utf-8")

            runtime = repo / "runtime"
            builder.build_skill_wrappers(repo, runtime, [])

            runtime_skill = runtime / "skills" / "demo-skill"
            missing_targets = []
            for markdown_file in sorted(runtime_skill.rglob("*.md")):
                for target in runtime_markdown_link_targets(builder, markdown_file):
                    if not target.exists():
                        missing_targets.append(os.path.relpath(target, runtime_skill))

            self.assertEqual(missing_targets, [])

    def test_skill_runtime_rebuild_preserves_hidden_local_overlay(self):
        builder = load_runtime_builder_module()

        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir)
            skill = repo / "registry" / "skills" / "demo-skill"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("# Demo\n", encoding="utf-8")

            runtime_skills = repo / "runtime" / "skills"
            (runtime_skills / ".system" / "local").mkdir(parents=True)
            (runtime_skills / ".system" / "local" / "SKILL.md").write_text("# Local\n", encoding="utf-8")
            (runtime_skills / "old-skill").mkdir()
            (runtime_skills / "old-skill" / "SKILL.md").write_text("# Old\n", encoding="utf-8")

            builder.build_skill_wrappers(repo, repo / "runtime", [])

            self.assertTrue((runtime_skills / ".system" / "local" / "SKILL.md").is_file())
            self.assertFalse((runtime_skills / "old-skill").exists())
            self.assertTrue((runtime_skills / "demo-skill" / "SKILL.md").is_file())

    def test_runtime_parity_ignores_untracked_local_runtime_overlay(self):
        builder = load_runtime_builder_module()

        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir)
            runtime = repo / "runtime"
            generated = repo / ".runtime-dryrun"
            tracked_skill = runtime / "skills" / "demo-skill"
            generated_skill = generated / "skills" / "demo-skill"
            local_overlay = runtime / "skills" / "source-command-zh"
            tracked_skill.mkdir(parents=True)
            generated_skill.mkdir(parents=True)
            local_overlay.mkdir(parents=True)

            (tracked_skill / "SKILL.md").write_text("# Demo\n", encoding="utf-8", newline="\n")
            (generated_skill / "SKILL.md").write_text("# Demo\n", encoding="utf-8", newline="\n")
            (local_overlay / "SKILL.md").write_text("# Local only\n", encoding="utf-8", newline="\n")

            subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
            subprocess.run(
                ["git", "add", "runtime/skills/demo-skill/SKILL.md"],
                cwd=repo,
                check=True,
                capture_output=True,
            )

            summary = builder.compare_runtime_trees(generated, runtime)

            self.assertEqual(summary["status"], "clean")
            self.assertEqual(summary["stale_tracked_runtime_files"]["count"], 0)


if __name__ == "__main__":
    unittest.main()
