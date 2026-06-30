# Memory Schema

Use YAML frontmatter in every detailed memory file.

## Common frontmatter

```yaml
title: "Short human-readable title"
type: bug | decision | topic | pattern | command | api_contract | environment
status: active | superseded | archived | temporary
level: P0 | P1 | P2 | P3 | P4
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [backend, frontend, api, langgraph]
use_when:
  - "Short condition describing when to read this file"
related:
  - "project_memory/active/decisions/ADR-0001-example.md"
superseded_by: null
superseded_on: null
```

## Bug file template

```markdown
---
title: "PDF parse timeout after upload"
type: bug
status: active
level: P1
created: 2026-06-30
updated: 2026-06-30
tags: [backend, pdf, parsing]
use_when:
  - "PDF upload succeeds but analysis hangs or returns 500"
related: []
superseded_by: null
superseded_on: null
---

# BUG-0001: PDF parse timeout after upload

## Symptoms

## Root cause

## Fix

## Verification evidence

- Files changed:
- Tests run:
- Date:

## Notes
```

## ADR file template

```markdown
---
title: "Use FastAPI router boundaries"
type: decision
status: active
level: P0
created: 2026-06-30
updated: 2026-06-30
tags: [backend, architecture, fastapi]
use_when:
  - "Changing backend route organization or API boundaries"
related: []
superseded_by: null
superseded_on: null
---

# ADR-0001: Use FastAPI router boundaries

## Status

Accepted

## Context

## Decision

## Alternatives considered

## Consequences

## Evidence

- Files changed:
- Tests run:
- Date:
```

## Topic file template

```markdown
---
title: "Analysis pipeline overview"
type: topic
status: active
level: P1
created: 2026-06-30
updated: 2026-06-30
tags: [analysis, backend, pipeline]
use_when:
  - "Working on the analysis pipeline"
related: []
superseded_by: null
superseded_on: null
---

# TOPIC-0001: Analysis pipeline overview

## Summary

## Important files

## Current behavior

## Known pitfalls

## Related memories
```

## Command file template

```markdown
---
title: "Local development commands"
type: command
status: active
level: P1
created: 2026-06-30
updated: 2026-06-30
tags: [commands, local-dev]
use_when:
  - "Running or debugging the project locally"
related: []
superseded_by: null
superseded_on: null
---

# CMD-0001: Local development commands

## Backend

## Frontend

## Tests

## Notes
```
