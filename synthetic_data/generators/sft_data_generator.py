"""
SFT用合成データ生成スクリプト（サンプル）

このスクリプトは、LLM APIを使用してSFT用の合成データを生成します。
実際のコンペでは、タスクに応じてカスタマイズしてください。
"""

import json
import os
from pathlib import Path
from typing import List, Dict
import argparse


def generate_sft_data_with_llm(
    num_samples: int = 100,
    api_key: str = None,
    model: str = "gpt-4",
) -> List[Dict]:
    """
    LLM APIを使用してSFT用データを生成
    
    Args:
        num_samples: 生成するサンプル数
        api_key: API キー
        model: 使用するモデル
    
    Returns:
        生成されたデータのリスト
    """
    # 注: 実際の実装では、OpenAI API、Claude API、またはローカルLLMを使用
    # ここではサンプルとして、ダミーデータを生成
    
    print(f"📝 {num_samples}個のSFTサンプルを生成中...")
    
    data = []
    
    # サンプルのプロンプトテンプレート
    # 実際のコンペでは、タスクに応じたプロンプトを設計
    sample_instructions = [
        "次の文章を要約してください。",
        "次の質問に答えてください。",
        "次のコードを説明してください。",
        "次のテキストを翻訳してください。",
        "次の問題を解いてください。",
    ]
    
    for i in range(num_samples):
        # ここで実際にはLLM APIを呼び出してデータを生成
        # 例: response = openai.ChatCompletion.create(...)
        
        instruction = sample_instructions[i % len(sample_instructions)]
        
        data.append({
            "instruction": instruction,
            "input": f"サンプル入力 {i+1}",
            "output": f"サンプル出力 {i+1}（実際にはLLMが生成）"
        })
        
        if (i + 1) % 10 == 0:
            print(f"  進捗: {i+1}/{num_samples}")
    
    print(f"✅ {len(data)}個のサンプルを生成完了")
    return data


def generate_sft_data_with_templates(
    num_samples: int = 100,
    templates_file: str = None,
) -> List[Dict]:
    """
    テンプレートベースでSFT用データを生成
    
    Args:
        num_samples: 生成するサンプル数
        templates_file: テンプレートファイルのパス
    
    Returns:
        生成されたデータのリスト
    """
    print(f"📝 テンプレートから{num_samples}個のSFTサンプルを生成中...")
    
    # テンプレートの例
    # 実際のコンペでは、より洗練されたテンプレートを使用
    templates = [
        {
            "instruction": "次の数学の問題を解いてください。",
            "input_template": "{a} + {b} = ?",
            "output_template": "{a} + {b} = {result}",
        },
        {
            "instruction": "次の文章を丁寧語に変換してください。",
            "input_template": "{casual_text}",
            "output_template": "{polite_text}",
        },
    ]
    
    data = []
    
    for i in range(num_samples):
        template = templates[i % len(templates)]
        
        # テンプレートに値を埋め込む
        # 実際にはランダムな値や、データベースから取得した値を使用
        if "a" in template["input_template"]:
            import random
            a = random.randint(1, 100)
            b = random.randint(1, 100)
            result = a + b
            
            data.append({
                "instruction": template["instruction"],
                "input": template["input_template"].format(a=a, b=b),
                "output": template["output_template"].format(a=a, b=b, result=result)
            })
        else:
            data.append({
                "instruction": template["instruction"],
                "input": f"サンプル入力 {i+1}",
                "output": f"サンプル出力 {i+1}"
            })
    
    print(f"✅ {len(data)}個のサンプルを生成完了")
    return data


def split_train_val(data: List[Dict], val_ratio: float = 0.1) -> tuple:
    """
    データをトレーニングセットと検証セットに分割
    
    Args:
        data: 全データ
        val_ratio: 検証セットの割合
    
    Returns:
        (train_data, val_data)
    """
    import random
    random.shuffle(data)
    
    split_idx = int(len(data) * (1 - val_ratio))
    train_data = data[:split_idx]
    val_data = data[split_idx:]
    
    print(f"📊 データ分割: トレーニング={len(train_data)}, 検証={len(val_data)}")
    
    return train_data, val_data


def save_data(data: List[Dict], output_path: str):
    """
    データをJSONファイルとして保存
    
    Args:
        data: 保存するデータ
        output_path: 出力ファイルパス
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 データを保存: {output_path} ({len(data)}サンプル)")


def main():
    parser = argparse.ArgumentParser(description='SFT用合成データ生成')
    parser.add_argument('--num_samples', type=int, default=100, help='生成するサンプル数')
    parser.add_argument('--method', choices=['llm', 'template'], default='template', 
                        help='生成方法（llm: LLM API使用, template: テンプレート使用）')
    parser.add_argument('--val_ratio', type=float, default=0.1, help='検証セットの割合')
    parser.add_argument('--output_dir', type=str, default='../synthetic_data/processed',
                        help='出力ディレクトリ')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🚀 SFT用合成データ生成を開始")
    print("=" * 60)
    print(f"生成方法: {args.method}")
    print(f"サンプル数: {args.num_samples}")
    print(f"検証セット割合: {args.val_ratio}")
    print("")
    
    # データ生成
    if args.method == 'llm':
        # 環境変数からAPIキーを取得
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("⚠️  警告: OPENAI_API_KEY が設定されていません")
            print("   テンプレートモードに切り替えます")
            data = generate_sft_data_with_templates(args.num_samples)
        else:
            data = generate_sft_data_with_llm(args.num_samples, api_key)
    else:
        data = generate_sft_data_with_templates(args.num_samples)
    
    # トレーニング/検証セットに分割
    train_data, val_data = split_train_val(data, args.val_ratio)
    
    # 保存
    save_data(train_data, f"{args.output_dir}/sft_train.json")
    save_data(val_data, f"{args.output_dir}/sft_val.json")
    
    # 生データも保存（JSONL形式）
    raw_path = f"{args.output_dir}/../raw/sft_raw.jsonl"
    Path(raw_path).parent.mkdir(parents=True, exist_ok=True)
    with open(raw_path, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    print(f"💾 生データを保存: {raw_path}")
    
    print("")
    print("=" * 60)
    print("✅ SFT用合成データ生成が完了しました！")
    print("=" * 60)
    print("")
    print("🔄 次のステップ:")
    print("  1. データの品質をチェック:")
    print(f"     python synthetic_data/quality_check/check_sft_data.py")
    print("")
    print("  2. LLaMA-Factoryのデータディレクトリにコピー:")
    print(f"     cp {args.output_dir}/sft_train.json LLaMA-Factory/data/competition_sft/train.json")
    print(f"     cp {args.output_dir}/sft_val.json LLaMA-Factory/data/competition_sft/val.json")
    print("")
    print("  3. SFTトレーニングを実行:")
    print("     cd LLaMA-Factory && llamafactory-cli train ../configs/sft_config.yaml")
    print("")


if __name__ == "__main__":
    main()
