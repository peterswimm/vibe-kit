#!/usr/bin/env python3
"""Minimal demo for Event Agent kit.
Generates a mock itinerary based on interests, time window, and desired stops.
Extend with real data sources (Graph, Work IQ, Foundry IQ) later.
"""

from __future__ import annotations
import argparse
from dataclasses import dataclass
from typing import List, Tuple

MOCK_SESSIONS = [
    ("AI Safety Foundations", "13:00", "13:40", "Hall A", ["AI safety", "governance"]),
    (
        "Generative Agents in Production",
        "13:50",
        "14:30",
        "Hall C",
        ["agents", "gen ai"],
    ),
    (
        "Responsible GenAI Patterns",
        "14:40",
        "15:20",
        "Hall B",
        ["AI safety", "responsibility"],
    ),
    ("Edge Intelligence Demos", "13:10", "13:50", "Expo 2", ["edge", "agents"]),
    (
        "Telemetry for Agent Ecosystems",
        "15:30",
        "16:10",
        "Hall D",
        ["agents", "observability"],
    ),
]

BUFFER_MINUTES = 10  # walking buffer


@dataclass
class RankedSession:
    title: str
    start: str
    end: str
    location: str
    tags: List[str]
    score: float
    rationale: List[Tuple[str, float]]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Event Agent demo")
    p.add_argument(
        "--interests",
        required=True,
        help="Comma/space separated interests e.g. 'AI safety, agents'",
    )
    p.add_argument("--window", required=True, help="Time window HH:MM-HH:MM (24h)")
    p.add_argument("--stops", type=int, default=3, help="Desired number of sessions")
    return p.parse_args()


def time_to_minutes(t: str) -> int:
    h, m = map(int, t.split(":"))
    return h * 60 + m


def overlap(a_start: str, a_end: str, b_start: str, b_end: str) -> bool:
    return not (
        time_to_minutes(a_end) <= time_to_minutes(b_start)
        or time_to_minutes(b_end) <= time_to_minutes(a_start)
    )


def within_window(start: str, end: str, w_start: str, w_end: str) -> bool:
    return time_to_minutes(start) >= time_to_minutes(w_start) and time_to_minutes(
        end
    ) <= time_to_minutes(w_end)


def score_session(
    tags: List[str], interests: List[str]
) -> Tuple[float, List[Tuple[str, float]]]:
    # Simple similarity: count intersect + tag diversity heuristic
    intersection = len(set(tags) & set(interests))
    diversity = len(set(tags)) / 5.0
    score = intersection * 2.0 + diversity
    rationale = [
        ("interest_match", intersection * 2.0),
        ("diversity", diversity),
    ]
    return score, rationale


def build_ranked(interests: List[str], window: str) -> List[RankedSession]:
    w_start, w_end = window.split("-")
    ranked: List[RankedSession] = []
    for title, start, end, loc, tags in MOCK_SESSIONS:
        if not within_window(start, end, w_start, w_end):
            continue
        sc, rat = score_session(tags, interests)
        ranked.append(RankedSession(title, start, end, loc, tags, sc, rat))
    return sorted(ranked, key=lambda r: r.score, reverse=True)


def add_buffers(prev_end: str) -> str:
    return f"+{BUFFER_MINUTES}m walk"


def build_itinerary(candidates: List[RankedSession], stops: int) -> List[RankedSession]:
    itinerary: List[RankedSession] = []
    for cand in candidates:
        if len(itinerary) >= stops:
            break
        # check conflict with last session considering buffer
        conflict = False
        for existing in itinerary:
            if overlap(existing.start, existing.end, cand.start, cand.end):
                conflict = True
                break
        if not conflict:
            itinerary.append(cand)
    return itinerary


def main():
    args = parse_args()
    interests = [
        i.strip()
        for i in args.interests.replace("\n", " ").replace(",", " ").split()
        if i.strip()
    ]
    if "-" not in args.window:
        raise ValueError("Window must be HH:MM-HH:MM")
    ranked = build_ranked(interests, args.window)
    itinerary = build_itinerary(ranked, args.stops)

    print("\n=== Selected Sessions ===")
    for r in itinerary:
        print(f"{r.start}-{r.end} | {r.title} @ {r.location}")

    print("\n=== Itinerary Timeline ===")
    for idx, r in enumerate(itinerary):
        print(f"[{idx + 1}] {r.start}-{r.end} {r.title}")
        if idx < len(itinerary) - 1:
            print(f"    {add_buffers(r.end)}")

    print("\n=== Ranking Rationale (Top) ===")
    for r in itinerary:
        parts = ", ".join(f"{k}:{v:.2f}" for k, v in r.rationale)
        print(f"{r.title}: score={r.score:.2f} ({parts})")

    print("\n=== SharePoint Page Stub ===")
    print("Would create page: 'My Event Picks' with sections for:")
    for r in itinerary:
        print(f" - {r.title} ({r.start}-{r.end})")
    print("(Replace this stub with real authoring logic.)")

    print("\nDone.")


if __name__ == "__main__":
    main()
