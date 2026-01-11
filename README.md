# LLaMA-Factory + Unsloth テンプレート

**LLaMA-Factory**と**Unsloth**を組み合わせた高速でLLMのファインチューニングを行えるテンプレート


## 環境

- **OS**: Ubuntu 20.04+ / WSL2
- **Python**: 3.11以上
- **CUDA**: 12.x
- **GPU**: NVIDIA GPU
- **uv**: Pythonパッケージマネージャー

## クイックスタート

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

これだけで、**2倍高速なトレーニング**が可能になります！

## ディレクトリ構造

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