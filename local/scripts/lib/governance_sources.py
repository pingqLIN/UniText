from __future__ import annotations

import os
import re
from pathlib import Path


SECTION_HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
LIST_ITEM_PATTERN = re.compile(r"^(?:-|\d+\.)\s+(.+)$")


def extract_section_rules(text: str) -> list[dict[str, object]]:
    sections: list[dict[str, object]] = []
    current_heading = "Document"
    current_items: list[str] = []
    for raw_line in text.replace("\r\n", "\n").split("\n"):
        line = raw_line.rstrip()
        heading_match = SECTION_HEADING_PATTERN.match(line)
        if heading_match:
            if current_items:
                sections.append({"heading": current_heading, "items": current_items[:]})
            current_heading = heading_match.group(2).strip()
            current_items = []
            continue
        item_match = LIST_ITEM_PATTERN.match(line.strip())
        if item_match:
            current_items.append(item_match.group(1).strip())
    if current_items:
        sections.append({"heading": current_heading, "items": current_items[:]})
    return sections


def default_global_home_agents() -> Path:
    return Path.home() / ".codex" / "AGENTS.md"


def normalize_path_for_compare(path: Path) -> str:
    return os.path.normcase(str(path.resolve(strict=False))).rstrip("\\/")


def is_within_path(path: Path, parent: Path) -> bool:
    path_text = normalize_path_for_compare(path)
    parent_text = normalize_path_for_compare(parent)
    if path_text == parent_text:
        return True
    return path_text.startswith(parent_text + os.sep)


def classify_analysis_path(root: Path, analysis_path: Path | None = None) -> dict[str, object]:
    workspace_root = root.parent
    path_for_analysis = analysis_path or root
    if is_within_path(path_for_analysis, root):
        scope_hint = "repo"
        note = "Path is inside the current repository; global-home, workspace, and repo-local AGENTS are applicable file-governance candidates."
    elif is_within_path(path_for_analysis, workspace_root):
        scope_hint = "workspace"
        note = "Path is inside the workspace but outside the current repository; repo-local AGENTS is retained as evidence only."
    else:
        scope_hint = "external"
        note = "Path is outside the current repository/workspace boundary; project AGENTS are evidence only unless manually re-pointed and loaded."
    return {
        "path": str(path_for_analysis),
        "scope_hint": scope_hint,
        "note": note,
        "verified": True,
        "unverified_path_classification": False,
    }


def classify_rule_category(section: str, rule: str) -> str:
    text = f"{section} {rule}".lower()
    if any(token in text for token in ("must", "never", "不得", "不可", "必須", "禁止", "do not")):
        return "hard_rule"
    return "operational_guidance"


def candidate_sources(root: Path, analysis_path: Path | None = None) -> list[dict[str, object]]:
    workspace_root = root.parent
    global_path = default_global_home_agents()
    path_for_analysis = analysis_path or root
    path_classification = classify_analysis_path(root, path_for_analysis)
    return [
        {
            "scope": "global-home",
            "suggested_path": global_path,
            "precedence": 0,
            "project_external": True,
            "applies_to_path": True,
        },
        {
            "scope": "workspace",
            "suggested_path": workspace_root / "AGENTS.md",
            "precedence": 1,
            "project_external": True,
            "applies_to_path": path_classification["scope_hint"] in {"repo", "workspace"},
        },
        {
            "scope": "repo",
            "suggested_path": root / "AGENTS.md",
            "precedence": 2,
            "project_external": False,
            "applies_to_path": path_classification["scope_hint"] == "repo",
        },
    ]


def build_governance_sources(root: Path, analysis_path: Path | None = None) -> dict[str, object]:
    sources: list[dict[str, object]] = []
    effective_rules: list[dict[str, object]] = []
    path_for_analysis = analysis_path or root
    path_classification = classify_analysis_path(root, path_for_analysis)

    for candidate in candidate_sources(root, path_for_analysis):
        path = Path(candidate["suggested_path"])
        exists = path.exists()
        readable = False
        sections: list[dict[str, object]] = []
        unresolved_reason = None
        if exists:
            try:
                sections = extract_section_rules(path.read_text(encoding="utf-8"))
                readable = True
            except OSError as error:
                unresolved_reason = str(error)
        else:
            unresolved_reason = "source file does not exist"

        source = {
            "scope": candidate["scope"],
            "path": str(path),
            "suggested_path": str(path),
            "manual_path": None,
            "exists": exists,
            "readable": readable,
            "source_kind": "auto" if exists else "missing",
            "project_external": candidate["project_external"],
            "handle_bound": False,
            "permission_state": "local-process" if readable else "unavailable",
            "last_loaded_at": None,
            "applies_to_path": candidate["applies_to_path"],
            "inspectable": readable,
            "precedence": candidate["precedence"],
            "unresolved_reason": unresolved_reason,
            "definition_path": str(root / "local" / "config" / "agent-governance-layers.json"),
            "sections": sections,
        }
        sources.append(source)

        if not readable or not candidate["applies_to_path"]:
            continue
        for section in sections:
            heading = str(section["heading"])
            for index, item in enumerate(section["items"], start=1):
                effective_rules.append(
                    {
                        "precedence": candidate["precedence"],
                        "scope": candidate["scope"],
                        "source_path": str(path),
                        "section": heading,
                        "rule_index": index,
                        "rule": item,
                        "rule_category": classify_rule_category(heading, str(item)),
                        "inspectable": True,
                        "effective": True,
                        "evidence_only": False,
                        "shadowed": False,
                        "conflict": False,
                        "unresolved_reason": None,
                    }
                )

    effective_rules.sort(key=lambda item: (item["precedence"], item["source_path"], item["section"], item["rule_index"]))
    return {
        "hierarchy_note": "Runtime/system/developer/session instructions still sit above file-based AGENTS. This resolver evaluates the observable file-based portion: global-home, workspace overlay, then repo-local rules.",
        "analysis_path": str(path_for_analysis),
        "path_classification": path_classification,
        "sources": sources,
        "effective_file_rules": effective_rules,
        "effective_hard_rules": [rule for rule in effective_rules if rule["rule_category"] == "hard_rule"],
        "operational_guidance": [rule for rule in effective_rules if rule["rule_category"] == "operational_guidance"],
    }
