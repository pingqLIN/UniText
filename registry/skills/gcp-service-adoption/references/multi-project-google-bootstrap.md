# Multi-Project Google Bootstrap

Use this file when several local repositories need different Google Cloud capabilities and you want one consistent bootstrap plan instead of handling each repo ad hoc.

This reference captures a concrete three-project portfolio:

- `Q:\Projects\xiaohundan-i18n-hub`
- `Q:\Projects\taste`
- `Q:\Projects\codex-calendar-todo`

## Portfolio decision

Do not place all three workloads in one Google Cloud project.

Use three ordinary GCP projects:

| Local repo | Capability | Recommended GCP project purpose | Why separate |
| --- | --- | --- | --- |
| `xiaohundan-i18n-hub` | Cloud Translation Basic v2 with `GOOGLE_TRANSLATE_API_KEY` | Translate-only project | Isolate API key, quota, and paid translation usage |
| `taste` | Google sign-in through Supabase hosted auth | OAuth-only project | Only needs OAuth client; no Calendar or Translate billing |
| `codex-calendar-todo` | Google OAuth plus Calendar API access | OAuth + Calendar project | Uses a wider OAuth scope and actual Google Calendar API traffic |

## Shared defaults

Use these defaults unless the billing or ownership model changes:

- billing account: `billingAccounts/010E2C-B13825-AE66CC`
- labels:
  - `owner=addragonash`
  - `environment=dev`
  - `cost-center=personal-lab`

Recommended display names and project IDs:

| Local repo | Display name | Project ID pattern |
| --- | --- | --- |
| `xiaohundan-i18n-hub` | `Xiaohundan Translate Dev` | `xiaohundan-translate-dev-<suffix>` |
| `taste` | `Taste Auth Dev` | `taste-auth-dev-<suffix>` |
| `codex-calendar-todo` | `Codex Calendar Auth Dev` | `codex-calendar-auth-dev-<suffix>` |

Replace `<suffix>` with a short unique string, for example `a1b2`.

## Project 1: `xiaohundan-i18n-hub`

### What the repo currently expects

The repo already uses:

- `GOOGLE_TRANSLATE_API_KEY`
- `https://translation.googleapis.com/language/translate/v2`

That matches Cloud Translation Basic v2 and an API-key workflow.

### Required Google setup

- enable `translate.googleapis.com`
- create an API key
- restrict the key to `Cloud Translation API`
- set a monthly budget because this project can incur direct translation cost

### CLI draft

```powershell
$PROJECT_ID = "xiaohundan-translate-dev-a1b2"
$PROJECT_NAME = "Xiaohundan Translate Dev"
$BILLING_ACCOUNT = "010E2C-B13825-AE66CC"

gcloud projects create $PROJECT_ID --name=$PROJECT_NAME
gcloud beta billing projects link $PROJECT_ID --billing-account=$BILLING_ACCOUNT
gcloud config set project $PROJECT_ID

gcloud projects update $PROJECT_ID `
  --update-labels=owner=addragonash,environment=dev,cost-center=personal-lab

gcloud services enable translate.googleapis.com

gcloud services api-keys create --display-name="xiaohundan translate dev key"
```

After creating the key, open Google Cloud Console and apply restrictions:

- API restrictions: `Cloud Translation API`
- application restrictions:
  - none for local CLI usage
  - add tighter restrictions later if the key moves behind a fixed backend

### App-side mapping

Set these in `Q:\Projects\xiaohundan-i18n-hub\.env`:

```env
GOOGLE_TRANSLATE_API_KEY=<generated-api-key>
GOOGLE_TRANSLATE_BASE_URL=https://translation.googleapis.com/language/translate/v2
```

### Validation

```powershell
gcloud config set project $PROJECT_ID
gcloud services list --enabled
```

Run the repo's real smoke test only after the key is present.

## Project 2: `taste`

### What the repo currently expects

The app already calls Supabase browser auth:

- `supabase.auth.signInWithOAuth({ provider: 'google' })`

Google Cloud does not host the login flow directly. It only provides the Google OAuth client used by Supabase.

The repo's existing setup note already confirms the required callback:

- `https://eskreiijnziaqvwswvqc.supabase.co/auth/v1/callback`

### Required Google setup

- create an OAuth consent screen
- create an OAuth client ID of type `Web application`
- add JavaScript origins for the app
- add the Supabase callback URI as the redirect URI

No Calendar API, Translate API, or API key is needed for this repo.

### CLI draft

```powershell
$PROJECT_ID = "taste-auth-dev-a1b2"
$PROJECT_NAME = "Taste Auth Dev"
$BILLING_ACCOUNT = "010E2C-B13825-AE66CC"

gcloud projects create $PROJECT_ID --name=$PROJECT_NAME
gcloud beta billing projects link $PROJECT_ID --billing-account=$BILLING_ACCOUNT
gcloud config set project $PROJECT_ID

gcloud projects update $PROJECT_ID `
  --update-labels=owner=addragonash,environment=dev,cost-center=personal-lab
```

OAuth client creation is still best completed in Console because consent-screen and redirect-URI flows are easier to verify visually:

- Console path: `APIs & Services` -> `OAuth consent screen`
- Console path: `APIs & Services` -> `Credentials` -> `Create credentials` -> `OAuth client ID`

Use:

- application type: `Web application`
- authorized JavaScript origins:
  - `http://localhost:3010`
  - `https://your-domain.example`
- authorized redirect URI:
  - `https://eskreiijnziaqvwswvqc.supabase.co/auth/v1/callback`

### App-side mapping

Fill the generated OAuth values into Supabase, not directly into the Next.js app:

- Supabase `Authentication` -> `Providers` -> `Google`
  - `Client ID`
  - `Client Secret`

Then ensure `Q:\Projects\taste\.env.local` or hosted env contains the expected Supabase settings:

```env
NEXT_PUBLIC_SITE_URL=http://localhost:3010
NEXT_PUBLIC_SUPABASE_URL=https://eskreiijnziaqvwswvqc.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<supabase-anon-key>
SUPABASE_SERVICE_ROLE_KEY=<supabase-service-role-key>
NEXT_PUBLIC_ADMIN_EMAIL=addragonash@gmail.com
```

### Validation

- sign in on `/admin`
- confirm `addragonash@gmail.com` unlocks the admin UI
- confirm a different Google account is rejected

## Project 3: `codex-calendar-todo`

### What the repo currently expects

The repo runs its own Google OAuth flow and calls Google Calendar through `googleapis`.

Current expected env vars:

```env
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=http://127.0.0.1:4321/api/google/callback
```

The current server code asks for:

- `https://www.googleapis.com/auth/calendar`

### Required Google setup

- create an OAuth consent screen
- enable Google Calendar API
- create an OAuth client ID of type `Web application`
- add the local callback URI

### CLI draft

```powershell
$PROJECT_ID = "codex-calendar-auth-dev-a1b2"
$PROJECT_NAME = "Codex Calendar Auth Dev"
$BILLING_ACCOUNT = "010E2C-B13825-AE66CC"

gcloud projects create $PROJECT_ID --name=$PROJECT_NAME
gcloud beta billing projects link $PROJECT_ID --billing-account=$BILLING_ACCOUNT
gcloud config set project $PROJECT_ID

gcloud projects update $PROJECT_ID `
  --update-labels=owner=addragonash,environment=dev,cost-center=personal-lab

gcloud services enable calendar-json.googleapis.com
```

Then create the OAuth client in Console:

- application type: `Web application`
- authorized redirect URI:
  - `http://127.0.0.1:4321/api/google/callback`

If a hosted version is added later, add a second production callback instead of replacing the local callback.

### App-side mapping

Set these in `Q:\Projects\codex-calendar-todo\.env.local`:

```env
GOOGLE_CLIENT_ID=<generated-client-id>
GOOGLE_CLIENT_SECRET=<generated-client-secret>
GOOGLE_REDIRECT_URI=http://127.0.0.1:4321/api/google/callback
```

### Validation

```powershell
curl http://127.0.0.1:4321/api/google/connect
```

Then complete the browser OAuth flow and confirm tokens are written into `storage/state.json`.

## Budget baseline

Use project-scope budgets first.

| GCP project purpose | Suggested budget posture |
| --- | --- |
| Translate-only | Required; this project can accumulate direct paid API usage |
| OAuth-only for `taste` | Optional but recommended as a small baseline governance budget |
| OAuth + Calendar for `codex-calendar-todo` | Recommended as a small baseline governance budget |

Recommended alert thresholds:

- `50%`
- `80%`
- `100%`

If you want a generated budget payload, use `scripts/gcp_budget_api.py payload` after the project exists.

## Recommended execution order

1. Bootstrap `xiaohundan-i18n-hub` first because its dependency path is the most direct and already wired to an API key.
2. Bootstrap `taste` second because it only needs OAuth client wiring and Supabase mapping.
3. Bootstrap `codex-calendar-todo` third because it has the broadest Google permission scope and should be reviewed after the simpler OAuth case is working.

## Final operator checklist

- every repo has its own ordinary GCP project
- every project is linked to billing
- every project has `owner`, `environment`, and `cost-center` labels
- `xiaohundan-i18n-hub` has a restricted Translate API key
- `taste` has a Supabase-compatible OAuth client
- `codex-calendar-todo` has Calendar API enabled and a working OAuth client
- budgets are at least defined for the Translate project and preferably for all three
