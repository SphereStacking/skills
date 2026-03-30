#!/usr/bin/env python3
"""Validate that a phase document contains all required sections."""

import re
import sys
from pathlib import Path

# Patterns support both English and Japanese phase docs
REQUIRED_SECTIONS = [
    (r"^#+\s*(Phase\s+\d+|フェーズ\s*\d+)", "Phase header"),
    (r"\*\*(Objective|目的):\*\*", "Objective"),
    (r"\*\*(Status|ステータス):\*\*", "Status"),
    (r"\*\*(Risk Level|Risk|リスク):\*\*", "Risk Level"),
    (r"\*\*(Rollback|ロールバック):\*\*", "Rollback"),
    (r"^#+\s*.*(Tasks|タスク|対象|修正|新規|一覧|作業|コンポーネント|ページ|テスト|フロー|環境変数|API)", "Tasks section"),
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


def validate(filepath: str) -> tuple[list[str], list[str]]:
    """Return (errors, warnings) for a phase document."""
    path = Path(filepath)
    if not path.exists():
        return [f"File not found: {filepath}"], []

    content = path.read_text(encoding="utf-8")
    errors = []
    warnings = []

    for pattern, name in REQUIRED_SECTIONS:
        if not re.search(pattern, content, re.MULTILINE):
            errors.append(f"Missing required: {name}")

    for pattern, name in RECOMMENDED_SECTIONS:
        if not re.search(pattern, content, re.MULTILINE):
            warnings.append(f"Missing recommended: {name}")

    # Check completion conditions have checkboxes
    if "- [ ]" not in content and "- [x]" not in content:
        errors.append("Completion Conditions has no checkboxes (- [ ] or - [x])")

    # Check Go/No-Go has table (English or Japanese headers)
    has_table = any(marker in content for marker in ["| Item", "| 項目", "|---", "| ---"])
    if not has_table:
        warnings.append("Go/No-Go section may not have a table format")

    return errors, warnings


def main():
    if len(sys.argv) < 2:
        print("Usage: validate_phase.py <phase-doc.md> [phase-doc2.md ...]")
        sys.exit(1)

    all_pass = True
    for filepath in sys.argv[1:]:
        errors, warnings = validate(filepath)
        name = Path(filepath).name

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

    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
