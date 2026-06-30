import os
import pytest
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_health_endpoint_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "model" in data
    assert "ollama_status" in data


def test_ask_empty_question_returns_422():
    response = client.post("/ask", json={"question": ""})
    assert response.status_code == 422
    assert response.json()["detail"] == "Question cannot be empty. Please enter a question."


def test_query_support_assistant_returns_answer(monkeypatch):
    def fake_query_ollama(question):
        return "This is a test answer."

    monkeypatch.setattr("backend.main.query_ollama", fake_query_ollama)

    response = client.post("/ask", json={"question": "What is registration?"})
    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "This is a test answer."
    assert data["model"] == os.getenv("OLLAMA_MODEL", "llama3.2:1b")
    assert "timestamp" in data
