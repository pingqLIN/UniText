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
    embedded = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>UniText Project Map</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f4f0e8;
      --panel: rgba(255, 252, 246, 0.94);
      --panel-strong: #fffdf8;
      --ink: #1f1c16;
      --muted: #6b6457;
      --line: #d7cfbf;
      --accent: #0f766e;
      --accent-soft: #d7f3ed;
      --accent-deep: #0b5a54;
      --gold-soft: #fff1bf;
      --shadow: 0 14px 36px rgba(34, 28, 19, 0.08);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Segoe UI", "Noto Sans TC", sans-serif;
      background:
        radial-gradient(circle at top left, rgba(15, 118, 110, 0.08), transparent 28%),
        radial-gradient(circle at top right, rgba(202, 138, 4, 0.08), transparent 22%),
        linear-gradient(180deg, #fbfaf7 0%, var(--bg) 100%);
      color: var(--ink);
    }}
    header {{
      padding: 20px 24px 14px;
      border-bottom: 1px solid var(--line);
      background: rgba(255, 252, 246, 0.92);
      position: sticky;
      top: 0;
      backdrop-filter: blur(10px);
      z-index: 2;
    }}
    header h1 {{ margin: 0 0 8px; font-size: 28px; letter-spacing: -0.02em; }}
    header p {{ margin: 0; color: var(--muted); max-width: 900px; }}
    .summary {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-top: 14px;
    }}
    .chip {{
      padding: 6px 10px;
      border-radius: 999px;
      background: linear-gradient(180deg, #effaf7 0%, var(--accent-soft) 100%);
      color: var(--accent-deep);
      font-size: 13px;
      border: 1px solid rgba(15, 118, 110, 0.15);
    }}
    .controls {{
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      margin-top: 14px;
    }}
    .controls input,
    .controls select {{
      padding: 10px 12px;
      border: 1px solid var(--line);
      border-radius: 10px;
      background: var(--panel-strong);
      min-width: 220px;
    }}
    .legend {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-top: 12px;
    }}
    .legend span {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-size: 12px;
      color: var(--muted);
      padding: 6px 10px;
      background: rgba(255, 255, 255, 0.55);
      border: 1px solid rgba(170, 160, 138, 0.35);
      border-radius: 999px;
    }}
    .legend i {{
      width: 10px;
      height: 10px;
      border-radius: 50%;
      display: inline-block;
    }}
    .layout {{
      display: grid;
      grid-template-columns: 280px minmax(480px, 1fr) 320px;
      gap: 16px;
      padding: 16px;
      min-height: calc(100vh - 150px);
    }}
    .panel {{
      background: var(--panel);
      border: 1px solid rgba(155, 145, 120, 0.25);
      border-radius: 20px;
      box-shadow: var(--shadow);
      overflow: hidden;
      min-height: 400px;
    }}
    .panel h2 {{
      margin: 0;
      padding: 14px 16px;
      font-size: 15px;
      border-bottom: 1px solid var(--line);
    }}
    .sidebar {{
      padding: 8px 8px 18px;
      overflow: auto;
      max-height: calc(100vh - 210px);
    }}
    .group-title {{
      margin: 14px 8px 6px;
      font-size: 12px;
      text-transform: uppercase;
      color: var(--muted);
      letter-spacing: 0.08em;
    }}
    .node-button {{
      width: 100%;
      text-align: left;
      border: 0;
      background: transparent;
      border-radius: 14px;
      padding: 10px 12px;
      cursor: pointer;
      color: inherit;
      transition: background 120ms ease, transform 120ms ease;
    }}
    .node-button:hover,
    .node-button.active {{
      background: #f2eee2;
      transform: translateX(2px);
    }}
    .node-head {{
      display: flex;
      align-items: center;
      gap: 8px;
      justify-content: space-between;
    }}
    .node-head strong {{
      font-size: 14px;
      line-height: 1.35;
    }}
    .node-type {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-width: 58px;
      padding: 4px 8px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 700;
      color: #453d2f;
      background: #efe7d4;
    }}
    .node-description {{
      display: block;
      color: var(--muted);
      margin-top: 6px;
      line-height: 1.45;
      font-size: 12px;
    }}
    .node-path {{
      display: block;
      color: #8b816d;
      margin-top: 6px;
      line-height: 1.35;
      font-size: 11px;
    }}
    .map-wrap {{
      overflow: auto;
      background:
        radial-gradient(circle at 20% 20%, rgba(15, 118, 110, 0.06), transparent 24%),
        radial-gradient(circle at 80% 15%, rgba(202, 138, 4, 0.05), transparent 20%),
        linear-gradient(180deg, #fffdf8 0%, #f9f7f1 100%);
    }}
    svg {{
      width: 100%;
      min-height: 860px;
      display: block;
    }}
    .detail {{
      padding: 16px;
      overflow: auto;
      max-height: calc(100vh - 210px);
    }}
    .detail h3 {{
      margin: 0 0 10px;
      font-size: 22px;
    }}
    .detail p {{
      line-height: 1.7;
      color: #50493c;
    }}
    .detail .meta {{
      display: grid;
      gap: 8px;
      margin-top: 16px;
    }}
    .meta-row {{
      padding: 10px 12px;
      background: #f9f6ee;
      border-radius: 12px;
    }}
    .meta-row strong {{
      display: block;
      font-size: 12px;
      text-transform: uppercase;
      color: var(--muted);
      margin-bottom: 4px;
    }}
    .section-title {{
      margin: 22px 0 10px;
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--muted);
    }}
    .edge-list {{
      display: grid;
      gap: 8px;
    }}
    .edge-item {{
      padding: 10px 12px;
      border-radius: 12px;
      background: #f9f6ef;
      border: 1px solid #e4dbc7;
      font-size: 14px;
    }}
    .edge-item strong {{
      color: var(--accent-deep);
      text-transform: uppercase;
      font-size: 11px;
      letter-spacing: 0.08em;
    }}
    .edge-direction {{
      color: var(--muted);
      font-size: 12px;
      margin-bottom: 5px;
    }}
    .edge-visibility {{
      margin-top: 6px;
      font-size: 11px;
      color: #7a705e;
    }}
    .empty {{
      color: var(--muted);
      line-height: 1.6;
    }}
    @media (max-width: 1200px) {{
      .layout {{
        grid-template-columns: 1fr;
      }}
      .sidebar,
      .detail {{
        max-height: none;
      }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>UniText Project Map</h1>
    <p>一次性生成、純靜態、可直接用瀏覽器開啟的專案 MAP 頁面。</p>
    <div class="summary" id="summary"></div>
    <div class="legend">
      <span><i style="background:#ffe9b8"></i>Docs</span>
      <span><i style="background:#d6efe9"></i>Directories</span>
      <span><i style="background:#dbe8ff"></i>Skills</span>
      <span><i style="background:#f5d9ff"></i>MCP</span>
      <span><i style="background:#ffd8cb"></i>Agents</span>
      <span><i style="background:#d8f0ce"></i>Workflow</span>
    </div>
    <div class="controls">
      <input id="search" type="search" placeholder="搜尋節點名稱、描述、路徑" />
      <select id="type-filter">
        <option value="all">全部類型</option>
      </select>
    </div>
  </header>
  <main class="layout">
    <section class="panel">
      <h2>Nodes</h2>
      <div class="sidebar" id="sidebar"></div>
    </section>
    <section class="panel map-wrap">
      <h2>Map View</h2>
      <svg id="map" viewBox="0 0 1400 900" preserveAspectRatio="xMinYMin meet"></svg>
    </section>
    <section class="panel">
      <h2>Details</h2>
      <div class="detail" id="detail"></div>
    </section>
  </main>
  <script>
    const DATA = {embedded};
    const TYPE_ORDER = {json.dumps(TYPE_ORDER)};
    const TYPE_LABELS = {{
      doc: "Docs",
      directory: "Directories",
      skill: "Skills",
      mcp: "MCP",
      agent: "Agents",
      workflow: "Workflow",
    }};
    const TYPE_STYLES = {{
      doc: {{ fill: "#fff1c7", stroke: "#d29d21", badge: "#f4e1a2" }},
      directory: {{ fill: "#dff4ee", stroke: "#3b8f81", badge: "#cfe8e1" }},
      skill: {{ fill: "#e1ebff", stroke: "#5679c5", badge: "#d6e2fb" }},
      mcp: {{ fill: "#f0dcff", stroke: "#9254c7", badge: "#e7cef9" }},
      agent: {{ fill: "#ffdcca", stroke: "#d06c45", badge: "#f7cfbf" }},
      workflow: {{ fill: "#e0f1d7", stroke: "#5b9b51", badge: "#d3e8ca" }},
    }};
    const EDGE_LABELS = {{
      contains: "Contains",
      references: "References",
      catalog_entry: "Catalog",
      maps_to: "Maps To",
    }};
    const EDGE_STYLES = {{
      contains: {{ stroke: "#c4b89e", width: 1.1, opacity: 0.45, dash: "" }},
      references: {{ stroke: "#2563eb", width: 1.6, opacity: 0.75, dash: "5 5" }},
      catalog_entry: {{ stroke: "#0f766e", width: 1.9, opacity: 0.82, dash: "" }},
      maps_to: {{ stroke: "#ca8a04", width: 1.8, opacity: 0.8, dash: "7 4" }},
    }};

    const nodes = DATA.nodes;
    const edges = DATA.edges;
    const nodeById = new Map(nodes.map((node) => [node.id, node]));
    const state = {{
      search: "",
      type: "all",
      selectedId: nodeById.has("doc:INDEX.md") ? "doc:INDEX.md" : nodes[0]?.id ?? null,
    }};

    const summaryEl = document.getElementById("summary");
    const sidebarEl = document.getElementById("sidebar");
    const detailEl = document.getElementById("detail");
    const mapEl = document.getElementById("map");
    const searchEl = document.getElementById("search");
    const typeFilterEl = document.getElementById("type-filter");

    function setupControls() {{
      TYPE_ORDER.forEach((type) => {{
        const count = DATA.counts[type] || 0;
        const option = document.createElement("option");
        option.value = type;
        option.textContent = `${{TYPE_LABELS[type]}} (${{count}})`;
        typeFilterEl.appendChild(option);
      }});

      Object.entries(DATA.counts).forEach(([type, count]) => {{
        const chip = document.createElement("div");
        chip.className = "chip";
        chip.textContent = `${{TYPE_LABELS[type] || type}}: ${{count}}`;
        summaryEl.appendChild(chip);
      }});

      searchEl.addEventListener("input", () => {{
        state.search = searchEl.value.trim().toLowerCase();
        render();
      }});

      typeFilterEl.addEventListener("change", () => {{
        state.type = typeFilterEl.value;
        render();
      }});
    }}

    function matchesFilter(node) {{
      if (state.type !== "all" && node.type !== state.type) {{
        return false;
      }}
      if (!state.search) {{
        return true;
      }}
      const haystack = [node.label, node.path, node.logical_path, node.description]
        .filter(Boolean)
        .join(" ")
        .toLowerCase();
      return haystack.includes(state.search);
    }}

    function visibleNodes() {{
      return nodes.filter(matchesFilter);
    }}

    function visibleNodeIds() {{
      return new Set(visibleNodes().map((node) => node.id));
    }}

    function relatedEdges(nodeId, allowedIds = null) {{
      return edges.filter((edge) => {{
        const touchesNode = edge.from === nodeId || edge.to === nodeId;
        if (!touchesNode) {{
          return false;
        }}
        if (!allowedIds) {{
          return true;
        }}
        return allowedIds.has(edge.from) && allowedIds.has(edge.to);
      }});
    }}

    function renderSidebar(visible) {{
      sidebarEl.innerHTML = "";
      const grouped = new Map(TYPE_ORDER.map((type) => [type, []]));
      visible.forEach((node) => grouped.get(node.type)?.push(node));

      TYPE_ORDER.forEach((type) => {{
        const items = grouped.get(type) || [];
        if (!items.length) {{
          return;
        }}
        const title = document.createElement("div");
        title.className = "group-title";
        title.textContent = TYPE_LABELS[type] || type;
        sidebarEl.appendChild(title);

        items
          .slice()
          .sort((a, b) => a.label.localeCompare(b.label))
          .forEach((node) => {{
            const button = document.createElement("button");
            button.className = "node-button";
            if (node.id === state.selectedId) {{
              button.classList.add("active");
            }}
            const typeStyle = TYPE_STYLES[node.type] || TYPE_STYLES.directory;
            const description = node.description || "No description";
            button.innerHTML = `
              <div class="node-head">
                <strong>${{node.label}}</strong>
                <span class="node-type" style="background:${{typeStyle.badge}}">${{node.type}}</span>
              </div>
              <span class="node-description">${{description}}</span>
              <span class="node-path">${{node.path}}</span>
            `;
            button.addEventListener("click", () => {{
              state.selectedId = node.id;
              render();
            }});
            sidebarEl.appendChild(button);
          }});
      }});
    }}

    function renderDetail(visibleIds) {{
      const selected = nodeById.get(state.selectedId);
      if (!selected || !visibleIds.has(selected.id)) {{
        detailEl.innerHTML = '<p class="empty">從左側或中央地圖選一個節點，即可查看 metadata 與關係。</p>';
        return;
      }}

      const relatedAll = relatedEdges(selected.id);
      const outgoing = relatedAll.filter((edge) => edge.from === selected.id);
      const incoming = relatedAll.filter((edge) => edge.to === selected.id);
      const detailParts = [
        `<h3>${{selected.label}}</h3>`,
        `<p>${{selected.description || "沒有額外描述。"}}</p>`,
        '<div class="meta">',
        `<div class="meta-row"><strong>Type</strong>${{selected.type}}</div>`,
        `<div class="meta-row"><strong>Path</strong>${{selected.path}}</div>`,
      ];

      if (selected.logical_path) {{
        detailParts.push(`<div class="meta-row"><strong>Logical Path</strong>${{selected.logical_path}}</div>`);
      }}
      if (selected.status) {{
        detailParts.push(`<div class="meta-row"><strong>Status</strong>${{selected.status}}</div>`);
      }}
      if (selected.source_path) {{
        detailParts.push(`<div class="meta-row"><strong>Source File</strong>${{selected.source_path}}</div>`);
      }}
      detailParts.push("</div>");

      function pushEdgeSection(title, list, mode) {{
        if (!list.length) {{
          return;
        }}
        detailParts.push(`<div class="section-title">${{title}}</div>`);
        detailParts.push('<div class="edge-list">');
        list
          .slice()
          .sort((a, b) => (EDGE_LABELS[a.kind] || a.kind).localeCompare(EDGE_LABELS[b.kind] || b.kind))
          .forEach((edge) => {{
            const peerId = mode === "outgoing" ? edge.to : edge.from;
            const peer = nodeById.get(peerId);
            if (!peer) {{
              return;
            }}
            const directionText = mode === "outgoing"
              ? `${{selected.label}} → ${{peer.label}}`
              : `${{peer.label}} → ${{selected.label}}`;
            const visible = visibleIds.has(peer.id);
            const visibilityText = visible ? "目前可見於地圖與節點清單" : "目前被搜尋或類型篩選隱藏";
            detailParts.push(
              `<div class="edge-item"><strong>${{EDGE_LABELS[edge.kind] || edge.kind}}</strong><div class="edge-direction">${{directionText}}</div><div>${{peer.path}}</div><div class="edge-visibility">${{visibilityText}}</div></div>`
            );
          }});
        detailParts.push("</div>");
      }}

      if (relatedAll.length) {{
        pushEdgeSection("Outgoing", outgoing, "outgoing");
        pushEdgeSection("Incoming", incoming, "incoming");
      }} else {{
        detailParts.push('<p class="empty">目前篩選條件下沒有可見的關聯邊。</p>');
      }}

      detailEl.innerHTML = detailParts.join("");
    }}

    function layoutNodes(visible) {{
      const grouped = new Map(TYPE_ORDER.map((type) => [type, []]));
      visible.forEach((node) => grouped.get(node.type)?.push(node));

      const columnWidth = 220;
      const baseX = 90;
      const topPadding = 80;
      const rowGap = 82;
      const boxHeight = 52;
      const positions = new Map();
      let maxRows = 0;

      TYPE_ORDER.forEach((type, index) => {{
        const items = (grouped.get(type) || []).slice().sort((a, b) => a.label.localeCompare(b.label));
        maxRows = Math.max(maxRows, items.length);
        items.forEach((node, rowIndex) => {{
          positions.set(node.id, {{
            x: baseX + index * columnWidth,
            y: topPadding + rowIndex * rowGap,
            width: 188,
            height: boxHeight,
            type,
          }});
        }});
      }});

      const width = baseX + TYPE_ORDER.length * columnWidth + 120;
      const height = Math.max(900, topPadding + maxRows * rowGap + 120);
      return {{ positions, width, height }};
    }}

    function renderMap(visible, visibleIds) {{
      const selectedId = state.selectedId;
      const {{ positions, width, height }} = layoutNodes(visible);
      mapEl.setAttribute("viewBox", `0 0 ${{width}} ${{height}}`);
      mapEl.innerHTML = "";

      const titleLayer = document.createElementNS("http://www.w3.org/2000/svg", "g");
      TYPE_ORDER.forEach((type) => {{
        const sample = Array.from(positions.values()).find((entry) => entry.type === type);
        const x = sample ? sample.x : 90 + TYPE_ORDER.indexOf(type) * 220;
        const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
        label.setAttribute("x", String(x));
        label.setAttribute("y", "44");
        label.setAttribute("fill", "#5f5a4b");
        label.setAttribute("font-size", "15");
        label.setAttribute("font-weight", "700");
        label.textContent = TYPE_LABELS[type] || type;
        titleLayer.appendChild(label);
      }});
      mapEl.appendChild(titleLayer);

      const edgeLayer = document.createElementNS("http://www.w3.org/2000/svg", "g");
      edges
        .filter((edge) => visibleIds.has(edge.from) && visibleIds.has(edge.to))
        .forEach((edge) => {{
          const from = positions.get(edge.from);
          const to = positions.get(edge.to);
          if (!from || !to) {{
            return;
          }}
          const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
          line.setAttribute("x1", String(from.x + from.width));
          line.setAttribute("y1", String(from.y + from.height / 2));
          line.setAttribute("x2", String(to.x));
          line.setAttribute("y2", String(to.y + to.height / 2));
          const active = edge.from === selectedId || edge.to === selectedId;
          const style = EDGE_STYLES[edge.kind] || EDGE_STYLES.contains;
          line.setAttribute("stroke", active ? "#0f766e" : style.stroke);
          line.setAttribute("stroke-width", active ? String(style.width + 0.9) : String(style.width));
          line.setAttribute("stroke-opacity", active ? "0.96" : String(style.opacity));
          if (style.dash) {{
            line.setAttribute("stroke-dasharray", style.dash);
          }}
          edgeLayer.appendChild(line);
        }});
      mapEl.appendChild(edgeLayer);

      const nodeLayer = document.createElementNS("http://www.w3.org/2000/svg", "g");
      visible.forEach((node) => {{
        const box = positions.get(node.id);
        if (!box) {{
          return;
        }}
        const active = node.id === selectedId;
        const group = document.createElementNS("http://www.w3.org/2000/svg", "g");
        group.style.cursor = "pointer";
        const typeStyle = TYPE_STYLES[node.type] || TYPE_STYLES.directory;

        const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        rect.setAttribute("x", String(box.x));
        rect.setAttribute("y", String(box.y));
        rect.setAttribute("width", String(box.width));
        rect.setAttribute("height", String(box.height));
        rect.setAttribute("rx", "14");
        rect.setAttribute("fill", active ? "#fffdf7" : typeStyle.fill);
        rect.setAttribute("stroke", active ? "#0f766e" : typeStyle.stroke);
        rect.setAttribute("stroke-width", active ? "2" : "1");
        group.appendChild(rect);

        const accent = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        accent.setAttribute("x", String(box.x));
        accent.setAttribute("y", String(box.y));
        accent.setAttribute("width", "6");
        accent.setAttribute("height", String(box.height));
        accent.setAttribute("rx", "14");
        accent.setAttribute("fill", active ? "#0f766e" : typeStyle.stroke);
        group.appendChild(accent);

        const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
        label.setAttribute("x", String(box.x + 16));
        label.setAttribute("y", String(box.y + 22));
        label.setAttribute("fill", "#1f1f1f");
        label.setAttribute("font-size", "13");
        label.setAttribute("font-weight", active ? "700" : "600");
        label.textContent = node.label.length > 24 ? node.label.slice(0, 23) + "…" : node.label;
        group.appendChild(label);

        const sub = document.createElementNS("http://www.w3.org/2000/svg", "text");
        sub.setAttribute("x", String(box.x + 16));
        sub.setAttribute("y", String(box.y + 39));
        sub.setAttribute("fill", "#6f6a5a");
        sub.setAttribute("font-size", "10.5");
        sub.textContent = `${{TYPE_LABELS[node.type] || node.type}} · ${{node.status || "active"}}`;
        group.appendChild(sub);

        group.addEventListener("click", () => {{
          state.selectedId = node.id;
          render();
        }});

        nodeLayer.appendChild(group);
      }});
      mapEl.appendChild(nodeLayer);
    }}

    function render() {{
      const visible = visibleNodes();
      const ids = new Set(visible.map((node) => node.id));
      if (!ids.has(state.selectedId)) {{
        state.selectedId = visible[0]?.id ?? null;
      }}
      renderSidebar(visible);
      renderMap(visible, ids);
      renderDetail(ids);
    }}

    setupControls();
    render();
  </script>
</body>
</html>
"""


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
