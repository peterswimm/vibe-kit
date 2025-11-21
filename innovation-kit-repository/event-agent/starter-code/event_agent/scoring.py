from __future__ import annotations
from typing import List
from .models import (
    Session,
    InterestProfile,
    RecommendationResult,
    RecommendationFeatureContribution,
)


class ScoringEngine:
    def __init__(
        self,
        w_interest: float = 2.0,
        w_popularity: float = 0.5,
        w_diversity: float = 0.3,
    ):
        self.w_interest = w_interest
        self.w_popularity = w_popularity
        self.w_diversity = w_diversity

    def score(
        self, sessions: List[Session], profile: InterestProfile
    ) -> List[RecommendationResult]:
        results: List[RecommendationResult] = []
        for s in sessions:
            tokens = [t.lower() for tag in s.tags for t in tag.split()]
            interest_score = sum(profile.weights.get(t, 0) for t in tokens)
            diversity_score = len(set(tokens)) / max(len(tokens), 1)
            popularity_score = s.popularity
            total = (
                interest_score * self.w_interest
                + popularity_score * self.w_popularity
                + diversity_score * self.w_diversity
            )
            contributions = [
                RecommendationFeatureContribution(
                    name="interest_match", value=interest_score * self.w_interest
                ),
                RecommendationFeatureContribution(
                    name="popularity", value=popularity_score * self.w_popularity
                ),
                RecommendationFeatureContribution(
                    name="diversity", value=diversity_score * self.w_diversity
                ),
            ]
            results.append(
                RecommendationResult(
                    session=s, score=total, contributions=contributions
                )
            )
        return sorted(results, key=lambda r: r.score, reverse=True)
