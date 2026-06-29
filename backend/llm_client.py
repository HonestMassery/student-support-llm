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

    try:
        response = httpx.post(url, json=payload, timeout=OLLAMA_TIMEOUT)
        response.raise_for_status()
        return response.json()["response"]
    except httpx.ConnectError:
        raise httpx.ConnectError(
            f"Could not connect to Ollama at {OLLAMA_BASE_URL}. Is it running?"
        )
    except httpx.TimeoutException:
        raise httpx.TimeoutException(
            f"Ollama did not respond within {OLLAMA_TIMEOUT} seconds."
        )
    except httpx.HTTPStatusError as e:
        raise Exception(f"Ollama returned an error: {e.response.status_code} {e.response.text}")