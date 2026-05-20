---
runtime_projection: true
source_of_truth: registry/skills/cloudflare-deploy/references/web-analytics/integration.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/cloudflare-deploy/references/web-analytics/integration.md`
> Source of truth: `registry/skills/cloudflare-deploy/references/web-analytics/integration.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Framework Integration

**Web Analytics is dashboard-only** - no programmatic API. This covers beacon integration.

## Basic HTML

```html
<script defer src='https://static.cloudflareinsights.com/beacon.min.js' 
        data-cf-beacon='{"token": "YOUR_TOKEN", "spa": true}'></script>
```

Place before closing `</body>` tag.

## Framework Examples

| Framework | Location | Notes |
|-----------|----------|-------|
| React/Vite | `public/index.html` | Add `spa: true` |
| Next.js App Router | `app/layout.tsx` | Use `<Script strategy="afterInteractive">` |
| Next.js Pages | `pages/_document.tsx` | Use `<Script>` |
| Nuxt 3 | `app.vue` with `useHead()` | Or use plugin |
| Vue 3/Vite | `index.html` | Add `spa: true` |
| Gatsby | `gatsby-browser.js` | `onClientEntry` hook |
| SvelteKit | `src/app.html` | Before `</body>` |
| Astro | Layout component | Before `</body>` |
| Angular | `src/index.html` | Add `spa: true` |
| Docusaurus | `docusaurus.config.js` | In `scripts` array |

## Configuration

```json
{
  "token": "YOUR_TOKEN",
  "spa": true
}
```

**Use `spa: true` for:** React Router, Vue Router, Next.js, Nuxt, Gatsby, SvelteKit, Angular

**Use `spa: false` for:** Traditional server-rendered (PHP, Django, Rails, WordPress)

## CSP Headers

```
script-src 'self' https://static.cloudflareinsights.com;
connect-src 'self' https://cloudflareinsights.com;
```

## GDPR Consent

```typescript
// Load conditionally based on consent
if (localStorage.getItem('analytics-consent') === 'true') {
  const script = document.createElement('script');
  script.src = 'https://static.cloudflareinsights.com/beacon.min.js';
  script.defer = true;
  script.setAttribute('data-cf-beacon', '{"token": "YOUR_TOKEN", "spa": true}');
  document.body.appendChild(script);
}
```
