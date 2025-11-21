# Evaluation Checklists

## Functional correctness
- Finds sessions/projects matching the prompt intent and constraints (time/location/role).
- Handles edge cases: no results, conflicting events, offline data.
- Tool calls succeed with validated parameters; clear error messaging when blocked.

## Relevance
- Uses Graph People/Calendar/Insights and Work IQ memories to personalize results.
- Deduplicates previously saved items; respects user preferences and feedback.
- Ranks with explicit rationales tied to metadata/signals.

## Grounding & citations
- Sources every recommendation/synthesis to Fabric IQ / Foundry IQ / SharePoint / event feeds.
- Shows confidence or retrieval scores when available; exposes why items were chosen.
- Stores citations with responses for audit and replay.

## Security & DLP
- Honors Purview labels on inputs/outputs; redacts before sharing externally.
- Avoids cross-tenant actions unless explicitly approved.
- Logs safety decisions and blocked actions.

## Governance & observability
- Emits telemetry (intent, tool usage, latency, safety state) to Agent 365/Foundry Control Plane.
- Uses Entra Agent ID for every surface; policies applied consistently.
- Supports admin queries and pause/resume controls.

## Usability
- Explains steps in plain language; shows planned actions before execution.
- Provides retry/clarification prompts; keeps outputs concise for mobile.
- Default outputs are Office-un-styled so org themes apply automatically.
