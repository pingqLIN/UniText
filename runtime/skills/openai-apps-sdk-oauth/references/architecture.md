---
runtime_projection: true
source_of_truth: registry/skills/openai-apps-sdk-oauth/references/architecture.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/openai-apps-sdk-oauth/references/architecture.md`
> Source of truth: `registry/skills/openai-apps-sdk-oauth/references/architecture.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Architecture

Use this file to map the product into three separate concerns before discussing code.

## Core boundary model

- Website frontend: optional browser surface that explains linking state or routes the user into the ChatGPT-connected experience.
- MCP server: the protected resource server that serves tools to ChatGPT.
- Identity provider: the authorization server that issues access tokens for the MCP resource.

The MCP server is the security boundary that matters most for Apps SDK auth.
Do not confuse browser session auth with MCP tool auth.

## Common deployment shapes

### Website plus separate MCP server

Use this when the product already has a web app and only some features need to appear inside ChatGPT.

- Website handles ordinary browser UX and app settings.
- MCP server exposes tool endpoints to ChatGPT.
- Identity provider issues tokens accepted by the MCP server.

### Website and MCP server in one backend

Use this when a single backend owns both the website APIs and MCP tool execution.

- Keep browser session middleware and bearer-token verification separate.
- A browser cookie is not a substitute for MCP bearer-token validation.

### MCP-first integration without public website dependency

Use this when the product is mostly a backend capability surfaced in ChatGPT.

- Keep the implementation lean.
- Add a small admin or debug UI later only if needed.

## Recommended design defaults

- Prefer an established identity provider over custom auth infrastructure.
- Keep scope names product-specific and narrow.
- Design tool access around resource-server authorization, not around frontend page access.
- Treat anonymous and linked behavior as separate product modes.

## Questions to answer before coding

- Which tools are callable without linking?
- Which tools touch user-specific or write-capable data?
- What scopes are required per tool or tool family?
- Does the website need to show linked-account state, or is ChatGPT the only linking surface?
- Is the MCP server a distinct hostname and deployment unit?
