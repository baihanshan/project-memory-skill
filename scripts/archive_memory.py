#!/usr/bin/env python3
"""Archive a memory file from project_memory/active to project_memory/archive."""
from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


def update_status(text: str) -> str:
    today = date.today().isoformat()
    if text.startswith("---\n") and "\n---\n" in text:
        head, rest = text[4:].split("\n---\n", 1)
        lines = []
        keys_seen = set()
        for line in head.splitlines():
            if line.startswith("status:"):
                lines.append("status: archived")
                keys_seen.add("status")
            elif line.startswith("updated:"):
                lines.append(f"updated: {today}")
                keys_seen.add("updated")
            else:
                lines.append(line)
        if "status" not in keys_seen:
            lines.append("status: archived")
        if "updated" not in keys_seen:
            lines.append(f"updated: {today}")
        return "---\n" + "\n".join(lines) + "\n---\n" + rest
    return f"---\nstatus: archived\nupdated: {today}\n---\n\n" + text


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--file", required=True, help="Memory file to archive")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    src = Path(args.file)
    if not src.is_absolute():
        src = (root / src).resolve()
    pm = root / "project_memory"
    active = pm / "active"
    archive = pm / "archive"
    try:
        rel = src.relative_to(active)
    except ValueError:
        raise SystemExit("File must be inside project_memory/active/")
    dst = archive / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    text = src.read_text(encoding="utf-8")
    dst.write_text(update_status(text), encoding="utf-8")
    src.unlink()
    print(f"Archived {src} -> {dst}")


if __name__ == "__main__":
    main()
