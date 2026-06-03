from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ShareSafeStrippingRule:
    key: str
    description: str

    def as_dict(self) -> dict[str, str]:
        return {
            "key": self.key,
            "description": self.description,
        }


@dataclass(frozen=True)
class ProjectMapUiContract:
    input_root_argument: str
    input_root_role: str
    default_output_root: str
    output_root_role: str
    governance_policy_argument: str
    default_governance_policy: str
    governance_policy_role: str
    share_safe_stripping_rules: tuple[ShareSafeStrippingRule, ...]

    def default_governance_policy_path(self, input_root: Path) -> Path:
        return input_root / self.default_governance_policy

    def default_output_path(self, input_root: Path) -> Path:
        return input_root / self.default_output_root

    def as_dict(self) -> dict[str, object]:
        return {
            "input_root_argument": self.input_root_argument,
            "input_root_role": self.input_root_role,
            "default_output_root": self.default_output_root,
            "output_root_role": self.output_root_role,
            "governance_policy_argument": self.governance_policy_argument,
            "default_governance_policy": self.default_governance_policy,
            "governance_policy_role": self.governance_policy_role,
            "share_safe_stripping_rules": [
                rule.as_dict() for rule in self.share_safe_stripping_rules
            ],
        }


PROJECT_MAP_UI_CONTRACT = ProjectMapUiContract(
    input_root_argument="--repo-root",
    input_root_role=(
        "Canonical governance source folder to scan. In the current UniText "
        "adapter this is the repository root; future adapters may point it at "
        "another project folder or governance research folder."
    ),
    default_output_root="ops/project-map",
    output_root_role=(
        "Generated artifact root. Interactive, share-safe, JSON, and handoff "
        "artifacts are written below this folder."
    ),
    governance_policy_argument="--governance-policy",
    default_governance_policy="local/config/agent-governance-layers.json",
    governance_policy_role=(
        "Structured policy used by the interactive governance resolver. "
        "Share-safe artifacts must not embed this policy."
    ),
    share_safe_stripping_rules=(
        ShareSafeStrippingRule(
            "native_repo_paths",
            "Remove native filesystem roots and other local operator paths.",
        ),
        ShareSafeStrippingRule(
            "governance_sources",
            "Remove AGENTS source paths, extracted rules, and policy payloads.",
        ),
        ShareSafeStrippingRule(
            "write_controls",
            "Remove directory picker, browser refresh, and report-writing controls.",
        ),
        ShareSafeStrippingRule(
            "operator_panels",
            "Remove governance workspace panels and operator-only export controls.",
        ),
    ),
)
