import gradio as gr
import requests

BACKEND_URL = "http://127.0.0.1:8000/ask"
TIMEOUT_SECONDS = 15


def query_support_assistant(question: str) -> str:
    """Send the user's question to the backend and return the assistant's reply."""

    # Validate the input before calling the API.
    question = (question or "").strip()
    if not question:
        return "Please enter a question about university services before submitting."

    payload = {"question": question}
    headers = {"Content-Type": "application/json"}

    try:
        # Send a POST request to the backend /ask endpoint.
        response = requests.post(BACKEND_URL, json=payload, headers=headers, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        # Backend is unreachable.
        return "Unable to connect to the server. Please make sure the backend is running at http://127.0.0.1:8000."
    except requests.exceptions.Timeout:
        # The request timed out while waiting for the model.
        return "The server is taking too long to respond. Please try again in a moment."
    except requests.exceptions.HTTPError:
        # The backend returned an HTTP error status.
        return f"Server returned an error ({response.status_code}). Please try again."
    except requests.exceptions.RequestException:
        # A generic network error occurred.
        return "An unexpected network error occurred. Please try again."

    try:
        # Parse the backend JSON response.
        data = response.json()
    except ValueError:
        return "Received an invalid response from the server."

    # Extract the answer from expected response keys.
    answer = data.get("answer") or data.get("response") or data.get("result")
    if not answer:
        return "The server returned an empty reply. Please try again with a different question."

    return answer


def create_interface() -> gr.Blocks:
    """Build the Gradio interface for the student support assistant."""
    custom_css = """
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: #eef2f7;
        color: #1b1f23;
    }
    .gradio-container {
        max-width: 900px;
        margin: 20px auto;
        padding: 22px;
        background: #ffffff;
        border-radius: 16px;
        box-shadow: 0 16px 40px rgba(15, 23, 42, 0.08);
    }
    h1, h2, p {
        margin: 0;
    }
    .gradio-textbox, .gradio-button {
        font-size: 1rem;
    }
    .footer {
        color: #4b5563;
        font-size: 0.95rem;
    }
    """

    with gr.Blocks(css=custom_css) as demo:
        gr.Markdown(
            """
            # University Student Support Assistant
            Welcome to the student support assistant. Ask questions about registration, exams, fees, ICT support, library services, or campus resources.
            """
        )

        with gr.Row():
            question_input = gr.Textbox(
                label="Ask a question",
                placeholder="Example: How do I register for next semester's courses?",
                lines=3,
                max_lines=5,
            )

        submit_button = gr.Button("Submit question")

        answer_output = gr.Textbox(
            label="Assistant response",
            interactive=False,
            lines=10,
        )

        submit_button.click(
            fn=query_support_assistant,
            inputs=question_input,
            outputs=answer_output,
        )

        gr.Markdown(
            "---\n"
            "**Tips:** Use clear questions about university services and wait for the response indicator while the assistant processes your request."
        )

        gr.Markdown(
            "<div class='footer'>This interface sends your question to the local backend at <code>http://127.0.0.1:8000/ask</code> and displays the answer from the language model.</div>",
            elem_id="footer",
        )

    return demo


if __name__ == "__main__":
    interface = create_interface()
    interface.launch(server_name="127.0.0.1", server_port=7860, share=False)
