# sphere-skills

Claude Code プラグインコレクション。

## インストール

```
# 1. マーケットプレースをカタログに登録
/plugin marketplace add SphereStacking/skills

# 2. プラグインをインストール
/plugin install project-orchestrator@sphere-skills
/plugin install spec-architect@sphere-skills
```

## プラグイン一覧

### [project-orchestrator](./plugins/project-orchestrator)

マルチフェーズプロジェクトオーケストレーター。

- Claude の Plan モードで計画を立て、`/orchestrate generate` でフェーズドキュメントに構造化
- `project-orchestrator:implementer` エージェントに実装を委譲
- 3エージェント並列レビュー + Go/No-Go ゲートでフェーズを管理
- `.claude/project-orchestrator/{NNN}-{slug}/` に複数プランを独立管理

**コマンド:**

```
/orchestrate generate         # 合意済みの計画をフェーズドキュメントに変換
/orchestrate execute phase 0  # フェーズ 0 を実行
/orchestrate continue         # 中断したフェーズを再開
```

### [spec-architect](./plugins/spec-architect)

仕様書レビュー・詳細設計書生成プラグイン。

- 3つの並列エージェント（完全性・一貫性・実現可能性）で仕様書を徹底レビュー
- レビュー済み仕様書から12セクションの詳細設計書を自動生成
- 品質ゲートで REVIEW → DESIGN → HANDOFF の遷移を管理
- 完成した設計書を `/orchestrate generate` に連携可能

**コマンド:**

```
/spec-architect review docs/spec.md  # 仕様書をレビュー
/spec-architect design               # 詳細設計書を生成
/spec-architect handoff              # orchestrator に連携
```

## ライセンス

MIT
