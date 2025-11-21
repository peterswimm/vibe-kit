# Foundry MCP Tool Catalog Guidance

- **Purpose**: Expose enterprise connectors (Logic Apps, SAP, Salesforce, HubSpot, CRM/ERP) as MCP tools that event agents can call through Foundry Agent Service.
- **Catalog design**:
  - Standardize tool schemas (inputs/outputs/errors) so agents can reason across connectors.
  - Tag tools with data domains, sensitivity, and allowed roles (aligned to Agent 365 policies).
  - Provide discoverability metadata: description, sample prompts, cost/latency hints, required approvals.
- **Example catalog entries**:
  - `crm_lookup_contact` (Salesforce/HubSpot): inputs `email|alias`, outputs contact + open opps; errors `not_found`, `auth_failed`.
  - `sap_get_purchase_order`: inputs `po_id`, outputs status/items/vendor; errors `not_found`, `compliance_blocked`.
  - `logic_app_run_workflow`: inputs `workflow_id`, `payload`; outputs `run_id`, `status`, `result_link`; errors `validation_failed`, `rate_limited`.
- **Multi-agent usage**:
  - Orchestrator routes to cataloged tools based on intent; sub-agents specialize (e.g., CRM enrichment vs schedule recommendations).
  - Share telemetry for every tool via `log_agent_telemetry` so governance dashboards stay accurate.
- **Safety**:
  - Enforce Purview/Defender DLP policies before writing back to enterprise systems.
  - Require explicit confirmation for state-changing actions (e.g., creating records); expose dry-run mode.
  - Capture provenance and citations in responses so admins can audit decisions.
