"""Session cache with TTL for Event Guide Agent.

Caches sessions in memory with configurable expiration.
Reduces Graph API calls while ensuring fresh data.
"""

from __future__ import annotations
import time
from typing import List, Optional
from dataclasses import dataclass

try:
    from ..event_agent.models import Session  # type: ignore
except ImportError:
    from event_agent.models import Session  # type: ignore  # pragma: no cover


@dataclass
class CacheEntry:
    """Cached sessions with expiration timestamp."""

    sessions: List[Session]
    expires_at: float


class SessionCache:
    """In-memory session cache with TTL."""

    def __init__(self, ttl_minutes: int = 15):
        self.ttl_seconds = ttl_minutes * 60
        self._entry: Optional[CacheEntry] = None

    def get(self) -> Optional[List[Session]]:
        """Return cached sessions if still valid, else None."""
        if self._entry is None:
            return None
        if time.time() > self._entry.expires_at:
            self._entry = None
            return None
        return self._entry.sessions

    def set(self, sessions: List[Session]) -> None:
        """Store sessions with new expiration timestamp."""
        self._entry = CacheEntry(
            sessions=sessions, expires_at=time.time() + self.ttl_seconds
        )

    def invalidate(self) -> None:
        """Clear cached sessions."""
        self._entry = None

    def is_valid(self) -> bool:
        """Check if cache contains valid data."""
        return self.get() is not None
