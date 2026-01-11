# 合成データ作成とトレーニングのディレクトリ構造

## 📁 推奨ディレクトリ構造

```
your-competition-repo/
│
├── synthetic_data/                    # 合成データ作成用ディレクトリ
│   ├── generators/                    # データ生成スクリプト
│   │   ├── sft_data_generator.py     # SFT用データ生成
│   │   ├── dpo_data_generator.py     # DPO用データ生成
│   │   ├── prompt_templates.py       # プロンプトテンプレート
│   │   └── utils.py                  # ユーティリティ関数
│   │
│   ├── raw/                           # 生成された生データ
│   │   ├── sft_raw.jsonl             # SFT生データ
│   │   └── dpo_raw.jsonl             # DPO生データ
│   │
│   ├── processed/                     # 前処理済みデータ
│   │   ├── sft_train.json            # SFTトレーニングデータ
│   │   ├── sft_val.json              # SFT検証データ
│   │   ├── dpo_train.json            # DPOトレーニングデータ
│   │   └── dpo_val.json              # DPO検証データ
│   │
│   ├── quality_check/                 # 品質チェック用
│   │   ├── check_sft_data.py         # SFTデータ品質チェック
│   │   ├── check_dpo_data.py         # DPOデータ品質チェック
│   │   └── statistics.py             # データ統計
│   │
│   └── notebooks/                     # データ分析用ノートブック
│       ├── explore_sft_data.ipynb
│       └── explore_dpo_data.ipynb
│
├── LLaMA-Factory/
│   ├── data/                          # LLaMA-Factoryのデータディレクトリ
│   │   ├── competition_sft/          # SFT用データセット
│   │   │   ├── dataset_info.json
│   │   │   ├── train.json            # synthetic_data/processed/ からコピー
│   │   │   └── val.json
│   │   │
│   │   └── competition_dpo/          # DPO用データセット
│   │       ├── dataset_info.json
│   │       ├── train.json
│   │       └── val.json
│   │
│   └── outputs/                       # トレーニング出力
│       ├── sft_model/                # SFTモデル
│       └── dpo_model/                # DPOモデル
│
├── configs/                           # 設定ファイル
│   ├── sft_config.yaml               # SFTトレーニング設定
│   └── dpo_config.yaml               # DPOトレーニング設定
│
└── scripts/                           # ワークフロースクリプト
    ├── 01_generate_sft_data.sh       # SFTデータ生成
    ├── 02_train_sft.sh               # SFTトレーニング
    ├── 03_generate_dpo_data.sh       # DPOデータ生成
    └── 04_train_dpo.sh               # DPOトレーニング
```

## 🎯 ワークフローの説明

### ステップ1: SFT用合成データ生成
```bash
# synthetic_data/generators/ でデータ生成
python synthetic_data/generators/sft_data_generator.py

# 生成されたデータを確認
python synthetic_data/quality_check/check_sft_data.py

# LLaMA-Factoryのデータディレクトリにコピー
cp synthetic_data/processed/sft_train.json LLaMA-Factory/data/competition_sft/train.json
cp synthetic_data/processed/sft_val.json LLaMA-Factory/data/competition_sft/val.json
```

### ステップ2: SFTトレーニング
```bash
cd LLaMA-Factory
source .venv/bin/activate
llamafactory-cli train ../configs/sft_config.yaml
```

### ステップ3: DPO用合成データ生成
```bash
# SFTモデルを使ってDPO用のペアデータを生成
python synthetic_data/generators/dpo_data_generator.py \
    --sft_model LLaMA-Factory/outputs/sft_model/checkpoint-best

# LLaMA-Factoryのデータディレクトリにコピー
cp synthetic_data/processed/dpo_train.json LLaMA-Factory/data/competition_dpo/train.json
cp synthetic_data/processed/dpo_val.json LLaMA-Factory/data/competition_dpo/val.json
```

### ステップ4: DPOトレーニング
```bash
cd LLaMA-Factory
source .venv/bin/activate
llamafactory-cli train ../configs/dpo_config.yaml
```

## 📝 データフォーマット

### SFT用データフォーマット（train.json）
```json
[
  {
    "instruction": "質問やタスクの指示",
    "input": "追加のコンテキスト（オプション）",
    "output": "期待される回答"
  },
  {
    "instruction": "別の質問",
    "input": "",
    "output": "別の回答"
  }
]
```

### DPO用データフォーマット（train.json）
```json
[
  {
    "instruction": "質問やタスクの指示",
    "input": "追加のコンテキスト（オプション）",
    "output": [
      "好ましい回答（chosen）",
      "好ましくない回答（rejected）"
    ]
  }
]
```

または、LLaMA-Factory形式:
```json
[
  {
    "conversations": [
      {
        "from": "human",
        "value": "質問"
      },
      {
        "from": "gpt",
        "value": "好ましい回答"
      }
    ],
    "rejected_conversations": [
      {
        "from": "human",
        "value": "質問"
      },
      {
        "from": "gpt",
        "value": "好ましくない回答"
      }
    ]
  }
]
```

## 🔧 dataset_info.json の設定

### SFT用（LLaMA-Factory/data/competition_sft/dataset_info.json）
```json
{
  "competition_sft": {
    "file_name": "train.json",
    "formatting": "alpaca",
    "columns": {
      "prompt": "instruction",
      "query": "input",
      "response": "output"
    },
    "tags": {
      "role_tag": "role",
      "content_tag": "content",
      "user_tag": "user",
      "assistant_tag": "assistant"
    }
  }
}
```

### DPO用（LLaMA-Factory/data/competition_dpo/dataset_info.json）
```json
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
```

## 💡 なぜこの構造が良いのか

### 1. 分離された合成データディレクトリ
- **`synthetic_data/`** は独立しているため、バージョン管理しやすい
- データ生成ロジックとトレーニングを分離
- 複数の実験で同じデータを再利用可能

### 2. 段階的なワークフロー
- 生データ → 前処理 → LLaMA-Factoryへコピー
- 各段階で品質チェック可能
- 問題があれば該当ステップから再実行

### 3. 品質管理
- `quality_check/` でデータの統計や異常を検出
- ノートブックでデータを可視化・分析

### 4. 再現性
- すべてのステップがスクリプト化
- 設定ファイルで管理
- Gitで追跡可能

## 🚀 次のステップ

このディレクトリ構造を作成するスクリプトを用意しましょうか？
または、サンプルのデータ生成スクリプトを作成しますか？
