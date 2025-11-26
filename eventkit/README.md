# Event Kit

**Minimal declarative event recommendation agent** for Vibe Kit. Demonstrates core agent patterns with one manifest (`agent.json`) and one script (`agent.py`).

---

## Overview

Event Kit is a lightweight innovation kit showcasing:

- **Declarative manifest**: Sessions, weights, and feature flags in JSON
- **CLI + HTTP server**: Recommend, explain, export endpoints
- **Adaptive Cards**: Interactive UI for Copilot experiences
- **Telemetry**: Structured JSONL logging for observability
- **Profile persistence**: Save/load user preferences
- **External data override**: Swap in real event feeds

---

## How This Fits in Vibe Kit

Vibe Kit is a repository of innovation kits designed to accelerate AI agent prototyping. Event Kit serves as:

1. **Foundational example**: Minimal agent architecture (manifest + logic)
2. **Starter for real integrations**: Easily extend to Microsoft Graph, SharePoint, or Agent SDK hosting
3. **Pattern library**: Demonstrates scoring, conflict detection, adaptive cards, telemetry

For production-ready Graph/SharePoint integration, see [`innovation-kit-repository/event-agent/`](../innovation-kit-repository/event-agent/) which includes:

- Microsoft 365 Agents SDK hosting scaffold
- Graph Calendar fetching with MSAL auth
- SharePoint page publishing
- Pydantic configuration with feature flags
- Full setup guide in `MVP_GUIDE.md`

---

## Quick Start

### 1. Run Locally (No Setup)

```bash
cd eventkit

# Recommend sessions
python agent.py recommend --interests "agents, ai safety" --top 3

# Explain a session
python agent.py explain --session "Generative Agents in Production" --interests "agents, gen ai"

# Export itinerary
python agent.py export --interests "agents, privacy" --output my_itinerary.md

# Start HTTP server
python agent.py serve --port 8010 --card
```

Test endpoints:

```bash
curl http://localhost:8010/health
curl "http://localhost:8010/recommend?interests=agents,ai+safety&top=3&card=1"
curl "http://localhost:8010/explain?session=Generative+Agents+in+Production&interests=agents,gen+ai"
```

### 2. Profile Persistence

```bash
# Save interests for later
python agent.py recommend --interests "agents, telemetry" --profile-save demo

# Load saved profile
python agent.py recommend --profile-load demo --top 5
```

Profiles stored in `~/.event_agent_profiles.json`.

### 3. Run Tests

```bash
python -m pytest eventkit/tests -q
```

All 7 tests should pass (recommend, explain, export, profile, server, telemetry, external sessions).

---

## Setup Dev Environment in VS Code

### Prerequisites

- Python 3.11+
- VS Code with Python extension

### Steps

1. **Clone the Vibe Kit repo** (if not already):

   ```bash
   git clone https://github.com/peterswimm/vibe-kit.git
   cd vibe-kit
   ```

2. **Open eventkit in VS Code**:

   ```bash
   code eventkit
   ```

   Or open the workspace folder in VS Code and navigate to `eventkit/`.

3. **Create a virtual environment**:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

4. **Install dev dependencies** (optional, for testing):

   ```bash
   pip install pytest
   ```

   The agent itself has **zero dependencies** — runs with Python stdlib only.

5. **Configure VS Code**:

   - Open Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)
   - Select `Python: Select Interpreter`
   - Choose `.venv/bin/python`

6. **Run the agent**:

   Open integrated terminal in VS Code (`Ctrl+` `/`Cmd+` `) and:

   ```bash
   python agent.py recommend --interests "agents, ai safety" --top 3
   ```

7. **Run tests** (in VS Code terminal):

   ```bash
   python -m pytest tests -v
   ```

   Or use VS Code's Testing sidebar (flask icon) to discover and run tests interactively.

8. **Debug**:

   Set breakpoints in `agent.py`, then press `F5` (Run > Start Debugging). VS Code will prompt to create a `launch.json` — select "Python File" for CLI debugging or "Python: Current File" for general use.

---

## Extending with Agent SDK

To integrate with Microsoft 365 Agents SDK (Teams/Copilot Studio hosting):

1. **See the full Agent SDK starter** in [`innovation-kit-repository/event-agent/starter-code/agents_sdk_integration/`](../innovation-kit-repository/event-agent/starter-code/agents_sdk_integration/)
2. **Follow MVP_GUIDE.md** for Graph authentication, SharePoint publish, and SDK hosting setup
3. **Compare patterns**: Event Kit (`eventkit/agent.py`) shows minimal logic; Agent SDK starter adds authentication, caching, and enterprise features

### Key Differences

| Feature          | Event Kit (`eventkit/`)      | Agent SDK Starter (`innovation-kit-repository/event-agent/`) |
| ---------------- | ---------------------------- | ------------------------------------------------------------ |
| **Auth**         | None (mock data)             | MSAL (Graph + SharePoint)                                    |
| **Data Source**  | Static JSON or external file | Microsoft Graph Calendar                                     |
| **Publishing**   | Markdown export              | SharePoint page creation                                     |
| **Hosting**      | CLI + HTTP server            | Microsoft 365 Agents SDK (Teams/Copilot Studio)              |
| **Config**       | JSON manifest                | Pydantic settings + `.env`                                   |
| **Dependencies** | None                         | `pydantic`, `msal`, `requests`, `botbuilder-core`            |

**When to use Event Kit**: Prototyping agent logic, testing scoring algorithms, local demos

**When to use Agent SDK Starter**: Production deployment, Graph integration, Teams/Copilot experiences

---

## Project Structure

```
eventkit/
├── agent.py                 # Core logic (recommend, explain, export, serve)
├── agent.json               # Manifest (sessions, weights, features)
├── telemetry.py             # JSONL logging module
├── pyproject.toml           # Packaging (console script: "eventkit")
├── EVENT_KIT.md             # Quick start overview
├── QUICKSTART.md            # Detailed CLI/server usage
├── agent.schema.json        # JSON Schema for manifest validation
├── tests/                   # Pytest suite (7 tests)
│   ├── test_recommend.py
│   ├── test_explain.py
│   ├── test_export.py
│   ├── test_profile.py
│   ├── test_server.py
│   ├── test_telemetry.py
│   └── test_external_sessions.py
├── docs/                    # Technical guides
│   ├── technical-guide.md
│   ├── performance-guide.md
│   ├── troubleshooting.md
│   ├── application-patterns.md
│   ├── data-integration.md
│   ├── evaluation.md
│   ├── governance.md
│   └── openapi-snippet.yaml
├── scripts/                 # Utilities
│   ├── evaluate_profiles.py
│   ├── export_itinerary.py
│   ├── generate_sessions_template.py
│   └── summarize_telemetry.py
└── assets/                  # Sample data
    ├── sample_itinerary.md
    └── sessions_external.json
```

---

## Feature Flags

Adjust behavior in `agent.json > features`:

- **`telemetry.enabled`**: Log actions to `telemetry.jsonl`
- **`export.enabled`**: Save markdown to `exports/` directory
- **`externalSessions.enabled`**: Override sessions with `sessions_external.json`

---

## Next Steps

1. **Customize sessions**: Edit `agent.json` to add your event data
2. **Adjust scoring weights**: Tweak `weights` (interest, popularity, diversity)
3. **Connect real data**: Enable `externalSessions` and provide JSON feed
4. **Add authentication**: See Agent SDK starter for Graph/MSAL patterns
5. **Deploy as service**: Use systemd or containerize (see `QUICKSTART.md`)
6. **Integrate with Teams**: Follow `innovation-kit-repository/event-agent/MVP_GUIDE.md`

---

## Resources

- **Vibe Kit Repository**: <https://github.com/peterswimm/vibe-kit>
- **Agent SDK Starter**: `innovation-kit-repository/event-agent/starter-code/agents_sdk_integration/`
- **Full Setup Guide**: `innovation-kit-repository/event-agent/MVP_GUIDE.md`
- **Roadmap**: `innovation-kit-repository/event-agent/ROADMAP.md`
- **Technical Docs**: `eventkit/docs/technical-guide.md`

---

## License

MIT — See [LICENSE](../LICENSE) in repository root.
