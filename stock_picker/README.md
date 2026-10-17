# Stock Picker Crew

A hierarchical [CrewAI](https://crewai.com) workflow that researches trending companies in a chosen market sector and selects one company for further consideration.

The project uses Gemini for agent reasoning, Google embeddings for memory, Serper for current web search, and SMTP for email notifications.

> This project is an educational research tool, not financial advice.

## Workflow

The manager coordinates three specialist agents:

1. **Financial News Analyst** — finds two or three companies currently trending in the requested sector.
2. **Senior Financial Researcher** — researches each company’s market position, outlook, and investment potential.
3. **Stock Picker** — compares the research, selects one company, explains the decision, and sends an email notification.

The crew writes intermediate and final results to:

```text
output/
├── trending_companies.json
├── research_report.json
└── decision.md
```

## Technology

- Python 3.10–3.13
- CrewAI 1.14.4
- Gemini `gemini-3.5-flash-lite`
- Gemini `gemini-embedding-001` for semantic memory
- Serper for web search
- SMTP for email delivery
- `uv` for dependency management

## Setup

Install `uv` if needed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install the project dependencies:

```bash
cd stock_picker
uv sync
```

The crew explicitly loads the shared `.env` file from the parent `agentic-world` directory. Add these values to `agentic-world/.env`:

```env
GOOGLE_API_KEY=your_google_api_key
SERPER_API_KEY=your_serper_api_key
EMAIL_ADDRESS=your_email@example.com
EMAIL_SMTP_SERVER=smtp.example.com
EMAIL_APP_PASSWORD=your_email_app_password
```

The email tool sends the notification from and to `EMAIL_ADDRESS` using STARTTLS on port `587`. Use an app password rather than your normal email password.

## Run

From the `stock_picker` directory:

```bash
crewai run
```

Enter a sector when prompted:

```text
Enter the sector: technology
```

You can also invoke the project entry point directly:

```bash
uv run run_crew
```

## Project Structure

```text
stock_picker/
├── pyproject.toml
├── README.md
└── src/stock_picker/
    ├── main.py
    ├── crew.py
    ├── config/
    │   ├── agents.yaml
    │   └── tasks.yaml
    └── tools/
        └── messenger.py
```

- `main.py` collects the sector and starts the crew.
- `crew.py` defines the agents, tasks, manager, structured outputs, and memory.
- `agents.yaml` contains agent roles, goals, and Gemini model settings.
- `tasks.yaml` defines the workflow, context dependencies, and output files.
- `messenger.py` provides the email tool used by the stock picker.

## Customization

- Change agent behavior or models in `config/agents.yaml`.
- Change task instructions and outputs in `config/tasks.yaml`.
- Adjust the process, memory, tools, or structured schemas in `crew.py`.
- Change runtime inputs in `main.py`.
- Update SMTP behavior in `tools/messenger.py`.

## Notes

- No OpenAI key is required when both unified memory and embeddings are configured for Gemini.
- CrewAI’s current built-in Google embedding adapter uses the deprecated `google.generativeai` package and may display a `FutureWarning`. This warning does not stop execution.
- If tracing is not configured for your CrewAI account, set `tracing=False` in `crew.py` to avoid telemetry authorization errors.
