import logging
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

from backend.llm_client import query_ollama
from backend.config import OLLAMA_BASE_URL, OLLAMA_MODEL

logging.basicConfig(
    filename="backend/logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="University Student Support Assistant API",
    description="Backend API that connects to a local Ollama LLM to answer student questions.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    answer: str
    model: str
    timestamp: str


class HealthResponse(BaseModel):
    status: str
    model: str
    ollama_status: str


@app.get("/health", response_model=HealthResponse)
def health_check():
    try:
        resp = httpx.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        resp.raise_for_status()
        ollama_status = "connected"
    except Exception:
        ollama_status = "unreachable"

    return HealthResponse(
        status="ok",
        model=OLLAMA_MODEL,
        ollama_status=ollama_status,
    )


@app.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest):
    question = request.question.strip()

    if not question:
        logger.warning("Received empty question")
        return AnswerResponse(
            answer="Please provide a non-empty question.",
            model=OLLAMA_MODEL,
            timestamp=datetime.now().isoformat(),
        )

    logger.info("Question received: %s", question)

    try:
        answer = query_ollama(question)
    except httpx.ConnectError:
        logger.error("Cannot connect to Ollama at %s", OLLAMA_BASE_URL)
        return AnswerResponse(
            answer="The language model service is not running. Please start Ollama and try again.",
            model=OLLAMA_MODEL,
            timestamp=datetime.now().isoformat(),
        )
    except httpx.TimeoutException:
        logger.error("Ollama request timed out for question: %s", question)
        return AnswerResponse(
            answer="The model took too long to respond. Please try again.",
            model=OLLAMA_MODEL,
            timestamp=datetime.now().isoformat(),
        )
    except Exception as e:
        logger.error("Unexpected error: %s", str(e))
        return AnswerResponse(
            answer="An unexpected error occurred. Please try again later.",
            model=OLLAMA_MODEL,
            timestamp=datetime.now().isoformat(),
        )

    logger.info("Answer generated: %s", answer[:100])

    return AnswerResponse(
        answer=answer,
        model=OLLAMA_MODEL,
        timestamp=datetime.now().isoformat(),
    )
