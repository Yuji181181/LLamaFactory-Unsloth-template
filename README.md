# 🦙 LLaMA-Factory + Unsloth テンプレート

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![CUDA](https://img.shields.io/badge/CUDA-12.x-green.svg)](https://developer.nvidia.com/cuda-toolkit)

LLMコンペティション用のテンプレートリポジトリです。**LLaMA-Factory**と**Unsloth**を組み合わせて、高速かつ効率的にLLMのファインチューニングを行えます。

## ✨ 特徴

- 🚀 **2倍高速なトレーニング** - Unslothによる最適化
- 💾 **省メモリ** - 4bit量子化で8GBのVRAMでも大規模モデルを扱える
- 🎨 **使いやすいWeb UI** - GradioベースのGUI
- 📦 **ワンコマンドセットアップ** - 環境構築が数分で完了
- ⚡ **高速推論** - Flash Attention 2自動有効化
- 🔧 **複数の選好学習手法** - DPO, SimPO, ORPO対応

## 🎯 対応手法

- **SFT** (Supervised Fine-Tuning) - 教師あり学習
- **DPO** (Direct Preference Optimization) - 選好最適化
- **SimPO** (Simple Preference Optimization) - 参照モデル不要の選好最適化 ⭐推奨
- **ORPO** (Odds Ratio Preference Optimization) - 参照モデル不要

## 📋 必要な環境

- **OS**: Ubuntu 20.04+ / WSL2
- **Python**: 3.11以上
- **CUDA**: 12.x（GPUを使用する場合）
- **GPU**: NVIDIA GPU（推奨: 8GB VRAM以上）
- **uv**: Pythonパッケージマネージャー（自動インストール可能）

## 🚀 クイックスタート

### 1. リポジトリをクローン

```bash
git clone https://github.com/YOUR_USERNAME/LLamaFactory-Unsloth-template.git
cd LLamaFactory-Unsloth-template
```

### 2. 環境構築（ワンコマンド）

```bash
chmod +x setup.sh
./setup.sh
```

これで以下がインストールされます：
- LLaMA-Factory（最新版）
- Unsloth（2026.1.2+）
- PyTorch（CUDA対応）
- その他120+の依存パッケージ

**所要時間**: 約5-10分

### 3. 環境のアクティベート

```bash
cd LLaMA-Factory
source .venv/bin/activate
```

### 4. Web UIの起動

```bash
llamafactory-cli webui
```

ブラウザで `http://127.0.0.1:7860` が自動的に開きます。

### 5. Unslothを有効化

Web UIの上部にある **Booster** ドロップダウンで `unsloth` を選択してください。

これだけで、**2倍高速なトレーニング**が可能になります！🎉

## 📚 ドキュメント

詳細なガイドは `docs/` ディレクトリにあります：

- **[Getting Started](docs/GETTING_STARTED.md)** - 環境構築から最初のトレーニングまで
- **[Unslothガイド](docs/UNSLOTH.md)** - Unslothの使い方（Web UI & コード）
- **[選好学習ガイド](docs/PREFERENCE_LEARNING_GUIDE.md)** - DPO, SimPO, ORPOの比較と使い方
- **[合成データワークフロー](docs/SYNTHETIC_DATA_WORKFLOW.md)** - データ生成からトレーニングまで
- **[チェックリスト](docs/CHECKLIST.md)** - セットアップから提出までの完全チェックリスト

## 🏆 コンペティションでの典型的なワークフロー

### ステップ1: データ準備

```bash
# 合成データディレクトリを作成
./setup_synthetic_data_dirs.sh

# SFT用データを生成
cd synthetic_data/generators
python sft_data_generator.py --num_samples 1000

# データをLLaMA-Factoryにコピー
cp ../processed/sft_train.json ../../LLaMA-Factory/data/competition_sft/train.json
cp ../processed/sft_val.json ../../LLaMA-Factory/data/competition_sft/val.json
```

### ステップ2: SFTトレーニング

```bash
cd ../../LLaMA-Factory
source .venv/bin/activate
llamafactory-cli train ../configs/sft_config.yaml
```

### ステップ3: 選好学習（SimPO推奨）

```bash
# SimPOでトレーニング
llamafactory-cli train ../configs/simpo_config.yaml
```

### ステップ4: 評価と提出

```bash
# モデルの評価
llamafactory-cli eval ../configs/simpo_config.yaml

# 推論
llamafactory-cli chat ../configs/simpo_config.yaml
```

## 📁 ディレクトリ構造

```
LLamaFactory-Unsloth-template/
├── README.md                      # このファイル
├── setup.sh                       # 環境構築スクリプト
├── setup_synthetic_data_dirs.sh   # 合成データディレクトリ作成
│
├── docs/                          # ドキュメント
│   ├── QUICKSTART_UNSLOTH.md
│   ├── CHECKLIST.md
│   ├── TEMPLATE_USAGE.md
│   ├── SYNTHETIC_DATA_WORKFLOW.md
│   ├── PREFERENCE_LEARNING_GUIDE.md
│   ├── UNSLOTH_GUIDE.md
│   └── UNSLOTH_WEBUI_GUIDE.md
│
├── configs/                       # 設定ファイルテンプレート
│   ├── sft_config.yaml           # SFT設定
│   ├── dpo_config.yaml           # DPO設定
│   └── simpo_config.yaml         # SimPO設定（推奨）
│
├── synthetic_data/                # 合成データ作成用
│   ├── generators/               # データ生成スクリプト
│   ├── quality_check/            # 品質チェック
│   ├── raw/                      # 生データ
│   ├── processed/                # 処理済みデータ
│   └── notebooks/                # 分析用ノートブック
│
└── data/                         # データセット配置用
```

## 🔧 推奨設定

### RTX 4060 Ti 8GB の場合

**推奨モデル:**
- `unsloth/llama-3.2-1b-bnb-4bit` - 最軽量・最速
- `unsloth/llama-3.2-3b-bnb-4bit` - バランス型 ⭐推奨
- `unsloth/Phi-3.5-mini-instruct-bnb-4bit` - 高性能

**推奨手法:**
1. **SFT** → **SimPO** - 参照モデル不要でメモリ効率◎
2. **SFT** → **ORPO** - SFTとアライメントを統合

### より大きいVRAM（16GB+）の場合

**推奨モデル:**
- `unsloth/Meta-Llama-3.1-8B-bnb-4bit` - 8Bモデル

**推奨手法:**
- すべての手法（DPO, SimPO, ORPO）を試して比較

## 🛠️ トラブルシューティング

### CUDA Out of Memory

```bash
# より小さいモデルを使用
model_name_or_path: unsloth/llama-3.2-1b-bnb-4bit

# バッチサイズを減らす
per_device_train_batch_size: 1

# シーケンス長を減らす
cutoff_len: 1024
```

### 環境の再構築

```bash
# 仮想環境を削除
rm -rf LLaMA-Factory/.venv LLaMA-Factory/uv.lock

# セットアップを再実行
./setup.sh
```

## 📊 ベンチマーク

### トレーニング速度（RTX 4060 Ti 8GB）

| モデル | 通常 | Unsloth | 高速化率 |
|--------|------|---------|----------|
| Llama 3.2 1B | 100% | 210% | 2.1x |
| Llama 3.2 3B | 100% | 195% | 1.95x |

### メモリ使用量

| モデル | 通常（16bit） | 4bit量子化 | 削減率 |
|--------|---------------|------------|--------|
| Llama 3.2 3B | ~12GB | ~3GB | 75% |
| Llama 3.2 1B | ~4GB | ~1GB | 75% |

## 🤝 コントリビューション

改善提案やバグ報告は、IssueまたはPull Requestでお願いします。

## 📄 ライセンス

このテンプレートはApache 2.0ライセンスの下で公開されています。

- LLaMA-Factory: Apache 2.0
- Unsloth: Apache 2.0

## 🙏 謝辞

- [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) - 統合ファインチューニングフレームワーク
- [Unsloth](https://github.com/unslothai/unsloth) - 高速化ライブラリ
- [uv](https://github.com/astral-sh/uv) - 高速Pythonパッケージマネージャー

## 📞 サポート

質問や問題がある場合：
1. [ドキュメント](docs/)を確認
2. [Issues](../../issues)で既存の問題を検索
3. 新しいIssueを作成

---

**Happy Fine-tuning! 🦥⚡**

Made with ❤️ for LLM Competitions
