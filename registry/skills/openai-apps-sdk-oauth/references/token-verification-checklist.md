# Token Verification Checklist

Once ChatGPT completes the OAuth flow, the MCP server receives a bearer token on later requests.
Treat that token as untrusted input until verified.

## Required checks

- Verify token signature against the authorization server's signing keys, commonly via JWKS.
- Verify issuer.
- Reject expired tokens.
- Reject tokens that are not yet valid.
- Verify audience or resource targeting so the token is actually meant for this MCP server.
- Verify required scopes for the tool being called.

## Operational checks

- Attach the resolved identity to request context only after verification succeeds.
- Keep tool authorization separate from simple authentication.
- Return `401 Unauthorized` with a `WWW-Authenticate` challenge when verification fails.

## Design advice

- Centralize verification in auth middleware or a dedicated guard layer.
- Keep per-tool scope mapping in one place so reviews are easy.
- Log auth failures with enough context to debug environment issues, but never log raw bearer tokens.

## Failure cases to test

- malformed token
- bad signature
- wrong issuer
- wrong audience or resource
- missing scope
- expired token
- token for one environment used against another
