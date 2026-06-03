from __future__ import annotations

import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from gcp_pricing_api import filter_named_items


def test_filter_named_items_applies_match_and_limit() -> None:
    result = {
        "ok": True,
        "status": 200,
        "data": {
            "billingAccountSkuGroups": [
                {"name": "one", "displayName": "Cloud Run"},
                {"name": "two", "displayName": "Cloud Storage"},
                {"name": "three", "displayName": "Cloud SQL"},
            ]
        },
    }

    filtered = filter_named_items(
        result,
        collection_key="billingAccountSkuGroups",
        match="cloud",
        limit=2,
    )

    returned = filtered["data"]["billingAccountSkuGroups"]
    assert [item["displayName"] for item in returned] == ["Cloud Run", "Cloud Storage"]
    assert filtered["data"]["_meta"] == {
        "totalCount": 3,
        "matchedCount": 3,
        "returnedCount": 2,
        "match": "cloud",
        "limit": 2,
    }


def test_filter_named_items_returns_original_error() -> None:
    result = {"ok": False, "status": 403, "error": {"message": "denied"}}

    filtered = filter_named_items(
        result,
        collection_key="billingAccountSkuGroups",
        match="cloud",
        limit=2,
    )

    assert filtered is result
