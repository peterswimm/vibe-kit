---
description: Activation instructions for Event Agent Innovation Kit
applyTo: "**/*"
---

# Event Agent Innovation Kit Instructions

Invoke this kit when user mentions: "event agent", "event itinerary", "session recommendations", "MSR event", "conference route".

## Quick Routing

- "How do I start?" → Suggest running demo script with interests and window.
- "Explain scoring" → Reference `docs/technical-guide.md` scoring section.
- "Add more stops" → Increase `--stops` and widen time window.
- "Why ranked higher?" → Show rationale terms from output.

## Escalation

If user requests real Graph integration: prompt for tenant/app registration details (do not store) and outline next steps to replace stubs.
