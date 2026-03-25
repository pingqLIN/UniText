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

import yaml

MAX_SKILL_FILE_BYTES = 256 * 1024
MAX_FRONTMATTER_BYTES = 16 * 1024
ALLOWED_PROPERTIES = {'name', 'description', 'license', 'allowed-tools', 'metadata'}
NAME_PATTERN = re.compile(r'^[a-z0-9-]+$')
INVISIBLE_PATTERN = re.compile(r'[\u200b\u200c\u200d\u2060\ufeff\u00a0\u202a-\u202e]')
FRONTMATTER_PATTERN = re.compile(r'^---\r?\n(.*?)\r?\n---(?:\r?\n|$)', re.DOTALL)


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


def validate_skill(skill_path):
    skill_path = Path(skill_path)
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md not found"

    if skill_md.stat().st_size > MAX_SKILL_FILE_BYTES:
        return False, f"SKILL.md is too large. Maximum is {MAX_SKILL_FILE_BYTES} bytes."

    try:
        content = skill_md.read_text(encoding='utf-8')
    except UnicodeDecodeError as exc:
        return False, f"SKILL.md must be valid UTF-8: {exc}"

    if not content.startswith('---'):
        return False, "No YAML frontmatter found"

    match = FRONTMATTER_PATTERN.match(content)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)
    if len(frontmatter_text.encode('utf-8')) > MAX_FRONTMATTER_BYTES:
        return False, f"Frontmatter is too large. Maximum is {MAX_FRONTMATTER_BYTES} bytes."

    try:
        frontmatter = yaml.load(frontmatter_text, Loader=UniqueKeyLoader)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary"
    except yaml.YAMLError as exc:
        return False, f"Invalid YAML in frontmatter: {exc}"

    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, (
            f"Unexpected key(s) in SKILL.md frontmatter: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed properties are: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    if 'name' not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if 'description' not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    name = frontmatter.get('name', '')
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"
    name = name.strip()
    try:
        name = reject_unsafe_text(name, 'Name')
    except ValueError as exc:
        return False, str(exc)
    if not name:
        return False, "Name cannot be empty"
    if not NAME_PATTERN.match(name):
        return False, f"Name '{name}' should be hyphen-case (lowercase letters, digits, and hyphens only)"
    if name.startswith('-') or name.endswith('-') or '--' in name:
        return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
    if len(name) > 64:
        return False, f"Name is too long ({len(name)} characters). Maximum is 64 characters."

    folder_name = skill_path.name
    try:
        reject_unsafe_text(folder_name, 'Folder name')
    except ValueError as exc:
        return False, str(exc)
    if folder_name != name:
        return False, f"Folder name '{folder_name}' must match frontmatter name '{name}'"

    description = frontmatter.get('description', '')
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"
    description = description.strip()
    try:
        description = reject_unsafe_text(description, 'Description')
    except ValueError as exc:
        return False, str(exc)
    if not description:
        return False, "Description cannot be empty"
    if '<' in description or '>' in description:
        return False, "Description cannot contain angle brackets (< or >)"
    if len(description) > 1024:
        return False, f"Description is too long ({len(description)} characters). Maximum is 1024 characters."

    return True, "Skill is valid!"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Validate a skill directory')
    parser.add_argument('skill_directory')
    parser.add_argument('--json', action='store_true', dest='as_json')
    args = parser.parse_args()

    valid, message = validate_skill(args.skill_directory)
    if args.as_json:
        print(json.dumps({"ok": valid, "message": message}))
    else:
        print(message)
    sys.exit(0 if valid else 1)
