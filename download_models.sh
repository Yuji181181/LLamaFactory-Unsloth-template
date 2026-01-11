#!/bin/bash
# Hugging Faceからモデルを高速ダウンロードするスクリプト (aria2使用)
# 使い方: このファイルの MODEL_ID を編集してから実行してください
# 例: ./download_models.sh

set -e

# =================================================================
# 👇 ダウンロードしたいモデルIDをここに指定してください
# =================================================================
MODEL_ID="unsloth/Llama-3.2-3B-Instruct"
# =================================================================

# 保存先設定 (プロジェクトルート/models/モデル名)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MODEL_NAME=$(basename "${MODEL_ID}")
SAVE_DIR="${SCRIPT_DIR}/models/${MODEL_NAME}"

echo "=================================================="
echo "🚀 モデルダウンローダー"
echo "📦 モデルID: ${MODEL_ID}"
echo "📂 保存先:   ${SAVE_DIR}"
echo "=================================================="
echo ""

# aria2c の確認
if ! command -v aria2c &> /dev/null; then
    echo "❌ aria2c が見つかりません。"
    echo "インストールしてください: sudo apt install aria2"
    exit 1
fi

# 保存先ディレクトリ作成
mkdir -p "${SAVE_DIR}"

# ファイルリストの取得 (Pythonを使用してAPIから取得)
echo "� ファイルリストを取得中..."
FILES=$(python3 -c "
import urllib.request, json, sys
try:
    url = 'https://huggingface.co/api/models/${MODEL_ID}/tree/main'
    with urllib.request.urlopen(url) as response:
        data = json.load(response)
        for item in data:
            print(item['path'])
except Exception as e:
    print(f'Error: {e}', file=sys.stderr)
    sys.exit(1)
")

if [ $? -ne 0 ]; then
    echo "❌ ファイルリストの取得に失敗しました。モデルIDが正しいか確認してください。"
    exit 1
fi

echo "📋 ダウンロード対象ファイル:"
echo "$FILES"
echo ""

# ダウンロードループ
BASE_URL="https://huggingface.co/${MODEL_ID}/resolve/main"

for file in $FILES; do
    echo "⬇️  Downloading: $file"
    
    # フォルダ構造がある場合はディレクトリを作成
    FILE_DIR=$(dirname "${SAVE_DIR}/${file}")
    mkdir -p "${FILE_DIR}"
    
    # aria2cオプション
    # -x 16: サーバへの最大接続数
    # -s 16: ダウンロードに使用するコネクション数
    # -c: 中断したダウンロードを再開
    # --dir: 保存先ディレクトリ
    # --out: 出力ファイル名
    
    # 自動リトライループ (速度低下で切断されても即座に再開)
    until aria2c -x 16 -s 16 -k 1M -c \
        --lowest-speed-limit=500K \
        --max-tries=0 \
        --connect-timeout=30 \
        --dir="${FILE_DIR}" \
        --out="$(basename "${file}")" \
        "${BASE_URL}/${file}"; do
        
        echo "⚠️  接続が不安定または速度低下のため再接続します..."
        sleep 1
    done
        
    echo "✅ Completed: $file"
    echo ""
done

echo "🎉 全てのダウンロードが完了しました！"
echo "モデルパス: ${SAVE_DIR}"