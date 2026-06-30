#!/usr/bin/env python3
"""Rebuild project_memory/index.md from active memory files."""
from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def parse_frontmatter(text: str) -> dict[str, str]:
    match = FRONTMATTER_RE.match(text)
    data: dict[str, str] = {}
    if not match:
        return data
    for line in match.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip('"')
    return data


def first_heading(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return "Untitled memory"


def collect_entries(root: Path) -> list[str]:
    pm = root / "project_memory"
    active = pm / "active"
    entries: list[str] = []
    if not active.exists():
        return entries

    for path in sorted(active.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        meta = parse_frontmatter(text)
        status = meta.get("status", "active")
        if status not in {"active", "temporary"}:
            continue
        rel = path.relative_to(root).as_posix()
        title = meta.get("title") or first_heading(text)
        level = meta.get("level", "P2")
        tags = meta.get("tags", "[]")
        use_when = meta.get("use_when", "")
        entry_id = path.stem
        entries.append(
            f"- id: {entry_id}\n"
            f"  path: {rel}\n"
            f"  title: {title}\n"
            f"  level: {level}\n"
            f"  status: {status}\n"
            f"  tags: {tags}\n"
            f"  use_when: {use_when}\n"
        )
    return entries


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    pm = root / "project_memory"
    pm.mkdir(exist_ok=True)
    entries = collect_entries(root)
    body = "\n".join(entries) if entries else "<!-- No active entries yet. -->\n"
    index = f"""# Project Memory Index

Updated: {date.today().isoformat()}

This file is a bounded routing layer. Do not put long memory content here.

## Active Entries

<!-- Keep active entries <= 50. Current active entries: {len(entries)}. -->

{body}

## Pinned Entries

<!-- Keep pinned entries <= 10. -->

## Recent Entries

<!-- Keep recent entries <= 15. -->
"""
    (pm / "index.md").write_text(index, encoding="utf-8")
    print(f"Updated {pm / 'index.md'} with {len(entries)} active entries")
    if len(entries) > 50:
        print("WARNING: Active index entries exceed 50. Consolidate or archive before finishing.")


if __name__ == "__main__":
    main()
