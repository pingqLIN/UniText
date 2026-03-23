# Registry Curator Playbook

## Minimal Run

1. Read `INDEX.md`
2. Read `RESOURCE_SPEC.md`
3. Read `OPERATIONS.md`
4. Run `scan-skills.ps1`
5. Review candidate with `ADOPTION_CHECKLIST.md`
6. Run dry-run before adopt or deliver
7. Verify resulting registry and targets

## Escalation Rules

- `hold`
  - duplicate resource candidates
  - unresolved path mismatch
  - missing frontmatter
- `needs-fix`
  - metadata incomplete
  - missing supporting files
  - outdated path docs
- `approve`
  - review complete
  - backup path available
  - catalog can be updated safely

