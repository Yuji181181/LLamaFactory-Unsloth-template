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
git clone git@github.com:Yuji181181/LLamaFactory-Unsloth-template.git
cd LLamaFactory-Unsloth-template
```

### 2. 環境構築

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

### 3. アクティベート

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

---

## ディレクトリ構成

```text
/home/haseg/GitHub/LLamaFactory-Unsloth-template/
├── LLaMA-Factory/        (LLaMA-Factory本体)
│   └── data/             <-- 2. 合成データセット配置場所 (.json / .jsonl)
│       └── dataset_info.json  <-- データセット登録用ファイル
├── models/               <-- 3. 事前学習済み モデル配置場所
├── scripts/              <-- 1. 合成データ生成プログラム配置場所
└── setup.sh              
```

### 1. 合成データ生成プログラム
- **配置場所**: `scripts/` ディレクトリ
- ここにデータ作成用のPythonスクリプトなどを配置します。

### 2. 作成した合成データ
- **配置場所**: `LLaMA-Factory/data/` ディレクトリ
- 生成したデータ（例: `my_synth_data.json`）はここに移動または保存します。
- 保存後、同ディレクトリ内の `dataset_info.json` にデータセット情報を登録する必要があります。

### 3. 事前学習済みモデル
- **配置場所**: `models/` ディレクトリ
- UnslothやHugging Faceからダウンロードしたモデルフォルダをここに配置します。
- Web UIの "Model path" には、このディレクトリ内の各モデルフォルダの絶対パス（例: `/home/haseg/GitHub/LLamaFactory-Unsloth-template/models/Llama-3-8B-Unsloth`）を指定します。