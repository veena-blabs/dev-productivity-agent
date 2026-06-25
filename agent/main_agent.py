"""
main_agent.py — Main orchestration agent for the Developer Productivity Agent.

CCAF Concepts Proved:
- 2.1: Tool interfaces with clear descriptions/boundaries (allowed_tools list)
- 1.3: Subagent invocation, context passing, spawning (AgentDefinition + Task tool)
- 2.5: Built-in tools — Grep, Glob, Read, Write, Task
- 5.4: Context management — scratchpad re-loaded at session start
"""

import asyncio
import sys
from pathlib import Path
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition


# ── Subagent Definition ────────────────────────────────────────────────────────
# Proves concept 1.3: subagent with its own tools, prompt, and model.
# Spawned via Task tool. Only the summary returns to parent.

DEEP_EXPLORER_DEFINITION = AgentDefinition(
    description=(
        "Deep-dive code explorer. Invoke when tracing a feature across more than 5 files "
        "or when explicitly asked to deep-dive. Returns ONLY a concise structured summary "
        "under 300 words. Do NOT invoke for simple grep or single-file reads."
    ),
    prompt="""You are a deep-dive code exploration specialist invoked as a subagent.
Your job: handle verbose multi-file investigations so the parent context stays clean.

## Output Contract — STRICT
Return ONLY this format. Under 300 words. Never return raw file contents.

**Feature/Topic:** [what was investigated]
**Entry Point:** [file:line]
**Key Files Traced:** [list]
**Flow Summary:**
1. [step]
2. [step]
**Key Findings:**
- [finding]
**Recommended Reading:** [1-3 files]

## Tool Rules
- Grep first, Glob second, Read only relevant files
- Bash only for: find, wc -l, head, tail
- Never modify files. Never return full file contents.
""",
    tools=["Read", "Grep", "Glob", "Bash"],
    model="sonnet",
)


# ── Scratchpad Helpers ─────────────────────────────────────────────────────────

SCRATCHPAD = Path("scratchpad.md")


def read_scratchpad() -> str:
    """Read prior findings — proves concept 5.4 (context persistence)."""
    if not SCRATCHPAD.exists():
        return ""
    return SCRATCHPAD.read_text(encoding="utf-8")


def append_to_scratchpad(topic: str, content: str) -> None:
    """Persist findings — proves concept 5.4."""
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    section = f"\n## {topic} — {timestamp}\n{content}\n\n---\n"
    with SCRATCHPAD.open("a", encoding="utf-8") as f:
        f.write(section)
    print(f"✅ Scratchpad updated: [{topic}]")


# ── Main Agent Runner ──────────────────────────────────────────────────────────

async def run_agent(user_prompt: str, verbose: bool = True) -> str:
    """
    Run the main Developer Productivity Agent.

    Tool boundary (proves 2.1):
      - Grep, Glob, Read: navigate code without reading everything (2.5)
      - Write: persist findings to scratchpad (2.5)
      - Task: spawn the deep-explorer subagent (1.3)

    Scratchpad reload (proves 5.4):
      Prior findings are prepended so the agent remembers earlier sessions.
    """

    # Reload prior findings — proves concept 5.4
    prior = read_scratchpad()
    memory_prefix = ""
    if prior.strip() and "<!-- Agent appends" not in prior:
        memory_prefix = (
            "\n\n## Prior Session Findings (from scratchpad)\n"
            "Use these to answer follow-up questions without re-reading files:\n\n"
            f"{prior}\n\n---\n\n"
        )

    full_prompt = memory_prefix + user_prompt
    result_text = ""

    # query() — Agent SDK entry point
    # allowed_tools defines the boundary (concept 2.1)
    # agents= defines available subagents (concept 1.3)
    async for message in query(
        prompt=full_prompt,
        options=ClaudeAgentOptions(
            allowed_tools=["Grep", "Glob", "Read", "Write", "Task"],
            agents={
                "deep-explorer": DEEP_EXPLORER_DEFINITION,
            },
            max_turns=30,
        ),
    ):
        if hasattr(message, "result") and message.result:
            result_text = message.result
            if verbose:
                print(result_text)
        elif verbose and hasattr(message, "type"):
            if message.type == "assistant" and hasattr(message, "message"):
                for block in getattr(message.message, "content", []):
                    if hasattr(block, "text"):
                        print(block.text, end="", flush=True)

    return result_text


# ── CLI Entry Point ────────────────────────────────────────────────────────────

async def main():
    if len(sys.argv) < 2:
        print('Usage: python -m agent.main_agent "<question>"')
        sys.exit(1)
    prompt = " ".join(sys.argv[1:])
    print(f"\n🔍 Developer Productivity Agent\n{'─'*50}")
    print(f"Question: {prompt}\n{'─'*50}\n")
    await run_agent(prompt)


if __name__ == "__main__":
    asyncio.run(main())
