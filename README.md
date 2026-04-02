# sphere-skills

Claude Code プラグインコレクション。

## インストール

```
# 1. マーケットプレースをカタログに登録
/plugin marketplace add SphereStacking/skills

# 2. プラグインをインストール
/plugin install spec-refiner@sphere-skills
/plugin install spec-architect@sphere-skills
/plugin install project-orchestrator@sphere-skills
```

## パイプライン

```
spec-refiner (START→CONTINUE) → spec-architect (REVIEW→DESIGN→HANDOFF) → project-orchestrator (GENERATE→EXECUTE)
   ヒアリング・言語化            仕様レビュー・設計書生成               フェーズ実行・管理
```

## プラグイン一覧

### [spec-refiner](./plugins/spec-refiner)

ヒアリング・言語化プラグイン。

- ユーザーの「やりたいこと」を対話で徹底的にヒアリングし、言語化する
- 完成度や整合性は求めない（それは spec-architect の役割）
- ユーザーが明確に終了を告げるまでひたすら聞き続ける
- コードベース分析で技術的コンテキストをバックグラウンド取得
- ヒアリング記録を `/spec-architect review` にそのまま連携

**コマンド:**

```
/spec-refiner start "認証システム"  # 新しいヒアリングを開始
/spec-refiner continue              # 既存のヒアリングを再開
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

## ライセンス

MIT
