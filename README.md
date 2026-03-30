# sphere-skills

Claude Code プラグインコレクション。

## インストール

```
/plugin marketplace add SphereStacking/skills
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

## ライセンス

MIT
