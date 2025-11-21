# Quick Start

## Goal
Run the Event Agent demo to produce a 3-stop recommended route with rationale based on interests and time window.

## Steps
1. Ensure Python 3.11+ available.
2. Execute demo script:
   ```bash
   python innovation-kit-repository/event-agent/assets/scripts/run_event_agent_demo.py \
     --interests "AI safety" --window "13:00-16:00" --stops 3
   ```
3. Observe output sections:
   - Selected Sessions
   - Itinerary Timeline (with buffers)
   - Ranking Rationale (feature breakdown)
   - SharePoint Page Stub (optional)

## Customization
Change interests or window:
```bash
python .../run_event_agent_demo.py --interests "generative AI,agents" --window "10:00-14:30" --stops 4
```

## Next
For architecture and agent graph details, read `technical-guide.md`.
