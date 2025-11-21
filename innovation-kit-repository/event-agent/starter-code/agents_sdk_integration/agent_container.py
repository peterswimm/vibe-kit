"""Agent container scaffold integrating existing domain logic with Microsoft Agents SDK.
This file assumes availability of microsoft_agents.* imports; it degrades to mock mode if imports fail.
"""

from __future__ import annotations
from typing import Any, Dict, List

try:
    from microsoft_agents.activity import Activity  # type: ignore
    from microsoft_agents.hosting.core import TurnContext  # type: ignore

    HAVE_SDK = True
except ImportError:  # SDK not installed
    HAVE_SDK = False
    Activity = object  # type: ignore
    TurnContext = object  # type: ignore

from ..event_agent.models import Session, InterestProfile
from ..event_agent.scoring import ScoringEngine
from ..event_agent.itinerary import ItineraryBuilder
from ..event_agent.authoring import SharePointAuthor
from ..event_agent.work_iq import load_interest_profile


class EventGuideAgent:
    def __init__(
        self,
        scoring: ScoringEngine | None = None,
        itinerary: ItineraryBuilder | None = None,
    ):
        self.scoring = scoring or ScoringEngine()
        self.itinerary_builder = itinerary or ItineraryBuilder()
        self.author = SharePointAuthor()

    def recommend(self, interests: List[str], max_sessions: int = 3) -> Dict[str, Any]:
        profile = InterestProfile(
            raw_terms=interests, weights={t.lower(): 1.0 for t in interests}
        )
        sessions = self._load_sessions()
        ranked = self.scoring.score(sessions, profile)
        itin = self.itinerary_builder.build(ranked, max_sessions)
        return {
            "itinerary": [s.model_dump() for s in itin.sessions],
            "scoring": [
                {
                    "session": r.session.title,
                    "score": r.score,
                    "contributions": {c.name: c.value for c in r.contributions},
                }
                for r in ranked[:max_sessions]
            ],
        }

    def explain(self, session_title: str, interests: List[str]) -> Dict[str, Any]:
        profile = InterestProfile(
            raw_terms=interests, weights={t.lower(): 1.0 for t in interests}
        )
        sessions = self._load_sessions()
        ranked = self.scoring.score(sessions, profile)
        for r in ranked:
            if r.session.title.lower() == session_title.lower():
                return {
                    "session": r.session.title,
                    "score": r.score,
                    "contributions": {c.name: c.value for c in r.contributions},
                }
        return {"error": "Session not found"}

    def author_page(self, interests: List[str], max_sessions: int = 3) -> str:
        data = self.recommend(interests, max_sessions)
        titles = [it["title"] for it in data["itinerary"]]
        # NOTE: Authoring currently uses sessions with minimal details; integrate SharePoint later.
        return "Event Picks:\n" + "\n".join(f" - {t}" for t in titles)

    def _load_sessions(self) -> List[Session]:
        from ..event_agent.main import MOCK_SESSIONS  # reuse existing list

        return MOCK_SESSIONS


# SDK-specific handler example (placeholder)
if HAVE_SDK:

    class EventGuideActivityHandler:  # pragma: no cover - requires SDK runtime
        async def on_message_activity(self, turn_context: TurnContext):
            text = getattr(turn_context, "activity", {}).get("text", "")
            agent = EventGuideAgent()
            if text.startswith("recommend:"):
                interests_part = text.split(":", 1)[1]
                interests = [t.strip() for t in interests_part.split(",") if t.strip()]
                result = agent.recommend(interests)
                await turn_context.send_activity(str(result))
            elif text.startswith("explain:"):
                parts = text.split(":", 2)
                if len(parts) >= 3:
                    session_title = parts[1].strip()
                    interests_part = parts[2].strip()
                    interests = [
                        t.strip() for t in interests_part.split(",") if t.strip()
                    ]
                    result = agent.explain(session_title, interests)
                    await turn_context.send_activity(str(result))
                else:
                    await turn_context.send_activity(
                        "Format: explain:<session>:<interests>"
                    )
            else:
                await turn_context.send_activity(
                    "Commands: recommend:<interests> | explain:<session>:<interests>"
                )
