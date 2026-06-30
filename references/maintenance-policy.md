# Maintenance Policy

## When maintenance is required

Run memory maintenance before finishing any complex task.

A task is complex if it:

- Modifies 2 or more files.
- Fixes a bug.
- Changes API contracts.
- Changes project structure.
- Changes run/test/build/deploy commands.
- Makes or reverses an architecture decision.
- Discovers a recurring pitfall.
- Leaves unfinished work or risks.

## Required maintenance steps

1. Update `project_memory/handoff.md`.
2. Add or update detailed memories only when durable knowledge was produced.
3. Update `project_memory/index.md`.
4. Redact secrets.
5. Check index size and evidence completeness.
6. Consolidate, archive, or delete temporary entries if needed.

## Consolidation rules

Consolidate when:

- Five or more memories describe the same topic.
- Several bug entries share the same root cause.
- Several command entries are obsolete or duplicate.
- The index exceeds 50 active entries.

## Archive rules

Archive when:

- The memory is historically useful but no longer active.
- It has been superseded by a new memory.
- It is P2 reference material that is rarely used.

## Deletion rules

- Only P4 temporary memory may be deleted automatically.
- Important memory requires explicit user confirmation before deletion.
- If a file contains a secret, redact the secret immediately.

## Health check

Use:

```bash
python <skill_dir>/scripts/check_memory_health.py --project-root .
```

Resolve high-priority issues before completing the task.
