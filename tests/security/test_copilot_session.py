import importlib.util
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "local" / "scripts" / "verify-copilot-session.py"


def load_module():
    spec = importlib.util.spec_from_file_location("verify_copilot_session", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class CopilotSessionTests(unittest.TestCase):
    def test_extract_json_object_handles_fenced_payload(self):
        module = load_module()
        payload = module.extract_json_object('```json\n{"ok": true}\n```')
        self.assertEqual(payload, {"ok": True})

    def test_summarize_events_collects_mcp_and_final_payload(self):
        module = load_module()
        events = [
            {
                "type": "session.mcp_servers_loaded",
                "data": {"servers": [{"name": "unitext-registry", "status": "connected"}]},
            },
            {
                "type": "assistant.message",
                "data": {"content": '```json\n{"registry_roots":["/registry/skills"]}\n```'},
            },
            {
                "type": "result",
                "exitCode": 0,
            },
        ]
        summary = module.summarize_events(events)
        self.assertTrue(summary["ok"])
        self.assertEqual(summary["mcp_servers"]["unitext-registry"]["status"], "connected")
        self.assertEqual(summary["final_payload"]["registry_roots"], ["/registry/skills"])


if __name__ == "__main__":
    unittest.main()
