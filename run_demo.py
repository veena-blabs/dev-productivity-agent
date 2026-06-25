"""
run_demo.py — Runs the three required CCAF demo prompts in sequence.

EXACTLY these three prompts are required by the CCAF submission checklist.
Run: python run_demo.py
"""

import asyncio
from agent.main_agent import run_agent, read_scratchpad


def print_demo_header(num: int, prompt: str, concepts: list[str]) -> None:
    print("\n" + "=" * 70)
    print(f"DEMO PROMPT {num}  |  Concepts: {', '.join(concepts)}")
    print("=" * 70)
    print(f'📝 "{prompt}"')
    print("-" * 70 + "\n")


async def demo_1_password_reset() -> str:
    """
    CCAF Demo 1: "How does the password-reset flow work here?"
    Observe: Grep first → Glob → Read only relevant files → scratchpad persist
    Proves: 2.5 (Grep/Glob/Read), 3.4 (plan mode), 5.4 (scratchpad)
    """
    prompt = "How does the password-reset flow work here?"
    print_demo_header(1, prompt, ["2.5 (Grep/Glob/Read)", "3.4 (plan mode)", "5.4 (scratchpad)"])
    return await run_agent(prompt)


async def demo_2_orders_data_model() -> str:
    """
    CCAF Demo 2: "Summarize the data model for orders."
    Observe: traces across multiple files, saves notes to scratchpad mid-session
    Proves: 2.5 (built-in tools), 5.4 (context + scratchpad)
    """
    prompt = "Summarize the data model for orders."
    print_demo_header(2, prompt, ["2.5 (built-in tools)", "5.4 (context + scratchpad)"])
    return await run_agent(prompt)


async def demo_3_auth_middleware_subagent() -> str:
    """
    CCAF Demo 3 (exact wording required):
    "Deep-dive the auth middleware in a subagent, then return a concise
     parent summary and persist key findings in scratchpad."
    Observe: Task tool spawns deep-explorer → only summary returns → scratchpad persist
    Proves: 1.3 (subagent), 2.1 (tool boundaries), 3.2 (slash cmd), 5.4 (context)
    """
    prompt = (
        "Deep-dive the auth middleware in a subagent, then return a concise "
        "parent summary and persist key findings in scratchpad."
    )
    print_demo_header(
        3, prompt,
        ["1.3 (subagent)", "2.1 (tool boundaries)", "3.2 (slash cmd)", "5.4 (context)"]
    )
    return await run_agent(prompt)


async def main() -> None:
    print("\n" + "🚀 " * 20)
    print("DEVELOPER PRODUCTIVITY AGENT — CCAF DEMO RUN")
    print("🚀 " * 20)
    print("\nConcepts demonstrated:")
    concepts = [
        "1.3  Subagent invocation, context passing, spawning",
        "2.1  Tool interfaces with clear descriptions/boundaries",
        "2.4  MCP server integration (mcp_config.json → fetch-docs)",
        "2.5  Built-in tools: Grep, Glob, Read, Write",
        "3.1  CLAUDE.md hierarchy and scoped instructions",
        "3.2  Custom slash commands: /explore, /deep-dive",
        "3.4  Plan mode vs direct execution",
        "5.4  Context management in large codebase exploration",
    ]
    for c in concepts:
        print(f"  {c}")

    await demo_1_password_reset()
    await demo_2_orders_data_model()
    await demo_3_auth_middleware_subagent()

    print("\n" + "=" * 70)
    print("✅ ALL THREE DEMO PROMPTS COMPLETE")
    print("=" * 70)
    print("\n📋 Final scratchpad contents:")
    print("-" * 70)
    print(read_scratchpad())


if __name__ == "__main__":
    asyncio.run(main())
