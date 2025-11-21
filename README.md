# Event Agent Innovation Kit

A developer, product, and design scaffold for building agentic experiences around Microsoft Research events. Inspired by the vibe-kit philosophy, this kit is a set of interchangeable Lego blocks (instructions, prompts, personas, MCP tool blueprints, and starter flows) you can mix to ship fast, governed prototypes.

## Why this kit exists
- Focus use case: **MSR Event Guide** that recommends projects/sessions using Microsoft Graph + Work IQ + event signals, across Copilot Chat, Teams, Edge, Windows, and other Copilot surfaces.
- Built to reflect Ignite 2025 announcements so teams can align with the latest agent stack out of the box.
- Works as a starting point for multi-agent, MCP-powered, governed workflows rather than a single app template.

## Ignite 2025 ingredients (how they shape the kit)
- **Agent 365** as the control plane + Entra Agent ID for identity, policies, and visibility.
- **Work IQ** as the memory/intelligence layer for contextual retrieval and relevance.
- **Foundry Agent Service** for hosted agents, memory, and multi-agent workflows; **Foundry Control Plane** for governance.
- **MCP everywhere**: Power Apps MCP, Dataverse MCP, Windows MCP, Dynamics MCP; treat tools as portable capabilities.
- **Fabric IQ / Foundry IQ** for semantic knowledge and agentic RAG.
- **Edge for Business (Copilot Mode)** for multitab reasoning and agent mode.
- **Windows agent workspace + connectors** to bridge desktop signals into agent flows.

## What you get (navigation)
- `1-foundations/` – principles, problem spaces, reference architecture for the event guide.
- `2-inspiration/` – patterns, capability cards, Copilot examples, Ignite 2025 summary.
- `3-starters/` – personas, prompt starters, evaluation checklists for event agents.
- `4-mcp/` – MCP tool blueprints, Graph/Windows connectors, Foundry catalog guidance.
- `5-prototypes/` – scenario readmes with agent graphs for discovery, synthesis, orchestration.
- `6-resources/` – Book-of-News link placeholders, official doc placeholders, Copilot design guidance.

## How to use it
1. Skim `1-foundations/` to align on principles and architecture.
2. Grab ready-made patterns and capability cards from `2-inspiration/` to shape your solution.
3. Choose personas and prompts from `3-starters/` to kick off design + evaluation.
4. Map required MCP tools using `4-mcp/`; wire them to Foundry/Power Apps/Windows connectors.
5. Follow a prototype in `5-prototypes/` and iterate with your team.

This kit is intentionally Markdown-first and code-light so you can adapt it into Copilot Studio agents, Foundry Agent Service flows, or custom stacks without fighting boilerplate.
