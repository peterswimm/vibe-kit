"""MSAL authentication wrapper for acquiring tokens.
Supports client credentials flow with caching.
"""

from __future__ import annotations
import os
from typing import Optional
import time

try:
    import msal  # type: ignore

    HAVE_MSAL = True
except ImportError:  # pragma: no cover
    HAVE_MSAL = False


class TokenCache:
    def __init__(self):
        self._token: Optional[str] = None
        self._expires: float = 0.0

    def set(self, token: str, expires_in: int):
        self._token = token
        self._expires = time.time() + expires_in - 30  # safety margin

    def get(self) -> Optional[str]:
        if not self._token or time.time() >= self._expires:
            return None
        return self._token


class MsalClientCredentials:
    def __init__(self, scope: str = "https://graph.microsoft.com/.default"):
        self.tenant = os.getenv("GRAPH_TENANT_ID")
        self.client_id = os.getenv("GRAPH_CLIENT_ID")
        self.secret = os.getenv("GRAPH_CLIENT_SECRET")
        self.scope = scope
        self.cache = TokenCache()
        if not HAVE_MSAL:
            raise RuntimeError("msal not installed")
        if not all([self.tenant, self.client_id, self.secret]):
            raise RuntimeError("Missing required environment variables for MSAL auth")
        self.app = msal.ConfidentialClientApplication(
            client_id=self.client_id,
            client_credential=self.secret,
            authority=f"https://login.microsoftonline.com/{self.tenant}",
        )

    def acquire_token(self) -> str:
        cached = self.cache.get()
        if cached:
            return cached
        result = self.app.acquire_token_for_client(scopes=[self.scope])
        if "access_token" not in result:
            raise RuntimeError(f"Token acquisition failed: {result}")
        token = result["access_token"]
        expires_in = int(result.get("expires_in", 3600))
        self.cache.set(token, expires_in)
        return token
