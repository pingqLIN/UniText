#!/usr/bin/env python3
"""Quick validation script for skills with machine-readable output."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml


class UniqueKeyLoader(yaml.SafeLoader):
    """YAML loader that rejects duplicate keys in mappings."""


def construct_unique_mapping(loader: UniqueKeyLoader, node: yaml.nodes.MappingNode, deep: bool = False) -> dict[str, Any]:
    mapping: dict[str, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise yaml.YAMLError(f"Duplicate key in frontmatter: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_unique_mapping)


def read_text_file(path: Path) -> str:
    raw = path.read_bytes()
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("utf-8", errors="replace")


def inspect_skill(skill_path: str) -> dict[str, Any]:
    """Read and validate a skill file while preserving parsed metadata."""
    skill_path = Path(skill_path)
    skill_md = skill_path / "SKILL.md"
    result: dict[str, Any] = {
        "skill_path": str(skill_path),
        "skill_md_exists": skill_md.exists(),
        "has_frontmatter": False,
        "frontmatter": None,
        "ok": False,
        "message": "SKILL.md not found",
    }

    if not skill_md.exists():
        return result

    content = read_text_file(skill_md)
    if not content.startswith('---'):
        result["message"] = "No YAML frontmatter found"
        return result

    match = re.match(r'^---\r?\n(.*?)\r?\n---', content, re.DOTALL)
    if not match:
        result["message"] = "Invalid frontmatter format"
        return result

    result["has_frontmatter"] = True
    frontmatter_text = match.group(1)

    try:
        frontmatter = yaml.load(frontmatter_text, Loader=UniqueKeyLoader)
        if not isinstance(frontmatter, dict):
            result["message"] = "Frontmatter must be a YAML dictionary"
            return result
    except yaml.YAMLError as e:
        result["message"] = f"Invalid YAML in frontmatter: {e}"
        return result

    ALLOWED_PROPERTIES = {
        'name',
        'description',
        'license',
        'allowed-tools',
        'metadata',
        'source',
        'category',
        'tags',
        'risk',
        'date_added',
    }
    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        result["message"] = (
            f"Unexpected key(s) in SKILL.md frontmatter: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed properties are: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )
        return result

    if 'name' not in frontmatter:
        result["message"] = "Missing 'name' in frontmatter"
        return result
    if 'description' not in frontmatter:
        result["message"] = "Missing 'description' in frontmatter"
        return result

    name = frontmatter.get('name', '')
    if not isinstance(name, str):
        result["message"] = f"Name must be a string, got {type(name).__name__}"
        return result
    name = name.strip()
    if name:
        if not re.match(r'^[a-z0-9-]+$', name):
            result["message"] = f"Name '{name}' should be hyphen-case (lowercase letters, digits, and hyphens only)"
            return result
        if name.startswith('-') or name.endswith('-') or '--' in name:
            result["message"] = f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
            return result
        if len(name) > 64:
            result["message"] = f"Name is too long ({len(name)} characters). Maximum is 64 characters."
            return result

    description = frontmatter.get('description', '')
    if not isinstance(description, str):
        result["message"] = f"Description must be a string, got {type(description).__name__}"
        return result
    description = description.strip()
    if description:
        if '<' in description or '>' in description:
            result["message"] = "Description cannot contain angle brackets (< or >)"
            return result
        if len(description) > 1024:
            result["message"] = f"Description is too long ({len(description)} characters). Maximum is 1024 characters."
            return result

    result["frontmatter"] = frontmatter
    result["ok"] = True
    result["message"] = "Skill is valid!"
    return result


def validate_skill(skill_path: str) -> tuple[bool, str]:
    """Basic validation of a skill."""
    result = inspect_skill(skill_path)
    return bool(result["ok"]), str(result["message"])


def emit_result(as_json: bool, ok: bool, message: str, metadata: dict[str, Any] | None = None) -> None:
    if as_json:
        payload: dict[str, Any] = {"ok": ok, "message": message}
        if metadata is not None:
            payload.update(metadata)
        print(json.dumps(payload))
        return
    print(message)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate a skill directory")
    parser.add_argument("skill_directory")
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--metadata-json", action="store_true", dest="as_metadata_json")
    args = parser.parse_args()

    report = inspect_skill(args.skill_directory)
    valid = bool(report["ok"])
    message = str(report["message"])
    metadata = report if args.as_metadata_json else None
    emit_result(args.as_json or args.as_metadata_json, valid, message, metadata=metadata)
    sys.exit(0 if valid else 1)
