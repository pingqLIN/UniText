from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from gcp_billing_rest import append_query, billing_request


def normalize_billing_account(billing_account: str) -> str:
    if billing_account.startswith("billingAccounts/"):
        return billing_account
    return f"billingAccounts/{billing_account}"


def limit_items(items: list[dict[str, Any]], limit: int | None) -> list[dict[str, Any]]:
    if limit is None or limit < 0:
        return items
    return items[:limit]


def filter_named_items(
    result: dict[str, Any],
    *,
    collection_key: str,
    match: str | None,
    limit: int | None,
) -> dict[str, Any]:
    if not result.get("ok"):
        return result

    data = result.get("data")
    if not isinstance(data, dict):
        return result

    items = data.get(collection_key)
    if not isinstance(items, list):
        return result

    normalized_match = match.casefold() if match else None
    filtered_items = items
    if normalized_match:
        filtered_items = [
            item
            for item in items
            if normalized_match in str(item.get("displayName", "")).casefold()
            or normalized_match in str(item.get("name", "")).casefold()
        ]

    limited_items = limit_items(filtered_items, limit)
    updated_data = dict(data)
    updated_data[collection_key] = limited_items
    updated_data["_meta"] = {
        "totalCount": len(items),
        "matchedCount": len(filtered_items),
        "returnedCount": len(limited_items),
        "match": match,
        "limit": limit,
    }
    return {**result, "data": updated_data}


def list_sku_groups(billing_account: str, match: str | None, limit: int | None) -> dict[str, Any]:
    account_name = normalize_billing_account(billing_account)
    url = append_query(
        f"https://cloudbilling.googleapis.com/v1beta/{account_name}/skuGroups",
        {"pageSize": 5000},
    )
    result = billing_request(method="GET", url=url)
    return filter_named_items(
        result,
        collection_key="billingAccountSkuGroups",
        match=match,
        limit=limit,
    )


def list_group_skus(
    billing_account: str,
    sku_group_id: str,
    match: str | None,
    limit: int | None,
) -> dict[str, Any]:
    account_name = normalize_billing_account(billing_account)
    url = append_query(
        f"https://cloudbilling.googleapis.com/v1beta/{account_name}/skuGroups/{sku_group_id}/skus",
        {"pageSize": 5000},
    )
    result = billing_request(method="GET", url=url)
    return filter_named_items(
        result,
        collection_key="skus",
        match=match,
        limit=limit,
    )


def list_sku_prices(billing_account: str, sku_id: str) -> dict[str, Any]:
    account_name = normalize_billing_account(billing_account)
    url = append_query(
        f"https://cloudbilling.googleapis.com/v1beta/{account_name}/skus/{sku_id}/prices",
        {"pageSize": 100},
    )
    return billing_request(method="GET", url=url)


def get_sku_price(billing_account: str, sku_id: str, currency_code: str | None) -> dict[str, Any]:
    account_name = normalize_billing_account(billing_account)
    url = append_query(
        f"https://cloudbilling.googleapis.com/v1beta/{account_name}/skus/{sku_id}/price",
        {"currencyCode": currency_code},
    )
    return billing_request(method="GET", url=url)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read pricing data from the Cloud Billing Pricing API using gcloud auth."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    groups_parser = subparsers.add_parser("list-sku-groups", help="List SKU groups for a billing account.")
    groups_parser.add_argument("--billing-account", required=True)
    groups_parser.add_argument("--match", help="Case-insensitive substring filter for displayName or name.")
    groups_parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Maximum number of matched rows to return. Use -1 for no limit.",
    )

    skus_parser = subparsers.add_parser("list-group-skus", help="List SKUs for a billing account SKU group.")
    skus_parser.add_argument("--billing-account", required=True)
    skus_parser.add_argument("--sku-group-id", required=True)
    skus_parser.add_argument("--match", help="Case-insensitive substring filter for displayName or name.")
    skus_parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Maximum number of matched rows to return. Use -1 for no limit.",
    )

    prices_parser = subparsers.add_parser("list-sku-prices", help="List prices for a billing-account SKU.")
    prices_parser.add_argument("--billing-account", required=True)
    prices_parser.add_argument("--sku-id", required=True)

    price_parser = subparsers.add_parser("get-sku-price", help="Get the current price for a billing-account SKU.")
    price_parser.add_argument("--billing-account", required=True)
    price_parser.add_argument("--sku-id", required=True)
    price_parser.add_argument("--currency-code")

    args = parser.parse_args()

    if args.command == "list-sku-groups":
        result = list_sku_groups(args.billing_account, args.match, args.limit)
    elif args.command == "list-group-skus":
        result = list_group_skus(args.billing_account, args.sku_group_id, args.match, args.limit)
    elif args.command == "list-sku-prices":
        result = list_sku_prices(args.billing_account, args.sku_id)
    else:
        result = get_sku_price(args.billing_account, args.sku_id, args.currency_code)

    print(json.dumps(result, indent=2))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
