# MCP Resource Metadata

Publish OAuth protected-resource metadata from the MCP server at a well-known endpoint such as:

- `https://your-mcp.example.com/.well-known/oauth-protected-resource`

## What this endpoint is for

This metadata tells the client where the protected resource lives and how OAuth should be started for it.
Treat it as part of the resource-server contract, not as a generic website config document.

## Implementation guidance

- Host it on the MCP server origin that the bearer token protects.
- Keep auth-related URLs, issuer assumptions, and supported scopes aligned with the actual IdP and tool policy.
- Version and deploy this metadata together with auth changes when possible.

## Minimal implementation checklist

- stable HTTPS URL
- correct resource identity
- issuer or authorization-server linkage that matches the chosen IdP
- supported scopes that map to real tool policy
- deployment ownership tied to the MCP service, not the marketing site

## Review questions

- Does the metadata describe the same resource the token is minted for?
- Would a scope or issuer change require this document to change too?
- Is the endpoint served from the same environment as the MCP server being tested?
