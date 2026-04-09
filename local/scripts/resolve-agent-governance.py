#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class Inputs:
    model: str
    environment: str
    instruction_profile: str


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_policy(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def matches(layer: dict[str, object], inputs: Inputs) -> bool:
    match = layer.get("match", {})
    if not isinstance(match, dict):
        return False

    model_allow = match.get("models")
    if isinstance(model_allow, list) and inputs.model not in model_allow:
        return False

    env_allow = match.get("environments")
    if isinstance(env_allow, list) and inputs.environment not in env_allow:
        return False

    profile_allow = match.get("instruction_profiles")
    if isinstance(profile_allow, list) and inputs.instruction_profile not in profile_allow:
        return False

    return True


def resolve(policy: dict[str, object], inputs: Inputs) -> dict[str, object]:
    meta = policy.get("meta", {})
    precedence = meta.get("precedence", ["base", "model", "environment", "instruction_profile"])
    layers = policy.get("layers", [])

    ordered_matches: list[dict[str, object]] = []
    for scope in precedence:
        for layer in layers:
            if layer.get("scope") != scope:
                continue
            if matches(layer, inputs):
                ordered_matches.append(layer)

    effective: dict[str, object] = {}
    provenance: dict[str, dict[str, object]] = {}
    for layer in ordered_matches:
        layer_id = layer["id"]
        config = layer.get("config", {})
        if not isinstance(config, dict):
            continue
        for key, value in config.items():
            effective[key] = value
            provenance[key] = {
                "value": value,
                "source_layer": layer_id,
                "scope": layer.get("scope"),
            }

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "inputs": {
            "model": inputs.model,
            "environment": inputs.environment,
            "instruction_profile": inputs.instruction_profile,
        },
        "policy_meta": meta,
        "matched_layers": [
            {
                "id": layer["id"],
                "scope": layer.get("scope"),
                "description": layer.get("description"),
                "config": layer.get("config", {}),
            }
            for layer in ordered_matches
        ],
        "effective_config": effective,
        "provenance": provenance,
    }


def render_markdown(resolution: dict[str, object]) -> str:
    inputs = resolution["inputs"]
    lines = [
        "# Agent Governance Resolution",
        "",
        f"- Generated at: `{resolution['generated_at']}`",
        f"- Model: `{inputs['model']}`",
        f"- Environment: `{inputs['environment']}`",
        f"- Instruction profile: `{inputs['instruction_profile']}`",
        "",
        "## Matched Layers",
        "",
    ]

    matched_layers = resolution["matched_layers"]
    if matched_layers:
        for layer in matched_layers:
            lines.extend([
                f"- `{layer['id']}`",
                f"  - Scope: `{layer['scope']}`",
                f"  - Description: {layer['description'] or 'No description'}",
            ])
    else:
        lines.append("- None")

    lines.extend([
        "",
        "## Effective Config",
        "",
    ])
    for key, value in sorted(resolution["effective_config"].items()):
        source = resolution["provenance"][key]["source_layer"]
        lines.append(f"- `{key}` = `{value}` (from `{source}`)")

    lines.extend([
        "",
        "## Resolution Notes",
        "",
        "- Precedence is resolved as `base > model > environment > instruction_profile`, with later layers overriding earlier keys.",
        "- This tool is simulation-first: it reports intended effective configuration but does not mutate runtime settings by itself.",
    ])
    return "\n".join(lines) + "\n"


def write_reports(resolution: dict[str, object], output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "agent-governance-resolution.json"
    md_path = output_dir / "agent-governance-resolution.md"
    json_path.write_text(json.dumps(resolution, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(resolution), encoding="utf-8")
    return json_path, md_path


def main() -> int:
    root = repo_root()
    default_policy = root / "local" / "config" / "agent-governance-layers.json"
    parser = argparse.ArgumentParser(
        description="Resolve effective agent governance from model, work environment, and instruction profile."
    )
    parser.add_argument("--model", required=True, help="Agent model identifier, e.g. gpt-5.4")
    parser.add_argument("--environment", required=True, help="Work environment identifier, e.g. codex-local-dev")
    parser.add_argument("--instruction-profile", required=True, help="Instruction profile identifier, e.g. mapping")
    parser.add_argument("--policy", default=str(default_policy), help="Path to governance layer policy JSON")
    parser.add_argument("--write-report", action="store_true", help="Write JSON and Markdown reports under ops/agent-governance")
    parser.add_argument("--output-dir", default=str(root / "ops" / "agent-governance"), help="Output directory for generated reports")
    args = parser.parse_args()

    policy = load_policy(Path(args.policy).resolve())
    resolution = resolve(
        policy,
        Inputs(
            model=args.model,
            environment=args.environment,
            instruction_profile=args.instruction_profile,
        ),
    )

    summary: dict[str, object] = {"resolution": resolution}
    if args.write_report:
        json_path, md_path = write_reports(resolution, Path(args.output_dir).resolve())
        summary["report_paths"] = {
            "json": str(json_path),
            "markdown": str(md_path),
        }

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
