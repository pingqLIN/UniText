#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def run_command(cmd: list[str], cwd: Path, timeout: int = 300) -> dict[str, object]:
    try:
        completed = subprocess.run(
            cmd,
            cwd=cwd,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        return {
            "command": cmd,
            "ok": False,
            "timed_out": True,
            "returncode": None,
            "stdout": exc.stdout or "",
            "stderr": exc.stderr or "",
        }
    return {
        "command": cmd,
        "ok": completed.returncode == 0,
        "timed_out": False,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def parse_json_output(result: dict[str, object]) -> dict[str, object] | None:
    stdout = result.get("stdout", "")
    if not isinstance(stdout, str):
        return None
    try:
        body = json.loads(stdout)
    except json.JSONDecodeError:
        return None
    return body if isinstance(body, dict) else None


def run_mcp_smoke(repo_root: Path) -> dict[str, object]:
    inline = (
        "import json, subprocess, sys;"
        "cmd=[sys.executable,'registry/mcp/claude-project-mcp-seed/server.py','--root',sys.argv[1]];"
        "p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE);"
        "req={'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'release-evidence','version':'1.0'}}};"
        "body=json.dumps(req).encode('utf-8');"
        "msg=f'Content-Length: {len(body)}\\r\\n\\r\\n'.encode('utf-8')+body;"
        "out,err=p.communicate(msg,timeout=5);"
        "print(json.dumps({'stdout':out.decode('utf-8','replace'),'stderr':err.decode('utf-8','replace'),'returncode':p.returncode}))"
    )
    result = run_command([sys.executable, "-c", inline, str(repo_root)], repo_root, timeout=10)
    payload = parse_json_output(result)
    ok = False
    if payload is not None:
        stdout = payload.get("stdout", "")
        ok = isinstance(stdout, str) and '"serverInfo": {"name": "unitext-registry"' in stdout
    return {
        "command": ["python3", "registry/mcp/claude-project-mcp-seed/server.py", "--root", str(repo_root)],
        "ok": ok,
        "payload": payload,
    }


def format_markdown(report: dict[str, object]) -> str:
    sections = [
        "# Release Evidence 2026-03-26",
        "",
        "## Scope",
        "",
        "This evidence bundle captures the current release-gating baseline after aligning release hygiene tooling, adding Copilot session verification, and collecting a repeatable local evidence chain.",
        "",
        "## Environment",
        "",
        f"- generated_at: `{report['generated_at']}`",
        f"- repo_root: `{report['repo_root']}`",
        f"- pwsh_available: `{str(report['pwsh_available']).lower()}`",
        f"- copilot_available: `{str(report['copilot_available']).lower()}`",
        "",
        "## Verification Summary",
        "",
    ]

    for key in [
        "verify_bootstrap",
        "security_tests",
        "i18n_wave",
        "release_hygiene",
        "unitext_mcp_smoke",
        "copilot_session",
    ]:
        item = report["checks"][key]
        sections.append(f"- `{key}`: `{'ok' if item['ok'] else 'not_ok'}`")

    sections.extend(
        [
            "",
            "## Key Findings",
            "",
            f"- `verify-bootstrap.py` status: `{str(report['checks']['verify_bootstrap'].get('payload', {}).get('ok')).lower()}`",
            f"- `report-i18n-wave.py` safe_to_split: `{str(report['checks']['i18n_wave'].get('payload', {}).get('safe_to_split')).lower()}`",
            f"- `report-release-hygiene.py` blockers: `{report['checks']['release_hygiene'].get('payload', {}).get('summary', {}).get('blockers')}`",
            f"- `unitext-registry` manual MCP initialize smoke: `{str(report['checks']['unitext_mcp_smoke']['ok']).lower()}`",
        ]
    )

    copilot = report["checks"]["copilot_session"]
    copilot_summary = copilot.get("payload", {}).get("summary", {})
    if copilot_summary:
        mcp_servers = copilot_summary.get("mcp_servers", {})
        unitext = mcp_servers.get("unitext-registry", {})
        sections.extend(
            [
                f"- Copilot final payload parsed: `{str(copilot_summary.get('final_payload') is not None).lower()}`",
                f"- Copilot `unitext-registry` status during prompt: `{unitext.get('status', 'unknown')}`",
            ]
        )

    if not report["pwsh_available"]:
        sections.extend(
            [
                "",
                "## PowerShell Boundary",
                "",
                "- `pwsh` is not available in this Linux/WSL environment, so `export-template-package.ps1` and `verify-template-package.ps1` were not re-run here.",
                "- Existing PowerShell-backed template export remains a documented boundary rather than freshly collected evidence in this run.",
            ]
        )

    sections.extend(
        [
            "",
            "## Raw Commands",
            "",
        ]
    )
    for key, item in report["checks"].items():
        command = item.get("command")
        if command:
            sections.append(f"- `{key}`: `{ ' '.join(command) }`")

    return "\n".join(sections) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect a repeatable local release evidence bundle.")
    parser.add_argument("--repo-root", default=str(get_repo_root()))
    parser.add_argument("--markdown-out", default="")
    parser.add_argument("--json-out", default="")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    checks: dict[str, dict[str, object]] = {}

    verify_bootstrap = run_command([sys.executable, "local/scripts/verify-bootstrap.py"], repo_root)
    verify_bootstrap["payload"] = parse_json_output(verify_bootstrap)
    checks["verify_bootstrap"] = verify_bootstrap

    security_tests = run_command([sys.executable, "-m", "unittest", "discover", "-s", "tests/security", "-v"], repo_root)
    checks["security_tests"] = security_tests

    i18n_wave = run_command([sys.executable, "local/scripts/report-i18n-wave.py", "--json"], repo_root)
    i18n_wave["payload"] = parse_json_output(i18n_wave)
    checks["i18n_wave"] = i18n_wave

    release_hygiene = run_command([sys.executable, "local/scripts/report-release-hygiene.py", "--json"], repo_root)
    release_hygiene["payload"] = parse_json_output(release_hygiene)
    checks["release_hygiene"] = release_hygiene

    checks["unitext_mcp_smoke"] = run_mcp_smoke(repo_root)

    copilot_available = shutil.which("copilot") is not None
    copilot_session = {"ok": False, "command": [], "payload": None}
    if copilot_available:
        copilot_session = run_command(
            [
                sys.executable,
                "local/scripts/verify-copilot-session.py",
                "--use-project-mcp",
            ],
            repo_root,
            timeout=300,
        )
        copilot_session["payload"] = parse_json_output(copilot_session)
        copilot_session["ok"] = bool(copilot_session["payload"] and copilot_session["payload"].get("ok"))
    checks["copilot_session"] = copilot_session

    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(repo_root),
        "pwsh_available": shutil.which("pwsh") is not None,
        "copilot_available": copilot_available,
        "checks": checks,
    }
    report["ok"] = all(item.get("ok") for item in checks.values())

    markdown = format_markdown(report)
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.markdown_out:
        Path(args.markdown_out).write_text(markdown, encoding="utf-8")

    print(markdown)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
