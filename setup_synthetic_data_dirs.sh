#!/bin/bash

################################################################################
# 合成データワークフロー用ディレクトリ構造作成スクリプト
#
# 使用方法:
#   chmod +x setup_synthetic_data_dirs.sh
#   ./setup_synthetic_data_dirs.sh
################################################################################

set -e

echo "🏗️  合成データワークフロー用ディレクトリを作成中..."
echo ""

# ベースディレクトリ（スクリプトの親ディレクトリ）
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$BASE_DIR"

# synthetic_data ディレクトリ構造を作成
mkdir -p synthetic_data/{generators,raw,processed,quality_check,notebooks}

echo "✅ synthetic_data/ ディレクトリを作成"

# LLaMA-Factory/data ディレクトリ構造を作成
mkdir -p LLaMA-Factory/data/{competition_sft,competition_dpo}

echo "✅ LLaMA-Factory/data/ ディレクトリを作成"

# configs ディレクトリを作成（まだない場合）
mkdir -p configs

echo "✅ configs/ ディレクトリを作成"

# scripts ディレクトリを作成（まだない場合）
mkdir -p scripts

echo "✅ scripts/ ディレクトリを作成"

echo ""
echo "📝 サンプルファイルを作成中..."
echo ""

# .gitkeep ファイルを作成（空ディレクトリをGitで追跡するため）
touch synthetic_data/raw/.gitkeep
touch synthetic_data/processed/.gitkeep

# README ファイルを作成
cat > synthetic_data/README.md << 'EOF'
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
EOF

echo "✅ synthetic_data/README.md を作成"

# dataset_info.json テンプレートを作成
cat > LLaMA-Factory/data/competition_sft/dataset_info.json << 'EOF'
{
  "competition_sft": {
    "file_name": "train.json",
    "formatting": "alpaca",
    "columns": {
      "prompt": "instruction",
      "query": "input",
      "response": "output"
    }
  }
}
EOF

echo "✅ LLaMA-Factory/data/competition_sft/dataset_info.json を作成"

cat > LLaMA-Factory/data/competition_dpo/dataset_info.json << 'EOF'
{
  "competition_dpo": {
    "file_name": "train.json",
    "formatting": "sharegpt",
    "ranking": true,
    "columns": {
      "messages": "conversations",
      "chosen": "conversations",
      "rejected": "rejected_conversations"
    }
  }
}
EOF

echo "✅ LLaMA-Factory/data/competition_dpo/dataset_info.json を作成"

echo ""
echo "✨ ディレクトリ構造の作成が完了しました！"
echo ""
echo "📁 作成されたディレクトリ:"
echo "  - synthetic_data/"
echo "    ├── generators/"
echo "    ├── raw/"
echo "    ├── processed/"
echo "    ├── quality_check/"
echo "    └── notebooks/"
echo "  - LLaMA-Factory/data/"
echo "    ├── competition_sft/"
echo "    └── competition_dpo/"
echo "  - configs/"
echo "  - scripts/"
echo ""
echo "🚀 次のステップ:"
echo "  1. synthetic_data/generators/ にデータ生成スクリプトを作成"
echo "  2. configs/ にSFT/DPO設定ファイルを作成"
echo "  3. SYNTHETIC_DATA_WORKFLOW.md を参照してワークフローを確認"
echo ""
