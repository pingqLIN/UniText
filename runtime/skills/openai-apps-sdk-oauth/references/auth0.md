---
runtime_projection: true
source_of_truth: registry/skills/openai-apps-sdk-oauth/references/auth0.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/openai-apps-sdk-oauth/references/auth0.md`
> Source of truth: `registry/skills/openai-apps-sdk-oauth/references/auth0.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Auth0 for Apps SDK OAuth

Use this file when the user wants Auth0 as the authorization server for an MCP resource used by ChatGPT or another MCP client.

Official references:

- `https://auth0.com/ai/docs/mcp/intro/overview`
- `https://auth0.com/ai/docs/mcp/guides/registering-your-mcp-client-application`
- `https://auth0.com/ai/docs/mcp/guides/resource-param-compatibility-profile`
- `https://auth0.com/docs/get-started/applications/dynamic-client-registration`

## What Auth0 is good at here

- Enterprise identity and existing workforce or customer login flows
- Strong control over which clients may connect
- Clear guidance for MCP server authorization patterns
- Static client registration for controlled production environments

## Important Auth0-specific checks

### 1. Resource parameter compatibility

The MCP flow expects the standards-based `resource` parameter.
Auth0 documents a Resource Parameter Compatibility Profile for this.

Check this first:

- if disabled, token targeting may still depend on `audience`
- if enabled, Auth0 uses `resource` to specify the target API or resource server

Treat this as a required tenant-level review item, not as a late-stage tweak.

### 2. Dynamic client registration is not the default

Auth0 documents Dynamic Client Registration, but it is disabled by default.

That means:

- local demos may work once you enable DCR
- production should usually prefer static registration unless you intentionally accept open or semi-open DCR risk

Auth0's MCP guidance explicitly recommends static registration for most production use.

### 3. Protected resource metadata is your job

Auth0 does not host the MCP resource metadata for you.
Your MCP server still needs to expose:

- `/.well-known/oauth-protected-resource`
- `401 Unauthorized` with `WWW-Authenticate`

The Auth0 docs call these mandatory server configuration pieces.

## Recommended Auth0 shape

Use Auth0 when these are true:

- the product already uses Auth0 for website login
- enterprise SSO, MFA, or tenant controls matter
- you want tighter control over which MCP clients can register

Recommended split:

- Next.js website uses Auth0 browser login separately from MCP auth
- MCP server validates Auth0-issued bearer tokens
- Auth0 API or resource server configuration models the MCP scopes

## Scope design advice with Auth0

- Define scopes on the Auth0 API or resource server that represents the MCP server
- Keep tool scopes narrow and product-specific
- Avoid coupling website page roles directly to MCP tool scopes

## Risks and caveats

- Open DCR expands attack surface if enabled carelessly
- Auth0 tenant configuration has more moving parts than simpler hosted OAuth offerings
- `resource` compatibility must be verified early
- Browser login working does not prove MCP OAuth is wired correctly

## Good fit

- existing Auth0 customer
- enterprise or B2B product
- strong governance on client registration

## Weak fit

- user wants the most MCP-opinionated hosted path with minimal tenant tuning
- project needs fully turnkey DCR-first setup without much identity platform work
