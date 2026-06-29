import httpx
from fastapi.testclient import TestClient

from backend import main


client = TestClient(main.app)


class MockHealthResponse:
    def raise_for_status(self):
        return None


def test_health_returns_ok_when_ollama_is_reachable(monkeypatch):
    def fake_get(url, timeout):
        assert url.endswith("/api/tags")
        assert timeout == 5
        return MockHealthResponse()

    monkeypatch.setattr(main.httpx, "get", fake_get)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "model": main.OLLAMA_MODEL,
        "ollama_status": "connected",
    }


def test_ask_returns_model_answer(monkeypatch):
    monkeypatch.setattr(
        main,
        "query_ollama",
        lambda question: f"Mock answer for: {question}",
    )

    response = client.post("/ask", json={"question": "How do I register for exams?"})

    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "Mock answer for: How do I register for exams?"
    assert data["model"] == main.OLLAMA_MODEL
    assert "timestamp" in data


def test_ask_rejects_empty_question():
    response = client.post("/ask", json={"question": "   "})

    assert response.status_code == 422
    assert response.json()["detail"] == "Question cannot be empty. Please enter a question."


def test_ask_returns_clear_error_when_model_is_down(monkeypatch):
    def fake_query_ollama(question):
        raise httpx.ConnectError("Ollama is not running")

    monkeypatch.setattr(main, "query_ollama", fake_query_ollama)

    response = client.post("/ask", json={"question": "Where is the library?"})

    assert response.status_code == 503
    assert response.json()["detail"] == (
        "The AI model is not reachable. Please ensure Ollama is running."
    )
