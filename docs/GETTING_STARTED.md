# 🚀 Getting Started - はじめに

このガイドでは、テンプレートのセットアップから最初のトレーニングまでを説明します。

## 📋 目次

1. [環境構築](#環境構築)
2. [基本的な使い方](#基本的な使い方)
3. [データ準備](#データ準備)
4. [トレーニング実行](#トレーニング実行)
5. [次のステップ](#次のステップ)

## 環境構築

### 前提条件

- Ubuntu 20.04+ / WSL2
- Python 3.11+
- CUDA 12.x（GPUを使用する場合）
- NVIDIA GPU（推奨: 8GB VRAM以上）

### ワンコマンドセットアップ

```bash
# リポジトリをクローン
git clone https://github.com/YOUR_USERNAME/LLamaFactory-Unsloth-template.git
cd LLamaFactory-Unsloth-template

# 環境構築スクリプトを実行
chmod +x setup.sh
./setup.sh
```

**所要時間**: 約5-10分

セットアップスクリプトは以下を自動的に実行します：
- システム要件チェック
- LLaMA-Factoryのクローン
- uv仮想環境の作成
- 依存関係のインストール（PyTorch, Unsloth等）
- インストールの検証

## 基本的な使い方

### Web UIで始める（推奨）

最も簡単な方法は、Web UIを使用することです。

```bash
cd LLaMA-Factory
source .venv/bin/activate
llamafactory-cli webui
```

ブラウザで `http://127.0.0.1:7860` が開きます。

#### Unslothを有効化

1. Web UIの上部にある **Booster** ドロップダウンを見つける
2. `unsloth` を選択
3. これだけで2倍高速なトレーニングが可能に！

#### モデルの選択

**RTX 4060 Ti 8GB向け推奨モデル:**
- `unsloth/llama-3.2-1b-bnb-4bit` - 最軽量・最速
- `unsloth/llama-3.2-3b-bnb-4bit` - バランス型（推奨）
- `unsloth/Phi-3.5-mini-instruct-bnb-4bit` - 高性能

### CLIで始める

設定ファイルを使用してCLIから実行することもできます。

```bash
cd LLaMA-Factory
source .venv/bin/activate

# SFTトレーニング
llamafactory-cli train ../configs/sft_config.yaml

# SimPOトレーニング
llamafactory-cli train ../configs/simpo_config.yaml
```

## データ準備

### 方法1: サンプルデータで試す

LLaMA-Factoryには多数のサンプルデータセットが含まれています。

```bash
# Web UIで
# Dataset: alpaca_en を選択
```

### 方法2: 合成データを作成

```bash
# 合成データディレクトリを作成
./setup_synthetic_data_dirs.sh

# SFT用データを生成
cd synthetic_data/generators
python sft_data_generator.py --num_samples 100

# データをLLaMA-Factoryにコピー
cp ../processed/sft_train.json ../../LLaMA-Factory/data/competition_sft/train.json
cp ../processed/sft_val.json ../../LLaMA-Factory/data/competition_sft/val.json
```

### 方法3: カスタムデータを用意

`LLaMA-Factory/data/your_dataset/` にデータを配置し、`dataset_info.json` を作成します。

```json
{
  "your_dataset": {
    "file_name": "train.json",
    "formatting": "alpaca",
    "columns": {
      "prompt": "instruction",
      "query": "input",
      "response": "output"
    }
  }
}
```

## トレーニング実行

### ステップ1: SFT（教師あり学習）

#### Web UIの場合

1. **Train** タブを開く
2. 設定：
   - Model name: `unsloth/llama-3.2-3b-bnb-4bit`
   - Finetuning type: `lora`
   - Quantization bit: `4`
   - Booster: `unsloth` ← **重要！**
   - Dataset: `competition_sft` または `alpaca_en`
3. **Start** をクリック

#### CLIの場合

```bash
cd LLaMA-Factory
source .venv/bin/activate
llamafactory-cli train ../configs/sft_config.yaml
```

### ステップ2: 選好学習（SimPO推奨）

SFTモデルをベースに、選好学習を実行します。

#### Web UIの場合

1. **Train** タブで設定：
   - Model name: `unsloth/llama-3.2-3b-bnb-4bit`
   - Checkpoint path: SFTで作成したチェックポイントを選択
   - Stage: `dpo`
   - Preference loss: `simpo` ← **推奨！**
   - Booster: `unsloth`
2. **Start** をクリック

#### CLIの場合

```bash
# configs/simpo_config.yaml を編集
# adapter_name_or_path: outputs/sft_model/checkpoint-best

llamafactory-cli train ../configs/simpo_config.yaml
```

### ステップ3: 評価と推論

```bash
# チャット形式で推論
llamafactory-cli chat ../configs/simpo_config.yaml

# または Web UIの Chat タブを使用
```

## 次のステップ

### さらに学ぶ

- **[Unslothガイド](UNSLOTH.md)** - Unslothの詳細な使い方
- **[選好学習ガイド](PREFERENCE_LEARNING_GUIDE.md)** - DPO, SimPO, ORPOの比較
- **[合成データワークフロー](SYNTHETIC_DATA_WORKFLOW.md)** - データ生成の詳細

### 実験を管理する

1. **設定ファイルを整理**
   ```bash
   cp configs/sft_config.yaml configs/exp001_baseline.yaml
   # 設定を編集
   ```

2. **実験結果を記録**
   - トレーニングログを保存
   - 評価結果を記録
   - ベストモデルを特定

3. **バージョン管理**
   ```bash
   git add configs/exp001_baseline.yaml
   git commit -m "Add baseline experiment config"
   ```

### トラブルシューティング

#### CUDA Out of Memory

```yaml
# より小さいモデルを使用
model_name_or_path: unsloth/llama-3.2-1b-bnb-4bit

# バッチサイズを減らす
per_device_train_batch_size: 1

# シーケンス長を減らす
cutoff_len: 1024
```

#### Unslothが動作しない

```bash
# Unslothの確認
python -c "import unsloth; print(unsloth.__version__)"

# 環境の再構築
rm -rf .venv uv.lock
./setup.sh
```

## 📚 詳細ドキュメント

- [CHECKLIST.md](CHECKLIST.md) - セットアップから提出までのチェックリスト
- [UNSLOTH.md](UNSLOTH.md) - Unslothの詳細ガイド
- [PREFERENCE_LEARNING_GUIDE.md](PREFERENCE_LEARNING_GUIDE.md) - 選好学習の詳細
- [SYNTHETIC_DATA_WORKFLOW.md](SYNTHETIC_DATA_WORKFLOW.md) - 合成データ作成

---

**これで準備完了です！高速なファインチューニングを楽しんでください！** 🚀
