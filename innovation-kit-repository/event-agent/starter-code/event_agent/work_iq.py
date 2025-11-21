from __future__ import annotations
import json
from typing import List
from .models import InterestProfile

STOP_WORDS = {"the", "and", "of", "in", "for"}


def load_interest_profile(path: str) -> InterestProfile:
    """Load Work IQ style interests from JSON file.
    Expect format: {"interests": ["AI safety", "agents", ...]}
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    raw_terms = data.get("interests", [])
    weights = {}
    for term in raw_terms:
        tokens = [t.lower() for t in term.split() if t.lower() not in STOP_WORDS]
        base = 1.0 / max(len(tokens), 1)
        for tok in tokens:
            weights[tok] = weights.get(tok, 0) + base
    return InterestProfile(raw_terms=raw_terms, weights=weights)
