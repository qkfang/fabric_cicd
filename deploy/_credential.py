"""
_credential.py — Shared helper for building Azure ClientSecretCredential.

Reads <ENV>_TENANT_ID / <ENV>_CLIENT_ID / <ENV>_CLIENT_SECRET first, then
falls back to the generic FABRIC_* variables.  Shared between
deploy_workspace.py and preflight_check.py.
"""

from __future__ import annotations

import logging
import os
import sys

from azure.identity import ClientSecretCredential

logger = logging.getLogger(__name__)


def _env(name: str, required: bool = True, default: str | None = None) -> str | None:
    value = os.environ.get(name, default)
    if required and not value:
        logger.error("Required environment variable %s is not set.", name)
        sys.exit(1)
    return value


def build_credential(environment: str) -> tuple[ClientSecretCredential, str, str]:
    """Build a ClientSecretCredential for *environment* from env vars.

    Returns
    -------
    (credential, tenant_id, client_id)
    """
    env_prefix = environment.upper()
    tenant_id = (
        os.environ.get(f"{env_prefix}_TENANT_ID") or _env("FABRIC_TENANT_ID")
    )
    client_id = (
        os.environ.get(f"{env_prefix}_CLIENT_ID") or _env("FABRIC_CLIENT_ID")
    )
    client_secret = (
        os.environ.get(f"{env_prefix}_CLIENT_SECRET") or _env("FABRIC_CLIENT_SECRET")
    )
    return (
        ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret,
        ),
        tenant_id,
        client_id,
    )
