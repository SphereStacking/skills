#!/usr/bin/env python3
"""Validate design document structure: required sections, required fields,
traceability table, and Mermaid diagrams."""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Required sections — all must be present (error if missing)
REQUIRED_SECTIONS = [
    (r"^#+\s*(1\.\s*)?(概要|Overview)", "1. 概要"),
    (r"^#+\s*(2\.\s*)?(システムアーキテクチャ|System Architecture)", "2. システムアーキテクチャ"),
    (r"^#+\s*(3\.\s*)?(API\s*設計|API\s*Design)", "3. API 設計"),
    (r"^#+\s*(4\.\s*)?(DB\s*スキーマ設計|DB\s*Schema\s*Design)", "4. DB スキーマ設計"),
    (r"^#+\s*(5\.\s*)?(コンポーネント設計|Component\s*Design)", "5. コンポーネント設計"),
    (r"^#+\s*(6\.\s*)?(データフロー|Data\s*Flow)", "6. データフロー"),
    (r"^#+\s*(7\.\s*)?(ファイル構成|File\s*Structure)", "7. ファイル構成"),
    (r"^#+\s*(8\.\s*)?(エラーハンドリング|Error\s*Handling)", "8. エラーハンドリング"),
    (r"^#+\s*(9\.\s*)?(セキュリティ設計|Security\s*Design)", "9. セキュリティ設計"),
    (r"^#+\s*(10\.\s*)?(テスト戦略|Test\s*Strategy)", "10. テスト戦略"),
    (r"^#+\s*(11\.\s*)?(非機能要件|Non-Functional\s*Requirements)", "11. 非機能要件"),
    (r"^#+\s*(12\.\s*)?(仕様トレーサビリティ|Spec(?:ification)?\s*Traceability)", "12. 仕様トレーサビリティ"),
]

# Required fields — must be present somewhere in the document
REQUIRED_FIELDS = [
    (r"\*\*(目的|Purpose):\*\*", "目的"),
    (r"\*\*(スコープ|Scope):\*\*", "スコープ"),
]

# Recommended content — warn if missing
RECOMMENDED_CONTENT = [
    (r"\|\s*(メソッド|Method)\s*\|.*\|\s*(パス|Path)\s*\|", "API エンドポイントテーブル"),
    (r"\|\s*(カラム|Column)\s*\|.*\|\s*(型|Type)\s*\|", "DB テーブル定義テーブル"),
    (r"\|\s*(コード|Code)\s*\|.*\|\s*(HTTP|ステータス|Status)\s*\|", "エラーコード一覧テーブル"),
    (r"\|\s*(種別|Type)\s*\|.*\|\s*(対象|Target|ツール|Tool)\s*\|", "テスト種別テーブル"),
    (r"\|\s*(メトリクス|Metrics?)\s*\|.*\|\s*(目標|Target|Goal)\s*\|", "パフォーマンス目標テーブル"),
]


def validate(filepath: str) -> tuple[list[str], list[str]]:
    """Return (errors, warnings) for a design document."""
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

    # Check required sections
    for pattern, name in REQUIRED_SECTIONS:
        if not re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
            errors.append(f"Missing required section: {name}")

    # Check required fields
    for pattern, name in REQUIRED_FIELDS:
        if not re.search(pattern, content, re.MULTILINE):
            errors.append(f"Missing required field: {name}")

    # Check traceability table
    traceability_patterns = [
        r"\|\s*(要件\s*ID|Req(?:uirement)?\s*ID)\s*\|",
        r"\|\s*(要件|Requirement)\s*\|.*\|\s*(設計|Design)\s*\|",
    ]
    has_traceability = any(
        re.search(p, content, re.MULTILINE | re.IGNORECASE)
        for p in traceability_patterns
    )
    if not has_traceability:
        errors.append("Missing traceability table in 仕様トレーサビリティ section")

    # Check for at least one Mermaid diagram
    if "```mermaid" not in content:
        errors.append("No Mermaid diagram found (at least one ```mermaid block required)")

    # Check recommended content
    for pattern, name in RECOMMENDED_CONTENT:
        if not re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
            warnings.append(f"Missing recommended: {name}")

    return errors, warnings


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: validate_design.py <design-doc.md> [design-doc2.md ...]")
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
