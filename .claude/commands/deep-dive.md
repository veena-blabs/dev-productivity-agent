---
description: Delegate a deep-dive investigation to the deep-explorer subagent, then return a concise parent summary and persist findings to scratchpad. Usage: /deep-dive <topic>
allowed-tools: Task, Write, Read
---
<!-- Proves concept 1.3: Subagent invocation -->
<!-- Proves concept 3.2: Custom slash commands -->
<!-- Proves concept 3.4: Plan mode vs direct — delegation is a plan step, writing is direct -->

# Deep Dive: $ARGUMENTS

## Step 1: Delegate to Subagent (plan step)
Use the Task tool to invoke the deep-explorer subagent with this exact prompt:

"Deep dive investigation: $ARGUMENTS

Trace this feature thoroughly across all relevant files. Return your structured
summary in the required format under 300 words."

## Step 2: Receive Summary
Wait for the subagent's structured summary. Do NOT re-read the files yourself —
the subagent has already done that. This is how the main context stays clean.

## Step 3: Write Parent Summary (2 sentences max)
Based on the subagent's summary, write a 2-sentence synthesis for the engineer.
This is what the engineer sees first.

## Step 4: Persist to Scratchpad (direct execution)
Append to scratchpad.md:
```
## Deep Dive: $ARGUMENTS
### Subagent Summary:
[paste full subagent output here]

### Parent Synthesis:
[your 2-sentence summary]
```
