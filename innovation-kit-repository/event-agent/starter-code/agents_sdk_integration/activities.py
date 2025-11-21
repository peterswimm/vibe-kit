"""Activity abstractions independent from SDK runtime, enabling reuse in tests."""

from __future__ import annotations
from typing import List, Dict, Any

try:
    from ..event_agent.scoring import ScoringEngine  # type: ignore
    from ..event_agent.itinerary import ItineraryBuilder  # type: ignore
    from ..event_agent.models import InterestProfile  # type: ignore
    from ..event_agent.main import MOCK_SESSIONS  # type: ignore
    from . import graph_sources  # type: ignore
except ImportError:
    # Fallback when executed outside package context
    from event_agent.scoring import ScoringEngine  # type: ignore
    from event_agent.itinerary import ItineraryBuilder  # type: ignore
    from event_agent.models import InterestProfile  # type: ignore
    from event_agent.main import MOCK_SESSIONS  # type: ignore
    import graph_sources  # type: ignore


class RecommendActivity:
    def __init__(
        self,
        scoring: ScoringEngine | None = None,
        itinerary: ItineraryBuilder | None = None,
        include_card: bool = True,
        publish_itinerary: bool = False,
    ):
        self.scoring = scoring or ScoringEngine()
        self.itinerary_builder = itinerary or ItineraryBuilder()
        self.include_card = include_card
        self.publish_itinerary = publish_itinerary

    def run(
        self, interests: List[str], max_sessions: int = 3, user_name: str = "User"
    ) -> Dict[str, Any]:
        profile = InterestProfile(
            raw_terms=interests, weights={t.lower(): 1.0 for t in interests}
        )

        # Fetch sessions with telemetry capture
        dynamic_sessions = graph_sources.fetch_sessions()
        if dynamic_sessions:
            source_sessions = dynamic_sessions
            session_source = "graph"
        else:
            source_sessions = MOCK_SESSIONS
            session_source = "mock"

        ranked = self.scoring.score(source_sessions, profile)
        itinerary = self.itinerary_builder.build(ranked, max_sessions)

        result: Dict[str, Any] = {
            "sessions": [s.model_dump() for s in itinerary.sessions],
            "scoring": [
                {
                    "title": r.session.title,
                    "score": r.score,
                    "contributions": {c.name: c.value for c in r.contributions},
                }
                for r in ranked[:max_sessions]
            ],
            "conflicts": itinerary.conflicts,
            "sessionSource": session_source,
        }

        # Adaptive card
        if self.include_card:
            try:
                from .adaptive_cards import build_itinerary_card  # type: ignore
            except ImportError:
                from adaptive_cards import build_itinerary_card  # type: ignore
            result["adaptiveCard"] = build_itinerary_card(result)

        # Publish itinerary to SharePoint if enabled
        if self.publish_itinerary:
            publish_result = graph_sources.publish_itinerary(
                itinerary.sessions, user_name
            )
            result["publish"] = publish_result

        return result


class ExplainActivity:
    def __init__(self, scoring: ScoringEngine | None = None):
        self.scoring = scoring or ScoringEngine()

    def run(self, session_title: str, interests: List[str]) -> Dict[str, Any]:
        profile = InterestProfile(
            raw_terms=interests, weights={t.lower(): 1.0 for t in interests}
        )
        dynamic_sessions = graph_sources.fetch_sessions()
        source_sessions = dynamic_sessions if dynamic_sessions else MOCK_SESSIONS
        ranked = self.scoring.score(source_sessions, profile)
        for r in ranked:
            if r.session.title.lower() == session_title.lower():
                return {
                    "title": r.session.title,
                    "score": r.score,
                    "contributions": {c.name: c.value for c in r.contributions},
                }
        return {"error": "Session not found"}
