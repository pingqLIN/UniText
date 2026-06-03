# Storage Patterns

Choose the lightest model that matches the product.

## In-memory only

Use when:

- state is ephemeral
- restarts can lose work
- prototype or transient assistant session

Avoid when:

- users create durable content
- audit history matters

## Local file storage

Use when:

- single-user local app
- config, caches, exports, or simple documents
- human-readable data helps debugging

Good fits:

- CLI tools
- desktop helpers
- browser-adjacent local utilities

Recommended split:

- `config/`
- `data/`
- `cache/`
- `logs/`

## SQLite

Use when:

- local structured data matters
- search, filtering, and durability are needed
- multi-table relationships exist

Good fits:

- desktop helper
- local dashboard
- small internal tool

Avoid when:

- true multi-tenant cloud scale is required from day one

## Hosted relational database

Use when:

- multi-user durable data
- server-side app state
- auth-linked entities
- reporting or relational queries matter

Common choice:

- PostgreSQL

## Object storage plus metadata store

Use when:

- large files are first-class data
- app stores uploads, media, archives, or generated artifacts

Typical pairing:

- object storage for blobs
- relational DB for metadata and permissions

## Rule of thumb

- user-facing app with only preferences: files
- local structured app data: SQLite
- shared networked product data: PostgreSQL
- large binary payloads: object storage plus DB metadata
