# Windows MCP Connectors

## File Explorer connector
- **Use cases**: Find/download decks, notes, transcripts saved locally during the event; stage content for Edge/Work IQ.
- **Patterns**: "Search my Event folder for decks tagged 'Agent 365' and open the latest two"; "Save these summaries to Event/Notes".
- **Safeguards**: Respect Purview labels; prompt before moving/copying outside governed locations; log file actions via telemetry MCP.

## System Settings connector
- **Use cases**: Optional for kiosk/demo setup (screen timeout, network settings) or accessibility tweaks before demos.
- **Patterns**: "Prepare kiosk mode for booth laptop"; "Enable HDR for demo station".
- **Safeguards**: Require explicit confirmation; limit to approved setting namespaces; log changes for rollback.

## Windows agent workspace
- **Role**: Acts as the desktop bridge for local context (files, clipboard, running apps) into multi-agent flows.
- **Notes**: Keep it opt-in; align with Agent 365 and Defender policies; surface what local context was shared in the response for transparency.
