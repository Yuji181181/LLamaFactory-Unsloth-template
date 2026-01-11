# 🦥 Unsloth完全ガイド

Unslothは、LLMのファインチューニングと推論を高速化するライブラリです。このガイドでは、Unslothの使い方を詳しく説明します。

## 📋 目次

1. [Unslothとは](#unslothとは)
2. [Web UIでの使用](#web-uiでの使用)
3. [コードでの使用](#コードでの使用)
4. [推奨設定](#推奨設定)
5. [トラブルシューティング](#トラブルシューティング)

## Unslothとは

### 特徴

- 🚀 **2倍高速なトレーニング** - 従来の方法と比較して2倍高速
- 💾 **メモリ効率** - 4bit量子化により少ないVRAMで大きなモデルを扱える
- ⚡ **高速推論** - 最適化された推論エンジン
- 🔧 **簡単な統合** - LLaMA-Factoryと完全統合

### 対応モデル

Unslothは以下のモデルファミリーをサポートしています：
- Llama (3, 3.1, 3.2)
- Mistral
- Qwen
- Phi
- Gemma
- その他多数

## Web UIでの使用

### 基本的な使い方

#### 1. Web UIを起動

```bash
cd LLaMA-Factory
source .venv/bin/activate
llamafactory-cli webui
```

ブラウザで `http://127.0.0.1:7860` が開きます。

#### 2. Boosterで「unsloth」を選択

Web UIの上部にある **Booster** ドロップダウンで `unsloth` を選択してください。

```
Booster: [unsloth ▼]
```

**これだけでUnslothが有効になります！**

### トレーニング設定（Trainタブ）

#### 推奨設定（RTX 4060 Ti 8GB）

**基本設定:**
- **Model name**: `unsloth/llama-3.2-3b-bnb-4bit`
- **Finetuning type**: `lora`
- **Quantization bit**: `4`
- **Quantization method**: `bnb`
- **Booster**: `unsloth` ← **重要！**

**LoRA設定:**
- **LoRA rank**: `32`
- **LoRA alpha**: `32`
- **LoRA target**: `all`

**トレーニングパラメータ:**
- **Learning rate**: `2e-4`
- **Epochs**: `3`
- **Batch size**: `2`
- **Gradient accumulation**: `8`
- **Max length**: `2048`

### チャット設定（Chatタブ）

**基本設定:**
- **Model name**: トレーニング済みモデル
- **Finetuning type**: `lora`
- **Checkpoint path**: トレーニング済みチェックポイント
- **Booster**: `unsloth` ← **重要！**

**生成パラメータ:**
- **Temperature**: `0.7`
- **Top-p**: `0.9`
- **Max new tokens**: `512`

## コードでの使用

### 推論の例

```python
from unsloth import FastLanguageModel

# モデルとトークナイザーのロード
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/llama-3.2-3b-bnb-4bit",
    max_seq_length=2048,
    dtype=None,  # 自動検出
    load_in_4bit=True,
)

# 推論用にセットアップ
FastLanguageModel.for_inference(model)

# テキスト生成
inputs = tokenizer(
    ["こんにちは、今日の天気は？"],
    return_tensors="pt"
).to("cuda")

outputs = model.generate(
    **inputs,
    max_new_tokens=128,
    temperature=0.7,
    top_p=0.9,
)

print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

### ファインチューニングの例

```python
from unsloth import FastLanguageModel
from trl import SFTTrainer
from transformers import TrainingArguments

# モデルのロード
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/llama-3.2-3b-bnb-4bit",
    max_seq_length=2048,
    dtype=None,
    load_in_4bit=True,
)

# LoRAアダプターの追加
model = FastLanguageModel.get_peft_model(
    model,
    r=32,  # LoRAランク
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_alpha=32,
    lora_dropout=0.05,
    bias="none",
    use_gradient_checkpointing="unsloth",  # Unsloth最適化
)

# トレーニング
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=2048,
    args=TrainingArguments(
        per_device_train_batch_size=2,
        gradient_accumulation_steps=8,
        learning_rate=2e-4,
        num_train_epochs=3,
        fp16=True,
        optim="adamw_8bit",
        output_dir="outputs",
    ),
)

trainer.train()
```

## 推奨設定

### RTX 4060 Ti 8GB向け

#### 小型モデル（1B-3B）

```yaml
model_name_or_path: unsloth/llama-3.2-3b-bnb-4bit
quantization_bit: 4
use_unsloth: true

per_device_train_batch_size: 2
gradient_accumulation_steps: 8
cutoff_len: 2048
```

#### 超軽量モデル（1B）

```yaml
model_name_or_path: unsloth/llama-3.2-1b-bnb-4bit
quantization_bit: 4
use_unsloth: true

per_device_train_batch_size: 4
gradient_accumulation_steps: 4
cutoff_len: 2048
```

### より大きいVRAM（16GB+）向け

```yaml
model_name_or_path: unsloth/Meta-Llama-3.1-8B-bnb-4bit
quantization_bit: 4
use_unsloth: true

per_device_train_batch_size: 2
gradient_accumulation_steps: 8
cutoff_len: 4096
```

## Unsloth最適化モデル

以下のモデルはUnslothで最適化されており、すぐに使用できます：

### 小型モデル（8GB VRAM）
- `unsloth/llama-3.2-1b-bnb-4bit`
- `unsloth/llama-3.2-3b-bnb-4bit`
- `unsloth/Phi-3.5-mini-instruct-bnb-4bit`

### 中型モデル（16GB VRAM推奨）
- `unsloth/Meta-Llama-3.1-8B-bnb-4bit`
- `unsloth/mistral-7b-v0.3-bnb-4bit`
- `unsloth/Qwen2.5-7B-bnb-4bit`

## トラブルシューティング

### CUDA Out of Memory

**解決策:**
1. より小さいモデルを使用（3B → 1B）
2. `per_device_train_batch_size` を減らす（2 → 1）
3. `cutoff_len` を減らす（2048 → 1024）
4. `gradient_accumulation_steps` を増やす

### Unslothが選択できない

**確認事項:**
```bash
# Unslothのインストール確認
python -c "import unsloth; print(unsloth.__version__)"

# 環境が正しくアクティベートされているか
which python
```

### インポートエラー

**解決策:**
```bash
# 環境を再同期
cd LLaMA-Factory
uv sync
```

### パフォーマンスが遅い

**確認事項:**
1. Boosterで `unsloth` が選択されているか
2. `use_unsloth: true` が設定されているか（YAML）
3. GPUが正しく認識されているか
   ```bash
   nvidia-smi
   ```

## ベンチマーク

### トレーニング速度（RTX 4060 Ti 8GB）

| モデル | 通常 | Unsloth | 高速化率 |
|--------|------|---------|----------|
| Llama 3.2 1B | 100% | 210% | 2.1x |
| Llama 3.2 3B | 100% | 195% | 1.95x |
| Phi-3.5 Mini | 100% | 200% | 2.0x |

### メモリ使用量

| モデル | 通常（16bit） | 4bit量子化 | 削減率 |
|--------|---------------|------------|--------|
| Llama 3.2 3B | ~12GB | ~3GB | 75% |
| Llama 3.2 1B | ~4GB | ~1GB | 75% |

## 参考リンク

- [Unsloth GitHub](https://github.com/unslothai/unsloth)
- [Unsloth ドキュメント](https://docs.unsloth.ai/)
- [対応モデル一覧](https://huggingface.co/unsloth)

---

**Unslothで高速なファインチューニングを楽しんでください！** 🦥⚡
