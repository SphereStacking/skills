# 4. DB スキーマ設計

**ER 図:**

```mermaid
erDiagram
    {ENTITY_A} ||--o{ {ENTITY_B} : "{関係}"
    {ENTITY_A} {
        {type} {column_name} PK "{説明}"
        {type} {column_name} "{説明}"
    }
    {ENTITY_B} {
        {type} {column_name} PK "{説明}"
        {type} {column_name} FK "{説明}"
    }
```

**テーブル定義:**

## {テーブル名}

| カラム | 型 | NULL | デフォルト | 説明 |
|--------|-----|------|----------|------|
| {id} | {UUID} | NO | {gen_random_uuid()} | {主キー} |
| {name} | {VARCHAR(255)} | NO | | {説明} |
| {created_at} | {TIMESTAMP} | NO | {NOW()} | {作成日時} |

**インデックス:**

| テーブル | インデックス名 | カラム | 種別 | 用途 |
|---------|--------------|--------|------|------|
| {テーブル名} | {idx_name} | {columns} | {UNIQUE/BTREE/GIN} | {用途} |

**マイグレーション方針:** {新規作成 / 既存テーブルの変更手順 / ダウンタイム有無}

<!-- ガイドライン: ER 図は全テーブルの関係を Mermaid で表現。テーブル定義は全カラムを網羅。インデックスはクエリパターンに基づいて設計 -->
