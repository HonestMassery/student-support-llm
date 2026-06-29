# Student Support LLM

## Overview

Student Support LLM is a university assistant powered by a local Large Language Model (LLM). It allows students to ask academic questions through a simple web interface while the backend communicates with Ollama to generate responses.

## Features

* Local AI assistant using Ollama
* FastAPI backend
* Frontend interface
* Prompt engineering for better responses
* Logging and error handling
* REST API endpoints
* Automated API testing

## Project Structure

```text
student-support-llm/
│── backend/
│── frontend/
│── tests/
│── docs/
│   ├── prompts.md
│   ├── report.md
│   └── screenshots/
│── README.md
│── requirements.txt
```

## Requirements

* Python 3.11+
* Ollama
* Git

## Installation

Clone the repository:

```bash
git clone https://github.com/HonestMassery/student-support-llm.git
cd student-support-llm
```

Create and activate a virtual environment:

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Install the LLM

Pull the model:

```bash
ollama pull llama3.2:1b
```

Start Ollama:

```bash
ollama serve
```

## Run the Backend

```bash
uvicorn backend.main:app --reload
```

## Run the Frontend

Follow the instructions provided in the frontend folder (for example, Streamlit if used).

## API Endpoints

### Health Check

```
GET /health
```

### Ask Question

```
POST /ask
```

Example request:

```json
{
  "question": "What is Object-Oriented Programming?"
}
```

## Documentation

Additional documentation is available in the `docs` folder, including:

* Prompt engineering
* Screenshots
* Project report

## Contributors

* Role 1 – Environment & LLM Setup
* Role 2 – Backend
* Role 3 – Logging & Error Handling
* Role 4 – Frontend
* Role 5 – Testing
* Role 6 – Prompt Engineering & Documentation
* Role 7 – Report & Reflection
