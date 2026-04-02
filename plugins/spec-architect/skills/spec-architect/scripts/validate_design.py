#!/usr/bin/env python3
"""Validate design document structure across section files in design/ directory.

Usage:
    validate_design.py <design-directory>
    validate_design.py <single-file.md>  (legacy: single file validation)

Exit codes:
    0: All required checks pass
    1: Required checks failed
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Section definitions: (filename, display_name, required_patterns, recommended_patterns)
SECTIONS = [
    (
        "01-overview.md",
        "1. 概要",
        [
            (r"\*\*(目的|Purpose):\*\*", "目的フィールド"),
            (r"\*\*(スコープ|Scope):\*\*", "スコープフィールド"),
        ],
        [],
    ),
    (
        "02-system-architecture.md",
        "2. システムアーキテクチャ",
        [
            (r"```mermaid", "Mermaid 図"),
        ],
        [],
    ),
    (
        "03-api-design.md",
        "3. API 設計",
        [],
        [
            (r"\|.*?(メソッド|Method).*?(パス|Path).*\|", "API エンドポイントテーブル"),
            (r"\|.*?(コード|Code).*?(HTTP|ステータス|Status).*\|", "エラーコード一覧テーブル"),
        ],
    ),
    (
        "04-db-schema.md",
        "4. DB スキーマ設計",
        [],
        [
            (r"\|.*?(カラム|Column).*?(型|Type).*\|", "DB テーブル定義テーブル"),
        ],
    ),
    (
        "05-component-design.md",
        "5. コンポーネント設計",
        [],
        [],
    ),
    (
        "06-data-flow.md",
        "6. データフロー",
        [],
        [],
    ),
    (
        "07-file-structure.md",
        "7. ファイル構成",
        [],
        [],
    ),
    (
        "08-error-handling.md",
        "8. エラーハンドリング",
        [],
        [],
    ),
    (
        "09-security.md",
        "9. セキュリティ設計",
        [],
        [],
    ),
    (
        "10-test-strategy.md",
        "10. テスト戦略",
        [],
        [
            (r"\|.*?(種別|Type).*?(対象|Target|ツール|Tool).*\|", "テスト種別テーブル"),
        ],
    ),
    (
        "11-non-functional.md",
        "11. 非機能要件",
        [],
        [
            (r"\|.*?(メトリクス|Metrics?).*?(目標|Target|Goal).*\|", "パフォーマンス目標テーブル"),
        ],
    ),
    (
        "12-traceability.md",
        "12. 仕様トレーサビリティ",
        [
            (
                r"\|\s*(要件\s*ID|Req(?:uirement)?\s*ID|要件|Requirement)\s*\|",
                "トレーサビリティテーブル",
            ),
        ],
        [],
    ),
]


def validate_directory(design_dir: Path) -> tuple[list[str], list[str]]:
    """Validate a design/ directory with section files."""
    errors: list[str] = []
    warnings: list[str] = []

    has_any_mermaid = False

    for filename, display_name, required, recommended in SECTIONS:
        filepath = design_dir / filename
        if not filepath.is_file():
            errors.append(f"Missing section file: {filename} ({display_name})")
            continue

        try:
            content = filepath.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as e:
            errors.append(f"Cannot read {filename}: {e}")
            continue

        # Check if file has meaningful content (not just template placeholders)
        lines = [
            line
            for line in content.strip().split("\n")
            if line.strip()
            and not line.strip().startswith("#")
            and not line.strip().startswith("<!--")
            and not line.strip().startswith("-->")
        ]
        if len(lines) < 2:
            errors.append(f"{filename}: Content is empty or only placeholders")
            continue

        # Check required patterns for this section
        for pattern, name in required:
            if not re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
                errors.append(f"{filename}: Missing required: {name}")

        # Check recommended patterns for this section
        for pattern, name in recommended:
            if not re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
                warnings.append(f"{filename}: Missing recommended: {name}")

        # Track mermaid presence
        if "```mermaid" in content:
            has_any_mermaid = True

    if not has_any_mermaid:
        errors.append("No Mermaid diagram found in any section (at least one required)")

    return errors, warnings


def validate_single_file(filepath: Path) -> tuple[list[str], list[str]]:
    """Legacy: validate a single design.md file."""
    if not filepath.is_file():
        return [f"Not a regular file or does not exist: {filepath}"], []

    try:
        content = filepath.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError) as e:
        return [f"Cannot read file: {filepath} ({e})"], []

    errors: list[str] = []
    warnings: list[str] = []

    # Check all sections exist in single file
    section_patterns = [
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
    for pattern, name in section_patterns:
        if not re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
            errors.append(f"Missing required section: {name}")

    for pattern, name in [
        (r"\*\*(目的|Purpose):\*\*", "目的"),
        (r"\*\*(スコープ|Scope):\*\*", "スコープ"),
    ]:
        if not re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
            errors.append(f"Missing required field: {name}")

    traceability_patterns = [
        r"\|\s*(要件\s*ID|Req(?:uirement)?\s*ID)\s*\|",
        r"\|\s*(要件|Requirement)\s*\|.*\|\s*(設計|Design)\s*\|",
    ]
    if not any(re.search(p, content, re.MULTILINE | re.IGNORECASE) for p in traceability_patterns):
        errors.append("Missing traceability table")

    if "```mermaid" not in content:
        errors.append("No Mermaid diagram found (at least one required)")

    recommended = [
        (r"\|.*?(メソッド|Method).*?(パス|Path).*\|", "API エンドポイントテーブル"),
        (r"\|.*?(カラム|Column).*?(型|Type).*\|", "DB テーブル定義テーブル"),
        (r"\|.*?(コード|Code).*?(HTTP|ステータス|Status).*\|", "エラーコード一覧テーブル"),
        (r"\|.*?(種別|Type).*?(対象|Target|ツール|Tool).*\|", "テスト種別テーブル"),
        (r"\|.*?(メトリクス|Metrics?).*?(目標|Target|Goal).*\|", "パフォーマンス目標テーブル"),
    ]
    for pattern, name in recommended:
        if not re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
            warnings.append(f"Missing recommended: {name}")

    return errors, warnings


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: validate_design.py <design-directory-or-file>")
        sys.exit(1)

    target = Path(sys.argv[1])

    if target.is_dir():
        errors, warnings = validate_directory(target)
        label = f"design/ ({target})"
    elif target.is_file():
        errors, warnings = validate_single_file(target)
        label = target.name
    else:
        print(f"ERROR: {target} is not a file or directory")
        sys.exit(1)

    # Output
    if errors:
        print(f"❌ {label}")
        for e in errors:
            print(f"   ERROR: {e}")
    else:
        print(f"✅ {label}")

    for w in warnings:
        print(f"   WARN:  {w}")

    print()
    print(f"Errors: {len(errors)}  Warnings: {len(warnings)}")
    sys.exit(0 if not errors else 1)


if __name__ == "__main__":
    main()
