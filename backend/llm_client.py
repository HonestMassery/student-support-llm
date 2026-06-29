import httpx
from backend.config import OLLAMA_BASE_URL, OLLAMA_MODEL, OLLAMA_TIMEOUT, SYSTEM_PROMPT


def query_ollama(question: str) -> str:
    url = f"{OLLAMA_BASE_URL}/api/generate"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": question,
        "system": SYSTEM_PROMPT,
        "stream": False,
    }
    response = httpx.post(url, json=payload, timeout=OLLAMA_TIMEOUT)
    response.raise_for_status()
    return response.json()["response"]
