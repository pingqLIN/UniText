# Project Map UI Contract

This file defines the standalone boundary for `web/project-map-ui`.

## Inputs

- `--repo-root`: the governance source folder to scan.
  - Current adapters:
    - `unitext`: UniText repository root with full registry and core document expectations.
    - `governance-folder`: generic governance/project/research folder validated by AGENTS, governance policy, runtime catalog, or registry markers.
  - Required role: provide project documents, registry directories, governance sources, and runtime metadata used to build map nodes and governance evidence.
  - Adapter rule: folder-specific markers, core docs, and registry directories are defined in `project_map_adapters.py`, not in UI control flow.

## Outputs

- `--output-dir`: generated artifact folder.
  - Default: `<input-root>/ops/project-map`.
  - Writes:
    - `project-map.json`
    - `site/project-map.html`
    - `site/project-map-share.html`
    - `site/project-map-handoff.md`
    - `site/project-map-handoff.json`

## Governance Policy

- `--governance-policy`: structured governance policy file for the interactive resolver.
  - Default: `<input-root>/local/config/agent-governance-layers.json`.
  - Interactive artifacts may embed the structured policy.
  - Share-safe and handoff artifacts must not embed raw external AGENTS content, global-home paths, or manual external source paths.

## Share-Safe Stripping

Share-safe output must strip these operator-only surfaces:

- native repo paths and local filesystem roots
- AGENTS source paths, extracted file rules, and governance policy payloads
- directory picker, browser refresh, and report-writing controls
- governance workspace panels and operator-only export controls

## Implementation Rule

`project_map_contract.py` is the machine-readable I/O contract source. `project_map_adapters.py` is the machine-readable root adapter source. Keep this document, the generator payload, and tests aligned when either contract surface changes.
