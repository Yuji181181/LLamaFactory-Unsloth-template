# 🚀 LLMコンペ テンプレートリポジトリ セットアップチェックリスト

このチェックリストに従って、新しいコンペティションを開始しましょう。

## ✅ 初期セットアップ（初回のみ）

### 1. リポジトリの準備
- [ ] テンプレートリポジトリをクローンまたはコピー
- [ ] 新しいGitリポジトリを初期化
- [ ] `.gitignore_template` を `.gitignore` にコピー

```bash
cp .gitignore_template .gitignore
git init
git add .
git commit -m "Initial commit from template"
```

### 2. 環境構築
- [ ] `setup.sh` に実行権限を付与
- [ ] セットアップスクリプトを実行
- [ ] インストールの検証

```bash
chmod +x setup.sh
./setup.sh
```

### 3. 動作確認
- [ ] 仮想環境をアクティベート
- [ ] Web UIを起動して動作確認
- [ ] Boosterで「unsloth」が選択できることを確認

```bash
cd LLaMA-Factory
source .venv/bin/activate
llamafactory-cli webui
```

## ✅ 新しいコンペティションの開始

### 1. プロジェクト設定
- [ ] `README_TEMPLATE.md` を `README.md` にコピーして編集
- [ ] コンペティション名と説明を更新
- [ ] 目標とタスクを記載

### 2. ディレクトリ構造の作成
- [ ] `configs/` ディレクトリを作成
- [ ] `scripts/` ディレクトリを作成
- [ ] `notebooks/` ディレクトリを作成（オプション）

```bash
mkdir -p configs scripts notebooks
```

### 3. データセットの準備
- [ ] コンペデータをダウンロード
- [ ] `LLaMA-Factory/data/` にデータセットを配置
- [ ] データセット情報ファイル（`dataset_info.json`）を作成
- [ ] データ前処理スクリプトを作成（必要に応じて）

```bash
mkdir -p LLaMA-Factory/data/my_competition
# データをコピー
cp /path/to/data/* LLaMA-Factory/data/my_competition/
```

## ✅ 実験の実施

### 1. ベースライン実験
- [ ] `config_template.yaml` をコピーして `configs/exp001_baseline.yaml` を作成
- [ ] 設定ファイルを編集（モデル、データセット、パラメータ）
- [ ] ベースライン実験を実行
- [ ] 結果を記録

```bash
cp config_template.yaml configs/exp001_baseline.yaml
# 編集後
cd LLaMA-Factory
source .venv/bin/activate
llamafactory-cli train ../configs/exp001_baseline.yaml
```

### 2. 実験の反復
- [ ] 新しい設定ファイルを作成（`exp002_`, `exp003_`, ...）
- [ ] ハイパーパラメータを調整
- [ ] 各実験の結果を記録
- [ ] ベストモデルを特定

### 3. 実験管理
- [ ] 各実験の設定をGitにコミット
- [ ] 実験結果をドキュメント化
- [ ] W&Bやその他のツールでトラッキング（オプション）

```bash
git add configs/exp*.yaml
git commit -m "Add experiment configurations"
```

## ✅ モデルの評価と選択

### 1. 評価
- [ ] 検証セットで各モデルを評価
- [ ] 評価スクリプトを作成（必要に応じて）
- [ ] 評価指標を記録

### 2. ベストモデルの選択
- [ ] 評価結果を比較
- [ ] ベストモデルを選択
- [ ] ベストモデルのチェックポイントを保存

## ✅ 提出準備

### 1. モデルのエクスポート
- [ ] エクスポート設定ファイルを作成
- [ ] モデルをエクスポート
- [ ] エクスポートされたモデルをテスト

```bash
llamafactory-cli export configs/export_config.yaml
```

### 2. 推論スクリプトの作成
- [ ] コンペ形式に合わせた推論スクリプトを作成
- [ ] テストデータで動作確認
- [ ] 出力形式を確認

### 3. 最終チェック
- [ ] すべての依存関係を確認
- [ ] 推論速度を確認
- [ ] メモリ使用量を確認
- [ ] 提出ファイルを準備

## ✅ 提出後

### 1. ドキュメント化
- [ ] 最終的なアプローチをREADMEに記載
- [ ] 使用した設定ファイルを整理
- [ ] 学んだことをメモ

### 2. リポジトリの整理
- [ ] 不要なファイルを削除
- [ ] 最終的な状態をコミット
- [ ] タグを作成（`v1.0-submission`など）

```bash
git tag -a v1.0-submission -m "Final submission"
git push origin v1.0-submission
```

## 📊 推奨実験パターン

### パターン1: モデルサイズの比較
- [ ] exp001: Llama 3.2 1B (ベースライン)
- [ ] exp002: Llama 3.2 3B
- [ ] exp003: Phi-3.5 Mini

### パターン2: ハイパーパラメータ調整
- [ ] exp004: Learning rate 2e-4
- [ ] exp005: Learning rate 5e-5
- [ ] exp006: Learning rate 1e-4

### パターン3: LoRAパラメータ調整
- [ ] exp007: LoRA rank 16
- [ ] exp008: LoRA rank 32
- [ ] exp009: LoRA rank 64

### パターン4: データ拡張
- [ ] exp010: オリジナルデータのみ
- [ ] exp011: データ拡張あり
- [ ] exp012: バックトランスレーション

## 🔧 トラブルシューティングチェックリスト

### メモリ不足の場合
- [ ] より小さいモデルを使用
- [ ] `per_device_train_batch_size` を減らす
- [ ] `cutoff_len` を減らす
- [ ] `gradient_accumulation_steps` を増やす

### トレーニングが遅い場合
- [ ] Boosterで「unsloth」が選択されているか確認
- [ ] `use_unsloth: true` が設定されているか確認
- [ ] GPUが正しく認識されているか確認
- [ ] `dataloader_num_workers` を調整

### 精度が低い場合
- [ ] より大きいモデルを試す
- [ ] エポック数を増やす
- [ ] 学習率を調整
- [ ] データの品質を確認

## 📚 参考ドキュメント

- [ ] [QUICKSTART_UNSLOTH.md](QUICKSTART_UNSLOTH.md) - 最速スタートガイド
- [ ] [UNSLOTH_WEBUI_GUIDE.md](UNSLOTH_WEBUI_GUIDE.md) - Web UI詳細ガイド
- [ ] [TEMPLATE_USAGE.md](TEMPLATE_USAGE.md) - テンプレート使用方法
- [ ] [config_template.yaml](config_template.yaml) - 設定ファイルテンプレート

---

**このチェックリストを印刷またはコピーして、進捗を追跡しましょう！** ✅
