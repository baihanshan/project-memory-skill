# Startup and Handoff Policy

## Purpose

`handoff.md` is the fast resume point for new Codex sessions. It must be short enough to read at the start of every session.

## Startup behavior

At the start of every new Codex session in a repository that contains `project_memory/`, or when the user asks to continue/resume/check project context, use the `project-memory` skill and read only the compact routing files first:

1. Read `AGENTS.md`, if present.
2. Read `project_memory/handoff.md`.
3. Focus on the latest `## Current Context` block and treat it as the fast resume state.
4. Read `project_memory/index.md` and treat it as the bounded routing layer.
5. Read detailed memory files only if linked from handoff/index or clearly relevant to the current task.
6. Do not load every file in `project_memory/`.

## Handoff structure

```markdown
# Handoff

## Current Context

Updated: YYYY-MM-DD

### Current goal

### Current project state

### Recently changed

### Open issues

### Next recommended steps

### Relevant memory entries

## Recent Handoffs

### YYYY-MM-DD
```

## Handoff limits

- `Current Context` should normally be under 80 lines.
- Keep only the latest 5 entries in `Recent Handoffs`.
- Move older handoffs to archive only when they are genuinely useful; otherwise remove old handoff summaries.

## What belongs in Current Context

- Current task state.
- What changed recently.
- Known blockers or risks.
- Next recommended steps.
- Links to detailed memory files that are likely relevant.

## What does not belong in Current Context

- Full logs.
- Full code blocks.
- Old history unrelated to the current task.
- Secrets.
- Long explanations already stored in detailed memory files.
