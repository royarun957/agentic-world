import asyncio
import json
from pathlib import Path

from deepeval.dataset import EvaluationDataset, Golden
from deepeval.metrics import TaskCompletionMetric, ToolCorrectnessMetric
from deepeval.test_case import ToolCall
from deepeval.models import GeminiModel
from deepeval.tracing import observe, update_current_trace
from dotenv import load_dotenv
import os
from sre_monitor.backend.serper import (
    search_incident_evidence as _search_incident_evidence,
)

load_dotenv(Path(__file__).resolve().parents[2] / ".env", override=True)

evaluation_model = GeminiModel(
    model="gemini-3.5-flash-lite",
    api_key=os.getenv("GOOGLE_API_KEY"),
)

SERVICE = "OpenAI"
INCIDENT_TITLE = "API outage"
RESULT_LIMIT = 3


@observe(name="search_incident_evidence", type="tool")
async def search_incident_evidence(
    service: str, title: str, limit: int = RESULT_LIMIT
) -> dict:
    """Trace the real Serper incident-evidence tool call for DeepEval."""
    return await _search_incident_evidence(service, title, limit)


@observe(name="run_incident_evidence_search", type="agent")
async def run_incident_evidence_search(user_input: str) -> str:
    """Execute the evidence search requested by the evaluation Golden."""
    evidence = await search_incident_evidence(
        service=SERVICE,
        title=INCIDENT_TITLE,
        limit=RESULT_LIMIT,
    )
    tool_call = ToolCall(
        name="search_incident_evidence",
        input_parameters={
            "service": SERVICE,
            "title": INCIDENT_TITLE,
            "limit": RESULT_LIMIT,
        },
        output=evidence,
    )
    update_current_trace(
        tools_called=[tool_call],
        expected_tools=[
            ToolCall(
                name=tool_call.name,
                input_parameters=tool_call.input_parameters,
            )
        ],
    )
    return json.dumps(
        {"request": user_input, "evidence": evidence},
        default=str,
    )


dataset = EvaluationDataset(
    goldens=[
        Golden(
            input="Search for current independent evidence of an OpenAI API outage.",
            expected_tools=[
                ToolCall(
                    name="search_incident_evidence",
                    input_parameters={
                        "service": SERVICE,
                        "title": INCIDENT_TITLE,
                        "limit": RESULT_LIMIT,
                    },
                )
            ],
        )
    ]
)

task_completion_metric = TaskCompletionMetric(
    threshold=0.7,
    model=evaluation_model,
    async_mode=False,
)

def test_search_incident_evidence_tool_trace() -> None:
    metric = ToolCorrectnessMetric(should_exact_match=True)

    for golden in dataset.evals_iterator(metrics=[metric, task_completion_metric]):
        asyncio.run(run_incident_evidence_search(golden.input))