#!/bin/bash

################################################################################
# LLaMA-Factory + Unsloth 環境構築スクリプト
# LLMコンペ用テンプレートリポジトリ
#
# 使用方法:
#   chmod +x setup.sh
#   ./setup.sh
#
# 必要な環境:
#   - Ubuntu/WSL2
#   - Python 3.11+
#   - CUDA 12.x
#   - uv (Pythonパッケージマネージャー)
################################################################################

set -e  # エラーが発生したら即座に終了

# 色付き出力用
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ログ関数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# ヘッダー表示
echo "=================================="
echo "🦙 LLaMA-Factory + Unsloth Setup"
echo "=================================="
echo ""

################################################################################
# 1. システム要件チェック
################################################################################

log_info "システム要件をチェック中..."

# Python バージョンチェック
if ! command -v python3 &> /dev/null; then
    log_error "Python3 が見つかりません。Python 3.11以上をインストールしてください。"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
log_success "Python ${PYTHON_VERSION} を検出"

# Git チェック
if ! command -v git &> /dev/null; then
    log_error "Git が見つかりません。Gitをインストールしてください。"
    exit 1
fi

GIT_VERSION=$(git --version | awk '{print $3}')
log_success "Git ${GIT_VERSION} を検出"

# uv チェック
if ! command -v uv &> /dev/null; then
    log_warning "uv が見つかりません。インストールを試みます..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
    
    if ! command -v uv &> /dev/null; then
        log_error "uv のインストールに失敗しました。"
        exit 1
    fi
fi

UV_VERSION=$(uv --version | awk '{print $2}')
log_success "uv ${UV_VERSION} を検出"

# CUDA チェック（オプション）
if command -v nvidia-smi &> /dev/null; then
    CUDA_VERSION=$(nvidia-smi | grep "CUDA Version" | awk '{print $9}')
    GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader | head -n 1)
    log_success "GPU検出: ${GPU_NAME} (CUDA ${CUDA_VERSION})"
else
    log_warning "CUDA/GPUが検出されませんでした。CPUモードで動作します。"
fi

echo ""

################################################################################
# 2. LLaMA-Factory リポジトリのクローン（既にある場合はスキップ）
################################################################################

if [ -d "LLaMA-Factory" ]; then
    log_info "LLaMA-Factory ディレクトリが既に存在します。スキップします。"
else
    log_info "LLaMA-Factory リポジトリをクローン中..."
    git clone https://github.com/hiyouga/LLaMA-Factory.git
    log_success "LLaMA-Factory のクローンが完了"
fi

cd LLaMA-Factory

echo ""

################################################################################
# 3. Python仮想環境の作成
################################################################################

log_info "uv仮想環境を作成中..."

if [ -d ".venv" ]; then
    log_warning ".venv が既に存在します。既存の環境を使用します。"
else
    uv venv
    log_success "仮想環境の作成が完了"
fi

echo ""

################################################################################
# 4. 依存関係のインストール
################################################################################

log_info "LLaMA-Factory の依存関係をインストール中..."
log_info "これには数分かかる場合があります..."

# uv.lock が存在する場合は削除（クリーンインストール）
if [ -f "uv.lock" ]; then
    log_info "既存の uv.lock を削除してクリーンインストールを実行..."
    rm -f uv.lock
fi

# LLaMA-Factory の依存関係をインストール
uv sync

log_success "LLaMA-Factory の依存関係インストールが完了"

echo ""

################################################################################
# 5. Unsloth のインストール
################################################################################

log_info "Unsloth をインストール中..."
log_info "これには数分かかる場合があります..."

# Unsloth のインストール
uv add "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"

log_success "Unsloth のインストールが完了"

echo ""

################################################################################
# 6. インストール検証
################################################################################

log_info "インストールを検証中..."

# 仮想環境をアクティベート
source .venv/bin/activate

# PyTorch + CUDA 検証
log_info "PyTorch と CUDA の検証..."
python -c "
import torch
print(f'PyTorch バージョン: {torch.__version__}')
print(f'CUDA 利用可能: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'CUDA バージョン: {torch.version.cuda}')
    print(f'GPU デバイス数: {torch.cuda.device_count()}')
    print(f'GPU 名: {torch.cuda.get_device_name(0)}')
"

echo ""

# Unsloth 検証
log_info "Unsloth の検証..."
python -c "
import unsloth
print(f'Unsloth バージョン: {unsloth.__version__}')
from unsloth import FastLanguageModel
print('FastLanguageModel インポート成功')
" 2>&1 | grep -E "(Unsloth|FastLanguageModel)" || true

echo ""

# LLaMA-Factory CLI 検証
log_info "LLaMA-Factory CLI の検証..."
llamafactory-cli version

echo ""

################################################################################
# 7. 完了メッセージ
################################################################################

log_success "=========================================="
log_success "✅ セットアップが完了しました！"
log_success "=========================================="
echo ""

echo "📦 インストールされたコンポーネント:"
echo "  - LLaMA-Factory (最新版)"
echo "  - Unsloth (2026.1.2+)"
echo "  - PyTorch (CUDA対応)"
echo "  - その他120+の依存パッケージ"
echo ""

echo "🚀 次のステップ:"
echo ""
echo "1. 仮想環境をアクティベート:"
echo "   cd LLaMA-Factory"
echo "   source .venv/bin/activate"
echo ""
echo "2. Web UIを起動:"
echo "   llamafactory-cli webui"
echo ""
echo "3. ブラウザで http://127.0.0.1:7860 を開く"
echo ""
echo "4. Booster で 'unsloth' を選択して高速化！"
echo ""

echo "📚 ドキュメント:"
echo "  - クイックスタート: QUICKSTART_UNSLOTH.md"
echo "  - Web UI ガイド: UNSLOTH_WEBUI_GUIDE.md"
echo "  - 詳細ガイド: UNSLOTH_GUIDE.md"
echo ""

log_success "Happy Fine-tuning! 🦥⚡"
