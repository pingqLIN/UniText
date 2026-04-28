#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from lib.integration_surfaces import (
    cli_ids_for_resource_type,
    default_delivery_guidance,
    load_integration_surfaces,
    surfaces_for_resource_type,
)


REPO_MARKERS = [
    Path("README.md"),
    Path("INDEX.md"),
    Path("registry") / "skills",
    Path("registry") / "agents",
    Path("registry") / "workflow",
]

FRONTMATTER_PATTERN = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)
LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
MANAGED_RUNTIME_PATHS = ("catalog.json", "skills", "agents", "workflow")
PAYLOAD_RUNTIME_DIRS = {"skills", "agents", "workflow"}
DIFF_SAMPLE_LIMIT = 25


@dataclass(frozen=True)
class RuntimeEntry:
    resource_id: str
    resource_type: str
    runtime_path: str
    source_of_truth: str
    canonical_location: str
    status: str | None
    supported_clis: list[str]
    delivery_guidance: str
    available_surfaces: list[str]
    entrypoint: str
    intent_tags: list[str]
    consumer_scope: str
    hot_path: bool
    registry_access: str

    def as_dict(self) -> dict[str, object]:
        return {
            "id": self.resource_id,
            "type": self.resource_type,
            "runtime_path": self.runtime_path,
            "source_of_truth": self.source_of_truth,
            "canonical_location": self.canonical_location,
            "status": self.status,
            "supported_clis": self.supported_clis,
            "delivery_guidance": self.delivery_guidance,
            "available_surfaces": self.available_surfaces,
            "entrypoint": self.entrypoint,
            "intent_tags": self.intent_tags,
            "consumer_scope": self.consumer_scope,
            "hot_path": self.hot_path,
            "registry_access": self.registry_access,
        }


def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def validate_repo_root(repo_root: Path) -> None:
    missing = [str(marker) for marker in REPO_MARKERS if not (repo_root / marker).exists()]
    if missing:
        raise SystemExit(f"repo root is missing required markers: {', '.join(missing)}")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = FRONTMATTER_PATTERN.match(text)
    if not match:
        return {}, text

    fields: dict[str, str] = {}
    for raw_line in match.group(1).splitlines():
        line = raw_line.strip()
        if not line or ":" not in line:
            continue
        key, raw_value = line.split(":", 1)
        fields[key.strip()] = raw_value.strip().strip("'").strip('"')
    return fields, text[match.end() :]


def split_frontmatter_block(text: str) -> tuple[str | None, str]:
    match = FRONTMATTER_PATTERN.match(text)
    if not match:
        return None, text
    return match.group(1), text[match.end() :]


def repo_relative(path: Path, repo_root: Path) -> str:
    return path.relative_to(repo_root).as_posix()


def runtime_projection_display_path(runtime_file: Path, repo_root: Path) -> str:
    return repo_relative(runtime_projection_logical_path(runtime_file, repo_root), repo_root)


def runtime_projection_logical_path(path: Path, repo_root: Path) -> Path:
    relative_parts = Path(repo_relative(path, repo_root)).parts
    if "runtime" in relative_parts:
        runtime_index = relative_parts.index("runtime")
        logical_parts = list(relative_parts[runtime_index + 1 :])
        if logical_parts and logical_parts[0].startswith(".runtime-dryrun-"):
            logical_parts = logical_parts[1:]
        return repo_root / "runtime" / Path(*logical_parts)
    return path


def logical_runtime_projection_target(path: Path, repo_root: Path) -> Path:
    runtime_root = repo_root / "runtime"
    try:
        path.relative_to(runtime_root)
    except ValueError:
        return path
    return runtime_projection_logical_path(path, repo_root)


def rewrite_relative_links(
    text: str,
    *,
    source_file: Path,
    wrapper_dir: Path,
    repo_root: Path,
    source_root: Path | None = None,
    runtime_root: Path | None = None,
) -> str:
    logical_wrapper_dir = runtime_projection_logical_path(wrapper_dir, repo_root)

    def replace(match: re.Match[str]) -> str:
        label = match.group(1)
        raw_target = match.group(2).strip()
        if not raw_target:
            return match.group(0)

        if "#" in raw_target:
            target, anchor = raw_target.split("#", 1)
            anchor_suffix = f"#{anchor}"
        else:
            target = raw_target
            anchor_suffix = ""

        if not target:
            return f"[{label}]({anchor_suffix})" if anchor_suffix else match.group(0)

        if target.startswith(("#", "http://", "https://", "mailto:", "file:", "vscode:")):
            return match.group(0)

        resolved = (source_file.parent / target).resolve()
        try:
            resolved.relative_to(repo_root)
        except ValueError:
            return match.group(0)

        if source_root is not None and runtime_root is not None:
            try:
                resource_relative = resolved.relative_to(source_root)
            except ValueError:
                runtime_resolved = resolved
            else:
                runtime_resolved = runtime_root / resource_relative
        else:
            runtime_resolved = resolved

        logical_target = logical_runtime_projection_target(runtime_resolved, repo_root)
        replacement = Path(os.path.relpath(logical_target, logical_wrapper_dir)).as_posix()
        return f"[{label}]({replacement}{anchor_suffix})"

    return LINK_PATTERN.sub(replace, text)


def build_projection_preamble(
    *,
    source_file: Path,
    runtime_file: Path,
    repo_root: Path,
    resource_type: str,
) -> str:
    source_relative = repo_relative(source_file, repo_root)
    runtime_relative = runtime_projection_display_path(runtime_file, repo_root)
    return "\n".join(
        [
            f"> Runtime projection for consumer agents.",
            f"> First-read entrypoint: `{runtime_relative}`",
            f"> Source of truth: `{source_relative}`",
            f"> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.",
            f"> Consumer scope: `{resource_type}`",
            "",
        ]
    )


def render_runtime_markdown(
    *,
    source_file: Path,
    runtime_file: Path,
    repo_root: Path,
    resource_type: str,
    source_root: Path | None = None,
    runtime_root: Path | None = None,
) -> str:
    original = source_file.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(original)
    raw_frontmatter, raw_body = split_frontmatter_block(original)
    preamble = build_projection_preamble(
        source_file=source_file,
        runtime_file=runtime_file,
        repo_root=repo_root,
        resource_type=resource_type,
    )
    rewritten_body = rewrite_relative_links(
        raw_body,
        source_file=source_file,
        wrapper_dir=runtime_file.parent,
        repo_root=repo_root,
        source_root=source_root,
        runtime_root=runtime_root,
    )

    if raw_frontmatter is None:
        frontmatter_lines = [
            "---",
            "runtime_projection: true",
            f"source_of_truth: {repo_relative(source_file, repo_root)}",
            "---",
        ]
        frontmatter_block = "\n".join(frontmatter_lines)
    else:
        frontmatter_lines = ["---", raw_frontmatter.rstrip()]
        if "runtime_projection:" not in raw_frontmatter:
            frontmatter_lines.append("runtime_projection: true")
        if "source_of_truth:" not in raw_frontmatter:
            frontmatter_lines.append(f"source_of_truth: {repo_relative(source_file, repo_root)}")
        frontmatter_lines.append("---")
        frontmatter_block = "\n".join(frontmatter_lines)

    return f"{frontmatter_block}\n\n{preamble}{rewritten_body.lstrip()}"


def slug_tags(text: str) -> list[str]:
    tokens = re.findall(r"[a-z0-9][a-z0-9-]+", text.lower())
    seen: list[str] = []
    for token in tokens:
        if token not in seen:
            seen.append(token)
    return seen[:8]


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")


def project_markdown_tree(
    *,
    source_root: Path,
    runtime_root: Path,
    repo_root: Path,
    resource_type: str,
    entrypoint_name: str,
) -> None:
    for source_file in sorted(source_root.rglob("*.md")):
        if source_file.name.startswith(".") or source_file.name == entrypoint_name:
            continue
        runtime_file = runtime_root / source_file.relative_to(source_root)
        rendered = render_runtime_markdown(
            source_file=source_file,
            runtime_file=runtime_file,
            repo_root=repo_root,
            resource_type=resource_type,
            source_root=source_root,
            runtime_root=runtime_root,
        )
        write_text(runtime_file, rendered)


def load_catalog_exclusions(repo_root: Path) -> set[str]:
    exclusions_path = repo_root / "registry" / "catalog-exclusions.json"
    if not exclusions_path.exists():
        return set()

    body = json.loads(exclusions_path.read_text(encoding="utf-8"))
    skills = body.get("skills", {})
    if not isinstance(skills, dict):
        return set()
    return set(skills.keys())


def canonical_location_for(resource_type: str, resource_id: str) -> str:
    roots = {
        "skill": "skills",
        "agent": "agents",
        "workflow": "workflow",
    }
    return f"/registry/{roots[resource_type]}/{resource_id}"


def metadata_from_frontmatter(
    frontmatter: dict[str, str],
    *,
    resource_type: str,
    matched_surfaces: list[object],
) -> tuple[str | None, list[str], str]:
    status = frontmatter.get("status") or None
    supported_clis_raw = frontmatter.get("supported_clis", "")
    if supported_clis_raw:
        supported_clis = [item.strip() for item in supported_clis_raw.split(",") if item.strip()]
    else:
        supported_clis = cli_ids_for_resource_type(matched_surfaces, resource_type)
    delivery_guidance = frontmatter.get("delivery_guidance") or default_delivery_guidance(resource_type, matched_surfaces)
    return status, supported_clis, delivery_guidance


def build_skill_wrappers(repo_root: Path, runtime_root: Path, integration_surfaces: list[object]) -> list[RuntimeEntry]:
    runtime_skills_root = runtime_root / "skills"
    if runtime_skills_root.exists():
        shutil.rmtree(runtime_skills_root)
    runtime_skills_root.mkdir(parents=True, exist_ok=True)

    entries: list[RuntimeEntry] = []
    excluded_skills = load_catalog_exclusions(repo_root)
    for skill_dir in sorted((repo_root / "registry" / "skills").iterdir()):
        if not skill_dir.is_dir() or skill_dir.name.startswith("."):
            continue
        if skill_dir.name in excluded_skills:
            continue
        source_file = skill_dir / "SKILL.md"
        if not source_file.exists():
            continue
        runtime_file = runtime_skills_root / skill_dir.name / "SKILL.md"
        rendered = render_runtime_markdown(
            source_file=source_file,
            runtime_file=runtime_file,
            repo_root=repo_root,
            resource_type="skill",
            source_root=skill_dir,
            runtime_root=runtime_file.parent,
        )
        write_text(runtime_file, rendered)
        project_markdown_tree(
            source_root=skill_dir,
            runtime_root=runtime_file.parent,
            repo_root=repo_root,
            resource_type="skill-support",
            entrypoint_name="SKILL.md",
        )
        frontmatter, body = parse_frontmatter(source_file.read_text(encoding="utf-8"))
        matched_surfaces = surfaces_for_resource_type(integration_surfaces, "skill")
        status, supported_clis, delivery_guidance = metadata_from_frontmatter(
            frontmatter,
            resource_type="skill",
            matched_surfaces=matched_surfaces,
        )
        summary_source = " ".join(filter(None, [frontmatter.get("name", ""), frontmatter.get("description", ""), body[:400]]))
        entries.append(
            RuntimeEntry(
                resource_id=skill_dir.name,
                resource_type="skill",
                runtime_path=runtime_projection_display_path(runtime_file, repo_root),
                source_of_truth=repo_relative(source_file, repo_root),
                canonical_location=canonical_location_for("skill", skill_dir.name),
                status=status,
                supported_clis=supported_clis,
                delivery_guidance=delivery_guidance,
                available_surfaces=[surface.surface_id for surface in matched_surfaces],
                entrypoint=runtime_projection_display_path(runtime_file, repo_root),
                intent_tags=slug_tags(summary_source),
                consumer_scope="runtime-first",
                hot_path=skill_dir.name in {"env", "cloudflare-governance", "doc-coauthoring", "frontend-design", "webapp-testing"},
                registry_access="runtime-first-then-linked-registry",
            )
        )
    return entries


def build_agent_wrappers(repo_root: Path, runtime_root: Path, integration_surfaces: list[object]) -> list[RuntimeEntry]:
    runtime_agents_root = runtime_root / "agents"
    if runtime_agents_root.exists():
        shutil.rmtree(runtime_agents_root)
    runtime_agents_root.mkdir(parents=True, exist_ok=True)

    entries: list[RuntimeEntry] = []
    for agent_dir in sorted((repo_root / "registry" / "agents").iterdir()):
        if not agent_dir.is_dir() or agent_dir.name.startswith("."):
            continue
        source_file = agent_dir / "AGENT.md"
        if not source_file.exists():
            continue
        runtime_file = runtime_agents_root / agent_dir.name / "AGENT.md"
        rendered = render_runtime_markdown(
            source_file=source_file,
            runtime_file=runtime_file,
            repo_root=repo_root,
            resource_type="agent",
            source_root=agent_dir,
            runtime_root=runtime_file.parent,
        )
        write_text(runtime_file, rendered)
        project_markdown_tree(
            source_root=agent_dir,
            runtime_root=runtime_file.parent,
            repo_root=repo_root,
            resource_type="agent-support",
            entrypoint_name="AGENT.md",
        )
        frontmatter, body = parse_frontmatter(source_file.read_text(encoding="utf-8"))
        matched_surfaces = surfaces_for_resource_type(integration_surfaces, "agent")
        status, supported_clis, delivery_guidance = metadata_from_frontmatter(
            frontmatter,
            resource_type="agent",
            matched_surfaces=matched_surfaces,
        )
        summary_source = " ".join(filter(None, [frontmatter.get("name", ""), frontmatter.get("description", ""), body[:400]]))
        entries.append(
            RuntimeEntry(
                resource_id=agent_dir.name,
                resource_type="agent",
                runtime_path=runtime_projection_display_path(runtime_file, repo_root),
                source_of_truth=repo_relative(source_file, repo_root),
                canonical_location=canonical_location_for("agent", agent_dir.name),
                status=status,
                supported_clis=supported_clis,
                delivery_guidance=delivery_guidance,
                available_surfaces=[surface.surface_id for surface in matched_surfaces],
                entrypoint=runtime_projection_display_path(runtime_file, repo_root),
                intent_tags=slug_tags(summary_source),
                consumer_scope="runtime-first",
                hot_path=agent_dir.name == "registry-curator",
                registry_access="runtime-first-then-linked-registry",
            )
        )
    return entries


def build_workflow_wrappers(repo_root: Path, runtime_root: Path, integration_surfaces: list[object]) -> list[RuntimeEntry]:
    runtime_workflow_root = runtime_root / "workflow"
    if runtime_workflow_root.exists():
        shutil.rmtree(runtime_workflow_root)
    runtime_workflow_root.mkdir(parents=True, exist_ok=True)

    entries: list[RuntimeEntry] = []
    for workflow_dir in sorted((repo_root / "registry" / "workflow").iterdir()):
        if not workflow_dir.is_dir() or workflow_dir.name.startswith("."):
            continue
        source_file = workflow_dir / "WORKFLOW.md"
        if not source_file.exists():
            continue
        runtime_file = runtime_workflow_root / workflow_dir.name / "WORKFLOW.md"
        rendered = render_runtime_markdown(
            source_file=source_file,
            runtime_file=runtime_file,
            repo_root=repo_root,
            resource_type="workflow",
            source_root=workflow_dir,
            runtime_root=runtime_file.parent,
        )
        write_text(runtime_file, rendered)
        project_markdown_tree(
            source_root=workflow_dir,
            runtime_root=runtime_file.parent,
            repo_root=repo_root,
            resource_type="workflow-support",
            entrypoint_name="WORKFLOW.md",
        )
        frontmatter, body = parse_frontmatter(source_file.read_text(encoding="utf-8"))
        matched_surfaces = surfaces_for_resource_type(integration_surfaces, "workflow")
        status, supported_clis, delivery_guidance = metadata_from_frontmatter(
            frontmatter,
            resource_type="workflow",
            matched_surfaces=matched_surfaces,
        )
        entries.append(
            RuntimeEntry(
                resource_id=workflow_dir.name,
                resource_type="workflow",
                runtime_path=runtime_projection_display_path(runtime_file, repo_root),
                source_of_truth=repo_relative(source_file, repo_root),
                canonical_location=canonical_location_for("workflow", workflow_dir.name),
                status=status,
                supported_clis=supported_clis,
                delivery_guidance=delivery_guidance,
                available_surfaces=[surface.surface_id for surface in matched_surfaces],
                entrypoint=runtime_projection_display_path(runtime_file, repo_root),
                intent_tags=slug_tags(body[:400]),
                consumer_scope="runtime-first",
                hot_path=False,
                registry_access="runtime-first-then-linked-registry",
            )
        )
    return entries


def write_catalog(repo_root: Path, runtime_root: Path, entries: list[RuntimeEntry], integration_manifest: Path) -> None:
    catalog = {
        "meta": {
            "catalog_version": 2,
            "generated_by": "local/scripts/build-runtime-layer.py",
            "description": "Tracked runtime read model for consumer agents.",
            "source_of_truth_root": "registry/",
            "integration_surfaces_manifest": repo_relative(integration_manifest, repo_root),
        },
        "entries": [entry.as_dict() for entry in sorted(entries, key=lambda item: (item.resource_type, item.resource_id))],
    }
    write_text(runtime_root / "catalog.json", json.dumps(catalog, indent=2, ensure_ascii=False))


def managed_runtime_files(root: Path) -> dict[str, Path]:
    files: dict[str, Path] = {}
    for managed_path in MANAGED_RUNTIME_PATHS:
        candidate = root / managed_path
        if candidate.is_file():
            files[managed_path] = candidate
            continue
        if not candidate.is_dir():
            continue
        for file_path in sorted(candidate.rglob("*")):
            if not file_path.is_file():
                continue
            relative = file_path.relative_to(root)
            if any(part.startswith(".") for part in relative.parts):
                continue
            files[relative.as_posix()] = file_path
    return files


def is_payload_runtime_path(relative_path: str) -> bool:
    first_part = Path(relative_path).parts[0]
    return first_part in PAYLOAD_RUNTIME_DIRS


def summarize_paths(paths: list[str]) -> dict[str, object]:
    return {
        "count": len(paths),
        "sample": paths[:DIFF_SAMPLE_LIMIT],
    }


def normalize_line_endings(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def compare_runtime_trees(generated_root: Path, tracked_runtime_root: Path) -> dict[str, object]:
    generated_files = managed_runtime_files(generated_root)
    tracked_files = managed_runtime_files(tracked_runtime_root)
    all_paths = sorted(set(generated_files) | set(tracked_files))

    added: list[str] = []
    changed: list[str] = []
    line_ending_only: list[str] = []
    content_changed: list[str] = []
    removed: list[str] = []
    for relative_path in all_paths:
        generated_file = generated_files.get(relative_path)
        tracked_file = tracked_files.get(relative_path)
        if generated_file is None:
            removed.append(relative_path)
            continue
        if tracked_file is None:
            added.append(relative_path)
            continue
        generated_bytes = generated_file.read_bytes()
        tracked_bytes = tracked_file.read_bytes()
        if generated_bytes != tracked_bytes:
            changed.append(relative_path)
            if normalize_line_endings(generated_bytes) == normalize_line_endings(tracked_bytes):
                line_ending_only.append(relative_path)
            else:
                content_changed.append(relative_path)

    payload_paths = [path for path in added + changed + removed if is_payload_runtime_path(path)]
    payload_content_paths = [path for path in added + content_changed + removed if is_payload_runtime_path(path)]
    payload_line_ending_paths = [path for path in line_ending_only if is_payload_runtime_path(path)]
    catalog_paths = [path for path in added + changed + removed if path == "catalog.json"]
    blocking_payload_paths = payload_content_paths
    routine_write_allowed = not blocking_payload_paths

    return {
        "compared_against": str(tracked_runtime_root),
        "managed_paths": list(MANAGED_RUNTIME_PATHS),
        "status": "clean" if not added and not changed and not removed else "drift",
        "generated_file_count": len(generated_files),
        "tracked_file_count": len(tracked_files),
        "added_by_generator": summarize_paths(added),
        "changed_by_generator": summarize_paths(changed),
        "content_changed_by_generator": summarize_paths(content_changed),
        "line_ending_only_drift": summarize_paths(line_ending_only),
        "stale_tracked_runtime_files": summarize_paths(removed),
        "payload_drift": summarize_paths(payload_paths),
        "blocking_payload_drift": summarize_paths(blocking_payload_paths),
        "payload_content_drift": summarize_paths(payload_content_paths),
        "payload_line_ending_only_drift": summarize_paths(payload_line_ending_paths),
        "catalog_drift": summarize_paths(catalog_paths),
        "write_gate": {
            "strategy": "no-payload-content-drift",
            "routine_write_allowed": routine_write_allowed,
            "requires_review": not routine_write_allowed,
            "reason": (
                "managed payload files have added, removed, or content-level drift that still requires review"
                if not routine_write_allowed
                else "only line-ending-only drift or catalog-only drift remains in managed runtime files"
            ),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the tracked runtime layer for consumer agents.")
    parser.add_argument("--write", action="store_true", help="Write the runtime layer into the repository.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Optional output directory for generated runtime files. Without --write this becomes a dry-run target.",
    )
    args = parser.parse_args()

    repo_root = get_repo_root()
    validate_repo_root(repo_root)
    if args.output_dir is None:
        runtime_root = repo_root / "runtime"
    else:
        runtime_root = args.output_dir
        if not runtime_root.is_absolute():
            runtime_root = (repo_root / runtime_root).resolve()

    if args.output_dir is not None:
        try:
            runtime_root.relative_to(repo_root.resolve())
        except ValueError:
            print(
                json.dumps(
                    {
                        "error": "output-dir must be inside the repository root when used with build-runtime-layer.py.",
                    },
                    indent=2,
                    ensure_ascii=False,
                )
            )
            return 1
    integration_manifest, integration_surfaces = load_integration_surfaces(repo_root)

    if not args.write:
        if args.output_dir is not None:
            if runtime_root.resolve() == (repo_root / "runtime").resolve():
                print(
                    json.dumps(
                        {
                            "error": "Dry-run output-dir may not target runtime/. Use --write to update tracked runtime.",
                        },
                        indent=2,
                        ensure_ascii=False,
                    )
                )
                return 1

            if runtime_root.exists():
                shutil.rmtree(runtime_root)
            entries: list[RuntimeEntry] = []
            entries.extend(build_skill_wrappers(repo_root, runtime_root, integration_surfaces))
            entries.extend(build_agent_wrappers(repo_root, runtime_root, integration_surfaces))
            entries.extend(build_workflow_wrappers(repo_root, runtime_root, integration_surfaces))
            write_catalog(repo_root, runtime_root, entries, integration_manifest)
            summary = {
                "repo_root": str(repo_root),
                "runtime_root": str(runtime_root),
                "integration_surfaces_manifest": str(integration_manifest),
                "dry_run": True,
                "output_dir_scope": "repository-relative",
                "actions": [
                    "rebuild runtime/skills from registry/skills",
                    "rebuild runtime/agents from registry/agents",
                    "rebuild runtime/workflow from registry/workflow",
                    "rewrite relative links back to registry source files",
                    "refresh runtime/catalog.json with integration surface metadata",
                ],
                "skills": len([entry for entry in entries if entry.resource_type == "skill"]),
                "agents": len([entry for entry in entries if entry.resource_type == "agent"]),
                "workflow": len([entry for entry in entries if entry.resource_type == "workflow"]),
                "catalog_entries": len(entries),
                "diff_summary": compare_runtime_trees(runtime_root, repo_root / "runtime"),
            }
            print(json.dumps(summary, indent=2, ensure_ascii=False))
            return 0

        summary = {
            "repo_root": str(repo_root),
            "runtime_root": str(runtime_root),
            "integration_surfaces_manifest": str(integration_manifest),
            "actions": [
                "rebuild runtime/skills from registry/skills",
                "rebuild runtime/agents from registry/agents",
                "rebuild runtime/workflow from registry/workflow",
                "rewrite relative links back to registry source files",
                "refresh runtime/catalog.json with integration surface metadata",
            ],
        }
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        return 0

    runtime_root.mkdir(parents=True, exist_ok=True)
    entries: list[RuntimeEntry] = []
    entries.extend(build_skill_wrappers(repo_root, runtime_root, integration_surfaces))
    entries.extend(build_agent_wrappers(repo_root, runtime_root, integration_surfaces))
    entries.extend(build_workflow_wrappers(repo_root, runtime_root, integration_surfaces))
    write_catalog(repo_root, runtime_root, entries, integration_manifest)

    summary = {
        "repo_root": str(repo_root),
        "runtime_root": str(runtime_root),
        "integration_surfaces_manifest": str(integration_manifest),
        "skills": len([entry for entry in entries if entry.resource_type == "skill"]),
        "agents": len([entry for entry in entries if entry.resource_type == "agent"]),
        "workflow": len([entry for entry in entries if entry.resource_type == "workflow"]),
        "catalog_entries": len(entries),
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
