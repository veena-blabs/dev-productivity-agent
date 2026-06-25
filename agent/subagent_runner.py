"""
subagent_runner.py — Standalone subagent invocation demo.

CCAF Concepts Proved:
- 1.3: Subagent invocation, context passing, spawning
- 2.1: Tool boundaries (subagent restricted to Read/Grep/Glob/Bash)
- 5.4: Verbose exploration stays in subagent context, not parent
"""

import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition


DEEP_EXPLORER = AgentDefinition(
    description=(
        "Deep-dive code explorer. Returns a structured summary under 300 words. "
        "Reads as many files as needed but never returns raw file contents."
    ),
    prompt="""You are a deep-dive code exploration specialist.

## Output Contract
Return ONLY this format. Total output under 300 words.

**Feature/Topic:** [topic]
**Entry Point:** [file:line]
**Key Files Traced:** [list]
**Flow Summary:**
1. [step]
2. [step]
**Key Findings:**
- [finding]
**Recommended Reading:** [1-3 files]

## Rules
- Grep → Glob → Read (relevant files only)
- Bash: find/wc -l/head/tail only
- Never modify files. Never return raw file contents.
""",
    tools=["Read", "Grep", "Glob", "Bash"],
    model="sonnet",
)


async def run_deep_explorer(topic: str, codebase_hint: str = "") -> str:
    """
    Invoke the deep-explorer subagent programmatically.
    Proves concept 1.3: subagent invocation, context passing, spawning.
    Only the 300-word summary returns — verbose exploration stays in the subagent (5.4).
    """
    prompt = f"Deep dive investigation: {topic}"
    if codebase_hint:
        prompt += f"\n\nStart exploring from: {codebase_hint}"
    prompt += "\n\nReturn your structured summary in the required format."

    print(f"\n🤖 Spawning deep-explorer subagent for: {topic}")
    print("   (Only its summary returns to parent — context stays clean)\n")

    summary = ""
    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            # Restricted tools — proves concept 2.1 (clear boundaries)
            allowed_tools=["Read", "Grep", "Glob", "Bash"],
            # No Task tool — subagents cannot spawn further subagents (1.3)
            agents={"deep-explorer": DEEP_EXPLORER},
            max_turns=20,
        ),
    ):
        if hasattr(message, "result") and message.result:
            summary = message.result

    print(f"✅ Subagent complete. Summary: {len(summary)} chars returned to parent.")
    return summary


async def demo():
    """Run standalone — shows subagent invocation proves concept 1.3."""
    print("=" * 60)
    print("SUBAGENT RUNNER DEMO — Proves concept 1.3")
    print("=" * 60)
    summary = await run_deep_explorer("authentication middleware", codebase_hint="./")
    print("\n" + "=" * 60)
    print("SUBAGENT SUMMARY (all parent receives):")
    print("=" * 60)
    print(summary)


if __name__ == "__main__":
    asyncio.run(demo())
