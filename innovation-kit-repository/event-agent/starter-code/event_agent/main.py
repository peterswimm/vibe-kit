from __future__ import annotations
import argparse
import json
from typing import List
from .models import Session
from .work_iq import load_interest_profile
from .scoring import ScoringEngine
from .itinerary import ItineraryBuilder
from .authoring import SharePointAuthor
from .telemetry import TelemetryLogger
from .graph_client import GraphClient

MOCK_SESSIONS = [
    Session(
        id="s1",
        title="AI Safety Foundations",
        start="13:00",
        end="13:40",
        location="Hall A",
        tags=["AI safety", "governance"],
        popularity=0.8,
    ),
    Session(
        id="s2",
        title="Generative Agents in Production",
        start="13:50",
        end="14:30",
        location="Hall C",
        tags=["agents", "gen ai"],
        popularity=0.9,
    ),
    Session(
        id="s3",
        title="Responsible GenAI Patterns",
        start="14:40",
        end="15:20",
        location="Hall B",
        tags=["AI safety", "responsibility"],
        popularity=0.7,
    ),
    Session(
        id="s4",
        title="Edge Intelligence Demos",
        start="13:10",
        end="13:50",
        location="Expo 2",
        tags=["edge", "agents"],
        popularity=0.6,
    ),
    Session(
        id="s5",
        title="Telemetry for Agent Ecosystems",
        start="15:30",
        end="16:10",
        location="Hall D",
        tags=["agents", "observability"],
        popularity=0.65,
    ),
]


def parse_args():
    p = argparse.ArgumentParser(description="Event Agent Orchestrator")
    p.add_argument(
        "--work-iq-json", help="Path to Work IQ interests JSON", required=False
    )
    p.add_argument(
        "--interests", help="Comma separated interests if no JSON", required=False
    )
    p.add_argument("--max-sessions", type=int, default=3)
    p.add_argument("--walking-buffer", type=int, default=10)
    p.add_argument("--output", help="Optional JSON output file", required=False)
    p.add_argument(
        "--show-calendar", action="store_true", help="Fetch mock/real calendar events"
    )
    return p.parse_args()


def build_sessions() -> List[Session]:
    return MOCK_SESSIONS


def main():
    args = parse_args()
    if args.work_iq_json:
        profile = load_interest_profile(args.work_iq_json)
    else:
        if not args.interests:
            raise SystemExit("Provide --interests or --work-iq-json")
        raw_terms = [t.strip() for t in args.interests.split(",") if t.strip()]
        # emulate Work IQ vectorization
        weights = {term.lower(): 1.0 for term in raw_terms}
        from .models import InterestProfile

        profile = InterestProfile(raw_terms=raw_terms, weights=weights)

    sessions = build_sessions()
    scoring = ScoringEngine()
    ranked = scoring.score(sessions, profile)
    itinerary_builder = ItineraryBuilder(walking_buffer_minutes=args.walking_buffer)
    itinerary = itinerary_builder.build(ranked, max_sessions=args.max_sessions)

    author = SharePointAuthor()
    telemetry = TelemetryLogger()
    graph = GraphClient()

    if args.show_calendar:
        events = graph.get_calendar_events(
            "2025-06-01T13:00:00Z", "2025-06-01T16:00:00Z"
        )
    else:
        events = []

    print("\n=== Recommended Itinerary ===")
    for s in itinerary.sessions:
        print(f"{s.start}-{s.end} | {s.title} @ {s.location}")

    print("\n=== Scoring Detail ===")
    for r in ranked[: args.max_sessions]:
        contrib = ", ".join(f"{c.name}:{c.value:.2f}" for c in r.contributions)
        print(f"{r.session.title}: score={r.score:.2f} ({contrib})")

    print("\n=== SharePoint Stub ===")
    print(author.create_page_stub(itinerary.sessions))

    if events:
        print("\n=== Calendar Events (Mock/Real) ===")
        for e in events:
            print(f"Event: {e.get('subject', '(no subject)')}")

    telemetry.log(
        "run", {"sessions": len(itinerary.sessions), "conflicts": itinerary.conflicts}
    )

    if args.output:
        out = {
            "itinerary": [s.model_dump() for s in itinerary.sessions],
            "ranked": [r.model_dump() for r in ranked],
            "calendar_events": events,
        }
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2)
        print(f"\nWrote output to {args.output}")

    print("\nDone.")


if __name__ == "__main__":
    main()
