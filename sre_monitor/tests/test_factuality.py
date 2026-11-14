from contextvars import ContextVar

from deepeval.metrics import GEval
from deepeval.test_case import SingleTurnParams
from deepeval.models import GeminiModel
from dotenv import load_dotenv
import os
from deepeval.dataset import EvaluationDataset, Golden
from pathlib import Path
from deepeval.tracing import observe, update_current_trace
import json
from langchain_core.messages import HumanMessage, SystemMessage

from sre_monitor.backend.agents import TriageReport
from sre_monitor.backend.prompts import TRIAGE_PROMPT
from sre_monitor.backend.settings import get_llm

load_dotenv(Path(__file__).resolve().parents[2] / ".env", override=True)

evaluation_model = GeminiModel(
    model="gemini-3.5-flash-lite",
    api_key=os.getenv("GOOGLE_API_KEY"),
)

expected_trace_output: ContextVar[str | None] = ContextVar(
    "expected_trace_output",
    default=None,
)


@observe(name="run_triage_prompt", type="agent")
def run_triage_prompt(user_input: str) -> str:
    """Run the production triage prompt and return its structured decision."""
    expected_output = expected_trace_output.get()
    if expected_output is not None:
        update_current_trace(input=user_input, expected_output=expected_output)
    result = get_llm().with_structured_output(TriageReport).invoke(
        [
            SystemMessage(content=TRIAGE_PROMPT),
            HumanMessage(content=user_input),
        ]
    )
    return result.model_dump_json()

#GEval is probabilistic, so scoring may vary
correctness = GEval(
    name="correctness",
    criteria="Determine if the actual output is factually correct as the expected output.Misleading information, such as misinformation, disinformation, or fake news, is not allowed.",
    model=evaluation_model,
    threshold=0.8,
    evaluation_params=[
        SingleTurnParams.INPUT,
        SingleTurnParams.ACTUAL_OUTPUT,
        SingleTurnParams.EXPECTED_OUTPUT,
    ]
)

dataset = EvaluationDataset(
    goldens=[
        Golden(
            input=json.dumps(
                [
                    {
                        "key": "test:pull-requests-degraded",
                        "is_service_incident": True,
                        "summary": "Only degraded components on pull requests",
                        "affected": ["API"],
                        "service": "GitHub",
                        "title": "Pull requests are degraded",
                        "kind": "new",
                        "vendor_impact": "partial",
                        "status": "investigating",
                        "components_affected": 2,
                        "vendor_page_status": "partial: Degraded",
                        "degraded_components_on_page": 2,
                    }
                ],
                indent=2,
            ),
            expected_output=json.dumps(
                {
                    "severity": "SEV3",
                    "rationale": "Only degraded components on pull requests",
                    "key": "test:pull-requests-degraded",
                },
                indent=2,
            ),
        ),
        Golden(
            input=json.dumps(
                [
                    {
                        "key": "test:global-api-outage",
                        "is_service_incident": True,
                        "summary": "The core API is unavailable in all regions worldwide.",
                        "affected": ["API", "all regions"],
                        "service": "ExampleCloud",
                        "title": "Global API outage",
                        "kind": "new",
                        "vendor_impact": "critical",
                        "status": "investigating",
                        "components_affected": 12,
                        "vendor_page_status": "critical: Major outage",
                        "degraded_components_on_page": 12,
                    }
                ],
                indent=2,
            ),
            expected_output=json.dumps(
                {
                    "severity": "SEV1",
                    "rationale": "The core API is unavailable in all regions worldwide.",
                    "key": "test:global-api-outage",
                },
                indent=2,
            ),
        ),
    ]
)

def test_factuality_evaluation() -> None:
    for golden in dataset.evals_iterator(metrics=[correctness]):
        token = expected_trace_output.set(golden.expected_output)
        try:
            run_triage_prompt(golden.input)
        finally:
            expected_trace_output.reset(token)
    