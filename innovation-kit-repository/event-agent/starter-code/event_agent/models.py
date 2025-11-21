from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Dict


class Session(BaseModel):
    id: str
    title: str
    start: str  # HH:MM
    end: str  # HH:MM
    location: str
    tags: List[str] = Field(default_factory=list)
    popularity: float = 0.0  # placeholder metric


class InterestProfile(BaseModel):
    raw_terms: List[str]
    weights: Dict[str, float]  # term -> weight


class RecommendationFeatureContribution(BaseModel):
    name: str
    value: float


class RecommendationResult(BaseModel):
    session: Session
    score: float
    contributions: List[RecommendationFeatureContribution]


class Itinerary(BaseModel):
    sessions: List[Session]
    total_sessions: int
    conflicts: int
    walking_buffer_minutes: int
