---
name: spec-architect
description: >
  仕様書の徹底レビューと詳細設計書生成プラグイン。
  3つの並列エージェントで仕様書をレビューし（完全性・一貫性・実現可能性）、
  レビュー済み仕様書から詳細設計書を自動生成する。
  完成した設計書は project-orchestrator に連携可能。
  使用場面: 「仕様書をレビューしたい」「仕様書から設計書を作りたい」
  「仕様の抜け漏れをチェックしたい」「設計書を orchestrator に連携したい」
  「仕様書の一貫性を確認したい」「技術的実現可能性を評価したい」
  など、仕様書のレビューと詳細設計書の生成が必要な場面全般。
---

# 仕様書レビュー・詳細設計書生成

`/spec-architect` コマンドで開始。3つのモード:

- **REVIEW**: `/spec-architect review docs/spec.md` — 仕様書を徹底レビュー
- **DESIGN**: `/spec-architect design` — レビュー済み仕様書から詳細設計書を生成
- **HANDOFF**: `/spec-architect handoff` — 完成した設計書を orchestrator に連携

## 主要コンセプト

- **3観点並列レビュー**: 完全性・一貫性・実現可能性の3つの Explore エージェントで仕様書をレビュー
- **トリアージ**: レビュー指摘を Critical/High/Medium/Low に分類し、Critical/High が 0 件になるまで修正サイクル
- **設計書テンプレート**: 12セクションの詳細設計書テンプレートに基づいて構造化された設計書を生成
- **spec-analyst エージェント**: 仕様書分析と設計書生成を担当する専門エージェント
- **品質ゲート**: REVIEW → DESIGN → HANDOFF の各遷移に品質ゲートを設置
- **バリデーション**: `validate_design.py` で設計書の構造を自動検証
- **トレーサビリティ**: 仕様要件 → 設計セクションの対応を追跡
- **orchestrator 連携**: 完成した設計書からフェーズ分割を推奨し、`/orchestrate generate` に連携
- **プロジェクト管理**: `.claude/spec-architect/{NNN}-{slug}/` 配下にプロジェクトごとに独立管理
