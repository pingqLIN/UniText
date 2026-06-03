---
runtime_projection: true
source_of_truth: registry/skills/openai-apps-sdk-oauth/references/oauth-requirements.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/openai-apps-sdk-oauth/references/oauth-requirements.md`
> Source of truth: `registry/skills/openai-apps-sdk-oauth/references/oauth-requirements.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# OAuth Requirements

This file captures the minimum protocol expectations called out by the OpenAI Apps SDK auth guide.

## IdP capability checklist

The identity provider should expose:

- OAuth discovery metadata
- dynamic client registration support
- correct token issuance for the `resource` parameter used by the MCP resource server

If the provider cannot satisfy these expectations, treat that as a meaningful blocker.

## Flow expectations

- Use Authorization Code flow with PKCE for public-client scenarios.
- Do not design around implicit flow patterns.
- Keep refresh-token handling and revocation policy on the IdP side, but make the MCP server robust to expired or missing access tokens.

## Resource modeling

The token should clearly identify the MCP server as the intended resource.
Depending on provider behavior, this may appear through `aud`, a resource claim, or equivalent provider-specific representation.

## Scope design rules

- Prefer verb-plus-domain style scopes such as `search.read`, `docs.write`, or `account.profile.read`.
- Keep scopes narrow enough to map to tool groups.
- Avoid one giant catch-all scope unless the product truly has a single privilege tier.

## Early blocker checklist

Stop and flag architecture risk if any of these are true:

- no discovery document
- no dynamic client registration path
- no reliable way to issue tokens for the MCP resource
- no support for the scopes the product needs
