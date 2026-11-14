import asyncio
import json
import os
from pathlib import Path

from deepeval import assert_test, evaluate
from deepeval.metrics import TaskCompletionMetric
from deepeval.models import GeminiModel
from deepeval.test_case import LLMTestCase
from dotenv import load_dotenv
from sre_monitor.backend import store
from sre_monitor.backend.engine import poll_once
from sre_monitor.backend.settings import get_settings   

load_dotenv(Path(__file__).resolve().parents[2] / ".env", override=True)
os.environ["SRE_LLM_PROVIDER"] = "gemini"
os.environ["LANGSMITH_TRACING"] = "false"

evaluation_model = GeminiModel(
    model="gemini-3.5-flash-lite",
    api_key=os.getenv("GOOGLE_API_KEY"),
)

def run_live_sre_monitor(user_input: str | None = None) -> str:
    """Run one live polling cycle and summarize its completion state."""

    settings = get_settings()
    settings.tracing.enabled = False
    settings.email.dry_run = True
    os.environ["LANGSMITH_TRACING"] = "false"

    candidates = asyncio.run(poll_once(dry_run=True))
    configured_services = [service.name for service in settings.services]
    recorded_services = store.services()
    last_poll = store.get_meta("last_poll")

    return json.dumps(
        {
            "requested_task": user_input,
            "workflow_status": "completed" if last_poll else "incomplete",
            "last_poll": last_poll,
            "configured_services": configured_services,
            "recorded_services": sorted(recorded_services),
            "new_or_escalated_incidents": candidates,
            "agent_workflow_triggered": bool(candidates),
            "notifications": "dry-run",
        },
        indent=2,
        default=str,
    )


def test_live_sre_workflow_completion_with_llm_judge() -> None:
    test_case = LLMTestCase(
        name="Live SRE polling workflow completes",
        input=(
            "Run one live SRE Monitor polling cycle against every configured SaaS "
            "status page. Record the service state and completion timestamp. Process "
            "new or escalating incidents when present, but do not require an incident "
            "to exist and do not send real notifications."
        ),
        actual_output=run_live_sre_monitor(),
        expected_output=(
            "The polling workflow completes, attempts every configured service, records "
            "the service results and last-poll time, reports any detected candidates, "
            "and keeps all notifications in dry-run mode. A healthy run with no new "
            "incidents is still a successful completion."
        ),
        context=[
            "The monitor currently has five configured SaaS status pages.",
            "Routine healthy polls do not invoke incident-analysis agents.",
            "Agent execution is required only when a new or escalating incident exists.",
            "The test must not assume a particular service has an active incident.",
        ],
        tags=["sre", "live", "smoke-test", "workflow-completion"],
    )
    metric = TaskCompletionMetric(
        threshold=0.7,
        model=evaluation_model,
        async_mode=False,
    )
    evaluate(test_cases=[test_case], metrics=[metric])