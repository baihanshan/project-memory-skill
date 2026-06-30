# Retrieval Policy

## Goal

Minimize context load while preserving useful project continuity.

## Default read set

At the beginning of a session, read only:

1. `AGENTS.md`, if present.
2. `project_memory/handoff.md`, especially the latest `## Current Context` section.
3. `project_memory/index.md`.

Do not read every file in `project_memory/`.

## When to read detailed memory

Read a detailed file when:

- It is referenced by the current handoff.
- It is referenced by a matching index entry.
- Its tags match the current module or task.
- Its `use_when` condition matches the current problem.
- It is needed to resolve a contradiction.

## When not to read detailed memory

Do not read detailed memory when:

- The task is trivial.
- The task can be answered directly from current code.
- The index entry is stale, archived, or superseded and not needed for history.
- The memory is unrelated to the current module or problem.

## Index entry shape

Each active index entry should be compact:

```markdown
- id: BUG-0001-pdf-parse-timeout
  path: project_memory/active/bugs/BUG-0001-pdf-parse-timeout.md
  level: P1
  status: active
  tags: [backend, pdf, parsing]
  use_when: "PDF upload succeeds but /analysis hangs or returns 500."
```

## Limits

- Active index entries: maximum 50.
- Pinned entries: maximum 10.
- Recent entries: maximum 15.
- If limits are exceeded, consolidate or archive before finishing a complex task.
