#!/usr/bin/env python3
"""Initialize project_memory/ and idempotently add AGENTS.md guidance."""
from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

PROJECT_MEMORY_SECTION_BEGIN = "<!-- PROJECT_MEMORY_SECTION_BEGIN -->"
PROJECT_MEMORY_SECTION_END = "<!-- PROJECT_MEMORY_SECTION_END -->"

AGENTS_SECTION = f"""
{PROJECT_MEMORY_SECTION_BEGIN}

## Project Memory

This project uses a local long-term memory folder named `project_memory/`.

At the start of every new Codex session in this project, use the `project-memory` skill and follow this startup protocol:

1. Read `project_memory/handoff.md` first, especially the latest `## Current Context` section. Treat it as the fast resume state.
2. Read `project_memory/index.md` second. Treat it as the bounded routing layer.
3. Do not load all memory files. Read detailed files only when the handoff or index indicates relevance.
4. If the user says "continue", "resume", "pick up where we left off", "check project context", or asks for project-memory work, apply this protocol before editing code.

Before finishing a complex task, update project memory when durable project knowledge was produced. A complex task includes bug fixes, architecture decisions, API contract changes, multi-file changes, command/environment changes, or unfinished handoff state.

Never store secrets in project memory. Temporary memory may be deleted automatically, but important memory requires explicit user confirmation before deletion.

{PROJECT_MEMORY_SECTION_END}
""".strip() + "\n"


def write_if_missing(path: Path, content: str) -> None:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def ensure_agents_md(root: Path) -> None:
    agents = root / "AGENTS.md"
    if not agents.exists():
        agents.write_text("# AGENTS.md\n\n" + AGENTS_SECTION + "\n", encoding="utf-8")
        return

    text = agents.read_text(encoding="utf-8")
    if PROJECT_MEMORY_SECTION_BEGIN in text and PROJECT_MEMORY_SECTION_END in text:
        start = text.index(PROJECT_MEMORY_SECTION_BEGIN)
        end = text.index(PROJECT_MEMORY_SECTION_END) + len(PROJECT_MEMORY_SECTION_END)
        updated = text[:start].rstrip() + "\n\n" + AGENTS_SECTION.strip() + "\n" + text[end:].lstrip("\n")
        if not updated.endswith("\n"):
            updated += "\n"
        agents.write_text(updated, encoding="utf-8")
        return
    if not text.endswith("\n"):
        text += "\n"
    agents.write_text(text + "\n" + AGENTS_SECTION + "\n", encoding="utf-8")


def init_memory(root: Path) -> None:
    today = date.today().isoformat()
    pm = root / "project_memory"
    dirs = [
        pm / "active" / "bugs",
        pm / "active" / "decisions",
        pm / "active" / "topics",
        pm / "active" / "patterns",
        pm / "active" / "commands",
        pm / "active" / "api_contracts",
        pm / "active" / "environment",
        pm / "archive" / "bugs",
        pm / "archive" / "decisions",
        pm / "archive" / "topics",
        pm / "archive" / "patterns",
        pm / "archive" / "commands",
        pm / "archive" / "api_contracts",
        pm / "archive" / "environment",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    write_if_missing(pm / "index.md", f"""# Project Memory Index

Updated: {today}

This file is a bounded routing layer. Do not put long memory content here.

## Active Entries

<!-- Keep active entries <= 50. -->

## Pinned Entries

<!-- Keep pinned entries <= 10. -->

## Recent Entries

<!-- Keep recent entries <= 15. -->
""")

    write_if_missing(pm / "handoff.md", f"""# Handoff

## Current Context

Updated: {today}

### Current goal

- Not recorded yet.

### Current project state

- Not recorded yet.

### Recently changed

- Not recorded yet.

### Open issues

- Not recorded yet.

### Next recommended steps

- Not recorded yet.

### Relevant memory entries

- None yet.

## Recent Handoffs
""")

    write_if_missing(pm / "inbox.md", f"""# Memory Inbox

Updated: {today}

Use this file for short-lived notes that still need classification. Do not let this file become permanent storage.

## Unclassified Notes
""")

    ensure_agents_md(root)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".", help="Path to project root")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    init_memory(root)
    print(f"Initialized project memory in {root / 'project_memory'}")
    print(f"Ensured AGENTS.md project memory section in {root / 'AGENTS.md'}")


if __name__ == "__main__":
    main()
