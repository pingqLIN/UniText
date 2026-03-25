#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


PROMPT = (
    'Read .github/copilot-instructions.md and README.md. '
    'Reply with a single JSON object only: '
    '{"registry_roots": [...], "copilot_status": "...", "catalog_exclusions_path": "..."}. '
    "Do not modify files."
)


def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def parse_jsonl(stdout: str) -> list[dict[str, object]]:
    events: list[dict[str, object]] = []
    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            body = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(body, dict):
            events.append(body)
    return events


def extract_json_object(text: str) -> dict[str, object] | None:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```[a-zA-Z0-9_-]*\n?", "", cleaned)
        cleaned = re.sub(r"\n?```$", "", cleaned)
    try:
        body = json.loads(cleaned)
    except json.JSONDecodeError:
        return None
    return body if isinstance(body, dict) else None


def summarize_events(events: list[dict[str, object]]) -> dict[str, object]:
    mcp_server_status: dict[str, dict[str, object]] = {}
    viewed_paths: list[str] = []
    final_message = ""
    final_payload = None
    result_event = None

    for event in events:
        event_type = event.get("type")
        data = event.get("data")
        if event_type == "session.mcp_servers_loaded" and isinstance(data, dict):
            servers = data.get("servers")
            if isinstance(servers, list):
                for server in servers:
                    if isinstance(server, dict) and isinstance(server.get("name"), str):
                        mcp_server_status[server["name"]] = server
        elif event_type == "tool.execution_complete" and isinstance(data, dict):
            result = data.get("result")
            if isinstance(result, dict):
                content = result.get("content")
                if isinstance(content, str) and content.startswith("/mnt/"):
                    viewed_paths.append(content)
        elif event_type == "assistant.message" and isinstance(data, dict):
            content = data.get("content")
            if isinstance(content, str):
                final_message = content
                parsed = extract_json_object(content)
                if parsed is not None:
                    final_payload = parsed
        elif event_type == "result":
            result_event = event

    unitext_status = mcp_server_status.get("unitext-registry", {}).get("status")
    ok = bool(final_payload)
    return {
        "ok": ok,
        "mcp_servers": mcp_server_status,
        "unitext_registry_status": unitext_status,
        "viewed_paths": viewed_paths,
        "final_message": final_message,
        "final_payload": final_payload,
        "result": result_event,
    }


def run_copilot(repo_root: Path, timeout_seconds: int, use_project_mcp: bool) -> dict[str, object]:
    binary = shutil.which("copilot")
    if binary is None:
        return {"ok": False, "available": False, "reason": "copilot binary not found"}

    cmd = [
        binary,
        "-p",
        PROMPT,
        "--allow-all",
        "--no-ask-user",
        "--output-format",
        "json",
    ]
    if use_project_mcp:
        cmd.extend(["--additional-mcp-config", "@.mcp.json"])

    completed = None
    timed_out = False
    try:
        completed = subprocess.run(
            cmd,
            cwd=repo_root,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as exc:
        completed = exc
        timed_out = True

    stdout = completed.stdout if completed and completed.stdout else ""
    stderr = completed.stderr if completed and completed.stderr else ""
    events = parse_jsonl(stdout)
    summary = summarize_events(events)
    exit_code = None if timed_out else completed.returncode
    mcp_attach_ok = True
    if use_project_mcp:
        mcp_attach_ok = summary.get("unitext_registry_status") not in {None, "failed"}

    return {
        "ok": summary["ok"] and exit_code == 0 and not timed_out and mcp_attach_ok,
        "available": True,
        "binary": binary,
        "cwd": str(repo_root),
        "timeout_seconds": timeout_seconds,
        "use_project_mcp": use_project_mcp,
        "timed_out": timed_out,
        "exit_code": exit_code,
        "stdout_line_count": len(stdout.splitlines()),
        "stderr": stderr.strip(),
        "mcp_attach_ok": mcp_attach_ok,
        "summary": summary,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a non-interactive Copilot CLI verification prompt.")
    parser.add_argument("--repo-root", default=str(get_repo_root()))
    parser.add_argument("--timeout-seconds", type=int, default=180)
    parser.add_argument("--use-project-mcp", action="store_true")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = run_copilot(repo_root, args.timeout_seconds, args.use_project_mcp)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
