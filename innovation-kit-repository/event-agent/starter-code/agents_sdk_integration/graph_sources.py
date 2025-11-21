"""Graph & SharePoint data source integration for Event Guide.

Fetches event sessions from Microsoft Graph Calendar API.
Publishes itinerary summaries to SharePoint Pages.
Includes caching, auth, and telemetry.
"""

from __future__ import annotations
from typing import List, Dict, Any, Optional
import os
import time
import requests

try:
    from ..event_agent.models import Session  # type: ignore
except ImportError:
    from event_agent.models import Session  # type: ignore  # pragma: no cover

try:
    from .auth import MsalClientCredentials  # type: ignore
    from .session_cache import SessionCache  # type: ignore
    from .settings import get_settings  # type: ignore
except ImportError:
    from auth import MsalClientCredentials  # type: ignore
    from session_cache import SessionCache  # type: ignore
    from settings import get_settings  # type: ignore


# Global cache instance
_cache: Optional[SessionCache] = None


def get_cache() -> SessionCache:
    """Lazy-load session cache singleton."""
    global _cache
    if _cache is None:
        settings = get_settings()
        _cache = SessionCache(ttl_minutes=settings.session_cache_ttl_minutes)
    return _cache


def _map_graph_event_to_session(event: Dict[str, Any]) -> Session:
    """Map Graph Calendar event JSON to Session model.

    Graph event schema:
    {
      "id": "...",
      "subject": "...",
      "start": {"dateTime": "2025-11-21T13:00:00", "timeZone": "UTC"},
      "end": {"dateTime": "2025-11-21T13:40:00", "timeZone": "UTC"},
      "location": {"displayName": "Hall A"},
      "categories": ["AI", "safety"]
    }
    """
    event_id = event.get("id", "unknown")
    title = event.get("subject", "Untitled Session")
    start_dt = event.get("start", {}).get("dateTime", "")
    end_dt = event.get("end", {}).get("dateTime", "")
    # Extract HH:MM from ISO datetime
    start_time = start_dt.split("T")[1][:5] if "T" in start_dt else "00:00"
    end_time = end_dt.split("T")[1][:5] if "T" in end_dt else "00:00"
    location = event.get("location", {}).get("displayName", "TBD")
    tags = event.get("categories", [])
    # Popularity heuristic: count attendees or default 0.5
    attendees = event.get("attendees", [])
    popularity = min(1.0, len(attendees) / 100.0) if attendees else 0.5

    return Session(
        id=event_id,
        title=title,
        start=start_time,
        end=end_time,
        location=location,
        tags=tags,
        popularity=popularity,
    )


def fetch_sessions_from_graph(calendar_id: str = "me") -> Dict[str, Any]:
    """Fetch sessions from Graph Calendar API with auth and timing.

    Returns dict with sessions list, latency, and error info.
    """
    settings = get_settings()
    start_time = time.time()

    try:
        auth_client = MsalClientCredentials()
        token = auth_client.acquire_token()
    except Exception as e:
        return {
            "sessions": [],
            "latency_ms": int((time.time() - start_time) * 1000),
            "error": f"Auth failed: {e}",
        }

    # Use provided calendar ID or fall back to user's default
    cal_id = settings.graph_calendar_id or calendar_id
    url = f"https://graph.microsoft.com/v1.0/me/calendars/{cal_id}/events"
    if cal_id == "me":
        url = "https://graph.microsoft.com/v1.0/me/events"

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        events = data.get("value", [])
        sessions = [_map_graph_event_to_session(e) for e in events]
        latency_ms = int((time.time() - start_time) * 1000)
        return {"sessions": sessions, "latency_ms": latency_ms, "count": len(sessions)}
    except requests.exceptions.RequestException as e:
        return {
            "sessions": [],
            "latency_ms": int((time.time() - start_time) * 1000),
            "error": f"Graph API call failed: {e}",
        }


def fetch_sessions() -> List[Session]:
    """Return sessions from cache or Graph, with fallback to empty list.

    Respects ENABLE_GRAPH_FETCH feature flag and cache TTL.
    Returns empty list if disabled or error; caller falls back to MOCK_SESSIONS.
    """
    settings = get_settings()

    if not settings.enable_graph_fetch:
        return []

    if not settings.graph_enabled():
        return []

    cache = get_cache()
    if settings.enable_session_cache:
        cached = cache.get()
        if cached is not None:
            return cached

    # Fetch from Graph
    result = fetch_sessions_from_graph()
    sessions = result.get("sessions", [])

    if sessions and settings.enable_session_cache:
        cache.set(sessions)

    return sessions


def publish_itinerary(
    sessions: List[Session], user_name: str = "User"
) -> Dict[str, Any]:
    """Publish itinerary to SharePoint page with real API call.

    Creates a new SharePoint page with markdown-formatted itinerary.
    Returns permalink URL or error info.
    """
    settings = get_settings()
    start_time = time.time()

    if not settings.enable_sharepoint_publish:
        return {
            "status": "skipped",
            "reason": "ENABLE_SHAREPOINT_PUBLISH=false",
            "latency_ms": 0,
        }

    if not settings.graph_enabled() or not settings.sharepoint_site_id:
        return {
            "status": "error",
            "reason": "Missing Graph credentials or SHAREPOINT_SITE_ID",
            "latency_ms": 0,
        }

    try:
        auth_client = MsalClientCredentials()
        token = auth_client.acquire_token()
    except Exception as e:
        return {
            "status": "error",
            "reason": f"Auth failed: {e}",
            "latency_ms": int((time.time() - start_time) * 1000),
        }

    # Build markdown itinerary
    markdown_body = f"# Event Itinerary for {user_name}\n\n"
    for idx, session in enumerate(sessions, start=1):
        markdown_body += f"## {idx}. {session.title}\n"
        markdown_body += f"**Time**: {session.start} - {session.end}\n\n"
        markdown_body += f"**Location**: {session.location}\n\n"
        if session.tags:
            markdown_body += f"**Tags**: {', '.join(session.tags)}\n\n"
        markdown_body += "---\n\n"

    # SharePoint Pages API: POST /sites/{site-id}/pages
    url = f"https://graph.microsoft.com/v1.0/sites/{settings.sharepoint_site_id}/pages"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # Page creation payload
    page_title = f"Event Itinerary - {user_name}"
    payload = {
        "name": f"itinerary-{int(time.time())}.aspx",
        "title": page_title,
        "pageLayout": "article",
        "promotionKind": "page",
        "canvasLayout": {
            "horizontalSections": [
                {
                    "layout": "oneColumn",
                    "columns": [
                        {
                            "width": 12,
                            "webparts": [
                                {
                                    "type": "text",
                                    "data": {
                                        "innerHTML": markdown_body.replace(
                                            "\n", "<br/>"
                                        )
                                    },
                                }
                            ],
                        }
                    ],
                }
            ]
        },
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        page_data = response.json()
        page_url = page_data.get("webUrl", "<URL not returned>")
        latency_ms = int((time.time() - start_time) * 1000)
        return {
            "status": "published",
            "url": page_url,
            "latency_ms": latency_ms,
            "page_id": page_data.get("id"),
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "reason": f"SharePoint API call failed: {e}",
            "latency_ms": int((time.time() - start_time) * 1000),
        }
