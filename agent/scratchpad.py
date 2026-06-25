"""
scratchpad.py — Persistent findings storage.

CCAF Concepts Proved:
- 2.5: Complement to the Write built-in tool
- 5.4: Findings survive context resets; reloaded each session
"""

from datetime import datetime
from pathlib import Path

SCRATCHPAD_PATH = Path("scratchpad.md")


def append_to_scratchpad(topic: str, content: str, filepath: Path = SCRATCHPAD_PATH) -> None:
    """Append a dated finding section. Proves concept 5.4."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    section = f"\n## {topic} — {timestamp}\n{content}\n\n---\n"
    if not filepath.exists():
        filepath.write_text(
            "# Developer Productivity Agent — Scratchpad\n\n"
            "Proves concept 5.4: persistent findings across long sessions.\n\n---\n"
        )
    with filepath.open("a", encoding="utf-8") as f:
        f.write(section)
    print(f"✅ Scratchpad updated: [{topic}] at {timestamp}")


def read_scratchpad(filepath: Path = SCRATCHPAD_PATH) -> str:
    """Read all prior findings. Used by main_agent at session start. Proves 5.4."""
    if not filepath.exists():
        return ""
    return filepath.read_text(encoding="utf-8")


def search_scratchpad(keyword: str, filepath: Path = SCRATCHPAD_PATH) -> list[str]:
    """Return sections containing keyword. Avoids re-reading files. Proves 5.4."""
    content = read_scratchpad(filepath)
    if not content:
        return []
    sections = content.split("---")
    return [s.strip() for s in sections if keyword.lower() in s.lower() and s.strip()]
