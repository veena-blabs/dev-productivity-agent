# Developer Productivity Agent — Scratchpad

This file persists key findings across long sessions, defending against context window loss.
**Proves concept 5.4:** Context management in large codebase exploration.

The agent appends to this file after answering each question. On the next session,
it reads this file first — so it "remembers" what it learned without re-reading files.

---
<!-- Agent appends findings below this line -->

## Auth Middleware Deep-Dive (subagent) — 2026-06-25 session
- **Entry point:** `run_demo.py:42` → `demo_3_auth_middleware_subagent()`
- **Key files traced:** `run_demo.py`, `agent/main_agent.py`, `agent/subagent_runner.py`, `agent/scratchpad.py`
- **Flow summary:**
  1. `run_demo.py:42` builds the prompt and calls `run_agent()`
  2. `main_agent.py` prepends scratchpad findings, dispatches to `query()`
  3. `subagent_runner.py:14` defines `DEEP_EXPLORER` — restricted to `Read/Grep/Glob/Bash`, no `Task` tool
  4. Only ≤300-word summary returns to parent; verbose exploration stays isolated in subagent context
- **Key findings:**
  - No actual auth middleware exists — "auth middleware" is a sample topic to prove concept 1.3/2.1
  - No JWT, bearer, session, cookie, or guard libraries imported anywhere
  - Single-depth restriction (no `Task` in subagent `allowed_tools`) prevents recursive subagent spawning
- **Proves:** 1.3 (subagent invocation), 2.1 (tool boundaries), 5.4 (context isolation)

---

## Orders Data Model — 2026-06-25 session
- **Entry point:** N/A — no data model exists in this repo
- **Key files searched:** all *.py, all *.md via Grep for `order|Order|ORDER`
- **Flow summary:** Only hits were `run_demo.py:37` (the demo prompt string) and `README.md:91` (CCAF checklist)
- **Key finding:** This project is the agent itself — no domain models, ORMs, migrations, or schemas exist. Demo Prompt 2 is meant to target an external app (e-commerce, ERP, etc.) with a real orders table.

---

## Password-Reset Flow — 2026-06-25 session
- **Entry point:** N/A — no such flow exists in this repo
- **Key files searched:** all *.py, all *.md via Grep
- **Flow summary:** Grep for `password.reset|reset_password|PasswordReset` returned only references to the demo prompt string in `run_demo.py:26` and `README.md:90`
- **Key finding:** This project IS the agent, not a target app. "Password-reset flow" is a CCAF demo prompt meant to be run against an external codebase with auth logic.

---
