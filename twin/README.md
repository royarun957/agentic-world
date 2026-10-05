# Digital Twin

A personal AI chatbot that answers questions about Arunendu Roy's career, experience, and skills. It uses Gemini through its OpenAI-compatible API, a Gradio interface, and optional Pushover notifications for contact requests and unanswered questions.

## Features

- Answers professional questions using a LinkedIn profile and personal summary
- Records visitor contact details through tool calling
- Reports questions it cannot answer through Pushover
- Includes a responsive custom Gradio theme
- Supports light and dark mode

## Requirements

- Python 3.12 or newer
- A Google AI API key
- Optional Pushover credentials for notifications

## Setup

From the repository root, install the dependencies:

```bash
uv sync
```

Create a `.env` file in the repository root:

```env
GOOGLE_API_KEY=your_google_api_key
PUSHOVER_USER=your_pushover_user_key
PUSHOVER_TOKEN=your_pushover_application_token
```

`PUSHOVER_USER` and `PUSHOVER_TOKEN` are only needed for contact and unanswered-question notifications. Never commit the `.env` file.

## Run

The app must run from the `twin` directory because it loads `linkedin.pdf` and `summary.txt` using relative paths:

```bash
cd twin
uv run python app.py
```

Open the URL displayed in the terminal, usually:

```text
http://127.0.0.1:7860
```

Stop the server with `Ctrl+C`.

## Customize

- Replace `linkedin.pdf` with your exported LinkedIn profile.
- Update `summary.txt` with a short personal introduction.
- Edit the behavior and guardrails in `context.py`.
- Change the model in `app.py`.
- Adjust the interface theme in `styles.py`.
- Modify notification tools in `tools.py`.

Restart the app after changing the profile, summary, prompt, or styles.

## Project Structure

```text
twin/
├── app.py           # Gradio app and Gemini client
├── context.py       # Profile loading and system prompt
├── tools.py         # Contact and unanswered-question tools
├── styles.py        # Theme, examples, and browser behavior
├── summary.txt      # Personal summary
├── linkedin.pdf     # LinkedIn profile used as context
└── requirements.txt # Minimal Python dependencies
```

## Alternative Installation

Without `uv`, create a virtual environment and install the local requirements:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r twin/requirements.txt
cd twin
python app.py
```
