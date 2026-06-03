# Workflow

## Goal

Publish a local site to a user-owned Cloudflare hostname with a reversible named tunnel workflow.

## Preconditions

- `cloudflared.exe` is installed and available in `PATH`
- the user already owns and controls the target Cloudflare zone
- a local origin is available on `127.0.0.1:<port>`
- the user has approved touching shared Cloudflare login state if reauthentication becomes necessary

## Recommended file layout

Keep project-specific tunnel files under a runtime folder such as:

```text
<project>\
  .runtime\
    cloudflared.<project>.yml
    <project>-tunnel.json
    cloudflared.named.log
```

Do not place new project tunnel credentials in the shared user directory unless there is a strong reason.

## Step 1. Verify the local origin

For a simple static site, an acceptable Windows pattern is:

```powershell
Start-Process -FilePath 'python.exe' `
  -ArgumentList '-m','http.server','43173','--bind','127.0.0.1' `
  -WorkingDirectory 'Q:\Projects\<project>\' `
  -WindowStyle Hidden -PassThru
```

Then verify:

```powershell
Invoke-WebRequest -UseBasicParsing http://127.0.0.1:43173/
```

If PowerShell HTTP checks are unreliable, use:

```powershell
@'
import urllib.request
with urllib.request.urlopen("http://127.0.0.1:43173/", timeout=10) as resp:
    print(resp.status, resp.headers.get("Content-Type"))
'@ | python -
```

## Step 2. Inventory Cloudflare state

Check:

- `C:\Users\<user>\.cloudflared\`
- existing `*.json` tunnel credential files
- existing `*.yml` configs
- current auth state:

```powershell
cloudflared.exe tunnel list
```

If this returns `Authentication error` or `unauthorized`, the shared login state is stale.

## Step 3. Refresh login only with approval

Treat `C:\Users\<user>\.cloudflared\cert.pem` as shared.

Safe pattern:

1. back it up
2. remove or move only after explicit user approval
3. rerun:

```powershell
cloudflared.exe tunnel login
```

## Step 4. Create the named tunnel with a project-local credential file

Use:

```powershell
cloudflared.exe tunnel create `
  --credentials-file 'Q:\Projects\<project>\.runtime\<project>-tunnel.json' `
  tracing-paper-system
```

This avoids writing the new tunnel credential into the shared `.cloudflared` folder.

## Step 5. Route DNS

Map the desired hostname:

```powershell
cloudflared.exe tunnel route dns `
  <tunnel-id> `
  tracing-paper.colorgeek.co
```

Verify the hostname is not already in use before routing it.

## Step 6. Write a project-local config

Example:

```yaml
tunnel: <tunnel-id>
credentials-file: Q:\Projects\<project>\.runtime\<project>-tunnel.json

ingress:
  - hostname: tracing-paper.colorgeek.co
    service: http://127.0.0.1:43173
  - service: http_status:404
```

## Step 7. Run the tunnel

Use:

```powershell
Start-Process -FilePath 'cloudflared.exe' `
  -ArgumentList 'tunnel','--config','Q:\Projects\<project>\.runtime\cloudflared.<project>.yml','--no-autoupdate','--logfile','Q:\Projects\<project>\.runtime\cloudflared.named.log','--loglevel','info','run' `
  -WindowStyle Hidden -PassThru
```

## Step 8. Verify the public hostname

Prefer verifying the final hostname directly:

```powershell
@'
import urllib.request
req = urllib.request.Request(
    "https://tracing-paper.colorgeek.co/",
    headers={"User-Agent": "Mozilla/5.0"},
)
with urllib.request.urlopen(req, timeout=20) as resp:
    body = resp.read(200).decode("utf-8", errors="replace")
    print(resp.status, resp.headers.get("Content-Type"))
    print(body[:120])
'@ | python -
```

## Step 9. Report cleanup

Report the exact stop command:

```powershell
Stop-Process -Id <origin-pid>,<tunnel-pid>
```

## Notes

- Keep the quick tunnel path separate from the named tunnel path.
- If the quick tunnel was started earlier, stop it after the named tunnel is verified.
- For repeated use on the same project, reuse the project-local config and credential file unless the user explicitly wants a fresh tunnel.
