---
---

# Mode: External Web Audit

Use this mode when the user wants visible, human-supervised review through a browser product such as ChatGPT or Gemini.

This is the safest fallback when automation boundaries are unclear.

## Why this mode

- avoids hidden automation
- easy to inspect exactly what was sent
- compatible with providers that do not expose stable CLI or MCP paths

## Procedure

1. build the audit packet
2. paste the packet into the web UI manually
3. ask for read-only findings only
4. copy the response back into the project note or audit report
5. normalize the findings into the standard report format
6. classify missing, acknowledgement-only, or confirmation-request-only responses as failed gates

## Required safeguards

- do not claim the web reviewer saw local files it did not actually receive
- keep sensitive content out unless the user explicitly approves the upload
- record the service name in `Audit Mode` or `Assumptions`

## Recommended prompt entry

Use [../assets/web/external-audit-request.md](../assets/web/external-audit-request.md) as the starting packet wrapper.

## Attribution note

If the web review guidance or decision criteria came from official docs or public skills, repeat those references in the final report.
