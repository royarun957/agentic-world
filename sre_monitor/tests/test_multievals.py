import json
import os
from pathlib import Path

from deepeval.dataset import EvaluationDataset, Golden
from deepeval.metrics import PromptAlignmentMetric, StepEfficiencyMetric, TaskCompletionMetric, AnswerRelevancyMetric
from deepeval.models import GeminiModel
from deepeval.tracing import observe
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage

from sre_monitor.backend.agents import TriageReport
from sre_monitor.backend.prompts import TRIAGE_PROMPT
from sre_monitor.backend.settings import get_llm

load_dotenv(Path(__file__).resolve().parents[2] / ".env", override=True)

evaluation_model = GeminiModel(
    model="gemini-3.5-flash-lite",
    api_key=os.getenv("GOOGLE_API_KEY"),
)

@observe(name="run_triage_prompt", type="agent")
def run_triage_prompt(user_input: str) -> str:
    """Run the production triage prompt and return its structured decision."""
    result = get_llm().with_structured_output(TriageReport).invoke(
        [
            SystemMessage(content=TRIAGE_PROMPT),
            HumanMessage(content=user_input),
        ]
    )
    return result.model_dump_json()


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

step_efficiency_metric = StepEfficiencyMetric(
    threshold=0.5,
    model=evaluation_model,
    async_mode=False,
)

task_completion_metric = TaskCompletionMetric(
    threshold=0.8,
    model=evaluation_model,
    async_mode=False,
)

prompt_alignment_metric = PromptAlignmentMetric(
    prompt_instructions=[TRIAGE_PROMPT],
    model=evaluation_model,
    threshold=0.8,
    async_mode=False,
)

answer_relevance_metric = AnswerRelevancyMetric(model=evaluation_model, threshold=0.5, async_mode=False)


def test_triage_prompt_evaluation() -> None:
    for golden in dataset.evals_iterator(
        metrics=[prompt_alignment_metric, task_completion_metric, step_efficiency_metric, answer_relevance_metric]
    ):
        run_triage_prompt(golden.input)