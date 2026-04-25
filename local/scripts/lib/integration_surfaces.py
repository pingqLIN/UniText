from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class IntegrationSurface:
    surface_id: str
    kind: str
    cli_id: str
    resource_types: tuple[str, ...]
    path_scope: str
    path_template: str
    delivery_modes: tuple[str, ...]
    preferred_delivery_resolution: str
    instruction_surface: str
    discovery_surface: str
    runtime_projection_rules: dict[str, object]
    verify_probe: str
    capabilities: dict[str, object]
    preserve_local_extras: bool = False

    def resolve_path(self, *, repo_root: Path, home_dir: Path | None = None) -> Path:
        if self.path_scope == "repo":
            return repo_root / Path(self.path_template)
        if self.path_scope == "home":
            if home_dir is None:
                raise ValueError(f"Surface {self.surface_id} requires a home directory.")
            return home_dir / Path(self.path_template)
        raise ValueError(f"Unsupported path_scope for {self.surface_id}: {self.path_scope}")


def manifest_path(repo_root: Path) -> Path:
    return repo_root / "local" / "config" / "integration-surfaces.json"


def load_integration_surfaces(repo_root: Path) -> tuple[Path, list[IntegrationSurface]]:
    path = manifest_path(repo_root)
    body = json.loads(path.read_text(encoding="utf-8"))
    surfaces: list[IntegrationSurface] = []
    for item in body.get("surfaces", []):
        surfaces.append(
            IntegrationSurface(
                surface_id=item["id"],
                kind=item["kind"],
                cli_id=item["cli_id"],
                resource_types=tuple(item.get("resource_types", [])),
                path_scope=item["path_scope"],
                path_template=item["path_template"],
                delivery_modes=tuple(item.get("delivery_modes", [])),
                preferred_delivery_resolution=item["preferred_delivery_resolution"],
                instruction_surface=item.get("instruction_surface", "repo-files"),
                discovery_surface=item.get("discovery_surface", "undocumented"),
                runtime_projection_rules=dict(item.get("runtime_projection_rules", {})),
                verify_probe=item.get("verify_probe", "undocumented"),
                capabilities=dict(item.get("capabilities", {})),
                preserve_local_extras=bool(item.get("preserve_local_extras", False)),
            )
        )
    return path, surfaces


def surfaces_by_kind(surfaces: list[IntegrationSurface], kind: str) -> list[IntegrationSurface]:
    return [surface for surface in surfaces if surface.kind == kind]


def find_surface(surfaces: list[IntegrationSurface], surface_id: str) -> IntegrationSurface:
    for surface in surfaces:
        if surface.surface_id == surface_id:
            return surface
    raise KeyError(f"Unknown integration surface: {surface_id}")


def surfaces_for_resource_type(surfaces: list[IntegrationSurface], resource_type: str) -> list[IntegrationSurface]:
    return [surface for surface in surfaces if resource_type in surface.resource_types]


def cli_ids_for_resource_type(surfaces: list[IntegrationSurface], resource_type: str) -> list[str]:
    cli_ids: list[str] = []
    for surface in surfaces_for_resource_type(surfaces, resource_type):
        if surface.cli_id in {"runtime", "repo"}:
            continue
        if surface.cli_id not in cli_ids:
            cli_ids.append(surface.cli_id)
    return cli_ids


def default_delivery_guidance(resource_type: str, matched_surfaces: list[IntegrationSurface]) -> str:
    if matched_surfaces:
        surface_ids = ", ".join(surface.surface_id for surface in matched_surfaces)
        return (
            "Use the declared integration surfaces; final delivery depends on the selected "
            f"surface capabilities and local environment. Surfaces: {surface_ids}."
        )
    return (
        f"Use the runtime-first entrypoint for {resource_type} resources. Actual delivery remains "
        "undocumented for this resource type."
    )
