# Memory Rules

## Purpose

The `project_memory/` folder is a project-local long-term memory system. It exists to help Codex resume work across sessions without loading every prior conversation or every memory file.

## Capture rules

Create or update memory when the information is likely to help future development sessions.

Capture:

1. Architecture decisions and tradeoffs.
2. API contracts and request/response schemas.
3. Resolved bugs with symptoms, root cause, fix, and verification.
4. Repeated setup, environment, dependency, or tooling issues.
5. Stable commands for running, testing, debugging, building, and deploying.
6. Module responsibilities and cross-file relationships.
7. Reusable implementation patterns.
8. Handoff state, next steps, blockers, and risks.

Do not capture:

1. Secrets or credentials.
2. Raw `.env` values.
3. Large source files or logs.
4. Temporary hypotheses that were not verified.
5. One-off conversation details unrelated to the project.
6. Information already obvious from code unless it is a cross-cutting project rule.
7. Personal information unrelated to project work.

## Classification rules

Use these categories:

- `bugs/`: symptoms, root cause, fix, and verification.
- `decisions/`: ADRs and architecture choices.
- `topics/`: durable explanation of a feature, module, or workflow.
- `patterns/`: recurring implementation patterns or conventions.
- `commands/`: run/test/build/deploy/debug commands.
- `api_contracts/`: API schemas, request/response shapes, frontend/backend contracts.
- `environment/`: local setup, dependencies, platform-specific notes.

## Memory levels

- `P0 Permanent`: must be kept unless user explicitly confirms deletion.
- `P1 Active`: current and important; deletion requires user confirmation.
- `P2 Reference`: useful but not always active; prefer archive over deletion.
- `P3 Archive`: historical and not loaded by default.
- `P4 Temporary`: may be deleted automatically.

## Evidence rules

Bug and decision memories must include evidence.

Evidence may include:

- Files changed.
- Tests run.
- Error messages summarized without secrets.
- Commit hash, if available.
- User confirmation.
- Date of observation or change.

## Conflict rules

Never silently overwrite old facts.

When a new fact conflicts with an old memory:

1. Mark the old memory as `superseded`.
2. Add `superseded_by` and `superseded_on`.
3. Create or update the new memory with date and evidence.
4. Update `index.md` so current routing points to the new memory.
5. Move the old memory to archive if it is no longer useful as active context.

## Deletion rules

- P4 temporary memory may be deleted automatically.
- P0/P1/P2 important memory cannot be deleted without explicit user confirmation.
- Prefer `archive` or `supersede` over deletion.
- If the memory contains secrets, redact immediately rather than preserving the secret in archive.
