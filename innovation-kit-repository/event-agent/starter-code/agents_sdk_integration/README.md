# Agents SDK Integration (Full Migration Scaffold)

This directory provides a migration scaffold to host the Event Guide logic inside the Microsoft 365 Agents SDK runtime.

## Components

- `agent_container.py` – Integrates domain scoring + itinerary with SDK Activity handler (placeholder if SDK missing).
- `activities.py` – Pure functions/activities for recommend & explain to ease unit testing.
- `run_agent.py` – Dual-mode runner: SDK hosting (aiohttp) vs fallback CLI.
- `pyproject.toml` – Declares placeholder dependencies on microsoft-agents packages (pin actual versions).
- `event_handler.py` – Concrete `EventGuideActivityHandler` mapping message text to recommend/explain.
- `adaptive_cards.py` – Builds Adaptive Card JSON for itinerary (now includes per-session `Explain` action buttons).
- `storage.py` – Azure Blob (when configured) or file-based persistent profile storage fallback (survives restarts).
- `auth.py` – MSAL client credentials token acquisition.
- `integration_telemetry.py` – Structured telemetry with latency & hashed user id.

## Install (Placeholder)

```bash
python -m pip install microsoft-agents-activity microsoft-agents-hosting-core \
  microsoft-agents-hosting-aiohttp microsoft-agents-authentication-msal
```

## Fallback CLI Usage

```bash
python innovation-kit-repository/event-agent/starter-code/agents_sdk_integration/run_agent.py \
  recommend --interests "AI safety, agents" --max-sessions 3
```

## Lightweight Hosting (aiohttp wrapper)

A minimal local server (no CloudAdapter wiring yet) wraps the Activity Handler using a fake `TurnContext` for rapid iteration. Exposes `POST /api/messages` accepting a JSON body with at least a `text` field.

```bash
python innovation-kit-repository/event-agent/starter-code/agents_sdk_integration/run_agent.py sdk --port 3978
```

Sample requests:

```bash
curl -X POST http://localhost:3978/api/messages \
  -H 'Content-Type: application/json' \
  -d '{"text":"recommend:AI safety, agents"}'

curl -X POST http://localhost:3978/api/messages \
  -H 'Content-Type: application/json' \
  -d '{"text":"explain:Generative Agents in Production:AI safety, agents"}'
```

Response JSON contains the recommendation or explanation payload. The `adaptiveCard` block is included for `recommend` requests.

### Upgrading to Full SDK Adapter

To use real channel integration (Teams, Copilot) replace the lightweight server with the `CloudAdapter` + `AgentApplication` pattern. This requires constructing `ApplicationOptions(storage=MemoryStorage(), bot_app_id=...)` and a connection manager for token acquisition. The current lightweight wrapper avoids those dependencies for simplicity.

### Message Command Formats

- `recommend:AI safety, agents`
- `explain:Generative Agents in Production:AI safety, agents`

### Adaptive Card Output & Actions

`recommend` responses include `adaptiveCard` key (schema v1.5). Each session has an `Action.Submit` button ("Explain #n") with payload `{ action: "explainSession", sessionTitle, start, end, room }` ready for channel routing to invoke an explain activity.

### Storage & Profiles

Profiles persist automatically when `--profile-save` is used. Resolution order:

1. Azure Blob (if `AZURE_STORAGE_CONNECTION_STRING` set)
2. File fallback at `~/.event_guide_storage.json` (override with `EVENT_GUIDE_STORAGE_FILE`)
3. In-memory (legacy, no longer used)

Load with `--profile-load <key>`; interests accept comma or semicolon separators.

### Auth

MSAL client credentials uses `GRAPH_TENANT_ID`, `GRAPH_CLIENT_ID`, `GRAPH_CLIENT_SECRET` to acquire tokens (see `auth.py`).

### Telemetry

Structured telemetry appended to `integration_telemetry.jsonl` with fields: `ts`, `action`, `channel`, `user`, `latency_ms`, `payload`.

### Enabling Channel Integration

The current harness sets up minimal adapter + application + handler. For Teams/Copilot channels, extend `AgentApplication` options and authorization as required by the SDK (connection manager, authorization objects). This minimal setup is suitable for local testing and iterative development.

## Next Steps

1. Wire `Explain` action submissions to `EventGuideActivityHandler` for interactive clarification.
2. Integrate Graph / SharePoint data sources for live session + authoring content.
3. Add Cosmos or Table storage for richer profile & history beyond simple JSON blob.
4. Expand telemetry with operation outcomes & errors for observability.

## Environment Variables

- `GRAPH_TENANT_ID`, `GRAPH_CLIENT_ID`, `GRAPH_CLIENT_SECRET` for Graph features.
- `AZURE_STORAGE_CONNECTION_STRING` for Blob profile storage.
- `EVENT_GUIDE_STORAGE_FILE` optional override for file-based persistent storage path.

## Testing Strategy

- Unit test `activities.py` with synthetic sessions.
- Integration test `run_agent.py recommend` path.
- When SDK installed, run hosted mode and send message activities to validate routing.
