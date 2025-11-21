# Copilot Design Guidelines

## Prompt design
- Be explicit about intent, data scope, and desired outputs; request citations and reasoning steps.
- Mention governing systems: "Use Work IQ context" or "Apply Agent 365 policies" to set expectations.
- Ask for preview/plan before execution for high-impact actions.

## Unstyled Office artifacts
- State: "Use organization defaults; avoid custom fonts/colors/layouts." 
- Favor semantic structure (headings, bullets, tables) over styling instructions.
- Include label guidance if needed: "Apply Purview label <label> if suggested by policy." 

## Multi-turn vs single-shot
- Start multi-turn: first ask for constraints (time, role, location), then propose a plan, then execute.
- Cache context in Work IQ to avoid re-prompting; remind users what is stored.
- Offer quick retries with clarified constraints when results are weak.

## Human-in-the-loop
- Show intended tool calls and data sources before acting; require confirmation for writes (SharePoint pages/lists, emails).
- Provide citations and alternative options so users can adjust without starting over.
- Capture thumbs-up/down and free-text feedback; route to telemetry for evaluation loops.

## Safety & governance cues
- Echo policy boundaries: "I cannot share externally because of Purview labels." 
- Use dry-run modes for destructive actions; log every tool call via telemetry MCP.
- Keep outputs concise and mobile-friendly for Teams/Edge surfaces.
