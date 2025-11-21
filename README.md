# Vibe Kit — Event Agent Innovation Kit

A production-ready AI event recommendation agent with Microsoft Graph integration, SharePoint publishing, and Microsoft 365 Agents SDK hosting. This kit provides everything needed to build, test, and deploy intelligent event discovery experiences.

## 🚀 Quick Start (5 Minutes)

**Test locally with mock data** (no credentials required):

```bash
cd innovation-kit-repository/event-agent/starter-code/agents_sdk_integration

# Install dependencies
pip install pydantic pydantic-settings requests msal

# Run recommendations
python run_agent.py recommend --interests "AI;agents" --max-sessions 3

# Run tests
python test_mvp.py
```

**Expected output**: Recommended sessions with adaptive card JSON, scoring breakdown, and session source indication.

## 🎯 What's Included

### Production-Ready MVP (November 2025)
- ✅ **Microsoft Graph Calendar** session fetching with caching
- ✅ **SharePoint Pages** itinerary publishing
- ✅ **Adaptive Cards** with interactive Explain buttons
- ✅ **Auto-profile persistence** (file or Azure Blob)
- ✅ **Pydantic configuration** with feature flags
- ✅ **Structured telemetry** (JSONL logging)
- ✅ **SDK hosting scaffold** ready for Teams/Copilot Studio

### Architecture
Built on proven Microsoft 365 patterns:
- **Graph API Integration**: Calendar events, SharePoint authoring
- **MSAL Authentication**: Client credentials flow
- **Scoring Engine**: Interest match + popularity + diversity
- **Conflict Resolution**: Time-aware itinerary building
- **Agents SDK Ready**: Message routing, activity handlers, hosting

## 📚 Documentation

| Guide | Purpose |
|-------|---------|
| [`innovation-kit-repository/event-agent/MVP_GUIDE.md`](innovation-kit-repository/event-agent/MVP_GUIDE.md) | Complete setup, configuration, troubleshooting |
| [`innovation-kit-repository/event-agent/ROADMAP.md`](innovation-kit-repository/event-agent/ROADMAP.md) | Maturity tiers: MVP → Integrated → Advanced → Enterprise |
| [`innovation-kit-repository/event-agent/INNOVATION_KIT.md`](innovation-kit-repository/event-agent/INNOVATION_KIT.md) | Kit overview and quick start |
| [`innovation-kit-repository/event-agent/MVP_SUMMARY.md`](innovation-kit-repository/event-agent/MVP_SUMMARY.md) | Implementation details and test results |

## 🧪 Testing Locally

### Run Full Test Suite
```bash
cd innovation-kit-repository/event-agent/starter-code/agents_sdk_integration
python test_mvp.py
```

**Expected**: `7 passed, 0 failed` — validates settings, recommendations, profiles, caching, adaptive cards

### Interactive CLI Testing
```bash
# Recommend sessions
python run_agent.py recommend --interests "agents;AI safety" --max-sessions 3

# Save profile
python run_agent.py recommend --interests "AI;cloud" --profile-save myprofile

# Load saved profile
python run_agent.py recommend --profile-load myprofile --max-sessions 3

# Explain session scoring
python run_agent.py explain --session "Generative Agents in Production" --interests "agents"

# Test publish capability (skips when disabled)
python run_agent.py recommend --interests "agents" --publish --max-sessions 2
```

### Enable Real Graph Integration

1. **Register Azure AD app** with permissions:
   - `Calendars.Read` (application)
   - `Sites.Read.All` (application)
   - `Sites.ReadWrite.All` (application, for publishing)

2. **Create `.env`** in `agents_sdk_integration/`:
   ```bash
   GRAPH_TENANT_ID=your-tenant-id
   GRAPH_CLIENT_ID=your-client-id
   GRAPH_CLIENT_SECRET=your-secret
   SHAREPOINT_SITE_ID=your-site-id
   ENABLE_GRAPH_FETCH=true
   ENABLE_SHAREPOINT_PUBLISH=true
   ```

3. **Test with real data**:
   ```bash
   python run_agent.py recommend --interests "AI" --max-sessions 5
   ```

## 🏗️ Architecture Overview

```
User → Handler (auto-save profile)
         ↓
      Activities (recommend/explain)
         ↓
      Settings (validate config)
         ↓
      Graph Sources (fetch w/ cache)
         ↓
      Scoring Engine (interest + popularity + diversity)
         ↓
      Itinerary Builder (conflict resolution)
         ↓
      Adaptive Card Builder (action buttons)
         ↓
      [Optional] SharePoint Publish
         ↓
      Telemetry Logger
         ↓
      Response (JSON + card)
```

## 📦 Repository Structure

```
innovation-kit-repository/event-agent/
├── ROADMAP.md                    # Maturity tiers & timeline
├── MVP_GUIDE.md                  # Complete usage guide
├── MVP_SUMMARY.md                # Implementation summary
├── INNOVATION_KIT.md             # Kit overview
├── docs/                         # Technical guides
├── assets/scripts/               # Demo scripts
└── starter-code/
    ├── event_agent/              # Core domain logic
    │   ├── models.py             # Data models
    │   ├── scoring.py            # Ranking engine
    │   ├── itinerary.py          # Conflict resolution
    │   └── main.py               # CLI orchestrator
    └── agents_sdk_integration/   # Production MVP
        ├── settings.py           # Config validation
        ├── graph_sources.py      # Graph API integration
        ├── session_cache.py      # TTL cache
        ├── activities.py         # Recommend & Explain
        ├── event_handler.py      # SDK message routing
        ├── storage.py            # Profile persistence
        ├── auth.py               # MSAL wrapper
        ├── integration_telemetry.py  # Structured logging
        ├── adaptive_cards.py     # Card builder
        ├── run_agent.py          # CLI + hosting
        └── test_mvp.py           # E2E tests
```

## 🚢 Deployment

### Local Development
```bash
python run_agent.py sdk --port 3978
```

### Azure Container Instances / App Service
1. Package Docker container with Python 3.11+
2. Set environment variables for Graph credentials
3. Expose port 3978 for Bot Framework adapter
4. Connect to Teams channel via Azure Bot Service

### Bot Framework Channel Registration
- Create bot registration in Azure Portal
- Configure messaging endpoint: `https://your-app.azurewebsites.net/api/messages`
- Add Teams channel
- Users interact via chat: `recommend:AI, agents` or adaptive card buttons

## 🎓 Learning Paths

### For Developers
1. Start with `test_mvp.py` to understand core flows
2. Review `activities.py` for recommend/explain logic
3. Explore `graph_sources.py` for Graph API patterns
4. Study `event_handler.py` for SDK message routing

### For Product/Design
1. Read `MVP_GUIDE.md` for feature overview
2. Review `ROADMAP.md` for maturity phases
3. Check `docs/application-patterns.md` for use cases
4. Explore adaptive card examples in test output

### For Operations
1. Study `settings.py` for configuration options
2. Review `integration_telemetry.py` for observability
3. Check `MVP_GUIDE.md` troubleshooting section
4. Plan deployment using Azure resources guide

## 🔧 Configuration Reference

### Feature Flags
| Flag | Default | Purpose |
|------|---------|---------|
| `ENABLE_GRAPH_FETCH` | `false` | Fetch sessions from Graph Calendar |
| `ENABLE_SHAREPOINT_PUBLISH` | `false` | Publish itineraries to SharePoint |
| `ENABLE_SESSION_CACHE` | `true` | Cache Graph responses |
| `SESSION_CACHE_TTL_MINUTES` | `15` | Cache expiration |

### Required Environment Variables (Graph Enabled)
- `GRAPH_TENANT_ID` — Azure AD tenant ID
- `GRAPH_CLIENT_ID` — Application (client) ID
- `GRAPH_CLIENT_SECRET` — Client secret value
- `SHAREPOINT_SITE_ID` — Target SharePoint site ID (for publishing)

### Optional Variables
- `AZURE_STORAGE_CONNECTION_STRING` — For Blob profile storage
- `EVENT_GUIDE_STORAGE_FILE` — Override file storage path
- `TELEMETRY_FILE` — Custom telemetry log path

## 📊 Performance Benchmarks

| Operation | Mock (p95) | Graph (expected) |
|-----------|-----------|------------------|
| Recommend | 25ms | 2s (first), 10ms (cached) |
| Explain | 15ms | 20ms (cached sessions) |
| Profile save | 5ms | 5ms |
| Graph fetch | N/A | 200-500ms (uncached) |
| SharePoint publish | N/A | 600-1200ms |

## 🛠️ Troubleshooting

### "Missing required environment variables"
**Fix**: Set `GRAPH_TENANT_ID`, `GRAPH_CLIENT_ID`, `GRAPH_CLIENT_SECRET` when enabling Graph features.

### `sessionSource: "mock"` despite credentials
**Check**:
1. `ENABLE_GRAPH_FETCH=true` in `.env`
2. Verify settings: `python -c "from settings import get_settings; print(get_settings().enable_graph_fetch)"`
3. Test token: `python run_agent.py recommend --test-token --interests "test" --max-sessions 1`

### Tests failing with import errors
**Fix**: Ensure you're in correct directory and dependencies installed:
```bash
cd innovation-kit-repository/event-agent/starter-code/agents_sdk_integration
pip install pydantic pydantic-settings requests msal
python test_mvp.py
```

## 🗺️ Roadmap

| Phase | Status | Key Features |
|-------|--------|--------------|
| **Foundation** | ✅ Complete | Core logic + CLI + mock data |
| **MVP** | ✅ Complete | Graph + SharePoint + Cards + Telemetry |
| **Integrated** | 🎯 Next 2 weeks | Retry logic + Cosmos + Free/busy |
| **Advanced** | 📋 Month 2-3 | Embeddings + Multi-tenant + Audit |
| **Enterprise** | 📋 Month 4+ | Scale + OpenTelemetry + Security |

See [`ROADMAP.md`](innovation-kit-repository/event-agent/ROADMAP.md) for detailed timeline.

## 🤝 Contributing

This kit follows the vibe-kit philosophy of composable, extensible patterns. Contributions welcome:
- Additional MCP tool integrations
- New scoring algorithm variants
- Enhanced adaptive card templates
- Additional use case templates

## 📄 License

See `LICENSE` file in repository root.

---

## Additional Resources (Original Kit Context)

### Why This Kit Exists
- Focus use case: **MSR Event Guide** that recommends projects/sessions using Microsoft Graph + Work IQ + event signals, across Copilot Chat, Teams, Edge, Windows, and other Copilot surfaces.
- Built to reflect Ignite 2025 announcements so teams can align with the latest agent stack out of the box.
- Works as a starting point for multi-agent, MCP-powered, governed workflows rather than a single app template.

## Ignite 2025 ingredients (how they shape the kit)
- **Agent 365** as the control plane + Entra Agent ID for identity, policies, and visibility.
- **Work IQ** as the memory/intelligence layer for contextual retrieval and relevance.
- **Foundry Agent Service** for hosted agents, memory, and multi-agent workflows; **Foundry Control Plane** for governance.
- **MCP everywhere**: Power Apps MCP, Dataverse MCP, Windows MCP, Dynamics MCP; treat tools as portable capabilities.
- **Fabric IQ / Foundry IQ** for semantic knowledge and agentic RAG.
- **Edge for Business (Copilot Mode)** for multitab reasoning and agent mode.
- **Windows agent workspace + connectors** to bridge desktop signals into agent flows.

## What you get (navigation)
- `1-foundations/` – principles, problem spaces, reference architecture for the event guide.
- `2-inspiration/` – patterns, capability cards, Copilot examples, Ignite 2025 summary.
- `3-starters/` – personas, prompt starters, evaluation checklists for event agents.
- `4-mcp/` – MCP tool blueprints, Graph/Windows connectors, Foundry catalog guidance.
- `5-prototypes/` – scenario readmes with agent graphs for discovery, synthesis, orchestration.
- `6-resources/` – Book-of-News link placeholders, official doc placeholders, Copilot design guidance.

## How to use it
1. Skim `1-foundations/` to align on principles and architecture.
2. Grab ready-made patterns and capability cards from `2-inspiration/` to shape your solution.
3. Choose personas and prompts from `3-starters/` to kick off design + evaluation.
4. Map required MCP tools using `4-mcp/`; wire them to Foundry/Power Apps/Windows connectors.
5. Follow a prototype in `5-prototypes/` and iterate with your team.

This kit is intentionally Markdown-first and code-light so you can adapt it into Copilot Studio agents, Foundry Agent Service flows, or custom stacks without fighting boilerplate.
