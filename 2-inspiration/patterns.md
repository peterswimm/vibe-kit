# Agent Patterns

## Event Discovery Funnel
- **When to use**: Attendee onboarding or schedule building.
- **Inputs**: User profile (Graph People/Role), Work IQ memories, event schedule/feed, BoN highlights.
- **Flow**: intent detect → retrieve event items → score with Work IQ/Graph signals → explain picks → deliver itinerary.
- **Ignite 2025 features**: Agent 365 gating, Work IQ for memory, Foundry Agent Service routing, Edge Copilot Mode for multitab comparisons.

## Multi-agent Pipeline (retrieve → reason → author)
- **When to use**: Any grounded response that ends in authored content.
- **Inputs**: Query, context, tool capabilities.
- **Outputs**: Draft with citations plus optional SharePoint/Outlook artifact.
- **Ignite 2025 features**: Foundry Agent Service orchestrator, Fabric IQ retrieval, SharePoint MCP authoring, telemetry MCP for observability.

## SharePoint Metadata Reasoning
- **When to use**: Need explainable recommendations from curated libraries.
- **Inputs**: SharePoint list/page metadata, labels, topics.
- **Outputs**: Ranked items with metadata-based rationale.
- **Ignite 2025 features**: Work IQ embeddings + metadata, SharePoint MCP search/create, Purview labels for compliance.

## Edge Multitab Synthesis
- **When to use**: Researching multiple project pages, videos, and docs in Edge.
- **Inputs**: Open tabs, page text, video transcripts.
- **Outputs**: Summaries or comparisons, plus follow-up actions (save to Work IQ, send to Teams).
- **Ignite 2025 features**: Edge for Business Copilot Mode (agent mode), Work IQ for memory, Windows MCP for local saves.

## Teams Channel Agent Loop
- **When to use**: Persistent event planning in Teams channels.
- **Inputs**: Channel context, files, SharePoint pages, participant roles.
- **Outputs**: Updates, lists, action items; pushes authored pages back to SharePoint.
- **Ignite 2025 features**: Teams channel agents, Power Apps MCP, SharePoint MCP authoring, Agent 365 policy enforcement.

## Safety + Governance Envelope
- **When to use**: Any agent calling external or high-impact tools.
- **Inputs**: Tool call intents, sensitivity labels, DLP rules.
- **Outputs**: Approved/blocked actions, audit entries, user-visible justifications.
- **Ignite 2025 features**: Agent 365, Foundry Control Plane, Purview/Defender, telemetry MCP logging.
