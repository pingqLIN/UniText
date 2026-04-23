---
runtime_projection: true
source_of_truth: registry/skills/openai-apps-sdk-oauth/references/stytch.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/openai-apps-sdk-oauth/references/stytch.md`
> Source of truth: `registry/skills/openai-apps-sdk-oauth/references/stytch.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Stytch for Apps SDK OAuth

Use this file when the user wants Stytch as the authorization server for an MCP resource used by ChatGPT or another MCP client.

Official references:

- `https://stytch.com/docs/connected-apps/guides/mcp-auth-overview`
- `https://stytch.com/docs/api-reference/consumer/api/connected-apps/application-management/dynamic-client-registration`

## What Stytch is good at here

- Hosted OAuth pieces that align closely with MCP flows
- Clear examples for protected-resource metadata on popular runtimes
- Built-in Dynamic Client Registration endpoint
- Strong documentation for the browser consent flow and token exchange path

## Important Stytch-specific checks

### 1. DCR is available but opt-in

Stytch documents Dynamic Client Registration as an opt-in feature in Connected Apps.

Check this first:

- Connected Apps is enabled
- DCR is enabled at the project level
- the correct custom domain is configured

### 2. Authorization server metadata is hosted by Stytch

In the Stytch MCP flow:

- your MCP server hosts protected-resource metadata
- Stytch hosts the authorization server metadata and token endpoint

This reduces the amount of auth-server plumbing you need to host yourself.

### 3. Your app still hosts the consent entry page

Stytch's docs describe the authorization endpoint as a page in your application that hosts the Stytch identity component.

That means:

- your website still needs a consent-capable route
- logged-in user state matters before consent can be granted
- website auth UX and MCP auth UX should still be designed together

## Recommended Stytch shape

Use Stytch when these are true:

- you want a more MCP-guided hosted OAuth path
- DCR-first client onboarding is important
- you want hosted token endpoints with fewer identity-platform knobs

Recommended split:

- Next.js website hosts the consent route and user login state
- MCP server publishes `/.well-known/oauth-protected-resource`
- Stytch issues tokens and serves the authorization server metadata

## Scope design advice with Stytch

- Use Stytch Connected Apps scopes for tool families
- keep `openid`, `email`, and `profile` separate from your product scopes
- request product scopes only where linked access is needed

## Risks and caveats

- you still need to design the website-side consent and login flow
- custom-domain setup matters for production polish and consistency
- DCR being enabled does not remove the need to validate scopes and tokens in the MCP server

## Good fit

- greenfield product
- team wants a more MCP-native hosted OAuth experience
- dynamic client onboarding is expected

## Weak fit

- organization already standardized on Auth0
- enterprise governance requirements strongly favor manually pre-registered clients
