# Technical Guide

## Agent Graph
```
Orchestrator (Event Guide)
  ├─ Retrieval Agent (Foundry IQ / SharePoint / search_event_content)
  ├─ Context Agent (Graph People/Calendar/Insights)
  ├─ Recommendation Agent (scoring + rationale)
  │    └─ Itinerary Builder (conflict checks, walking buffers)
  │         └─ Authoring Agent (SharePoint page/list stub)
  └─ Telemetry Logger (future: feature usage, latency)
```

## Data Signals (Planned)
- Calendar occupancy blocks
- Work IQ interest vectors
- Session metadata (topic, location, start/end, distance)
- Popularity or engagement scores
- People graph relations (colleagues presenting)

## Scoring Concept
```
score(session) = w_interest*similarity + w_conflict*availability + w_distance*proximity + w_popularity*engagement
```
Expose individual term contributions for explainability.

## Itinerary Logic
1. Sort top-N by score.
2. Sequentially add if no time overlap.
3. Insert walking buffer (configurable, default 10m) between locations.
4. If conflict: attempt next candidate.

## Extending Demo
| Feature | Action |
|---------|--------|
| Graph API | Add auth + client wrapper module |
| Work IQ | Ingest interests JSON, compute cosine similarity |
| SharePoint Authoring | Replace stub with REST/SDK calls |
| Telemetry | Log events to file or Application Insights |

## Error Handling
- Validate time window format `HH:MM-HH:MM`.
- Limit stops to safe range (1–10) to avoid runaway loops.

## Security Considerations
- Use principle of least privilege for Graph scopes.
- Avoid storing tokens in repo; rely on env variables or managed identity.
