import json
import os
from pathlib import Path
from ollama import AsyncClient

MODEL = os.environ.get("OLLAMA_MODEL", "gemma3:4b")
BASE_DIR = Path(__file__).parent

with open(BASE_DIR / "system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

VALID_CATEGORIES = {"bug", "payment", "account", "suggestion", "toxicity", "autre"}
VALID_SENTIMENTS = {"positive", "neutral", "negative"}

def is_valid_analysis(a: dict) -> bool:
    try:
        if a.get("category") not in VALID_CATEGORIES:
            return False
        if not isinstance(a.get("severity"), int):
            return False
        if not (1 <= a["severity"] <= 5):
            return False
        if a.get("sentiment") not in VALID_SENTIMENTS:
            return False
        if not isinstance(a.get("summary"), str):
            return False
        return True
    except Exception:
        return False


async def analyze_ticket(message: str) -> dict:
    client = AsyncClient()

    for attempt in range(2):  # ici les max 2 essais
        response = await client.chat(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message}
            ]
        )

        raw = response["message"]["content"]
        raw = raw.replace("```json", "").replace("```", "").strip()

        try:
            data = json.loads(raw)
        except Exception:
            continue  # retry

        if is_valid_analysis(data):
            return data

    return {"status": "to_check"}



