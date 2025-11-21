# MCP Tool Blueprints

Use MCP where possible so tools can run across Copilot, Foundry Agent Service, Power Apps MCP, Dataverse MCP, and Windows MCP.

## get_user_profile
- **Purpose**: Retrieve user role, org, interests for personalization.
- **Inputs**: `user_id` (Entra/Graph), optional scopes.
- **Outputs**: Display name, role, manager/team, skills/topics, calendar hints.
- **Errors**: `not_authorized`, `not_found`, `rate_limited`.
- **Layer**: Graph MCP (Agent 365-scoped).

## search_event_content
- **Purpose**: Query event schedule/BoN-style content.
- **Inputs**: `query`, `time_window`, `location`, optional `topic_filters`.
- **Outputs**: Items with title, slot, location, tags, confidence, citation URLs.
- **Errors**: `not_found`, `backend_unavailable`.
- **Layer**: Foundry/Power Apps MCP or custom event feed MCP.

## search_sharepoint_library_with_metadata
- **Purpose**: Retrieve SharePoint items with metadata reasoning.
- **Inputs**: `site_url` or `site_id`, `list_id`, `query`, `metadata_filters` (labels, topics).
- **Outputs**: Items with metadata, label info, permalink, citation fragment.
- **Errors**: `not_authorized`, `not_found`, `compliance_blocked`.
- **Layer**: SharePoint MCP.

## create_sharepoint_page
- **Purpose**: Author event pages with semantic sections (unstyled).
- **Inputs**: `site_id`, `title`, `sections` (structured blocks), `labels` (Purview), optional `publish` flag.
- **Outputs**: `page_id`, `url`, `status` (draft/published).
- **Errors**: `validation_failed`, `compliance_blocked`, `publish_failed`.
- **Layer**: SharePoint MCP (authoring).

## create_sharepoint_list
- **Purpose**: Create/update lists for follow-ups or schedules.
- **Inputs**: `site_id`, `list_name`, `columns` (name/type), optional seed `items`.
- **Outputs**: `list_id`, `url`, created items.
- **Errors**: `name_conflict`, `validation_failed`, `compliance_blocked`.
- **Layer**: SharePoint MCP.

## log_agent_telemetry
- **Purpose**: Emit observability and safety events.
- **Inputs**: `agent_id`, `user_id`, `intent`, `tools_used`, `latency_ms`, `safety_state`, `labels`, `timestamp`.
- **Outputs**: Ack with storage location/correlation ID.
- **Errors**: `not_authorized`, `backend_unavailable`.
- **Layer**: Foundry Control Plane MCP or SIEM MCP.

## query_fabric_iq / query_foundry_iq
- **Purpose**: Semantic retrieval with governance metadata.
- **Inputs**: `query`, `filters` (labels/topics/datasources), `top_k`, `need_explanations` flag.
- **Outputs**: Ranked chunks with citations, scores, provenance.
- **Errors**: `not_found`, `quota_exceeded`, `compliance_blocked`.
- **Layer**: Fabric IQ MCP / Foundry IQ MCP.

## query_work_iq_memory (optional)
- **Purpose**: Pull contextual memory for personalization.
- **Inputs**: `user_id`, `scope` (workstream/event), `time_range`, `signals` (files, chats, bookmarks).
- **Outputs**: Relevant memories with sources and recency.
- **Errors**: `not_authorized`, `not_found`.
- **Layer**: Work IQ via MCP when exposed.
