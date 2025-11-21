# MSR Event Guide Reference Architecture

## High-level flow
```mermaid
graph TD
    U[User surfaces<br/>Copilot Chat / Teams / Edge / Outlook / Windows] --> O[Orchestrator: MSR Event Guide]
    O --> R[Sub-agents<br/>retrieval | recommendation | synthesis | authoring]
    R --> T[MCP tools<br/>Graph / SharePoint / Fabric IQ / Foundry IQ / Windows / Power Apps]
    O --> M[Work IQ / Agent Memory]
    T --> D[Data & Knowledge<br/>Graph, SharePoint, BoN content, event feeds]
    O --> G[Governance & Observability<br/>Agent 365 / Foundry Control Plane / Purview / Defender]
```

## Layers
- **User surfaces**: Copilot Chat, Teams channel agents, Edge Copilot Mode (multitab reasoning), Outlook Copilot, Windows Ask Copilot / agent workspace.
- **Orchestrator agent (MSR Event Guide)**: Manages intent detection, routes to sub-agents, enforces policy, and aggregates responses with citations.
- **Specialized sub-agents**:
  - *Retrieval agent*: Queries Fabric IQ / Foundry IQ, SharePoint, event feeds via MCP tools.
  - *Recommendation agent*: Blends event signals + Graph People/Calendar + Work IQ memories to rank sessions/projects.
  - *Synthesis agent*: Generates briefs, FAQs, and citations; writes Office-un-styled outputs.
  - *Authoring agent*: Creates SharePoint pages/lists, Outlook summaries, Teams posts via MCP tools.
- **Data & knowledge**: Microsoft Graph (people, calendar, files), SharePoint libraries/pages, Fabric IQ / Foundry IQ knowledge stores, Book-of-News-like content, event schedule feeds.
- **Governance & observability**: Agent 365 and Foundry Control Plane for policy + fleet visibility; Purview/Defender for data loss protection; audit via log/telemetry MCP tools.

## Where MCP tools plug in
- **Graph/SharePoint MCP**: Retrieval, personalization, and authoring actions (pages/lists/files).
- **Fabric IQ / Foundry IQ MCP**: Semantic search and RAG grounding with explainable metadata.
- **Windows MCP**: Local file search for event decks/notes; optional kiosk/demo configuration helpers.
- **Power Apps / Dataverse MCP**: Business workflows (registration, badge data, CRM signal enrichment).
- **Telemetry MCP**: Emits agent/tool traces to Foundry Control Plane and security systems for live observability.

## Guardrails
- Use Entra Agent ID for identity; enforce Purview labels on outputs; block high-risk actions without explicit consent.
- Keep outputs citeable; store reasoning steps in Work IQ for replay and evaluation.
