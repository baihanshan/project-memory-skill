# Codex Project Memory Skill

[English](README.md) | [简体中文](README.zh-CN.md)

A Codex skill for maintaining project development memory across conversations.

This skill helps Codex and other coding agents remember the details of a software project: prior decisions, current progress, known bugs, API contracts, commands, environment notes, and handoff context. It is designed to prevent the common problem where a new Codex conversation starts without enough memory of previous work.

The memory is stored inside the project as plain Markdown files under `project_memory/`, so developers can inspect, edit, review, and version-control the memory directly. Codex uses a bounded `project_memory/index.md` as a routing layer and a fast-resume `project_memory/handoff.md` to quickly recover the latest project state, then reads detailed memory files only when needed.

## Features

- Project-local long-term memory folder: `project_memory/`
- Fast session resume via `handoff.md`
- Bounded routing index via `index.md`
- On-demand retrieval of detailed memory files
- Structured memory categories for bugs, ADRs, topics, commands, API contracts, environment notes, and patterns
- Sensitive information redaction rules
- Conflict handling with date and evidence
- Python scripts for initialization, index maintenance, health checks, redaction, and archiving

## Installation

Clone this repository and copy the skill folder into your Codex skills directory:

```bash
git clone https://github.com/baihanshan/project-memory-skill.git project-memory
mkdir -p ~/.codex/skills
cp -R project-memory ~/.codex/skills/project-memory
```

Restart Codex after installing the skill.

## Usage

Use this skill when a software project contains or should contain a `project_memory/` directory, or when you want Codex to preserve durable project context across sessions.

To initialize memory in a project:

```bash
python ~/.codex/skills/project-memory/scripts/init_memory.py --project-root .
```

The command creates:

```text
project_memory/
  index.md
  handoff.md
  inbox.md
  active/
  archive/
```

## Included Scripts

- `scripts/init_memory.py`: creates the project memory structure and templates
- `scripts/update_index.py`: rebuilds `project_memory/index.md` from active memory files
- `scripts/check_memory_health.py`: checks index size, missing links, handoff size, evidence, and possible secrets
- `scripts/redact_secrets.py`: redacts likely secret values from memory files
- `scripts/archive_memory.py`: moves active memory files into archive and updates status metadata

## License

MIT
