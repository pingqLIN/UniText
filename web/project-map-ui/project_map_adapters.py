from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


RootDirectory = tuple[str, str, str]


UNITEXT_REPO_MARKERS = (
    Path("README.md"),
    Path("INDEX.md"),
    Path("registry") / "skills",
    Path("registry") / "mcp",
)

GOVERNANCE_ROOT_MARKERS = (
    Path("AGENTS.md"),
    Path("local") / "config" / "agent-governance-layers.json",
    Path("runtime") / "catalog.json",
    Path("registry") / "skills",
    Path("registry") / "mcp",
    Path("registry") / "agents",
    Path("registry") / "workflow",
)

UNITEXT_CORE_DOCS = (
    "README.md",
    "INDEX.md",
    "VISION.md",
    "RESOURCE_SPEC.md",
    "OPERATIONS.md",
    "PROJECT_MODES.md",
    "DOCUMENT_PLACEMENT_POLICY.md",
    "WORKSPACE_SENSITIVE_METADATA_RULES.md",
    "docs/project-map/PROJECT_MAP_WEB_AUTOMATION_REPORT.md",
)

GOVERNANCE_CORE_DOCS = (
    "README.md",
    "AGENTS.md",
    "INDEX.md",
    "VISION.md",
    "RESOURCE_SPEC.md",
    "OPERATIONS.md",
)

REGISTRY_ROOT_DIRECTORIES: tuple[RootDirectory, ...] = (
    ("registry/skills", "skills", "/registry/skills"),
    ("registry/mcp", "mcp", "/registry/mcp"),
    ("registry/agents", "agents", "/registry/agents"),
    ("registry/workflow", "workflow", "/registry/workflow"),
)


@dataclass(frozen=True)
class ProjectMapAdapter:
    adapter_id: str
    label: str
    description: str
    root_markers: tuple[Path, ...]
    core_docs: tuple[str, ...]
    root_directories: tuple[RootDirectory, ...]
    default_governance_policy: str = "local/config/agent-governance-layers.json"

    def markers_present(self, root: Path) -> list[str]:
        return [marker.as_posix() for marker in self.root_markers if (root / marker).exists()]

    def markers_missing(self, root: Path) -> list[str]:
        return [marker.as_posix() for marker in self.root_markers if not (root / marker).exists()]

    def matches(self, root: Path) -> bool:
        return bool(self.markers_present(root))

    def as_dict(self) -> dict[str, object]:
        return {
            "adapter_id": self.adapter_id,
            "label": self.label,
            "description": self.description,
            "root_markers": [marker.as_posix() for marker in self.root_markers],
            "core_docs": list(self.core_docs),
            "root_directories": [list(directory) for directory in self.root_directories],
            "default_governance_policy": self.default_governance_policy,
        }


UNITEXT_ADAPTER = ProjectMapAdapter(
    adapter_id="unitext",
    label="UniText repository",
    description="Full UniText repository adapter with canonical registry roots and core project documents.",
    root_markers=UNITEXT_REPO_MARKERS,
    core_docs=UNITEXT_CORE_DOCS,
    root_directories=REGISTRY_ROOT_DIRECTORIES,
)

GOVERNANCE_FOLDER_ADAPTER = ProjectMapAdapter(
    adapter_id="governance-folder",
    label="Governance folder",
    description="Generic governance folder adapter for project roots, research folders, and AGENTS-led workspaces.",
    root_markers=GOVERNANCE_ROOT_MARKERS,
    core_docs=GOVERNANCE_CORE_DOCS,
    root_directories=REGISTRY_ROOT_DIRECTORIES,
)

PROJECT_MAP_ADAPTERS = (
    UNITEXT_ADAPTER,
    GOVERNANCE_FOLDER_ADAPTER,
)


def select_project_map_adapter(root: Path) -> ProjectMapAdapter | None:
    unitext_present = UNITEXT_ADAPTER.markers_present(root)
    if len(unitext_present) == len(UNITEXT_ADAPTER.root_markers):
        return UNITEXT_ADAPTER
    if GOVERNANCE_FOLDER_ADAPTER.matches(root):
        return GOVERNANCE_FOLDER_ADAPTER
    return None


def project_map_adapters_as_dicts() -> list[dict[str, object]]:
    return [adapter.as_dict() for adapter in PROJECT_MAP_ADAPTERS]
