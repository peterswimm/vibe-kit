from __future__ import annotations
from typing import List
from .models import Session, RecommendationResult, Itinerary


class ItineraryBuilder:
    def __init__(self, walking_buffer_minutes: int = 10):
        self.walking_buffer_minutes = walking_buffer_minutes

    def _to_minutes(self, hhmm: str) -> int:
        h, m = map(int, hhmm.split(":"))
        return h * 60 + m

    def _conflict(self, a: Session, b: Session) -> bool:
        return not (
            self._to_minutes(a.end) + self.walking_buffer_minutes
            <= self._to_minutes(b.start)
            or self._to_minutes(b.end) + self.walking_buffer_minutes
            <= self._to_minutes(a.start)
        )

    def build(self, ranked: List[RecommendationResult], max_sessions: int) -> Itinerary:
        chosen: List[Session] = []
        conflicts = 0
        for r in ranked:
            if len(chosen) >= max_sessions:
                break
            has_conflict = any(
                self._conflict(r.session, existing) for existing in chosen
            )
            if has_conflict:
                conflicts += 1
                continue
            chosen.append(r.session)
        return Itinerary(
            sessions=chosen,
            total_sessions=len(chosen),
            conflicts=conflicts,
            walking_buffer_minutes=self.walking_buffer_minutes,
        )
