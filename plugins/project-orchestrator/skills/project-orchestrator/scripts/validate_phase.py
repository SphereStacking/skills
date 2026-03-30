#!/usr/bin/env python3
"""Validate phase document structure: required sections, recommended sections,
completion condition checkboxes, and Go/No-Go table format."""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Patterns support both English and Japanese phase docs
REQUIRED_SECTIONS = [
    (r"^#+\s*(Phase\s+\d+|フェーズ\s*\d+)", "Phase header"),
    (r"\*\*(Objective|目的):\*\*", "Objective"),
    (r"\*\*(Status|ステータス):\*\*", "Status"),
    (r"\*\*(Risk Level|Risk|リスクレベル|リスク):\*\*", "Risk Level"),
    (r"\*\*(Rollback|ロールバック):\*\*", "Rollback"),
    (r"^#+\s*(Tasks|タスク)", "Tasks section"),
    (r"^#+\s*(Completion Conditions|完了条件)", "Completion Conditions"),
    (r"(Go/No-Go|Go\/No-Go)", "Go/No-Go Checklist"),
    (r"^#+\s*(Review|レビュー)", "Review section"),
]

RECOMMENDED_SECTIONS = [
    (r"\*\*(Prerequisites|前提):\*\*", "Prerequisites"),
    (r"^#+\s*(Verification|検証)", "Verification Steps"),
    (r"Review 1:", "Review 1 (Code Review)"),
    (r"Review 2:", "Review 2 (Expert Review)"),
    (r"Review 3:", "Review 3 (Critical Review)"),
]


def _extract_section(content: str, heading_pattern: str) -> str:
    """Extract text from a heading match to the next heading of equal or higher level."""
    match = re.search(heading_pattern, content, re.MULTILINE)
    if not match:
        return ""
    start = match.start()
    level = content[start:].split("\n")[0].count("#")
    rest = content[match.end():]
    next_heading = re.search(rf"^#{{1,{level}}}\s", rest, re.MULTILINE)
    if next_heading:
        return content[start:match.end() + next_heading.start()]
    return content[start:]


def validate(filepath: str) -> tuple[list[str], list[str]]:
    """Return (errors, warnings) for a phase document."""
    path = Path(filepath)
    if not path.exists():
        return [f"File not found: {filepath}"], []

    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as e:
        return [f"File is not valid UTF-8: {filepath} ({e})"], []
    except OSError as e:
        return [f"Cannot read file: {filepath} ({e})"], []

    errors: list[str] = []
    warnings: list[str] = []

    for pattern, name in REQUIRED_SECTIONS:
        if not re.search(pattern, content, re.MULTILINE):
            errors.append(f"Missing required: {name}")

    for pattern, name in RECOMMENDED_SECTIONS:
        if not re.search(pattern, content, re.MULTILINE):
            warnings.append(f"Missing recommended: {name}")

    # Check completion conditions have checkboxes (scoped to section)
    cc_section = _extract_section(content, r"^#+\s*(Completion Conditions|完了条件)")
    if cc_section:
        if "- [ ]" not in cc_section and "- [x]" not in cc_section:
            errors.append("Completion Conditions has no checkboxes (- [ ] or - [x])")

    # Check Go/No-Go has table (scoped to section)
    gng_section = _extract_section(content, r"^#+\s*.*(Go/No-Go|Go\/No-Go)")
    if gng_section:
        has_table = any(marker in gng_section for marker in ["| Item", "| 項目", "|---", "| ---"])
        if not has_table:
            warnings.append("Go/No-Go section may not have a table format")

    return errors, warnings


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: validate_phase.py <phase-doc.md> [phase-doc2.md ...]")
        sys.exit(1)

    all_pass = True
    files_processed = 0
    for filepath in sys.argv[1:]:
        errors, warnings = validate(filepath)
        name = Path(filepath).name
        files_processed += 1

        if errors:
            all_pass = False
            print(f"❌ {name}")
            for e in errors:
                print(f"   ERROR: {e}")
        else:
            print(f"✅ {name}")

        for w in warnings:
            print(f"   WARN:  {w}")
        print()

    if files_processed == 0:
        print("ERROR: No files were validated.")
        sys.exit(1)

    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
