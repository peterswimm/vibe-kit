# Event Agent Innovation Kit

## Overview
This kit packages an attendee-facing Event Discovery Agent. It recommends Microsoft Research (MSR) projects, demos, and sessions with explainable rankings, leveraging Graph signals (people, calendar, insights), Work IQ interests, and curated event feeds. It can build itineraries, avoid time/location conflicts, and optionally author SharePoint pages summarizing selections.

## Capabilities
- Multi-agent orchestration (Guide, Retrieval, Context, Recommendation, Itinerary, Authoring, Telemetry)
- Explainable ranking (surface feature contributions/weights)
- Itinerary conflict detection (time + walking buffer)
- SharePoint authoring (page/list) stub
- Extensible tooling layer (Graph, Foundry IQ, Work IQ, Search)

## Quick Start Path
1. Read `docs/quick-start.md` for minimal local run.
2. Run the demo script:
   ```bash
   python innovation-kit-repository/event-agent/assets/scripts/run_event_agent_demo.py \
     --interests "AI safety" --window "13:00-16:00" --stops 3
   ```
3. Review itinerary + rationale output.
4. Explore deeper agent graph in `docs/technical-guide.md`.

## Folder Structure
```
innovation-kit-repository/event-agent/
  INNOVATION_KIT.md
  MANIFEST.yml
  docs/
    quick-start.md
    technical-guide.md
    application-patterns.md
    troubleshooting.md
  assets/
    scripts/
      run_event_agent_demo.py
  starter-code/
    requirements.txt
    event_agent/
      __init__.py
      models.py
      graph_client.py
      work_iq.py
      scoring.py
      itinerary.py
      authoring.py
      telemetry.py
      main.py
  customizations/
    event-agent-innovation-kit.instructions.md
    Event-Agent.agent.md
```

## Prerequisites
- Python 3.11+
- Network access if later integrating live Graph or SharePoint APIs (demo script uses mock data)

## Extend Next
- Integrate real Graph client (people/calendar) and Work IQ feed.
- Implement feature-weighted scoring & expose top explanatory factors.
- Add persistent telemetry logging.

## Production Integration
Set environment variables for Graph app-only auth:
```
export GRAPH_TENANT_ID="<tenant-id>"
export GRAPH_CLIENT_ID="<app-id>"
export GRAPH_CLIENT_SECRET="<client-secret>"
```
Install dependencies:
```
python -m pip install -r innovation-kit-repository/event-agent/starter-code/requirements.txt
```
Run orchestrator:
```
python -m innovation-kit-repository.event-agent.starter-code.event_agent.main \
  --interests "AI safety, agents" --max-sessions 3 --show-calendar
```
Or with Work IQ JSON:
```
python innovation-kit-repository/event-agent/starter-code/event_agent/main.py \
  --work-iq-json path/to/interests.json --max-sessions 4
```
Output JSON:
```
python innovation-kit-repository/event-agent/starter-code/event_agent/main.py \
  --interests "AI safety, agents" --output itinerary.json
```

Telemetry events append to `telemetry.jsonl`; examine with:
```
tail -f telemetry.jsonl
```

## MVP — Production Ready (November 21, 2025)

**Status**: ✅ Complete and tested

The `starter-code/agents_sdk_integration/` directory provides a **production-ready MVP** with:
- ✅ Microsoft Graph Calendar session fetching with caching
- ✅ SharePoint Pages itinerary publishing
- ✅ Adaptive Cards with interactive Explain action buttons
- ✅ Auto-profile persistence (file or Blob storage)
- ✅ Pydantic settings validation with feature flags
- ✅ Structured telemetry (JSONL) with latency, success/error tracking
- ✅ SDK hosting scaffold ready for deployment

### Quick Start (Mock Data)
```bash
cd starter-code/agents_sdk_integration

# Recommend sessions
python run_agent.py recommend --interests "agents;AI" --max-sessions 3

# Save and load profile
python run_agent.py recommend --interests "AI;cloud" --profile-save myprofile --max-sessions 2
python run_agent.py recommend --profile-load myprofile --max-sessions 3

# Explain session
python run_agent.py explain --session "Generative Agents in Production" --interests "agents;AI"

# Run full test suite
python test_mvp.py  # Expected: 7 passed, 0 failed
```

### Enable Graph Integration
Create `.env` in `agents_sdk_integration/`:
```bash
GRAPH_TENANT_ID=your-tenant-id
GRAPH_CLIENT_ID=your-app-client-id
GRAPH_CLIENT_SECRET=your-client-secret

ENABLE_GRAPH_FETCH=true
ENABLE_SESSION_CACHE=true
SESSION_CACHE_TTL_MINUTES=15

# Optional: SharePoint publish
ENABLE_SHAREPOINT_PUBLISH=true
SHAREPOINT_SITE_ID=your-sharepoint-site-id
```

Then run with live data:
```bash
python run_agent.py recommend --interests "AI;agents" --max-sessions 5
python run_agent.py recommend --interests "cloud" --max-sessions 3 --publish
```

### SDK Hosting (Production)
```bash
# Install SDK packages
pip install microsoft-agents-activity microsoft-agents-hosting-core \
  microsoft-agents-hosting-aiohttp microsoft-agents-authentication-msal

# Start agent server
python run_agent.py sdk --port 3978
```
Connect to Teams/Copilot Studio via Bot Framework adapter.

### Architecture
```
agents_sdk_integration/
├── settings.py              # Pydantic config + validation
├── graph_sources.py         # Graph Calendar fetch + SharePoint publish
├── session_cache.py         # TTL-based cache
├── activities.py            # Recommend & Explain logic
├── event_handler.py         # SDK message routing + auto-profile
├── storage.py               # File/Blob profile persistence
├── auth.py                  # MSAL token acquisition
├── integration_telemetry.py # Structured JSONL logging
├── adaptive_cards.py        # Itinerary card builder
├── run_agent.py             # CLI + SDK hosting
├── test_mvp.py              # End-to-end tests
└── README.md                # Integration docs
```

### Documentation
- **MVP Guide**: `MVP_GUIDE.md` — Complete usage, configuration, troubleshooting
- **Roadmap**: `ROADMAP.md` — Maturity tiers (Foundation → MVP → Integrated → Advanced → Enterprise)
- **Technical Deep Dive**: `docs/technical-guide.md`

### Telemetry
All operations logged to `integration_telemetry.jsonl`:
```json
{
  "ts": 1732204800.123,
  "action": "recommend",
  "channel": "teams",
  "user": "a1b2c3...",
  "latency_ms": 450,
  "payload": {"sessions": 3},
  "success": true,
  "error": null
}
```

### Next Steps (Post-MVP)
See `ROADMAP.md` for:
- **Integrated** (2 weeks): Retry logic, Cosmos storage, calendar free/busy
- **Advanced** (2–3 months): Semantic matching, multi-tenant, audit trail
- **Enterprise** (4+ months): Horizontal scaling, OpenTelemetry, security hardening

## Support & Issues
Log questions or enhancement ideas where your project tracks issues; consider adding a `docs/troubleshooting.md` entry if a pattern repeats.
