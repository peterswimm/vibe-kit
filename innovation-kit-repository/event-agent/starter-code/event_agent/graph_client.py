from __future__ import annotations
import os
from typing import List, Dict, Any, Optional
import requests

GRAPH_BASE = "https://graph.microsoft.com/v1.0"


class GraphClient:
    """Minimal Microsoft Graph client wrapper.
    Falls back to mock data if credentials unavailable.
    Expects environment variables:
      GRAPH_TENANT_ID, GRAPH_CLIENT_ID, GRAPH_CLIENT_SECRET
    Uses client credentials flow for app-only tokens.
    """

    def __init__(self, scopes: Optional[List[str]] = None):
        self.tenant_id = os.getenv("GRAPH_TENANT_ID")
        self.client_id = os.getenv("GRAPH_CLIENT_ID")
        self.client_secret = os.getenv("GRAPH_CLIENT_SECRET")
        self.scopes = scopes or ["https://graph.microsoft.com/.default"]
        self._token: Optional[str] = None
        self.mock_mode = not all([self.tenant_id, self.client_id, self.client_secret])

    def _acquire_token(self) -> Optional[str]:
        if self.mock_mode:
            return None
        token_url = (
            f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        )
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": " ".join(self.scopes),
            "grant_type": "client_credentials",
        }
        resp = requests.post(token_url, data=data, timeout=15)
        resp.raise_for_status()
        return resp.json().get("access_token")

    def token(self) -> Optional[str]:
        if self._token:
            return self._token
        self._token = self._acquire_token()
        return self._token

    def _headers(self) -> Dict[str, str]:
        if self.mock_mode or not self.token():
            return {}
        return {"Authorization": f"Bearer {self.token()}"}

    # --- Mock/real endpoints ---
    def get_calendar_events(self, start_iso: str, end_iso: str) -> List[Dict[str, Any]]:
        if self.mock_mode:
            return [
                {"subject": "Team Sync", "start": start_iso, "end": end_iso},
            ]
        url = f"{GRAPH_BASE}/me/calendarView?startDateTime={start_iso}&endDateTime={end_iso}"
        resp = requests.get(url, headers=self._headers(), timeout=15)
        if resp.status_code != 200:
            return []
        return resp.json().get("value", [])

    def get_people_insights(self) -> List[Dict[str, Any]]:
        if self.mock_mode:
            return [{"displayName": "Colleague Presenter", "id": "user-123"}]
        url = f"{GRAPH_BASE}/me/people"
        resp = requests.get(url, headers=self._headers(), timeout=15)
        if resp.status_code != 200:
            return []
        return resp.json().get("value", [])
