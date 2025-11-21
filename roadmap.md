# Roadmap

## Near term (1–2 sprints)
- Add real Ignite 2025 Book-of-News and official doc URLs to `6-resources/*`.
- Validate MCP tool blueprints against live APIs; align schemas with actual Graph/SharePoint/Fabric/Foundry endpoints.
- Create Copilot Studio/Foundry Agent Service flows for the three prototypes; wire telemetry (`log_agent_telemetry`) and Purview/Defender policies.
- Build evaluation scripts or Copilot Studio evals using `3-starters/evaluation-checklists.md`; include citation coverage and DLP checks.

## Mid term (3–5 sprints)
- Implement Work IQ + Graph signal fusion scorer for recommendations; expose feature weights and rationales.
- Add itinerary conflict checker (time/location) and Edge multitab ingestion for the Event Discovery agent.
- Stand up ingestion/labeling pipeline for BoN/research PDFs to feed Fabric/Foundry IQ with Purview labels.
- Publish a Foundry MCP tool catalog entry set (CRM, Logic Apps, SAP) and dry-run modes for state-changing calls.

## Longer term
- Build admin dashboards (Agent 365/Foundry Control Plane) for fleet visibility, policy overrides, and pause/resume.
- Add safety regression harness (hallucination, grounding, DLP) with periodic eval runs and reporting.
- Pilot Windows MCP workflows for kiosk/demo prep and local file DLP enforcement.
- Package the kit into a Copilot Studio starter and a Foundry Agent Service template for internal distribution.
