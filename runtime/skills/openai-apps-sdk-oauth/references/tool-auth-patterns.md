---
runtime_projection: true
source_of_truth: registry/skills/openai-apps-sdk-oauth/references/tool-auth-patterns.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/openai-apps-sdk-oauth/references/tool-auth-patterns.md`
> Source of truth: `registry/skills/openai-apps-sdk-oauth/references/tool-auth-patterns.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Tool Auth Patterns

This file covers the two places where Apps SDK auth behavior is expressed:

- static tool metadata
- runtime auth challenges

## Per-tool `securitySchemes`

Prefer explicit tool-level declarations.
This keeps public and privileged tools easy to reason about and evolve.

### Auth-required tool

Use this shape when the tool should not run until the user links an account:

```ts
securitySchemes: [{ type: "oauth2", scopes: ["docs.write"] }]
```

### Optional-auth tool

Use this shape when anonymous use is allowed but linking unlocks a privileged result path:

```ts
securitySchemes: [
  { type: "noauth" },
  { type: "oauth2", scopes: ["search.read"] },
]
```

Do not advertise optional auth unless the backend really supports both anonymous and linked behavior.

## Runtime challenge behavior

When the MCP server detects a missing or invalid token, return an auth failure result that includes:

- user-readable text explaining that linking is required
- `_meta["mcp/www_authenticate"]`
- an OAuth bearer challenge that references protected-resource metadata
- an `error`
- an `error_description`

## Minimal challenge example

```json
{
  "_meta": {
    "mcp/www_authenticate": [
      "Bearer resource_metadata=\"https://your-mcp.example.com/.well-known/oauth-protected-resource\", error=\"insufficient_scope\", error_description=\"You need to link your account to continue.\""
    ]
  }
}
```

## Review rules

- Tool metadata alone is not enough to trigger linking UX.
- Runtime challenge alone is not enough either.
- Keep the protected-resource URL in the challenge aligned with the deployed MCP environment.
