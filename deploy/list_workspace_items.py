#!/usr/bin/env python3
"""
list_workspace_items.py — Post-deployment workspace item listing.

Queries the Fabric REST API to list all items in the target workspace
and prints a summary. Useful for verifying that a deployment succeeded.

Usage:
    # TOKEN is read from stdin or the FABRIC_ACCESS_TOKEN env var
    python deploy/list_workspace_items.py

Required environment variables:
    TARGET_WORKSPACE_ID   — Fabric workspace GUID to query
    FABRIC_ACCESS_TOKEN   — Bearer token with Fabric API access (optional;
                            if not set the script exits 0 with a warning)
"""

from __future__ import annotations

import logging
import os
import sys

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S%z",
    stream=sys.stdout,
)
logger = logging.getLogger("fabric-cicd-list-items")

FABRIC_API_BASE = "https://api.fabric.microsoft.com"


def main() -> None:
    workspace_id = os.environ.get("TARGET_WORKSPACE_ID")
    token = os.environ.get("FABRIC_ACCESS_TOKEN")

    if not workspace_id:
        logger.error("TARGET_WORKSPACE_ID is not set.")
        sys.exit(1)

    if not token:
        logger.warning(
            "FABRIC_ACCESS_TOKEN is not set — skipping workspace item listing."
        )
        sys.exit(0)

    url = f"{FABRIC_API_BASE}/v1/workspaces/{workspace_id}/items"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        resp = requests.get(url, headers=headers, timeout=30)
    except requests.RequestException as exc:
        logger.error("HTTP request to Fabric API failed: %s", exc)
        sys.exit(1)

    if resp.status_code != 200:
        logger.error(
            "Fabric API returned HTTP %d: %s", resp.status_code, resp.text[:500]
        )
        sys.exit(1)

    items = resp.json().get("value", [])
    logger.info("=== Fabric workspace items after deployment ===")
    logger.info("Workspace ID  : %s", workspace_id)
    logger.info("Total items   : %d", len(items))
    for item in items:
        logger.info(
            "  %-22s  %s",
            item.get("type", "?"),
            item.get("displayName", "?"),
        )


if __name__ == "__main__":
    main()
