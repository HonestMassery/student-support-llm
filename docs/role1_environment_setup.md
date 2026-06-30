# Role 1: Environment and LLM Setup

## 1. Introduction

The first phase of the University Student Support Assistant project involved setting up the development environment and installing a Local Large Language Model (LLM). This stage was essential because all other components of the system, including the backend API, frontend interface, testing, logging, and documentation, depend on a properly configured environment and a functioning AI model.

The objective of this role was to prepare the project workspace, install all required software dependencies, download a local AI model, verify that it runs correctly, and confirm that it can be accessed through an API.

---

## 2. Development Environment Setup

The project was developed using Kali Linux. A dedicated Python virtual environment was created to isolate project dependencies from the operating system and prevent package conflicts.

### Creating the Virtual Environment

The following command was used:

```bash
python3 -m venv venv
```

This command created a folder named `venv`, which contains an isolated Python environment.

### Activating the Virtual Environment

```bash
source venv/bin/activate
```

After activation, the terminal displayed:

```bash
(venv)
```

indicating that all subsequent Python packages would be installed inside the virtual environment rather than globally on the operating system.

### Why Virtual Environments Are Important

Virtual environments provide:

* Dependency isolation
* Easier project management
* Reduced package conflicts
* Better collaboration among team members
* Consistent project configuration

Each team member creates their own virtual environment locally and installs packages using the shared requirements file.

---

## 3. Installing Project Dependencies

The project dependencies were specified in the `requirements.txt` file.

### Installed Packages

```text
fastapi
uvicorn
requests
streamlit
ollama
python-dotenv
```

### Purpose of Each Package

#### FastAPI

FastAPI is a modern Python framework used to create APIs. It enables the backend to receive user questions and communicate with the AI model.

#### Uvicorn

Uvicorn is an ASGI server used to run FastAPI applications.

#### Requests

Requests is a Python library that allows the application to send HTTP requests to APIs and external services.

#### Gradio

Gradio is a Python framework used to build simple web-based user interfaces. In this project, the UI is implemented with Gradio in `frontend/app.py`.

#### Ollama

Ollama provides a simple way to run Large Language Models locally on a computer without relying on external cloud services.

#### Python-dotenv

Python-dotenv allows environment variables to be stored securely in a `.env` file.

---

## 4. Understanding Large Language Models (LLMs)

A Large Language Model (LLM) is an Artificial Intelligence system trained on large amounts of text data. It can understand natural language, answer questions, summarize information, generate content, and assist users conversationally.

Examples of LLMs include:

* GPT models
* Llama models
* Phi models
* Gemini models
* Claude models

In this project, a local LLM was selected to ensure privacy, offline capability, and reduced dependency on external APIs.

---

## 5. Introduction to Ollama

Ollama is a platform that enables users to download and run Large Language Models locally on their own machines.

### Benefits of Ollama

* Runs AI models locally
* No internet connection required after download
* Improved privacy and security
* No API subscription costs
* Easy model management
* Simple REST API integration

Ollama acts as the bridge between the application and the AI model.

### Installed Version

The installed version was:

```bash
ollama version 0.23.3
```

---

## 6. Downloading the AI Model

The selected model for this project was:

```text
llama3.2:1b
```

### Why llama3.2:1b?

The model was selected because:

* Small size (~1.3 GB)
* Fast execution
* Low memory requirements
* Suitable for student projects
* Good balance between speed and performance

### Download Command

```bash
ollama pull llama3.2:1b
```

The download completed successfully and the model was stored locally on the machine.

---

## 7. Running the AI Model

After downloading, the model was started using:

```bash
ollama run llama3.2:1b
```

A test prompt was submitted:

```text
What is course registration?
```

The model successfully generated a response, confirming that it was functioning correctly.

---

## 8. Verifying the Model Through the API

Ollama provides a REST API that allows applications to communicate with the model programmatically.

### Checking Available Models

```bash
curl http://localhost:11434/api/tags
```

The API returned information about the downloaded model, confirming that the service was active and accessible.

Example response:

```json
{
  "models": [
    {
      "name": "llama3.2:1b"
    }
  ]
}
```

This demonstrated that the backend would be able to interact with the model during later development stages.

---

## 9. Project Structure Contribution

As part of Role 1, the following project resources were prepared:

```text
student-support-llm/
│
├── docs/
│   └── screenshots/
│
├── requirements.txt
│
└── venv/
```

The screenshots folder was created to store evidence required for project assessment.

---

## 10. Challenges Encountered

Several challenges were encountered during setup:

### Ollama Service Not Running

Initially, Ollama returned a warning indicating that it could not connect to a running instance.

Solution:

The Ollama service was started correctly, allowing the client to communicate with the local AI model.

### Dependency Management

Ensuring all required packages were installed inside the virtual environment rather than globally required careful verification.

Solution:

The virtual environment was activated before installing dependencies.

---

## 11. Conclusion

The Environment and LLM Setup phase was successfully completed. A dedicated Python virtual environment was created, project dependencies were installed, Ollama was configured, the llama3.2:1b model was downloaded and executed successfully, and API communication was verified. This setup provides the foundation required for backend development, frontend integration, testing, logging, and deployment of the University Student Support Assistant system.
