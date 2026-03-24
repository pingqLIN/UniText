#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


CORE_DOCS = {
    "README.md",
    "INDEX.md",
    "VISION.md",
    "RESOURCE_SPEC.md",
    "OPERATIONS.md",
    "PROJECT_MODES.md",
    "MILESTONES.md",
    "SECRET_HANDLING_GUIDELINES.md",
}


def list_entries(root: Path, kind: str) -> list[str]:
    path = root / "registry" / kind
    if not path.exists():
        return []
    return sorted(item.name for item in path.iterdir() if item.is_dir())


def safe_repo_path(root: Path, relative: str) -> Path:
    candidate = (root / relative).resolve()
    if root.resolve() not in candidate.parents and candidate != root.resolve():
        raise ValueError("path escapes repo root")
    relative_path = candidate.relative_to(root.resolve())
    if relative_path.parts and relative_path.parts[0] == "registry":
        return candidate
    if relative_path.name in CORE_DOCS and len(relative_path.parts) == 1:
        return candidate
    raise ValueError("path is outside the read-only registry surface")


def make_text(body: object) -> dict[str, object]:
    text = body if isinstance(body, str) else json.dumps(body, indent=2, ensure_ascii=False)
    return {"type": "text", "text": text}


class Server:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()

    def handle(self, request: dict[str, object]) -> dict[str, object] | None:
        method = request.get("method")
        if method == "notifications/initialized":
            return None
        if method == "initialize":
            return {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "unitext-registry", "version": "0.1.0"},
            }
        if method == "ping":
            return {}
        if method == "shutdown":
            return {}
        if method == "tools/list":
            return {
                "tools": [
                    {
                        "name": "registry_summary",
                        "description": "Return registry counts and the core UniText doc surface.",
                        "inputSchema": {"type": "object", "properties": {}},
                    },
                    {
                        "name": "list_registry_entries",
                        "description": "List registry entry ids by type or across all types.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "kind": {
                                    "type": "string",
                                    "enum": ["skills", "mcp", "agents", "workflow"],
                                }
                            },
                        },
                    },
                    {
                        "name": "read_registry_file",
                        "description": "Read a core doc or registry file from the repo in a safe, read-only way.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {"path": {"type": "string"}},
                            "required": ["path"],
                        },
                    },
                ]
            }
        if method == "tools/call":
            params = request.get("params", {})
            if not isinstance(params, dict):
                raise ValueError("invalid tool params")
            return self.call_tool(params)
        raise ValueError(f"unsupported method: {method}")

    def call_tool(self, params: dict[str, object]) -> dict[str, object]:
        name = params.get("name")
        arguments = params.get("arguments", {})
        if not isinstance(arguments, dict):
            raise ValueError("tool arguments must be an object")
        if name == "registry_summary":
            return {
                "content": [
                    make_text(
                        {
                            "repo_root": str(self.root),
                            "docs": sorted(CORE_DOCS),
                            "skills": len(list_entries(self.root, "skills")),
                            "mcp": len(list_entries(self.root, "mcp")),
                            "agents": len(list_entries(self.root, "agents")),
                            "workflow": len(list_entries(self.root, "workflow")),
                        }
                    )
                ]
            }
        if name == "list_registry_entries":
            kinds = ["skills", "mcp", "agents", "workflow"]
            kind = arguments.get("kind")
            if kind is None:
                return {
                    "content": [
                        make_text({item: list_entries(self.root, item) for item in kinds})
                    ]
                }
            if kind not in kinds:
                raise ValueError(f"unknown kind: {kind}")
            return {"content": [make_text({"kind": kind, "entries": list_entries(self.root, str(kind))})]}
        if name == "read_registry_file":
            relative = arguments.get("path")
            if not isinstance(relative, str):
                raise ValueError("path must be a string")
            path = safe_repo_path(self.root, relative)
            return {
                "content": [
                    make_text(
                        {
                            "path": str(path.relative_to(self.root)),
                            "content": path.read_text(encoding="utf-8"),
                        }
                    )
                ]
            }
        raise ValueError(f"unknown tool: {name}")


def read_message() -> dict[str, object] | None:
    headers: dict[str, str] = {}
    while True:
        line = sys.stdin.buffer.readline()
        if not line:
            return None
        if line in {b"\r\n", b"\n"}:
            break
        key, _, value = line.decode("utf-8").partition(":")
        headers[key.strip().lower()] = value.strip()
    length = int(headers.get("content-length", "0"))
    if length <= 0:
        return None
    body = sys.stdin.buffer.read(length)
    return json.loads(body.decode("utf-8"))


def write_message(body: dict[str, object]) -> None:
    encoded = json.dumps(body, ensure_ascii=False).encode("utf-8")
    sys.stdout.buffer.write(f"Content-Length: {len(encoded)}\r\n\r\n".encode("utf-8"))
    sys.stdout.buffer.write(encoded)
    sys.stdout.buffer.flush()


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only UniText MCP server.")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[3]))
    args = parser.parse_args()

    server = Server(Path(args.root))

    while True:
        request = read_message()
        if request is None:
            return 0
        request_id = request.get("id")
        try:
            result = server.handle(request)
            if request_id is not None and result is not None:
                write_message({"jsonrpc": "2.0", "id": request_id, "result": result})
            if request.get("method") == "shutdown":
                return 0
        except Exception as exc:
            if request_id is None:
                continue
            write_message(
                {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32000, "message": str(exc)},
                }
            )


if __name__ == "__main__":
    raise SystemExit(main())
