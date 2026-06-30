# student-support-llm

## University Student Support Assistant

This project provides a local student support assistant using a FastAPI backend, a Gradio frontend, and a local Ollama model.

## Prerequisites

- Python 3.11+ installed
- Ollama installed on your machine (the app requires the Ollama binary and a downloaded model)
- A project virtual environment

## Setup

From the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Install Ollama

Ollama is not installed via pip. Install the Ollama CLI separately before running the app.

Example (Windows):

```powershell
winget install Ollama.Ollama
```

Then download the local model:

```powershell
ollama pull llama3.2:1b
```

## Run the application

1. Start Ollama:

```powershell
ollama run llama3.2:1b
```

2. Start the backend API:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload
```

3. Start the frontend interface:

```powershell
.\.venv\Scripts\python.exe frontend/app.py
```

4. Open the browser at `http://127.0.0.1:7860`.

## Environment variables

Create a `.env` file if you want to override defaults. You can copy `.env.example` and edit values as needed.

## Tests

Run the API tests with:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```
