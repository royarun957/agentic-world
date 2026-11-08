# Agentic World

A collection of practical AI-agent projects built to explore conversational assistants, coordinated multi-agent research, and production-oriented reliability automation.

Each project is self-contained and has a dedicated README with setup, configuration, and operating details.

## Projects

### [Digital Twin](twin/README.md)

A personal AI chatbot that represents Arunendu Roy and answers questions about his career, experience, and technical background.

Technical overview:

- **Interface:** Gradio with a custom responsive light/dark theme
- **Model:** Gemini through its OpenAI-compatible API
- **Context:** Personal summary plus text extracted from a LinkedIn PDF
- **Tools:** Records contact requests and unanswered questions
- **Notifications:** Optional Pushover delivery
- **Key files:** `app.py`, `context.py`, `tools.py`, and `styles.py`

Run:

```bash
cd twin
uv run python app.py
```

### [Stock Picker Crew](stock_picker/README.md)

A hierarchical multi-agent research workflow that finds trending companies in a selected sector, researches them, and chooses one company for further consideration.

Technical overview:

- **Framework:** CrewAI with a hierarchical manager
- **Agents:** Financial News Analyst, Financial Researcher, Stock Picker, and Manager
- **Model:** Gemini for reasoning and memory analysis
- **Memory:** Unified semantic memory using Gemini embeddings
- **Research:** Serper web search
- **Output:** Structured JSON research artifacts and a Markdown decision report
- **Notifications:** SMTP email

Run:

```bash
cd stock_picker
uv sync
crewai run
```

> The stock picker is an educational research project, not financial advice.

### [SRE Monitor](sre_monitor/README.md)

An incident-intelligence system that monitors SaaS status pages, detects new or escalating incidents, verifies high-severity impact, and sends operational alerts.

Technical overview:

- **Orchestration:** LangGraph with explicit specialist handoffs and guardrails
- **Collection:** Statuspage JSON APIs, RSS feeds, and the Zscaler Trust Portal
- **Analysis:** Configurable Gemini or OpenAI model
- **Verification:** Serper evidence checks for SEV1 and SEV2 incidents
- **Notifications:** HTML email and priority Pushover alerts
- **Persistence:** SQLite operational state and notification history
- **Interface:** FastAPI, JSON endpoints, and a read-only live dashboard
- **Observability:** Optional LangSmith tracing

Run the monitor and dashboard in separate terminals:

```bash
uv run -m sre_monitor.backend.engine
uv run uvicorn sre_monitor.backend.api:app --port 8100
```

Then open [http://localhost:8100](http://localhost:8100).

## Repository Layout

```text
agentic-world/
├── twin/          # Personal Gemini chatbot
├── stock_picker/  # CrewAI market-research workflow
├── sre_monitor/   # LangGraph incident-intelligence system
├── pyproject.toml # Shared Python dependencies
├── uv.lock        # Reproducible dependency lock
└── .env           # Local secrets; excluded from Git
```

## Shared Setup

Install `uv`, then synchronize the repository environment:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync
```

Create a repository-level `.env` containing only the credentials needed by the projects you run:

```env
GOOGLE_API_KEY=...
OPENAI_API_KEY=...
SERPER_API_KEY=...

EMAIL_ADDRESS=...
EMAIL_SMTP_SERVER=...
EMAIL_APP_PASSWORD=...

PUSHOVER_USER=...
PUSHOVER_TOKEN=...
LANGSMITH_API_KEY=...
```

The `.env` file is ignored by Git. Never commit API keys, SMTP passwords, or notification tokens.

## Documentation

- [Digital Twin setup and customization](twin/README.md)
- [Stock Picker architecture and configuration](stock_picker/README.md)
- [SRE Monitor operations and configuration](sre_monitor/README.md)
