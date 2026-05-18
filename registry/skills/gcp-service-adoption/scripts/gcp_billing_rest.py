from __future__ import annotations

import json
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from gcp_shared import resolve_gcloud_command


def get_access_token() -> str:
    gcloud_command = resolve_gcloud_command()
    if gcloud_command is None:
        raise RuntimeError("gcloud not found on PATH")

    completed = subprocess.run(
        [gcloud_command, "auth", "print-access-token"],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "failed to get access token")

    token = completed.stdout.strip()
    if not token:
        raise RuntimeError("received empty access token from gcloud")
    return token


def billing_request(
    *,
    method: str,
    url: str,
    api_user_project: str | None = None,
    body: dict[str, Any] | None = None,
) -> dict[str, Any]:
    token = get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
    }
    if api_user_project:
        headers["x-goog-user-project"] = api_user_project

    data = None
    if body is not None:
        headers["Content-Type"] = "application/json; charset=utf-8"
        data = json.dumps(body).encode("utf-8")

    request = urllib.request.Request(url=url, method=method.upper(), headers=headers, data=data)
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read().decode("utf-8")
            return {"ok": True, "status": response.status, "data": json.loads(raw) if raw else {}}
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8")
        parsed: Any
        try:
            parsed = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            parsed = raw
        return {"ok": False, "status": exc.code, "error": parsed}


def append_query(url: str, params: dict[str, str | int | None]) -> str:
    filtered = {key: value for key, value in params.items() if value is not None}
    if not filtered:
        return url
    return f"{url}?{urllib.parse.urlencode(filtered)}"
