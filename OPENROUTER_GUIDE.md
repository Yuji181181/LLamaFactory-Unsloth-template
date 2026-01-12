## 導入手順

### 1. OpenRouter アカウント作成
1. [OpenRouter.ai](https://openrouter.ai/) にアクセスします。
2. Googleアカウント等でサインアップ（Sign up）します。

### 2. クレジットの購入
1. 右上のアイコンから **"Credits"** をクリックします。
2. **"Manage Credits"** (または "Add Credits") をクリックし、Stripe経由でクレジットを購入します。
   - テスト用なら **$5 (約750円)** で十分すぎるほど使えます。

### 3. APIキーの作成
1. **"Keys"** メニューに移動します。
2. **"Create Key"** をクリックします。
3. キーの名前（例: `LLaMA-Factory-Math`）を入力し、作成します。
4. **表示されたキー（sk-or-v1-...）をコピーします。**
   - ※この画面を閉じると二度と表示されないので注意してください。

### 4. ローカル環境への設定

1. `scripts` ディレクトリに移動します。
   ```bash
   cd scripts
   ```
2. `.env.example` をコピーして `.env` を作成します。
   ```bash
   cp .env.example .env
   ```
3. `.env` ファイルを編集し、先ほどのキーを貼り付けます。
   ```bash
   OPENROUTER_API_KEY="sk-or-v1-......"
   ```

### 5. モデルの確認・変更
`scripts/gen_data_pipeline.py` 内でデフォルトのモデルが設定されていますが、`.env` で上書き可能です。

```bash
# .env の例
MODEL_MASS="deepseek/deepseek-chat"       # 通常生成用
MODEL_HARD="deepseek/deepseek-r1"         # 難問生成用
MODEL_VERIFY="anthropic/claude-3.5-sonnet" # 検証用
```
