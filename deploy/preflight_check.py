#!/usr/bin/env python3
"""
preflight_check.py — Pre-deployment credential and workspace accessibility check.

Validates that the configured service principal can:
  1. Acquire an AAD token for the Fabric API.
  2. Reach the Fabric REST API (GET /v1/workspaces/<workspace_id>).

Exit codes:
  0 — all checks passed
  1 — one or more checks failed

Usage:
    python deploy/preflight_check.py

All configuration is read from the same environment variables used by
deploy_workspace.py (see .env.example).
"""

from __future__ import annotations

import logging
import sys

import requests
from azure.core.exceptions import ClientAuthenticationError
from azure.identity import ClientSecretCredential

from deploy._credential import _env, build_credential

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S%z",
    stream=sys.stdout,
)
logger = logging.getLogger("fabric-cicd-preflight")

FABRIC_API_BASE = "https://api.fabric.microsoft.com"
FABRIC_SCOPE = "https://api.fabric.microsoft.com/.default"


def check_token(credential: ClientSecretCredential, environment: str) -> bool:
    """Verify the service principal can acquire a Fabric API token."""
    logger.info("[%s] Checking AAD token acquisition…", environment)
    try:
        token = credential.get_token(FABRIC_SCOPE)
        # Mask token — only show first 10 chars for debugging
        logger.info(
            "[%s] AAD token acquired successfully (token[:10]=%s…).",
            environment,
            token.token[:10],
        )
        return True
    except ClientAuthenticationError as exc:
        logger.error(
            "[%s] AAD token acquisition FAILED.\n"
            "  Cause: %s\n"
            "  Hint: Verify TENANT_ID, CLIENT_ID, CLIENT_SECRET are correct for\n"
            "        this environment and that the service principal exists in the\n"
            "        target Azure AD tenant (not a different tenant/directory).",
            environment,
            exc,
        )
        return False
    except Exception as exc:  # noqa: BLE001
        logger.error("[%s] Unexpected error acquiring token: %s", environment, exc)
        return False


def check_workspace_access(
    credential: ClientSecretCredential, workspace_id: str, environment: str
) -> bool:
    """Verify the service principal can read the target Fabric workspace."""
    logger.info(
        "[%s] Checking Fabric workspace access (workspace_id=%s)…",
        environment,
        workspace_id,
    )
    try:
        token = credential.get_token(FABRIC_SCOPE).token
    except Exception as exc:  # noqa: BLE001
        logger.error("[%s] Cannot check workspace — token error: %s", environment, exc)
        return False

    url = f"{FABRIC_API_BASE}/v1/workspaces/{workspace_id}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        resp = requests.get(url, headers=headers, timeout=30)
    except requests.RequestException as exc:
        logger.error(
            "[%s] HTTP request to Fabric API failed: %s\n"
            "  Hint: Check network connectivity and that the Fabric API endpoint\n"
            "        (%s) is reachable from the runner.",
            environment,
            exc,
            FABRIC_API_BASE,
        )
        return False

    if resp.status_code == 200:
        data = resp.json()
        logger.info(
            "[%s] Workspace accessible — name=%r, capacity=%r.",
            environment,
            data.get("displayName"),
            data.get("capacityId"),
        )
        return True

    if resp.status_code == 403:
        logger.error(
            "[%s] Workspace access DENIED (HTTP 403).\n"
            "  Workspace ID : %s\n"
            "  Hint: The service principal (client_id in CLIENT_ID env var) must be\n"
            "        added to the Fabric workspace with at least 'Contributor' role.\n"
            "  Steps to fix:\n"
            "    1. Open the Fabric portal (https://app.fabric.microsoft.com).\n"
            "    2. Navigate to the workspace.\n"
            "    3. Go to Workspace settings → Manage access.\n"
            "    4. Add the service principal with the 'Contributor' role.",
            environment,
            workspace_id,
        )
        return False

    if resp.status_code == 404:
        logger.error(
            "[%s] Workspace NOT FOUND (HTTP 404).\n"
            "  Workspace ID : %s\n"
            "  Hint: Verify TARGET_WORKSPACE_ID is the correct Fabric workspace GUID.",
            environment,
            workspace_id,
        )
        return False

    logger.error(
        "[%s] Unexpected response from Fabric API (HTTP %d): %s",
        environment,
        resp.status_code,
        resp.text[:500],
    )
    return False


def main() -> None:
    environment = _env("TARGET_ENVIRONMENT")
    workspace_id = _env("TARGET_WORKSPACE_ID")

    credential, tenant_id, client_id = build_credential(environment)

    logger.info("=" * 60)
    logger.info("PRE-FLIGHT CHECK")
    logger.info("  Environment   : %s", environment)
    logger.info("  Workspace ID  : %s", workspace_id)
    logger.info("  Tenant ID     : %s", tenant_id)
    logger.info("  Client ID     : %s", client_id)
    logger.info("=" * 60)

    results = [
        ("AAD token acquisition", check_token(credential, environment)),
        (
            "Fabric workspace access",
            check_workspace_access(credential, workspace_id, environment),
        ),
    ]

    logger.info("-" * 60)
    all_passed = True
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        logger.info("  %-30s %s", name, status)
        if not passed:
            all_passed = False
    logger.info("-" * 60)

    if not all_passed:
        logger.error(
            "Pre-flight checks FAILED. Fix the errors above before deploying.\n"
            "Common fixes:\n"
            "  • Wrong tenant: ensure TENANT_ID matches the tenant that owns the\n"
            "    service principal AND the Fabric workspace.\n"
            "  • SP not in workspace: add the SP to the workspace with Contributor\n"
            "    role via Fabric portal → Workspace settings → Manage access.\n"
            "  • SP not consented: run  az ad sp show --id <CLIENT_ID>  to verify\n"
            "    the SP exists in the target tenant."
        )
        sys.exit(1)

    logger.info("All pre-flight checks PASSED — safe to deploy.")
    sys.exit(0)


if __name__ == "__main__":
    main()
