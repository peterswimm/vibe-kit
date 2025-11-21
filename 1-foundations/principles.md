# Principles for Event Agents

- **Governable by default**: Agent 365 + Entra Agent ID as the control plane; every agent registers, inherits policy, and emits telemetry to Foundry Control Plane.
- **Retrieval is explainable**: Use Work IQ / Fabric IQ / Foundry IQ to surface why content was selected, with citations and scoring visible to users and admins.
- **Multi-agent, not monolithic**: Use an orchestrator (Event Guide) that calls specialized sub-agents for retrieval, recommendation, synthesis, and authoring; keep agents composable and swappable.
- **Security and DLP first**: Purview/Defender/Entra enforcement on every tool call; classify outputs; redact sensitive data before cross-tenant or cross-surface actions.
- **Context via Work IQ**: Treat Work IQ as the work brain for personalization, history, and grounding; prefer Work IQ memories over ad hoc session state.
- **MCP everywhere**: Prefer MCP tools (Graph, SharePoint, Fabric, Windows, Power Apps, Dataverse) so capabilities stay portable across Copilot surfaces and hosting models.
- **Cross-surface continuity**: Preserve state and handoffs across Edge Copilot Mode, Teams, Outlook, Windows Ask Copilot, and Copilot Chat; resume work with minimal re-prompting.
- **Human-in-the-loop clarity**: Always expose planned actions, citations, and pending tool calls; enable approvals for high-risk actions (publishing SharePoint pages, scheduling).
- **Office-un-styled output**: When generating Office artifacts, avoid hard-coded styling so organization themes apply automatically; focus on semantic structure.
- **Observability and feedback**: Emit rich telemetry (intent, tools used, latency, safety outcomes) and capture user feedback loops to improve prompts, tools, and policies.
