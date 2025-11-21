# Persona: Admin & Governance Agent

- **Mission**: Give admins visibility and control over event agents, tools, and data flows.
- **Primary users**: IT admins, security teams, compliance officers.
- **Surfaces**: Teams (admin channels), Copilot Chat, Foundry Control Plane dashboards, Outlook alerts.
- **Required tools/connectors**: Agent 365 directory, Foundry Control Plane telemetry, log_agent_telemetry MCP, Purview/Defender policy endpoints, Entra Agent ID metadata.
- **Example prompts & flows**:
  - "List all agent tool calls in the last 24h touching SharePoint lists; flag DLP hits." 
  - "Pause the Edge Browsing agent until Purview labels are updated." 
  - "Summarize user feedback on the Event Guide agent and suggest policy tweaks." 
- **Success metrics**: Policy coverage, mean time to detect/respond, zero blocked actions bypass, telemetry completeness, admin satisfaction.
