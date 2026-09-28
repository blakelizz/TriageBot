import json
import os
from pathlib import Path
from ollama import AsyncClient

MODEL = os.environ.get("OLLAMA_MODEL", "gemma3:4b")
BASE_DIR = Path(__file__).parent

with open(BASE_DIR / "system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()


async def analyze_ticket(message: str) -> dict:
    client = AsyncClient()

    response = await client.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message}
        ]
    )

    raw = response["message"]["content"]
    raw = raw.replace("```json", "").replace("```", "").strip()
    
    return json.loads(raw)


