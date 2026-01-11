# LLaMA-Factory 選好学習手法ガイド

LLaMA-Factoryは、DPO以外にも複数の選好学習（Preference Learning）手法をサポートしています。

## 📊 サポートされている手法一覧

LLaMA-Factoryでは、以下の6つの選好学習手法が使用できます（`pref_loss`パラメータで指定）：

### 1. **sigmoid** (DPO - Direct Preference Optimization)
- **デフォルト手法**
- 最も一般的で安定した手法
- 参照モデル（reference model）が必要

**特徴：**
- ✅ 安定した学習
- ✅ 広く使われている
- ✅ 論文で検証済み
- ❌ 参照モデルが必要（メモリ使用量が多い）

**推奨設定：**
```yaml
stage: dpo
pref_loss: sigmoid
pref_beta: 0.1  # 0.1-0.5が一般的
pref_ftx: 0.0   # SFT損失の重み
```

### 2. **hinge** (Hinge Loss DPO)
- Hinge損失を使用したDPOの変種
- マージンベースの学習

**特徴：**
- ✅ マージンを明示的に最大化
- ✅ ロバストな学習
- ❌ 参照モデルが必要

**推奨設定：**
```yaml
stage: dpo
pref_loss: hinge
pref_beta: 0.1
```

### 3. **ipo** (Identity Preference Optimization)
- DPOの改良版
- より安定した学習が可能

**特徴：**
- ✅ DPOより安定
- ✅ 過学習しにくい
- ❌ 参照モデルが必要

**推奨設定：**
```yaml
stage: dpo
pref_loss: ipo
pref_beta: 0.1
```

### 4. **kto_pair** (KTO - Kahneman-Tversky Optimization)
- ペアワイズデータ用のKTO
- 人間のフィードバックをより効果的に活用

**特徴：**
- ✅ 少ないデータで効果的
- ✅ 人間の判断により近い
- ❌ 参照モデルが必要

**推奨設定：**
```yaml
stage: dpo  # または kto
pref_loss: kto_pair
pref_beta: 0.1
kto_chosen_weight: 1.0
kto_rejected_weight: 1.0
```

### 5. **orpo** (ORPO - Odds Ratio Preference Optimization) ⭐
- **参照モデル不要**
- メモリ効率が良い
- SFTとアライメントを同時に実行

**特徴：**
- ✅ 参照モデル不要（メモリ節約）
- ✅ SFTとアライメントを統合
- ✅ 高速
- ✅ シンプル

**推奨設定：**
```yaml
stage: dpo
pref_loss: orpo
pref_beta: 0.1
```

### 6. **simpo** (SimPO - Simple Preference Optimization) ⭐⭐
- **参照モデル不要**
- 最もシンプルで効率的
- 最新の手法

**特徴：**
- ✅ 参照モデル不要（メモリ節約）
- ✅ 非常にシンプル
- ✅ 高性能
- ✅ 実装が軽量
- ✅ **推奨！**

**推奨設定：**
```yaml
stage: dpo
pref_loss: simpo
pref_beta: 2.0  # SimPOは大きめのbetaを使用
simpo_gamma: 0.5  # ターゲットリワードマージン
```

## 🎯 どの手法を選ぶべきか？

### コンペティションでの推奨順位

#### 1位: **SimPO** 🥇
```yaml
pref_loss: simpo
pref_beta: 2.0
simpo_gamma: 0.5
```
**理由：**
- 参照モデル不要でメモリ効率が良い
- 最新の手法で高性能
- 実装がシンプルで安定
- **8GB VRAMでも使いやすい**

#### 2位: **ORPO** 🥈
```yaml
pref_loss: orpo
pref_beta: 0.1
```
**理由：**
- 参照モデル不要
- SFTとアライメントを統合
- 安定した性能

#### 3位: **DPO (sigmoid)** 🥉
```yaml
pref_loss: sigmoid
pref_beta: 0.1
```
**理由：**
- 最も一般的で検証済み
- 安定した学習
- ただし参照モデルが必要（メモリ使用量が多い）

### メモリ使用量の比較

| 手法 | 参照モデル | メモリ使用量 | 推奨VRAM |
|------|-----------|-------------|----------|
| SimPO | 不要 | 低 | 8GB+ |
| ORPO | 不要 | 低 | 8GB+ |
| DPO (sigmoid) | 必要 | 高 | 16GB+ |
| IPO | 必要 | 高 | 16GB+ |
| Hinge | 必要 | 高 | 16GB+ |
| KTO | 必要 | 高 | 16GB+ |

## 📝 設定ファイルテンプレート

### SimPO設定（推奨）

```yaml
# configs/simpo_config.yaml
### モデル設定
model_name_or_path: unsloth/llama-3.2-3b-bnb-4bit
adapter_name_or_path: outputs/sft_model/checkpoint-best

stage: dpo
do_train: true
finetuning_type: lora

### LoRA パラメータ
lora_target: all
lora_rank: 32
lora_alpha: 32
lora_dropout: 0.05

### 量子化設定
quantization_bit: 4
quantization_method: bnb

### Unsloth最適化
use_unsloth: true
use_unsloth_gc: true

### データセット設定
dataset: competition_dpo
template: llama3
cutoff_len: 2048
val_size: 0.1
overwrite_cache: true

### SimPO固有パラメータ
pref_loss: simpo  # SimPOを使用
pref_beta: 2.0    # SimPOは大きめのbeta
simpo_gamma: 0.5  # ターゲットリワードマージン
pref_ftx: 0.0     # SFT損失の重み

### トレーニングパラメータ
output_dir: outputs/simpo_model
overwrite_output_dir: true

per_device_train_batch_size: 2  # SimPOは参照モデル不要なので大きめでOK
gradient_accumulation_steps: 8
per_device_eval_batch_size: 2

learning_rate: 5.0e-6
lr_scheduler_type: cosine
warmup_ratio: 0.1
num_train_epochs: 1

### 最適化設定
optim: adamw_torch
fp16: true
max_grad_norm: 1.0

### ロギングと保存
logging_steps: 5
save_steps: 50
save_total_limit: 3
eval_strategy: steps
eval_steps: 50

### その他
seed: 42
report_to: none
dataloader_num_workers: 4
remove_unused_columns: false
save_safetensors: true
```

### ORPO設定

```yaml
# configs/orpo_config.yaml
# （SimPOとほぼ同じだが、以下を変更）

pref_loss: orpo
pref_beta: 0.1  # ORPOは小さめのbeta
# simpo_gamma は不要
```

### DPO設定（従来型）

```yaml
# configs/dpo_config.yaml
# （参照モデルが必要）

pref_loss: sigmoid
pref_beta: 0.1

# 参照モデルの設定（オプション、指定しない場合はベースモデルを使用）
# ref_model: unsloth/llama-3.2-3b-bnb-4bit
# ref_model_quantization_bit: 4

# メモリ節約のため、バッチサイズを小さく
per_device_train_batch_size: 1
gradient_accumulation_steps: 16
```

## 🔬 実験の推奨順序

### ステップ1: SFT
まず、SFTでベースラインを作成

### ステップ2: SimPOで試す
```bash
llamafactory-cli train configs/simpo_config.yaml
```

### ステップ3: ハイパーパラメータ調整
- `pref_beta`: 1.0, 2.0, 3.0
- `simpo_gamma`: 0.3, 0.5, 0.7
- `learning_rate`: 1e-6, 5e-6, 1e-5

### ステップ4: 他の手法も試す（オプション）
- ORPO
- DPO (メモリに余裕があれば)

## 📊 データフォーマット

すべての選好学習手法で、同じデータフォーマットを使用できます：

```json
[
  {
    "conversations": [
      {"from": "human", "value": "質問"},
      {"from": "gpt", "value": "好ましい回答"}
    ],
    "rejected_conversations": [
      {"from": "human", "value": "質問"},
      {"from": "gpt", "value": "好ましくない回答"}
    ]
  }
]
```

## 💡 コンペでの戦略

### RTX 4060 Ti 8GB の場合

1. **SFT**: `unsloth/llama-3.2-3b-bnb-4bit`
2. **SimPO**: 参照モデル不要なので8GBで快適に動作
3. **ハイパーパラメータ調整**: beta, gamma, learning rateを調整

### より大きいVRAM（16GB+）の場合

1. **SFT**: `unsloth/Meta-Llama-3.1-8B-bnb-4bit`
2. **SimPO, ORPO, DPO**を全て試す
3. **アンサンブル**: 複数の手法の結果を組み合わせる

## 📚 参考論文

- **DPO**: [Direct Preference Optimization](https://arxiv.org/abs/2305.18290)
- **IPO**: [A General Theoretical Paradigm to Understand Learning from Human Preferences](https://arxiv.org/abs/2310.12036)
- **KTO**: [KTO: Model Alignment as Prospect Theoretic Optimization](https://arxiv.org/abs/2402.01306)
- **ORPO**: [ORPO: Monolithic Preference Optimization without Reference Model](https://arxiv.org/abs/2403.07691)
- **SimPO**: [SimPO: Simple Preference Optimization with a Reference-Free Reward](https://arxiv.org/abs/2405.14734)

## 🚀 まとめ

**コンペで最初に試すべき手法：**
1. **SimPO** - 参照モデル不要、高性能、メモリ効率◎
2. **ORPO** - SFTとアライメントを統合、シンプル
3. **DPO** - 従来型、安定しているがメモリ使用量が多い

**RTX 4060 Ti 8GBでは SimPO が最適！** 🎯
