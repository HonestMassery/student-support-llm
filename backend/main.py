import logging
import os
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time
from backend.llm_client import query_ollama
from backend.config import OLLAMA_BASE_URL, OLLAMA_MODEL

# Logging setup
LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, "app.log"), encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("student_support")

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
        logger.warning("Empty question submitted by client")
        raise HTTPException(
            status_code=422,
            detail="Question cannot be empty. Please enter a question.",
        )

    logger.info(f"Question received: \"{question}\"")
    start_time = time.time()

    try:
        answer = query_ollama(question)
        elapsed = round(time.time() - start_time, 2)
        logger.info(f"Response generated ({len(answer)} chars) in {elapsed}s")
        return AnswerResponse(
            answer=answer,
            model=OLLAMA_MODEL,
            timestamp=datetime.now().isoformat(),
        )
    except httpx.ConnectError:
        logger.error(f"LLM connection failed: Could not connect to Ollama at {OLLAMA_BASE_URL}")
        raise HTTPException(
            status_code=503,
            detail="The AI model is not reachable. Please ensure Ollama is running.",
        )
    except httpx.TimeoutException:
        logger.error(f"Ollama request timed out for question: {question}")
        raise HTTPException(
            status_code=503,
            detail="The model took too long to respond. Please try again later.",
        )
    except Exception as e:
        logger.error(f"Unexpected error: {type(e).__name__}: {e}")
        raise HTTPException(
            status_code=500,
            detail="An internal server error occurred. Check the logs for details.",
        )