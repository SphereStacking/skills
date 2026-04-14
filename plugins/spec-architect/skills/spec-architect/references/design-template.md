# 詳細設計書テンプレート

設計書は12セクションの独立した md ファイルで構成される。各セクションのテンプレートは `design-sections/` 配下にある。

## 出力構造

```
.claude/works/{NNN}-{slug}/design/
├── 00-index.md              ← 全体目次（自動生成）
├── 01-overview.md
├── 02-system-architecture.md
├── 03-api-design.md
├── 04-db-schema.md
├── 05-component-design.md
├── 06-data-flow.md
├── 07-file-structure.md
├── 08-error-handling.md
├── 09-security.md
├── 10-test-strategy.md
├── 11-non-functional.md
└── 12-traceability.md
```

## セクション一覧

| # | ファイル | セクション名 | テンプレート | 主な内容 |
|---|---------|------------|-----------|---------|
| 1 | `01-overview.md` | 概要 | `design-sections/01-overview.md` | 目的、スコープ、前提条件、用語定義 |
| 2 | `02-system-architecture.md` | システムアーキテクチャ | `design-sections/02-system-architecture.md` | 技術スタック、全体構成図、レイヤー構成 |
| 3 | `03-api-design.md` | API 設計 | `design-sections/03-api-design.md` | エンドポイント、認証、リクエスト/レスポンス、エラーコード |
| 4 | `04-db-schema.md` | DB スキーマ設計 | `design-sections/04-db-schema.md` | ER 図、テーブル定義、インデックス、マイグレーション |
| 5 | `05-component-design.md` | コンポーネント設計 | `design-sections/05-component-design.md` | コンポーネント一覧、インターフェース、依存関係図 |
| 6 | `06-data-flow.md` | データフロー | `design-sections/06-data-flow.md` | ユースケース別シーケンス図 |
| 7 | `07-file-structure.md` | ファイル構成 | `design-sections/07-file-structure.md` | ディレクトリツリー、命名規則 |
| 8 | `08-error-handling.md` | エラーハンドリング | `design-sections/08-error-handling.md` | エラー分類、リトライ、フォールバック |
| 9 | `09-security.md` | セキュリティ設計 | `design-sections/09-security.md` | 認証/認可フロー、バリデーション、データ保護 |
| 10 | `10-test-strategy.md` | テスト戦略 | `design-sections/10-test-strategy.md` | テスト種別、テストデータ、実行方針 |
| 11 | `11-non-functional.md` | 非機能要件 | `design-sections/11-non-functional.md` | パフォーマンス、スケーラビリティ、監視 |
| 12 | `12-traceability.md` | 仕様トレーサビリティ | `design-sections/12-traceability.md` | 要件→設計の対応表、カバレッジ |

## 00-index.md テンプレート

```markdown
# {プロジェクト名} 詳細設計書

**生成日:** {日時}
**仕様書:** {仕様書パス}

## セクション一覧

| # | セクション | ステータス | 概要 |
|---|-----------|----------|------|
| 1 | [概要](./01-overview.md) | {生成済/未生成} | {一行サマリー} |
| 2 | [システムアーキテクチャ](./02-system-architecture.md) | {生成済/未生成} | {一行サマリー} |
| 3 | [API 設計](./03-api-design.md) | {生成済/未生成} | {一行サマリー} |
| 4 | [DB スキーマ設計](./04-db-schema.md) | {生成済/未生成} | {一行サマリー} |
| 5 | [コンポーネント設計](./05-component-design.md) | {生成済/未生成} | {一行サマリー} |
| 6 | [データフロー](./06-data-flow.md) | {生成済/未生成} | {一行サマリー} |
| 7 | [ファイル構成](./07-file-structure.md) | {生成済/未生成} | {一行サマリー} |
| 8 | [エラーハンドリング](./08-error-handling.md) | {生成済/未生成} | {一行サマリー} |
| 9 | [セキュリティ設計](./09-security.md) | {生成済/未生成} | {一行サマリー} |
| 10 | [テスト戦略](./10-test-strategy.md) | {生成済/未生成} | {一行サマリー} |
| 11 | [非機能要件](./11-non-functional.md) | {生成済/未生成} | {一行サマリー} |
| 12 | [仕様トレーサビリティ](./12-traceability.md) | {生成済/未生成} | {一行サマリー} |
```

## ルール

- 全12セクションが必須。該当しないセクションは「該当なし」と理由を記載する
- `{プレースホルダ}` を全て実際の内容で埋める
- 各セクションファイルは独立して読めるように、必要なコンテキストを含める
- セクション間で参照が必要な場合は相対リンク（例: `[コンポーネント設計](./05-component-design.md)`）を使う
