# Student Support LLM Project Report

## Overview

This project implements a local university student support assistant using a FastAPI backend, a Gradio frontend, and a local Ollama model.

## Completed Work

- Configured the backend in `backend/main.py` with `/ask` and `/health` endpoints.
- Implemented Ollama communication in `backend/llm_client.py`.
- Added environment configuration in `backend/config.py`.
- Built a Gradio interface in `frontend/app.py`.
- Documented environment setup in `docs/role1_environment_setup.md`.

## Fixes Applied

- Added the missing `httpx` import in `backend/main.py`.
- Updated `requirements.txt` to include `gradio`, `httpx`, and `pytest`.
- Added `tests/test_api.py` for API endpoint validation.

## Remaining Recommendations

- Ensure the local Ollama server is running and reachable at `http://localhost:11434`.
- Confirm `backend.config.OLLAMA_MODEL` is set to the downloaded model name.
- Optionally replace `streamlit` with `gradio` in any documentation references if the frontend is exclusively Gradio.

## Usage

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the backend:

```bash
uvicorn backend.main:app --reload
```

3. Run the frontend:

```bash
python frontend/app.py
```

4. Run tests:

```bash
pytest
```
