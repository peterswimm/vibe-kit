"""Adaptive Card builders for Event Guide responses.
Produces JSON ready for Teams or other channels supporting Adaptive Cards.
"""

from __future__ import annotations
from typing import Dict, Any, List

CARD_VERSION = "1.5"


def build_itinerary_card(recommend_result: Dict[str, Any]) -> Dict[str, Any]:
    sessions: List[Dict[str, Any]] = recommend_result.get("sessions", [])
    body_items: List[Dict[str, Any]] = [
        {
            "type": "TextBlock",
            "text": "Event Guide Recommendations",
            "weight": "Bolder",
            "size": "Medium",
        }
    ]
    body = list(body_items)
    actions = []
    for idx, s in enumerate(sessions, start=1):
        title = s.get("title")
        time_range = f"{s.get('start')} - {s.get('end')}"
        loc = s.get("location")
        body_items.append(
            {
                "type": "Container",
                "items": [
                    {"type": "TextBlock", "text": title, "weight": "Bolder"},
                    {
                        "type": "TextBlock",
                        "text": f"{time_range} @ {loc}",
                        "isSubtle": True,
                        "spacing": "None",
                    },
                ],
                "style": "emphasis",
            }
        )
        body.append(
            {
                "type": "Container",
                "items": [
                    {
                        "type": "TextBlock",
                        "text": f"{idx}. {title}",
                        "weight": "Bolder",
                    },
                    {
                        "type": "TextBlock",
                        "text": f"{time_range} @ {loc}",
                        "isSubtle": True,
                        "spacing": "None",
                    },
                ],
                "style": "default",
            }
        )
        actions.append(
            {
                "type": "Action.Submit",
                "title": f"Explain #{idx}",
                "data": {
                    "action": "explainSession",
                    "sessionTitle": title,
                    "start": s.get("start"),
                    "end": s.get("end"),
                    "room": loc,
                },
            }
        )
    scoring_rows = []
    for r in recommend_result.get("scoring", []):
        scoring_rows.append(
            {
                "type": "TextBlock",
                "text": f"{r['title']}: {r['score']:.2f}",
                "wrap": True,
            }
        )
    if scoring_rows:
        body_items.append(
            {
                "type": "TextBlock",
                "text": "Scoring",
                "weight": "Bolder",
                "spacing": "Medium",
            }
        )
        body_items.extend(scoring_rows)
    card = {
        "type": "AdaptiveCard",
        "version": CARD_VERSION,
        "body": body,
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    }
    if actions:
        card["actions"] = actions
    return card
    return {
        "type": "AdaptiveCard",
        "version": CARD_VERSION,
        "body": body_items,
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    }
