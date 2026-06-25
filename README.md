# Developer Productivity Agent

A codebase exploration agent for engineers dropped into unfamiliar repos.
Built for CCAF (Claude Code Architect Fundamentals) certification.

## Architecture

```
Engineer's Question
       │
       ▼
┌─────────────────────────────────────────────────────┐
│              Main Agent (main_agent.py)             │
│  Tools: Grep → Glob → Read → Write (scratchpad)     │
│  CLAUDE.md: exploration rules, plan mode, MCP docs  │
│                    │            │                   │
│          ┌─────────┘            └──────────┐        │
│          ▼                                ▼         │
│  ┌──────────────┐              ┌──────────────────┐ │
│  │  MCP Server  │              │  deep-explorer   │ │
│  │  fetch-docs  │              │   (subagent)     │ │
│  │ (real docs)  │              │ Grep+Glob+Read   │ │
│  └──────────────┘              │ returns summary  │ │
│                                └──────────────────┘ │
│                    │                                 │
│                    ▼                                 │
│              scratchpad.md                           │
│         (findings persist here)                      │
└─────────────────────────────────────────────────────┘
```

## CCAF Concepts Demonstrated

| Concept | File(s) |
|---------|---------|
| **1.3** Subagent invocation, context passing, spawning | `agent/main_agent.py` (`DEEP_EXPLORER_DEFINITION`), `agent/subagent_runner.py`, `.claude/agents/deep-explorer.md`, `.claude/commands/deep-dive.md` |
| **2.1** Tool interfaces with clear descriptions/boundaries | `agent/main_agent.py` (`allowed_tools` + `AgentDefinition`), `agent/subagent_runner.py` |
| **2.4** MCP server integration | `mcp_config.json` — `fetch-docs` via `@modelcontextprotocol/server-fetch` |
| **2.5** Built-in tools: Grep, Glob, Read, Write | `agent/main_agent.py` `ClaudeAgentOptions(allowed_tools=[...])` |
| **3.1** CLAUDE.md hierarchy and scoped instructions | `CLAUDE.md` |
| **3.2** Custom slash commands | `.claude/commands/explore.md`, `.claude/commands/deep-dive.md` |
| **3.4** Plan mode vs direct execution | `CLAUDE.md`, `.claude/commands/explore.md` |
| **5.4** Context management in large codebase exploration | `agent/scratchpad.py`, `scratchpad.md`, `agent/main_agent.py` (`memory_prefix`) |

## Project Structure

```
dev-productivity-agent/
├── CLAUDE.md                          # Agent identity + exploration rules (3.1, 3.4)
├── mcp_config.json                    # fetch-docs MCP server (2.4)
├── scratchpad.md                      # Persistent findings store (5.4)
├── run_demo.py                        # Three required CCAF demo prompts
├── requirements.txt
├── .claude/
│   ├── agents/
│   │   └── deep-explorer.md          # Subagent spec + 300-word output contract (1.3)
│   └── commands/
│       ├── explore.md                # /explore slash command (3.2)
│       └── deep-dive.md              # /deep-dive slash command (3.2)
└── agent/
    ├── __init__.py
    ├── main_agent.py                  # Main agent loop via claude_agent_sdk (1.3, 2.1, 2.5, 5.4)
    ├── scratchpad.py                  # Scratchpad persistence functions (5.4)
    └── subagent_runner.py             # Standalone subagent invocation demo (1.3, 2.1)
```

## Setup

```bash
cd dev-productivity-agent
pip install -r requirements.txt
export ANTHROPIC_API_KEY=<your-key>
```

**MCP docs server** (requires Node.js ≥ 18):
```bash
# mcp_config.json is auto-loaded by Claude Code when you open this project.
# To verify the server works standalone:
npx -y @modelcontextprotocol/server-fetch
```

## Running the Demo

```bash
python run_demo.py
```

Runs the three required CCAF prompts in sequence:

1. `"How does the password-reset flow work here?"` — proves 2.5, 3.4, 5.4
2. `"Summarize the data model for orders."` — proves 2.5, 5.4
3. `"Deep-dive the auth middleware in a subagent, then return a concise parent summary and persist key findings in scratchpad."` — proves 1.3, 2.1, 3.2, 5.4

Findings from each prompt are persisted to `scratchpad.md`. The agent re-loads them at the start of the next session.

## Slash Commands

Open this project in Claude Code to use:

- `/explore <topic>` — 5-step guided exploration: Orient → Entry Points → Trace → Synthesize → Persist
- `/deep-dive <topic>` — Immediately delegates to the deep-explorer subagent; use when a feature spans > 5 files

## How Context Management Works (Concept 5.4)

```
Session 1: Agent explores "password reset"
           → appends findings to scratchpad.md

Session 2: Agent starts
           → reads scratchpad.md into context prefix
           → answers "how does the token expire?" without re-reading files
           → appends new findings to scratchpad.md
```

The append-only scratchpad survives context window resets. `search_scratchpad(keyword)` lets the agent check prior findings before doing fresh file reads.

## How Subagent Delegation Works (Concept 1.3)

When the engineer asks to deep-dive something complex:

```
Main Agent
  └─ calls Task tool with deep-explorer AgentDefinition
       └─ deep-explorer subagent:
            Grep → Glob → Read (many files, verbose)
            returns 300-word structured summary
  └─ parent receives ONLY the summary (context stays clean)
  └─ parent persists summary to scratchpad.md
```

The subagent is constrained to `["Read", "Grep", "Glob", "Bash"]` — no `Write`, no `Task`. This boundary (concept 2.1) prevents side effects and further subagent spawning.
