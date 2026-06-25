---
description: Explore how a feature works in this codebase. Greps first, reads only relevant files, saves findings to scratchpad. Usage: /explore <feature or question>
allowed-tools: Grep, Glob, Read, Write
---
<!-- Proves concept 3.2: Custom slash commands and skills -->

# Explore: $ARGUMENTS

You are in codebase exploration mode. The engineer wants to understand: **$ARGUMENTS**

## Execution Plan (plan mode — think before acting)

### Step 1: Orient with Grep + Glob
- Extract 2-3 key terms from the question
- Run Grep for each key term to find relevant files
- Run Glob to understand the folder structure around those files
- Do NOT open any files yet

### Step 2: Identify Entry Points
- From Grep results, identify the most likely entry point (route handler, controller, function definition)
- List the top 3-5 files to read, in order of relevance

### Step 3: Trace the Flow (targeted Read only)
- Read identified files — use line ranges where possible, not full file reads
- Follow imports to adjacent files (max 3 hops from entry point)
- Stop reading when you have enough to explain the flow end-to-end

### Step 4: Synthesize and Explain
Write a clear explanation structured as:
- **Entry point:** where the feature starts
- **Flow:** step-by-step trace through the code
- **Data:** what data structures / models are involved
- **Output:** what the feature returns or triggers

### Step 5: Persist to Scratchpad (direct execution)
Append to scratchpad.md:
```
## $ARGUMENTS — Session Notes
- Entry point: [file:line]
- Key files: [list]
- Flow: [one-paragraph summary]
- Key findings: [bullets]
```

## Guardrails
- If tracing requires more than 5 files → stop and invoke the deep-explorer subagent instead
- Never read a file not identified by Grep or Glob
- Never guess at file locations — always search first
- Keep your explanation under 400 words; link to files for detail
