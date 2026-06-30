#!/usr/bin/env python3
"""Check project_memory health."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|secret|token|password|authorization|bearer)\s*[:=]\s*[^\s`]+"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
]


def count_index_entries(index_text: str) -> int:
    return len(re.findall(r"^- id:\s+", index_text, flags=re.MULTILINE))


def has_evidence(text: str) -> bool:
    return "## Evidence" in text or "## Verification evidence" in text


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    pm = root / "project_memory"
    issues: list[str] = []

    if not pm.exists():
        print("ERROR: project_memory/ does not exist. Run init_memory.py first.")
        return

    index = pm / "index.md"
    if index.exists():
        count = count_index_entries(index.read_text(encoding="utf-8"))
        if count > 50:
            issues.append(f"index.md has {count} active entries; limit is 50")
    else:
        issues.append("index.md is missing")

    handoff = pm / "handoff.md"
    if handoff.exists():
        text = handoff.read_text(encoding="utf-8")
        current = text.split("## Recent Handoffs", 1)[0]
        if len(current.splitlines()) > 100:
            issues.append("Current Context appears long; recommended <= 80 lines")
    else:
        issues.append("handoff.md is missing")

    for path in pm.rglob("*.md"):
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                issues.append(f"Possible secret in {path.relative_to(root)}")
                break
        if ("/bugs/" in path.as_posix() or "/decisions/" in path.as_posix()) and not has_evidence(text):
            issues.append(f"Missing evidence section in {path.relative_to(root)}")

    if issues:
        print("Memory health issues:")
        for issue in issues:
            print(f"- {issue}")
    else:
        print("Memory health check passed.")


if __name__ == "__main__":
    main()
