# Testing And Rollout

Use this file once the OAuth contract is wired and the next question is confidence.

## Local testing

- Start with a development IdP tenant or app that issues short-lived tokens.
- Verify the protected-resource metadata endpoint from the exact MCP environment under test.
- Exercise both public tools and auth-required tools.
- Confirm that missing-token and insufficient-scope failures trigger the expected linking path.

## High-signal test matrix

- public tool with no linking
- optional-auth tool with no linking
- optional-auth tool after linking
- auth-required tool before linking
- auth-required tool after linking
- expired token replay
- scope-upgrade flow after adding a new privileged tool

## Rollout sequence

1. validate in development with short-lived tokens
2. dogfood with a trusted internal tester group
3. require linking only for the privileged tool set first
4. expand scope coverage or write-capable tools after auth logs are clean

## Production checks

- plan for token revocation and relinking
- handle stale tokens as unauthenticated, not as server errors
- keep auth error messages clear enough for user recovery
- watch for environment mismatches between issuer, resource metadata, and MCP hostname

## Optional connector-side hardening

If the deployment path also uses connector authentication, verify mTLS independently.
Do not treat mTLS as a replacement for end-user OAuth.
