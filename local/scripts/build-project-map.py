#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


REPO_MARKERS = [
    Path("README.md"),
    Path("INDEX.md"),
    Path("registry") / "skills",
    Path("registry") / "mcp",
]

CORE_DOCS = [
    "README.md",
    "INDEX.md",
    "VISION.md",
    "RESOURCE_SPEC.md",
    "OPERATIONS.md",
    "PROJECT_MODES.md",
    "DOCUMENT_PLACEMENT_POLICY.md",
    "WORKSPACE_SENSITIVE_METADATA_RULES.md",
    "PROJECT_MAP_WEB_AUTOMATION_REPORT.md",
]

ROOT_DIRECTORIES = [
    ("registry/skills", "skills", "/registry/skills"),
    ("registry/mcp", "mcp", "/registry/mcp"),
    ("registry/agents", "agents", "/registry/agents"),
    ("registry/workflow", "workflow", "/registry/workflow"),
]

TYPE_ORDER = ["doc", "directory", "skill", "mcp", "agent", "workflow"]

LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
HEADING_PATTERN = re.compile(r"^#\s+(.+)$", re.MULTILINE)


@dataclass(frozen=True)
class Node:
    node_id: str
    node_type: str
    label: str
    path: str
    logical_path: str | None = None
    status: str | None = None
    description: str | None = None
    source_path: str | None = None

    def as_dict(self) -> dict[str, object]:
        body: dict[str, object] = {
            "id": self.node_id,
            "type": self.node_type,
            "label": self.label,
            "path": self.path,
        }
        if self.logical_path:
            body["logical_path"] = self.logical_path
        if self.status:
            body["status"] = self.status
        if self.description:
            body["description"] = self.description
        if self.source_path:
            body["source_path"] = self.source_path
        return body


def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def validate_repo_root(repo_root: Path) -> None:
    missing = [str(marker) for marker in REPO_MARKERS if not (repo_root / marker).exists()]
    if missing:
        joined = ", ".join(missing)
        raise SystemExit(f"repo root is missing required markers: {joined}")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def repo_path(repo_root: Path, target: Path) -> str:
    return "/" + target.relative_to(repo_root).as_posix()


def node_id_for(kind: str, key: str) -> str:
    return f"{kind}:{key}"


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}

    fields: dict[str, str] = {}
    for raw_line in text[4:end].splitlines():
        line = raw_line.strip()
        if not line or ":" not in line:
            continue
        key, raw_value = line.split(":", 1)
        value = raw_value.strip().strip('"').strip("'")
        fields[key.strip()] = value
    return fields


def extract_title(text: str, fallback: str) -> str:
    match = HEADING_PATTERN.search(text)
    if match:
        return match.group(1).strip()
    return fallback


def label_for_core_doc(relative: str, text: str) -> str:
    if relative == "README.md":
        return "README"
    return extract_title(text, Path(relative).stem)


def build_nodes(repo_root: Path) -> tuple[list[Node], dict[str, str], dict[str, str]]:
    nodes: list[Node] = []
    path_to_node_id: dict[str, str] = {}
    logical_to_node_id: dict[str, str] = {}

    def register(node: Node) -> None:
        nodes.append(node)
        path_to_node_id[node.path] = node.node_id
        if node.logical_path:
            logical_to_node_id[node.logical_path] = node.node_id

    register(
        Node(
            node_id="repo:root",
            node_type="directory",
            label="Repo Root",
            path="/",
            logical_path="/",
            status="repo-root",
            description="Repository root directory",
        )
    )

    for relative, label, logical_path in ROOT_DIRECTORIES:
        register(
            Node(
                node_id=node_id_for("dir", relative),
                node_type="directory",
                label=label,
                path="/" + relative,
                logical_path=logical_path,
                status="canonical-root",
                description=f"Canonical {label} root",
                source_path="/" + relative,
            )
        )

    for relative in CORE_DOCS:
        path = repo_root / relative
        if not path.exists():
            continue
        text = read_text(path)
        register(
            Node(
                node_id=node_id_for("doc", relative),
                node_type="doc",
                label=label_for_core_doc(relative, text),
                path="/" + relative,
                logical_path="/" + relative,
                status="core-doc",
                description=extract_title(text, path.stem),
                source_path="/" + relative,
            )
        )

    skills_root = repo_root / "registry" / "skills"
    for skill_dir in sorted(path for path in skills_root.iterdir() if path.is_dir()):
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        text = read_text(skill_file)
        frontmatter = parse_frontmatter(text)
        skill_name = frontmatter.get("name", skill_dir.name)
        register(
            Node(
                node_id=node_id_for("skill", skill_name),
                node_type="skill",
                label=skill_name,
                path=repo_path(repo_root, skill_dir),
                logical_path=repo_path(repo_root, skill_dir),
                status="active",
                description=frontmatter.get("description"),
                source_path=repo_path(repo_root, skill_file),
            )
        )

    mcp_root = repo_root / "registry" / "mcp"
    for mcp_dir in sorted(path for path in mcp_root.iterdir() if path.is_dir()):
        definition_file = mcp_dir / "definition.json"
        if not definition_file.exists():
            continue
        definition = json.loads(read_text(definition_file))
        servers = definition.get("mcpServers", {})
        server_id = mcp_dir.name
        notes = None
        if isinstance(servers, dict) and servers:
            first_key = next(iter(servers))
            server_id = str(first_key)
            first_server = servers[first_key]
            if isinstance(first_server, dict):
                notes = first_server.get("notes")
        register(
            Node(
                node_id=node_id_for("mcp", server_id),
                node_type="mcp",
                label=server_id,
                path=repo_path(repo_root, mcp_dir),
                logical_path=repo_path(repo_root, mcp_dir),
                status="active-baseline",
                description=notes,
                source_path=repo_path(repo_root, definition_file),
            )
        )

    agents_root = repo_root / "registry" / "agents"
    for agent_dir in sorted(path for path in agents_root.iterdir() if path.is_dir()):
        agent_file = agent_dir / "AGENT.md"
        if not agent_file.exists():
            continue
        text = read_text(agent_file)
        register(
            Node(
                node_id=node_id_for("agent", agent_dir.name),
                node_type="agent",
                label=agent_dir.name,
                path=repo_path(repo_root, agent_dir),
                logical_path=repo_path(repo_root, agent_dir),
                status="active",
                description=extract_title(text, agent_dir.name),
                source_path=repo_path(repo_root, agent_file),
            )
        )

    workflow_root = repo_root / "registry" / "workflow"
    for workflow_dir in sorted(path for path in workflow_root.iterdir() if path.is_dir()):
        workflow_file = workflow_dir / "WORKFLOW.md"
        if not workflow_file.exists():
            workflow_file = workflow_dir / "README.md"
        if not workflow_file.exists():
            continue
        text = read_text(workflow_file)
        register(
            Node(
                node_id=node_id_for("workflow", workflow_dir.name),
                node_type="workflow",
                label=workflow_dir.name,
                path=repo_path(repo_root, workflow_dir),
                logical_path=repo_path(repo_root, workflow_dir),
                status="draft",
                description=extract_title(text, workflow_dir.name),
                source_path=repo_path(repo_root, workflow_file),
            )
        )

    return nodes, path_to_node_id, logical_to_node_id


def build_edges(
    repo_root: Path,
    nodes: Iterable[Node],
    path_to_node_id: dict[str, str],
    logical_to_node_id: dict[str, str],
) -> list[dict[str, str]]:
    edges: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()

    def add_edge(from_id: str, to_id: str, kind: str) -> None:
        key = (from_id, to_id, kind)
        if from_id == to_id or key in seen:
            return
        seen.add(key)
        edges.append({"from": from_id, "to": to_id, "kind": kind})

    for node in nodes:
        if node.node_id == "repo:root":
            continue
        if node.node_type == "directory":
            add_edge("repo:root", node.node_id, "contains")
            continue
        if node.path.startswith("/registry/skills/"):
            add_edge(node_id_for("dir", "registry/skills"), node.node_id, "contains")
        elif node.path.startswith("/registry/mcp/"):
            add_edge(node_id_for("dir", "registry/mcp"), node.node_id, "contains")
        elif node.path.startswith("/registry/agents/"):
            add_edge(node_id_for("dir", "registry/agents"), node.node_id, "contains")
        elif node.path.startswith("/registry/workflow/"):
            add_edge(node_id_for("dir", "registry/workflow"), node.node_id, "contains")
        else:
            add_edge("repo:root", node.node_id, "contains")

    markdown_sources = [
        repo_root / relative
        for relative in CORE_DOCS
        if (repo_root / relative).exists()
    ]
    markdown_sources.extend((repo_root / "registry" / "agents").glob("*/AGENT.md"))
    markdown_sources.extend((repo_root / "registry" / "workflow").glob("*/README.md"))
    markdown_sources.extend((repo_root / "registry" / "workflow").glob("*/WORKFLOW.md"))

    for source in markdown_sources:
        source_path = repo_path(repo_root, source)
        source_id = path_to_node_id.get(source_path)
        if not source_id:
            continue
        text = read_text(source)
        for target in LINK_PATTERN.findall(text):
            if not target or target.startswith("http") or target.startswith("#"):
                continue
            if target.startswith("mailto:"):
                continue
            normalized = target.split("#", 1)[0]
            resolved = (source.parent / normalized).resolve()
            if not resolved.exists() or repo_root not in resolved.parents and resolved != repo_root:
                continue
            target_path = repo_path(repo_root, resolved)
            target_id = path_to_node_id.get(target_path)
            if target_id:
                add_edge(source_id, target_id, "references")

    index_path = repo_root / "INDEX.md"
    if index_path.exists():
        index_id = path_to_node_id.get("/INDEX.md")
        index_text = read_text(index_path)
        if index_id:
            for logical_path, target_id in logical_to_node_id.items():
                if logical_path.startswith("/registry/") and logical_path in index_text:
                    add_edge(index_id, target_id, "catalog_entry")

    operations_id = path_to_node_id.get("/OPERATIONS.md")
    if operations_id:
        for logical_path in ["/registry/skills", "/registry/mcp", "/registry/agents", "/registry/workflow"]:
            target_id = logical_to_node_id.get(logical_path)
            if target_id:
                add_edge(operations_id, target_id, "maps_to")

    return edges


def build_payload(repo_root: Path) -> dict[str, object]:
    nodes, path_to_node_id, logical_to_node_id = build_nodes(repo_root)
    edges = build_edges(repo_root, nodes, path_to_node_id, logical_to_node_id)
    counts = defaultdict(int)
    for node in nodes:
        counts[node.node_type] += 1
    return {
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "source_root": "/",
            "version": 1,
        },
        "counts": dict(sorted(counts.items())),
        "nodes": [node.as_dict() for node in nodes],
        "edges": edges,
    }


def render_html(payload: dict[str, object]) -> str:
    repo_root = get_repo_root()
    template_path = repo_root / "local" / "scripts" / "project-map-template.html"
    runtime_path = repo_root / "local" / "scripts" / "project-map-runtime.js"
    template = read_text(template_path)
    runtime_source = read_text(runtime_path).replace("</", "<\\/")
    replacements = {
        "__BOOTSTRAP_DATA__": json.dumps(payload, ensure_ascii=False).replace("</", "<\\/"),
        "__TYPE_ORDER__": json.dumps(TYPE_ORDER, ensure_ascii=False),
        "__CORE_DOCS__": json.dumps(CORE_DOCS, ensure_ascii=False),
        "__ROOT_DIRECTORIES__": json.dumps(ROOT_DIRECTORIES, ensure_ascii=False),
        "__REPO_MARKERS__": json.dumps([marker.as_posix() for marker in REPO_MARKERS], ensure_ascii=False),
        "__RUNTIME_SOURCE__": runtime_source,
    }
    for key, value in replacements.items():
        template = template.replace(key, value)
    return template


def write_outputs(payload: dict[str, object], output_root: Path) -> tuple[Path, Path]:
    output_root.mkdir(parents=True, exist_ok=True)
    site_dir = output_root / "site"
    site_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_root / "project-map.json"
    html_path = site_dir / "project-map.html"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    html_path.write_text(render_html(payload), encoding="utf-8")
    return json_path, html_path


def main() -> int:
    default_repo_root = get_repo_root()
    parser = argparse.ArgumentParser(
        description="Build a static, self-contained UniText project map page."
    )
    parser.add_argument("--repo-root", default=str(default_repo_root))
    parser.add_argument("--output-dir", default=None)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    validate_repo_root(repo_root)
    output_dir = Path(args.output_dir).resolve() if args.output_dir else repo_root / "ops" / "project-map"

    payload = build_payload(repo_root)
    json_path, html_path = write_outputs(payload, output_dir)

    summary = {
      "generated_at": payload["meta"]["generated_at"],
      "repo_root": str(repo_root),
      "node_count": len(payload["nodes"]),
      "edge_count": len(payload["edges"]),
      "json_path": str(json_path),
      "html_path": str(html_path),
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
