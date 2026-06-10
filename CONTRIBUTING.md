# Contributing to UniText

> Contribution guide for documentation, governance, registry resources, runtime projections, adapters, and supporting scripts.

## Read this first

Before proposing changes, read these files in order:

1. `README.md`
2. `INDEX.md`
3. `OPERATIONS.md`
4. `DOCUMENT_PLACEMENT_POLICY.md`
5. `NO_PUBLISH_POLICY.md`

If your work touches shared resource metadata, also read `RESOURCE_SPEC.md`.

## What makes a good contribution

A good UniText contribution is:

- small in scope
- clear about source of truth
- safe to review
- consistent with local-first and no-publish boundaries
- explicit about verification

## Contribution lanes

| Lane | Examples | Notes |
|---|---|---|
| Documentation | README updates, policy wording, adapter notes | Prefer clarity, routing, and boundary reduction |
| Governance | policy docs, placement rules, review gates | Must match scripts and ignore rules |
| Registry resources | skills, workflows, agents, MCP definitions | Shared resources must remain template-safe |
| Runtime projections | generated or projection-facing files | Do not edit generated projections manually unless explicitly human-authored |
| Local operations | bootstrap, verification, export helpers | Prefer dry-run, backup, and rollback-aware behavior |

## Documentation changes

For documentation work:

- improve readability before adding more jargon
- reduce ambiguity before adding more examples
- keep `README.md` and `README.zh-TW.md` aligned when they describe the same surface
- prefer stable routing language in `INDEX.md`
- do not place live workspace values in shared docs
- do not edit `runtime/catalog.json` by hand as docs-only work

## Placement and publication boundaries

Before adding a new document, ask:

1. Is this shared canonical guidance?
2. Is this live workspace state?
3. Is this generated evidence or output?

Use `DOCUMENT_PLACEMENT_POLICY.md` for the decision and respect `NO_PUBLISH_POLICY.md` at all times.

A private remote, a clean branch, or a publishability report does not equal permission to publish.

## Validation

Choose the smallest verification set that matches your change.

### Documentation and governance changes

```bash
git diff --check
python local/scripts/verify-workspace-boundaries.py --format json
python local/scripts/audit-i18n-drift.py --format json --sample-size 0 --exit-zero
python -m unittest tests.test_registry_inventory tests.security.test_i18n_drift tests.security.test_workspace_sensitive_metadata tests.security.test_release_hygiene
```

### Runtime or delivery changes

Also run the relevant operational verification described in `OPERATIONS.md`.

## Pull request expectations

A strong pull request for UniText should state:

- what changed
- why it changed
- which files are now the source of truth
- what verification was performed
- what assumptions remain open

If a change is intentionally incomplete, say so explicitly.

## Language and style

- Keep public-facing guidance readable before becoming comprehensive.
- Explain niche terms on first use.
- Prefer stable headings so agents and maintainers can find sections quickly.
- When English and Traditional Chinese companions exist, keep structure synchronized unless a documented reason requires divergence.

## Questions

If you are unsure where a document belongs, start with:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\get-document-placement-recommendation.ps1 -Topic "deployment-provider workflow" -CanonicalSharedTruth -SharedForm registry-reference
```

If unsure whether a change is publication-safe, ask for explicit approval instead of guessing.
