#!/usr/bin/env python3
"""
Quick validation script for skills.
"""

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError:
    yaml = None

MAX_SKILL_FILE_BYTES = 256 * 1024
MAX_FRONTMATTER_BYTES = 16 * 1024
ALLOWED_PROPERTIES = {'name', 'description', 'license', 'allowed-tools', 'metadata'}
NAME_PATTERN = re.compile(r'^[a-z0-9-]+$')
INVISIBLE_PATTERN = re.compile(r'[\u200b\u200c\u200d\u2060\ufeff\u00a0\u202a-\u202e]')
FRONTMATTER_PATTERN = re.compile(r'^---\r?\n(.*?)\r?\n---(?:\r?\n|$)', re.DOTALL)


if yaml is not None:
    class UniqueKeyLoader(yaml.SafeLoader):
        pass


    def construct_unique_mapping(loader, node, deep=False):
        mapping = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if key in mapping:
                raise yaml.YAMLError(f"Duplicate key in frontmatter: {key}")
            mapping[key] = loader.construct_object(value_node, deep=deep)
        return mapping


    UniqueKeyLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_unique_mapping,
    )


def reject_unsafe_text(value, label):
    normalized = unicodedata.normalize('NFC', value)
    if normalized != value:
        raise ValueError(f"{label} must already be NFC-normalized")
    if INVISIBLE_PATTERN.search(value):
        raise ValueError(f"{label} cannot contain invisible or bidi-control characters")
    return value


def parse_scalar(value):
    value = value.strip()
    if not value:
        return ""
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    return value


def parse_frontmatter_without_yaml(frontmatter_text):
    result = {}
    lines = frontmatter_text.splitlines()
    index = 0
    while index < len(lines):
        raw_line = lines[index]
        if not raw_line.strip():
            index += 1
            continue
        if raw_line.startswith((" ", "\t")):
            raise ValueError("Unsupported frontmatter indentation without PyYAML")

        match = re.match(r"^([A-Za-z0-9_-]+):(.*)$", raw_line)
        if not match:
            raise ValueError(f"Invalid frontmatter line: {raw_line}")

        key = match.group(1)
        if key in result:
            raise ValueError(f"Duplicate key in frontmatter: {key}")

        rest = match.group(2).strip()
        if rest:
            result[key] = parse_scalar(rest)
            index += 1
            continue

        block_lines = []
        index += 1
        while index < len(lines):
            candidate = lines[index]
            if not candidate.strip():
                block_lines.append(candidate)
                index += 1
                continue
            if not candidate.startswith((" ", "\t")):
                break
            block_lines.append(candidate)
            index += 1

        entries = [line for line in block_lines if line.strip()]
        if not entries:
            result[key] = ""
            continue

        if all(re.match(r"^\s*-\s+.+$", line) for line in entries):
            result[key] = [parse_scalar(re.sub(r"^\s*-\s+", "", line, count=1)) for line in entries]
            continue

        if all(re.match(r"^\s+[A-Za-z0-9_-]+:\s*.*$", line) for line in entries):
            nested = {}
            for line in entries:
                nested_match = re.match(r"^\s+([A-Za-z0-9_-]+):\s*(.*)$", line)
                nested_key = nested_match.group(1)
                if nested_key in nested:
                    raise ValueError(f"Duplicate key in frontmatter: {nested_key}")
                nested[nested_key] = parse_scalar(nested_match.group(2))
            result[key] = nested
            continue

        raise ValueError(f"Unsupported frontmatter block for key '{key}' without PyYAML")

    return result


def parse_frontmatter(frontmatter_text):
    if yaml is not None:
        try:
            frontmatter = yaml.load(frontmatter_text, Loader=UniqueKeyLoader)
        except yaml.YAMLError as exc:
            raise ValueError(f"Invalid YAML in frontmatter: {exc}") from exc
        if not isinstance(frontmatter, dict):
            raise ValueError("Frontmatter must be a YAML dictionary")
        return frontmatter
    return parse_frontmatter_without_yaml(frontmatter_text)


def build_result(skill_path, ok, message, *, frontmatter=None, has_frontmatter=False):
    skill_path = Path(skill_path)
    result = {
        "ok": ok,
        "message": message,
        "id": skill_path.name,
        "path": str(skill_path),
        "canonical_location": f"/registry/skills/{skill_path.name}",
        "has_skill_md": (skill_path / "SKILL.md").exists(),
        "has_frontmatter": has_frontmatter,
        "name": None,
        "description": None,
    }
    if isinstance(frontmatter, dict):
        name = frontmatter.get("name")
        description = frontmatter.get("description")
        if isinstance(name, str):
            result["name"] = name.strip()
        if isinstance(description, str):
            result["description"] = description.strip()
    result["has_description"] = bool(result["description"])
    return result


def validate_skill_details(skill_path):
    skill_path = Path(skill_path)
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return build_result(skill_path, False, "SKILL.md not found")

    if skill_md.stat().st_size > MAX_SKILL_FILE_BYTES:
        return build_result(skill_path, False, f"SKILL.md is too large. Maximum is {MAX_SKILL_FILE_BYTES} bytes.")

    try:
        content = skill_md.read_text(encoding='utf-8')
    except UnicodeDecodeError as exc:
        return build_result(skill_path, False, f"SKILL.md must be valid UTF-8: {exc}")

    if not content.startswith('---'):
        return build_result(skill_path, False, "No YAML frontmatter found")

    match = FRONTMATTER_PATTERN.match(content)
    if not match:
        return build_result(skill_path, False, "Invalid frontmatter format", has_frontmatter=True)

    frontmatter_text = match.group(1)
    if len(frontmatter_text.encode('utf-8')) > MAX_FRONTMATTER_BYTES:
        return build_result(
            skill_path,
            False,
            f"Frontmatter is too large. Maximum is {MAX_FRONTMATTER_BYTES} bytes.",
            has_frontmatter=True,
        )

    try:
        frontmatter = parse_frontmatter(frontmatter_text)
    except ValueError as exc:
        return build_result(skill_path, False, str(exc), has_frontmatter=True)

    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return build_result(
            skill_path,
            False,
            (
                f"Unexpected key(s) in SKILL.md frontmatter: {', '.join(sorted(unexpected_keys))}. "
                f"Allowed properties are: {', '.join(sorted(ALLOWED_PROPERTIES))}"
            ),
            frontmatter=frontmatter,
            has_frontmatter=True,
        )

    if 'name' not in frontmatter:
        return build_result(skill_path, False, "Missing 'name' in frontmatter", frontmatter=frontmatter, has_frontmatter=True)
    if 'description' not in frontmatter:
        return build_result(
            skill_path,
            False,
            "Missing 'description' in frontmatter",
            frontmatter=frontmatter,
            has_frontmatter=True,
        )

    name = frontmatter.get('name', '')
    if not isinstance(name, str):
        return build_result(
            skill_path,
            False,
            f"Name must be a string, got {type(name).__name__}",
            frontmatter=frontmatter,
            has_frontmatter=True,
        )
    name = name.strip()
    try:
        name = reject_unsafe_text(name, 'Name')
    except ValueError as exc:
        return build_result(skill_path, False, str(exc), frontmatter=frontmatter, has_frontmatter=True)
    if not name:
        return build_result(skill_path, False, "Name cannot be empty", frontmatter=frontmatter, has_frontmatter=True)
    if not NAME_PATTERN.match(name):
        return build_result(
            skill_path,
            False,
            f"Name '{name}' should be hyphen-case (lowercase letters, digits, and hyphens only)",
            frontmatter=frontmatter,
            has_frontmatter=True,
        )
    if name.startswith('-') or name.endswith('-') or '--' in name:
        return build_result(
            skill_path,
            False,
            f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens",
            frontmatter=frontmatter,
            has_frontmatter=True,
        )
    if len(name) > 64:
        return build_result(
            skill_path,
            False,
            f"Name is too long ({len(name)} characters). Maximum is 64 characters.",
            frontmatter=frontmatter,
            has_frontmatter=True,
        )

    folder_name = skill_path.name
    try:
        reject_unsafe_text(folder_name, 'Folder name')
    except ValueError as exc:
        return build_result(skill_path, False, str(exc), frontmatter=frontmatter, has_frontmatter=True)
    if folder_name != name:
        return build_result(
            skill_path,
            False,
            f"Folder name '{folder_name}' must match frontmatter name '{name}'",
            frontmatter=frontmatter,
            has_frontmatter=True,
        )

    description = frontmatter.get('description', '')
    if not isinstance(description, str):
        return build_result(
            skill_path,
            False,
            f"Description must be a string, got {type(description).__name__}",
            frontmatter=frontmatter,
            has_frontmatter=True,
        )
    description = description.strip()
    try:
        description = reject_unsafe_text(description, 'Description')
    except ValueError as exc:
        return build_result(skill_path, False, str(exc), frontmatter=frontmatter, has_frontmatter=True)
    if not description:
        return build_result(
            skill_path,
            False,
            "Description cannot be empty",
            frontmatter=frontmatter,
            has_frontmatter=True,
        )
    if '<' in description or '>' in description:
        return build_result(
            skill_path,
            False,
            "Description cannot contain angle brackets (< or >)",
            frontmatter=frontmatter,
            has_frontmatter=True,
        )
    if len(description) > 1024:
        return build_result(
            skill_path,
            False,
            f"Description is too long ({len(description)} characters). Maximum is 1024 characters.",
            frontmatter=frontmatter,
            has_frontmatter=True,
        )

    return build_result(
        skill_path,
        True,
        "Skill is valid!",
        frontmatter=frontmatter,
        has_frontmatter=True,
    )


def validate_skill(skill_path):
    result = validate_skill_details(skill_path)
    return result["ok"], result["message"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Validate a skill directory')
    parser.add_argument('skill_directory')
    parser.add_argument('--json', action='store_true', dest='as_json')
    args = parser.parse_args()

    result = validate_skill_details(args.skill_directory)
    if args.as_json:
        print(json.dumps(result))
    else:
        print(result["message"])
    sys.exit(0 if result["ok"] else 1)
