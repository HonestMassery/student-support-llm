# Role 5: Testing and Quality Assurance

## 1. Introduction

The purpose of Role 5 was to test the backend API and confirm that the main endpoints work correctly. Testing was important because the Student Support Assistant depends on the backend to receive questions, validate user input, communicate with the LLM service, and return useful responses.

Automated tests were written using `pytest` and FastAPI's `TestClient`. These tests allow the backend to be checked quickly without manually opening the API every time.

---

## 2. Test File Created

The main test file for this role is:

```text
tests/test_api.py
```

This file contains automated tests for the FastAPI backend. The tests use mocked responses so that the test results do not depend on Ollama being active during the test run.

---

## 3. Endpoints Tested

### Health Endpoint

The `/health` endpoint was tested to confirm that the backend returns a successful response when the API is running.

Expected result:

```text
status: ok
ollama_status: connected
```

### Ask Endpoint

The `/ask` endpoint was tested to confirm that the backend accepts a valid student question and returns an answer.

Example tested question:

```text
How do I register for exams?
```

Expected result:

```text
HTTP 200 response with an answer, model name, and timestamp
```

---

## 4. Error Cases Tested

### Empty Question

The backend was tested with an empty question containing only spaces. The API correctly rejected the request and returned a validation error.

Expected result:

```text
422 error
Question cannot be empty. Please enter a question.
```

### Model Not Running

The backend was tested for the case where the Ollama model is not reachable. This confirms that users receive a clear error message instead of an unclear system failure.

Expected result:

```text
503 error
The AI model is not reachable. Please ensure Ollama is running.
```

---

## 5. Test Command Used

The tests were run from the project folder using Python and pytest.

Because Python was not fully available on the normal system PATH, the available Python interpreter from pgAdmin was used to run the tests:

```cmd
"C:\Program Files\PostgreSQL\18\pgAdmin 4\python\python.exe" -c "import sys; sys.path.insert(0, r'C:\Users\hp\student-support-llm'); sys.path.insert(0, r'C:\Users\hp\student-support-llm\.testdeps'); import pytest; raise SystemExit(pytest.main(['-q']))"
```

---

## 6. Test Result

The test run completed successfully.

```text
4 passed, 1 warning in 1.05s
```

The warning was a dependency deprecation warning from FastAPI/Starlette's test client. It did not affect the test result because all four tests passed successfully.

Screenshot evidence:

```text
docs/screenshots/role5_pytest_success.png
```

---

## 7. Quality Assurance Summary

Role 5 was completed successfully. The backend API was tested for normal successful behavior and important error cases. The tests confirmed that the `/health` endpoint works, the `/ask` endpoint returns an answer, empty questions are rejected, and model connection failures are handled clearly.

These tests improve the reliability of the project and provide evidence that the backend behaves correctly under expected and error conditions.
