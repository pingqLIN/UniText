---
name: supabase-hosted-admin-oauth
description: Verify and prepare hosted Supabase admin OAuth flows before real sign-in testing. Use when a repo has a protected `/admin` route backed by Supabase Auth or Google OAuth, when local and hosted Supabase environments may be confused, when the CLI token exists under a nonstandard env var such as `SPB_Access_Token`, or when Codex needs to fetch hosted API keys, populate hosted env files, run repo preflight checks, and determine whether real Google sign-in validation is actually ready.
metadata:
  runtime_support_files: true
---

# Supabase Hosted Admin OAuth

## Overview

Use this skill to stop false-positive OAuth validation.
First prove the app is running against hosted Supabase, then verify provider readiness, and only then attempt real `/admin` sign-in checks.

## Workflow

### 1. Confirm the execution target

Check the repo state before editing.

- Run `git status --short --branch`
- Identify whether the app currently reads local or hosted Supabase env
- Prefer existing repo docs such as:
  - `docs/google-oauth-setup.md`
  - `.env.hosted.example`
  - `.env.hosted.local.example`
  - repo scripts such as `scripts/check-hosted-admin-oauth.mjs`

Do not treat a public URL as "hosted OAuth ready" just because the page loads.

### 2. Normalize Supabase CLI authentication

Supabase CLI expects `SUPABASE_ACCESS_TOKEN`.
If the workstation stores the token under a custom name such as `SPB_Access_Token`, map it explicitly in the same shell session before running management commands.

PowerShell pattern:

```powershell
$env:SUPABASE_ACCESS_TOKEN=[Environment]::GetEnvironmentVariable('SPB_Access_Token','User')
```

Then use the CLI:

```powershell
npx supabase projects list
npx supabase projects api-keys --project-ref <project-ref>
```

### 3. Fetch the minimum hosted data needed

Collect only the fields required for hosted auth validation:

- project ref
- hosted Supabase URL
- anon key
- service role key
- intended public site URL
- admin email

If the repo already has a hosted env template, fill that instead of inventing a new format.

### 4. Separate local and hosted env profiles

Never overwrite local development env just to test hosted auth.
Prefer a dedicated hosted profile such as:

- `.env.hosted.local`
- `npm run dev:hosted`
- `npm run build:hosted`

If the repo lacks this separation, create it before continuing.

The hosted profile should point at:

- `NEXT_PUBLIC_SITE_URL=<public hosted URL>`
- `NEXT_PUBLIC_SUPABASE_URL=https://<project-ref>.supabase.co`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY=<hosted anon key>`
- `SUPABASE_SERVICE_ROLE_KEY=<hosted service role key>`
- `NEXT_PUBLIC_ADMIN_EMAIL=<allowed admin email>`

### 5. Run a hosted preflight before real OAuth testing

If the repo has a preflight script, use it.
If not, create one before claiming validation.

The preflight must answer these questions:

- Is the env profile actually hosted, not local?
- Does the app point at the intended public site URL?
- Are hosted anon and service role keys present?
- Does the public app still respond?
- Is the next action "real sign-in validation" or "fix env/profile first"?

If the preflight says the app still uses local Supabase, stop there.
That is not a Google OAuth bug; it is an environment selection bug.

### 6. Perform real sign-in validation only after preflight passes

When `hostedAdminOAuthReady` is true:

1. Start the app with the hosted profile
2. Open `/admin`
3. Trigger Google sign-in
4. Sign in with the allowed admin account
5. Confirm the admin editor unlocks
6. Confirm protected write paths work
7. Confirm a different account is rejected

### 7. Common failure interpretation

- `redirect_uri_mismatch`
  - Google OAuth client redirect URI does not exactly match the Supabase callback
- `Admin authentication is required`
  - browser session or bearer token is missing
- sign-in succeeds but admin remains locked
  - signed-in email does not match the allowed admin email
- public site works but preflight fails
  - the app is still using local Supabase or missing hosted keys

## Output expectations

When finishing a run, report these separately:

- local Supabase status
- hosted Supabase project identity
- whether hosted env files are populated
- whether hosted preflight passes
- whether real Google sign-in was actually tested
- the exact remaining blocker, if any

Do not collapse "hosted profile prepared" and "Google OAuth validated" into one statement.
