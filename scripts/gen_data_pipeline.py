import os
import json
import logging
from typing import List, Dict, Optional
from openai import OpenAI
from tqdm import tqdm
from dotenv import load_dotenv

# .envの読み込み
load_dotenv()

# ロガー設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# ==========================================
# 設定定数
# ==========================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "../LLaMA-Factory/data")
SAVE_FILE = os.path.join(OUTPUT_DIR, "math_synth_advanced.json")

# モデル設定 (OpenRouter)
MODEL_MASS = os.getenv("MODEL_MASS", "deepseek/deepseek-chat")
MODEL_HARD = os.getenv("MODEL_HARD", "deepseek/deepseek-r1") 
MODEL_VERIFY = os.getenv("MODEL_VERIFY", "anthropic/claude-3.5-sonnet")

# プロンプト設定
PROMPT_MASS_SYSTEM = """あなたは数学教材の作成者です。指定されたトピックについて、明確で教育的な数学の問題と詳細な解答を作成してください。
必ずJSON形式で出力してください。"""

PROMPT_HARD_SYSTEM = """あなたは数学オリンピックレベルの問題作成者です。
深く複雑な推論（Chain of Thought）を必要とする難問を作成してください。
思考プロセスを含めて解答を作成し、論理の飛躍がないようにしてください。
必ずJSON形式で出力してください。"""

PROMPT_VERIFY_SYSTEM = """あなたは厳格な数学の検証者です。
与えられた数学の問題と解答をレビューし、以下の点を検証してください：
1. 数学的に正しいか
2. 計算ミスはないか
3. 論理の飛躍はないか

出力フォーマット（JSON）:
{
  "is_valid": true/false,
  "reason": "OK または 具体的なエラー内容",
  "corrected_output": "必要であれば修正後の解答、なければnull"
}
"""

PROMPT_USER_TEMPLATE = """トピック: {topic}
レベル: {level}

以下のフォーマットのJSONオブジェクトを1つ作成してください:
{{
  "instruction": "問題文...",
  "input": "",
  "output": "解答..."
}}
"""

# ==========================================
# OpenRouter クライアント
# ==========================================
class OpenRouterClient:
    def __init__(self):
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("❌ OPENROUTER_API_KEY が .env に設定されていません。")
        
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            default_headers={
                "HTTP-Referer": "https://github.com/Yuji181181/LLamaFactory-Unsloth-template", 
                "X-Title": "LLaMA-Factory Data Gen",
            }
        )

    def generate(self, model: str, system_prompt: str, user_prompt: str, json_mode: bool = True) -> Optional[Dict]:
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"} if json_mode else None
            )
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            logger.error(f"Generate Error ({model}): {e}")
            return None

# ==========================================
# パイプライン
# ==========================================
class DataPipeline:
    def __init__(self):
        self.api = OpenRouterClient()
        self.dataset = []

    def mass_produce(self, topics: List[str], count_per_topic: int):
        logger.info(f"🚀 Mass Production Mode (Model: {MODEL_MASS})")
        for topic in topics:
            logger.info(f"Generating {count_per_topic} problems for: {topic}")
            for _ in tqdm(range(count_per_topic), desc=topic):
                data = self.api.generate(
                    model=MODEL_MASS,
                    system_prompt=PROMPT_MASS_SYSTEM,
                    user_prompt=PROMPT_USER_TEMPLATE.format(topic=topic, level="標準")
                )
                if data:
                    self.dataset.append(data)

    def hard_mode_produce(self, topics: List[str], count_per_topic: int):
        logger.info(f"🔥 Hard Mode Production (Model: {MODEL_HARD})")
        for topic in topics:
            logger.info(f"Generating {count_per_topic} HARD problems for: {topic}")
            for _ in tqdm(range(count_per_topic), desc=topic + " (Hard)"):
                data = self.api.generate(
                    model=MODEL_HARD,
                    system_prompt=PROMPT_HARD_SYSTEM,
                    user_prompt=PROMPT_USER_TEMPLATE.format(topic=topic, level="難問・応用")
                )
                if data:
                    # R1などの思考モデル用に応答フィールドを調整する処理が必要な場合はここに追加
                    self.dataset.append(data)

    def verify_and_clean(self):
        logger.info(f"⚖️  Verification Mode (Model: {MODEL_VERIFY})")
        verified_dataset = []
        
        for data in tqdm(self.dataset, desc="Verifying"):
            verify_prompt = f"Problem: {data['instruction']}\nSolution: {data['output']}"
            result = self.api.generate(
                model=MODEL_VERIFY,
                system_prompt=PROMPT_VERIFY_SYSTEM,
                user_prompt=verify_prompt
            )
            
            if result and result.get("is_valid"):
                verified_dataset.append(data)
            elif result and result.get("corrected_output"):
                logger.info("🔧 Auto-corrected a problem.")
                data["output"] = result["corrected_output"]
                verified_dataset.append(data)
            else:
                logger.warning(f"❌ Invalid data rejected: {result.get('reason') if result else 'Unknown error'}")

        self.dataset = verified_dataset

    def save(self):
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.dataset, f, indent=2, ensure_ascii=False)
        logger.info(f"💾 Saved {len(self.dataset)} items to {SAVE_FILE}")

# ==========================================
# メイン実行
# ==========================================
if __name__ == "__main__":
    pipeline = DataPipeline()
    
    # テスト用トピック
    math_topics = ["微分積分", "線形代数", "確率論"]
    
    # 1. 大量生成 (DeepSeek-V3)
    pipeline.mass_produce(math_topics, count_per_topic=1)
    
    # 2. 難問生成 (DeepSeek-R1)
    pipeline.hard_mode_produce(["数論", "位相幾何"], count_per_topic=1)
    
    # 3. 検証 (Claude)
    pipeline.verify_and_clean()
    
    # 保存
    pipeline.save()
