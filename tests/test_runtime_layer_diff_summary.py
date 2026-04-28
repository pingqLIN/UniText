import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "local" / "scripts" / "build-runtime-layer.py"


def load_runtime_builder_module():
    module_name = "unitext_build_runtime_layer"
    spec = importlib.util.spec_from_file_location(module_name, SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load script module from {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def run_command(args, cwd=REPO_ROOT):
    return subprocess.run(
        args,
        cwd=cwd,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


class RuntimeLayerDiffSummaryTests(unittest.TestCase):
    def test_write_text_uses_lf_newlines_on_windows(self):
        builder = load_runtime_builder_module()

        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "nested" / "file.md"
            builder.write_text(path, "first\nsecond\r\n")
            raw = path.read_bytes()

        self.assertEqual(raw, b"first\nsecond\n")

    def test_compare_runtime_trees_classifies_payload_and_catalog_drift(self):
        builder = load_runtime_builder_module()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            generated = root / "generated"
            tracked = root / "tracked"
            generated.mkdir()
            tracked.mkdir()

            (generated / "skills" / "env").mkdir(parents=True)
            (tracked / "skills" / "env").mkdir(parents=True)
            (generated / "skills" / "env" / "SKILL.md").write_text("new\n", encoding="utf-8")
            (tracked / "skills" / "env" / "SKILL.md").write_text("old\n", encoding="utf-8")

            (generated / "catalog.json").write_text('{"entries":[]}\n', encoding="utf-8")
            (tracked / "catalog.json").write_text('{"entries":[1]}\n', encoding="utf-8")

            (tracked / "workflow" / "old-flow").mkdir(parents=True)
            (tracked / "workflow" / "old-flow" / "WORKFLOW.md").write_text("stale\n", encoding="utf-8")

            (generated / "agents" / "registry-curator").mkdir(parents=True)
            (tracked / "agents" / "registry-curator").mkdir(parents=True)
            (generated / "agents" / "registry-curator" / "AGENT.md").write_bytes(b"one\ntwo\n")
            (tracked / "agents" / "registry-curator" / "AGENT.md").write_bytes(b"one\r\ntwo\r\n")

            (tracked / "START.md").write_text("manual runtime entry\n", encoding="utf-8")
            (tracked / "skills" / ".system").mkdir(parents=True)
            (tracked / "skills" / ".system" / "local.md").write_text("local overlay\n", encoding="utf-8")

            summary = builder.compare_runtime_trees(generated, tracked)

        self.assertEqual(summary["status"], "drift")
        self.assertEqual(summary["changed_by_generator"]["count"], 3)
        self.assertEqual(summary["content_changed_by_generator"]["count"], 2)
        self.assertEqual(summary["line_ending_only_drift"]["count"], 1)
        self.assertEqual(summary["stale_tracked_runtime_files"]["count"], 1)
        self.assertEqual(summary["payload_drift"]["count"], 3)
        self.assertEqual(summary["blocking_payload_drift"]["count"], 2)
        self.assertEqual(summary["payload_content_drift"]["count"], 2)
        self.assertEqual(summary["payload_line_ending_only_drift"]["count"], 1)
        self.assertEqual(summary["catalog_drift"]["count"], 1)
        self.assertFalse(summary["write_gate"]["routine_write_allowed"])
        self.assertTrue(summary["write_gate"]["requires_review"])
        self.assertNotIn("START.md", summary["stale_tracked_runtime_files"]["sample"])
        self.assertNotIn("skills/.system/local.md", summary["stale_tracked_runtime_files"]["sample"])

    def test_output_dir_dry_run_emits_diff_summary_and_write_gate(self):
        runtime_root = REPO_ROOT / "runtime"
        runtime_root.mkdir(exist_ok=True)

        with tempfile.TemporaryDirectory(dir=runtime_root, prefix=".runtime-dryrun-test-") as temp_dir:
            result = run_command([sys.executable, str(SCRIPT_PATH), "--output-dir", temp_dir])

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["dry_run"])
        self.assertEqual(payload["runtime_root"], temp_dir)
        self.assertEqual(payload["output_dir_scope"], "repository-relative")
        self.assertIn("diff_summary", payload)
        self.assertEqual(payload["diff_summary"]["compared_against"], str(REPO_ROOT / "runtime"))
        self.assertIn("write_gate", payload["diff_summary"])
        self.assertIn("routine_write_allowed", payload["diff_summary"]["write_gate"])

    def test_output_dir_dry_run_uses_runtime_logical_link_paths(self):
        runtime_root = REPO_ROOT / "runtime"
        runtime_root.mkdir(exist_ok=True)

        with tempfile.TemporaryDirectory(dir=runtime_root, prefix=".runtime-dryrun-test-") as temp_dir:
            result = run_command([sys.executable, str(SCRIPT_PATH), "--output-dir", temp_dir])
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

            runtime_skill = Path(temp_dir) / "skills" / "cloudflare-governance" / "SKILL.md"
            content = runtime_skill.read_text(encoding="utf-8")

        self.assertIn(
            "[cloudflare-zerotrust-device](../../../registry/skills/cloudflare-zerotrust-device/SKILL.md)",
            content,
        )
        self.assertNotIn(
            "[cloudflare-zerotrust-device](../../../../registry/skills/cloudflare-zerotrust-device/SKILL.md)",
            content,
        )

    def test_compare_runtime_trees_allows_line_ending_only_payload_drift(self):
        builder = load_runtime_builder_module()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            generated = root / "generated"
            tracked = root / "tracked"
            generated.mkdir()
            tracked.mkdir()

            (generated / "skills" / "env").mkdir(parents=True)
            (tracked / "skills" / "env").mkdir(parents=True)
            (generated / "skills" / "env" / "SKILL.md").write_bytes(b"one\ntwo\n")
            (tracked / "skills" / "env" / "SKILL.md").write_bytes(b"one\r\ntwo\r\n")

            (generated / "catalog.json").write_text('{"entries":[]}\n', encoding="utf-8")
            (tracked / "catalog.json").write_text('{"entries":[]}\n', encoding="utf-8")

            summary = builder.compare_runtime_trees(generated, tracked)

        self.assertEqual(summary["status"], "drift")
        self.assertEqual(summary["payload_drift"]["count"], 1)
        self.assertEqual(summary["blocking_payload_drift"]["count"], 0)
        self.assertEqual(summary["payload_content_drift"]["count"], 0)
        self.assertEqual(summary["payload_line_ending_only_drift"]["count"], 1)
        self.assertTrue(summary["write_gate"]["routine_write_allowed"])
        self.assertFalse(summary["write_gate"]["requires_review"])


if __name__ == "__main__":
    unittest.main()
