# 合成データディレクトリ

このディレクトリには、LLMコンペ用の合成データ生成スクリプトと生成されたデータが含まれます。

## ディレクトリ構造

- `generators/` - データ生成スクリプト
- `raw/` - 生成された生データ
- `processed/` - 前処理済みデータ
- `quality_check/` - 品質チェックスクリプト
- `notebooks/` - データ分析用ノートブック

## ワークフロー

1. `generators/` でデータを生成
2. `quality_check/` で品質を確認
3. `processed/` に前処理済みデータを保存
4. `LLaMA-Factory/data/` にコピーしてトレーニング

詳細は `SYNTHETIC_DATA_WORKFLOW.md` を参照してください。
