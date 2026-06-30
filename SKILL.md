---
name: project-memory
description: Use this skill whenever Codex works in a software project that contains or should contain project_memory/. Use at the start of a new Codex session, when the user says continue, resume, pick up previous work, check project context, initialize project memory, read handoff.md, read index.md, update handoff.md, maintain index.md, record bugs, record ADR architecture decisions, record API contracts, record commands, consolidate/archive/delete project memory, or preserve long-term project context without loading all memory files.
---

# Project Memory Skill

This skill defines a Codex-managed workflow for maintaining a single project's long-term memory in a normal project folder named `project_memory/`.

The skill package is installed and managed by Codex. The memory data is stored separately inside the project repository:

```text
project-root/
  AGENTS.md
  project_memory/
    index.md
    handoff.md
    inbox.md
    active/
    archive/
```

Do not store this skill itself inside `project_memory/`. `project_memory/` is only the project's memory data directory.

## Core principles

1. Do not load all memories into context.
2. At the start of a session, read only `AGENTS.md`, `project_memory/handoff.md`, and `project_memory/index.md` when available.
3. Use the latest `## Current Context` section in `handoff.md` as the fast resume point for the new session.
4. Use `index.md` as a bounded routing layer. Read detailed memory files only when relevant to the current task.
5. Keep `index.md` below 50 active entries. If it exceeds the limit, consolidate, archive, or delete temporary entries before finishing a complex task.
6. Maintain memory only when it improves future project work. Do not record trivia, raw logs, large source code blocks, secrets, or unverified guesses.
7. Never silently overwrite old facts. If a new fact supersedes an old one, preserve the old fact with a `superseded` status and create a dated, evidenced replacement.
8. Temporary memory may be deleted automatically. Important memory requires explicit user confirmation before deletion. Prefer archive or supersede over deletion.
9. Always run or apply secret redaction before writing memory content.

## Startup protocol

This skill should be selected automatically whenever the current repository has a `project_memory/` folder or the user asks to continue/resume prior project work. If there is any ambiguity, prefer reading only `project_memory/handoff.md` and `project_memory/index.md` rather than loading detailed memory files.

When starting work in a project:

1. Check whether `project_memory/` exists in the project root.
2. If it does not exist and the user wants project memory, run:

```bash
python <skill_dir>/scripts/init_memory.py --project-root .
```

3. If `project_memory/` exists, read `project_memory/handoff.md` first.
4. In `handoff.md`, focus on the latest `## Current Context` section. Treat it as the compact resume state.
5. Read `project_memory/index.md` second.
6. Do not read all detailed memory files. Read only entries linked from `handoff.md` or entries from `index.md` whose `tags`, `use_when`, or `related` fields match the current task.

## Retrieval protocol

Use `index.md` as a bounded map from the current task to detailed memories.

Read a detailed memory file only when at least one of these is true:

- The file is listed in `handoff.md` under `Relevant memory entries`.
- The current task matches the index entry's `use_when` description.
- The current task matches the entry's tags or module path.
- The file is needed to resolve a conflict or verify a prior decision.

If no index entry clearly matches, do not guess. Continue with normal code inspection, then create or update memory only if the task produces durable project knowledge.

For more detail, read `references/retrieval-policy.md`.

## What to remember

Capture durable project knowledge:

- Architecture decisions and important tradeoffs.
- API contracts, request/response schemas, and frontend/backend agreements.
- Resolved bugs with symptoms, root cause, fix, and verification evidence.
- Repeated environment/setup/debugging issues.
- Stable commands for running, testing, building, deploying, or debugging.
- Important module responsibilities and cross-file relationships.
- Reusable implementation patterns.
- Current project state and next steps for handoff.

Do not remember:

- Secrets, credentials, tokens, cookies, private keys, or raw `.env` values.
- Large pasted logs or generated output.
- Large blocks of source code already present in the repository.
- Temporary guesses that were not verified.
- One-off conversational details unrelated to the project.
- Information that is already obvious from a nearby README or source file unless it is a cross-cutting rule.

For complete rules, read `references/memory-rules.md`.

## Memory levels

Use these levels consistently:

- `P0 Permanent`: core architecture, critical rules, non-negotiable project constraints.
- `P1 Active`: current project facts, active bugs, current API contracts, active design direction.
- `P2 Reference`: lower-frequency but useful knowledge, historical fixes, commands, environment notes.
- `P3 Archive`: history that should not be loaded by default.
- `P4 Temporary`: short-lived notes that may be deleted automatically.

## File categories

Store active memory under:

```text
project_memory/active/
  bugs/
  decisions/
  topics/
  patterns/
  commands/
  api_contracts/
  environment/
```

Store archived memory under matching subdirectories in `project_memory/archive/`.

Use mixed readable filenames:

```text
BUG-0001-pdf-parse-timeout.md
ADR-0001-use-fastapi-router.md
TOPIC-0001-analysis-pipeline.md
CMD-0001-local-dev-commands.md
```

ADR numbers are globally incremented: `ADR-0001`, `ADR-0002`, etc.

## Complex task completion protocol

A task is complex when any of these are true:

- It modifies 2 or more files.
- It fixes a bug.
- It changes API contracts.
- It changes project structure.
- It changes run/test/build/deploy commands.
- It makes or reverses an architecture decision.
- It discovers a likely recurring pitfall.
- It leaves unfinished work or risks for the next session.

Before finishing a complex task:

1. Update `project_memory/handoff.md`.
2. Keep the latest `## Current Context` short enough to read at every new session.
3. Move the previous current context into `Recent Handoffs` and keep only the 5 most recent handoffs.
4. Add or update detailed memory files only when durable knowledge was produced.
5. Update `project_memory/index.md` so it routes to the relevant files.
6. Run or apply secret redaction before writing any memory.
7. If `index.md` exceeds 50 active entries, consolidate, archive, or delete temporary entries.
8. If important memory should be deleted, ask the user first.

For more detail, read `references/maintenance-policy.md` and `references/startup-and-handoff.md`.

## Scripts

This skill includes Python scripts. Prefer executing scripts over manually editing repetitive structures when safe.

### Initialize project memory

```bash
python <skill_dir>/scripts/init_memory.py --project-root .
```

Creates `project_memory/`, standard subdirectories, initial templates, and idempotently creates or updates `AGENTS.md` with a Project Memory section.

### Update index

```bash
python <skill_dir>/scripts/update_index.py --project-root .
```

Scans active memory files and rebuilds bounded `project_memory/index.md` entries from frontmatter and headings.

### Check memory health

```bash
python <skill_dir>/scripts/check_memory_health.py --project-root .
```

Checks index count, missing files, oversized handoff, missing evidence for bugs/decisions, and possible secrets.

### Redact secrets

```bash
python <skill_dir>/scripts/redact_secrets.py --path project_memory
```

Scans memory files and replaces likely secret values with `[REDACTED]`.

### Archive memory

```bash
python <skill_dir>/scripts/archive_memory.py --project-root . --file project_memory/active/topics/TOPIC-0001-example.md
```

Moves a memory file from `active/` to the matching `archive/` category and updates status metadata.

## Safety rules

- Do not write secret values to memory.
- Do not auto-delete P0/P1/P2 memory.
- Do not silently replace old facts.
- Do not use project memory as a substitute for reading the actual code when correctness matters.
- Do not treat archived memory as current without verifying dates and status.
- Do not modify Git ignore policy unless the user explicitly requests it.
