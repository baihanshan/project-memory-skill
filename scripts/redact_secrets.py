#!/usr/bin/env python3
"""Redact likely secrets from project memory markdown files."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

REPLACEMENTS = [
    (re.compile(r"(?i)(api[_-]?key\s*[:=]\s*)[^\s`]+"), r"\1[REDACTED]"),
    (re.compile(r"(?i)(secret\s*[:=]\s*)[^\s`]+"), r"\1[REDACTED]"),
    (re.compile(r"(?i)(token\s*[:=]\s*)[^\s`]+"), r"\1[REDACTED]"),
    (re.compile(r"(?i)(password\s*[:=]\s*)[^\s`]+"), r"\1[REDACTED]"),
    (re.compile(r"(?i)(authorization\s*[:=]\s*)[^\n`]+"), r"\1[REDACTED]"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.DOTALL), "[REDACTED PRIVATE KEY]"),
]


def redact_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    new = text
    for pattern, repl in REPLACEMENTS:
        new = pattern.sub(repl, new)
    if new != text:
        path.write_text(new, encoding="utf-8")
        return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", default="project_memory")
    args = parser.parse_args()
    target = Path(args.path).resolve()
    if not target.exists():
        print(f"Path not found: {target}")
        return
    changed = 0
    files = [target] if target.is_file() else list(target.rglob("*.md"))
    for path in files:
        if redact_file(path):
            changed += 1
            print(f"Redacted possible secret in {path}")
    print(f"Done. Files changed: {changed}")


if __name__ == "__main__":
    main()
