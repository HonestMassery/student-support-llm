import socket
import gradio as gr
import requests

BACKEND_URL = "http://127.0.0.1:8000/ask"
TIMEOUT_SECONDS = 120
CUSTOM_CSS = """
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: #eef2f7;
    color: #1b1f23;
    margin: 0;
}
.gradio-container {
    width: 100%;
    max-width: 100%;
    margin: 0 auto;
    padding: 0;
    background: transparent;
}
.header {
    margin-bottom: 20px;
}
.header h1 {
    margin: 0;
    font-size: 2.2rem;
    font-weight: 700;
}
.header p {
    margin: 8px 0 0;
    color: #4b5563;
    font-size: 1rem;
}
#chat-panel {
    width: 80vw;
    max-width: 1100px;
    min-width: 600px;
    margin: 0 auto;
    background: #ffffff;
    border-radius: 22px;
    box-shadow: 0 24px 80px rgba(15, 23, 42, 0.12);
    padding: 20px;
}
#chat-wrapper {
    display: flex;
    flex-direction: column;
    gap: 16px;
}
#chatbot {
    min-height: 70vh;
    max-height: 70vh;
    overflow: auto;
}
#chatbot .message {
    border-radius: 18px;
    padding: 14px 16px;
}
#chatbot .message.user {
    background: #eef7ff;
    border: 1px solid #dbeafe;
}
#chatbot .message.assistant {
    background: #f7f7f9;
    border: 1px solid #e5e7eb;
}
#input-row {
    position: sticky;
    bottom: 0;
    width: 100%;
    margin-top: 0;
    padding-top: 10px;
    background: linear-gradient(180deg, rgba(255,255,255,0.0), rgba(255,255,255,0.95));
    z-index: 20;
}
#chat-input {
    width: 100%;
}
#chat-input textarea {
    width: 100%;
    min-height: 60px;
    padding: 18px 80px 18px 20px !important;
    border-radius: 999px !important;
    border: 1px solid transparent !important;
    background: #ffffff;
    box-shadow: 0 1px 12px rgba(15, 23, 42, 0.1) !important;
    resize: none !important;
}
#send-button {
    position: absolute;
    right: 16px;
    top: 50%;
    transform: translateY(-50%);
    height: 50px;
    width: 50px;
    border-radius: 50%;
    background: #4f46e5;
    color: white;
    border: none;
    box-shadow: 0 16px 30px rgba(79, 70, 229, 0.22);
    padding: 0;
    font-size: 1.3rem;
    line-height: 1;
    z-index: 30;
}
#send-button:hover {
    background: #4338ca;
}
"""


def get_free_port(start: int = 7860, end: int = 7999) -> int:
    """Return the first available TCP port in the requested range."""
    for port in range(start, end + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    raise OSError("No free ports available in the requested range")


def query_support_assistant(question: str) -> str:
    """Send the user's question to the backend and return the assistant's reply."""

    question = (question or "").strip()
    if not question:
        return "Please enter a question about university services before submitting."

    payload = {"question": question}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(BACKEND_URL, json=payload, headers=headers, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        return "Unable to connect to the server. Please make sure the backend is running at http://127.0.0.1:8000."
    except requests.exceptions.Timeout:
        return "The server is taking too long to respond. Please try again in a moment."
    except requests.exceptions.HTTPError:
        if response.status_code == 503:
            return "The server could not reach the local AI model. Please make sure Ollama is installed and running at http://localhost:11434."
        return f"Server returned an error ({response.status_code}). Please try again."
    except requests.exceptions.RequestException:
        return "An unexpected network error occurred. Please try again."

    try:
        data = response.json()
    except ValueError:
        return "Received an invalid response from the server."

    answer = data.get("answer") or data.get("response") or data.get("result")
    if not answer:
        return "The server returned an empty reply. Please try again with a different question."

    return answer


def append_chat_history(question: str, history: list[dict[str, str]]) -> tuple[list[dict[str, str]], str, list[dict[str, str]]]:
    """Send the user's question to the backend and append the result to chat history."""
    question = (question or "").strip()
    if not question:
        return history, "", history

    answer = query_support_assistant(question)
    history = history + [
        {"role": "user", "content": question},
        {"role": "assistant", "content": answer},
    ]
    return history, "", history


def create_interface() -> gr.Blocks:
    """Build the Gradio interface for the student support assistant."""
    with gr.Blocks() as demo:
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown(
                    """
                    <div class='header'>
                        <h1>University Student Support Assistant</h1>
                        <p>Ask questions about registration, exams, fees, ICT support, library services, or campus resources.</p>
                    </div>
                    """
                )

        with gr.Row():
            with gr.Column(scale=1, elem_id="chat-panel"):
                with gr.Column(elem_id="chat-wrapper"):
                    chatbot = gr.Chatbot(value=[], label=None, elem_id="chatbot", layout="bubble", show_label=False, height=600)
                    conversation_state = gr.State([])

                    with gr.Row(elem_id="input-row"):
                        question_input = gr.Textbox(
                            label="",
                            show_label=False,
                            placeholder="Type your message...",
                            lines=2,
                            max_lines=4,
                            elem_id="chat-input",
                        )
                        submit_button = gr.Button("→", elem_id="send-button")

                submit_button.click(
                    fn=append_chat_history,
                    inputs=[question_input, conversation_state],
                    outputs=[chatbot, question_input, conversation_state],
                )
                question_input.submit(
                    fn=append_chat_history,
                    inputs=[question_input, conversation_state],
                    outputs=[chatbot, question_input, conversation_state],
                )

    return demo


if __name__ == "__main__":
    interface = create_interface()
    interface.launch(
        server_name="127.0.0.1",
        server_port=get_free_port(),
        share=False,
        css=CUSTOM_CSS,
    )
