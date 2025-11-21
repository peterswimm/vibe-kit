# Agent Capability Cards

## Metadata Reasoner
- **Purpose**: Interpret SharePoint metadata, labels, and topics to rank and explain items.
- **Inputs**: List/page metadata, Purview labels, user intent.
- **Outputs**: Ranked items with rationale and citations.
- **Dependencies**: SharePoint MCP search, Work IQ embeddings, Agent 365 policy.

## Semantic Retriever
- **Purpose**: Retrieve semantically relevant content across Fabric IQ / Foundry IQ and Graph files.
- **Inputs**: Query + context, Work IQ memory, allowed data scopes.
- **Outputs**: Chunks with citations, scores, and safety tags.
- **Dependencies**: Fabric IQ / Foundry IQ MCP, Graph Files MCP, Purview label awareness.

## Event Recommender
- **Purpose**: Recommend sessions/projects based on role, history, and live event signals.
- **Inputs**: Graph People/Calendar, event schedule feed, Work IQ memory, location/time.
- **Outputs**: Ranked recommendations with explanations and availability fit.
- **Dependencies**: Graph MCP (people/calendar/insights), Work IQ, Foundry Agent Service routing.

## Notebook Summarizer
- **Purpose**: Summarize Copilot Notebooks or structured research notes into briefs.
- **Inputs**: Notebook content, tags, desired audience.
- **Outputs**: Summaries, FAQs, action items with citations.
- **Dependencies**: Fabric IQ / Foundry IQ RAG, Word/PPT agents for output, Agent 365 guardrails.

## SharePoint List/Page Creator
- **Purpose**: Author new event pages/lists with consistent structure and compliance.
- **Inputs**: Payload describing sections, metadata, and links.
- **Outputs**: Created pages/lists with IDs and publish status.
- **Dependencies**: SharePoint MCP create/update tools, Purview label enforcement, telemetry MCP.

## PPT Agent / Word Agent / Excel Agent
- **Purpose**: Generate Office artifacts with org styling applied automatically.
- **Inputs**: Structured outline + data tables; explicit instruction to avoid custom styling.
- **Outputs**: Draft documents/spreadsheets/decks with semantic structure only.
- **Dependencies**: Office agents, Work IQ for context, Purview for DLP, Agent 365 for policy.

## Edge Browsing Synthesizer
- **Purpose**: Summarize multiple tabs or videos and push insights to Teams/Work IQ.
- **Inputs**: Tab content, transcripts, bookmarks.
- **Outputs**: Comparisons, summaries, suggested next steps.
- **Dependencies**: Edge Copilot Mode agent, Windows MCP for local saves, Work IQ for memory.

## Telemetry Logger
- **Purpose**: Emit standardized traces and safety events for governance.
- **Inputs**: Intent, tool calls, outcomes, sensitivity labels.
- **Outputs**: Telemetry events routed to Foundry Control Plane / SIEM.
- **Dependencies**: log_agent_telemetry MCP tool, Agent 365 policy, Purview labels.
