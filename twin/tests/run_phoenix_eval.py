"""Evaluate the digital twin's multi-turn conversations with DeepEval and log the
scores to a local Phoenix.

Start the dashboard first (leave it running, UI at http://localhost:6006):

    uv run phoenix serve

Then, from the repository root:

    uv run python twin/tests/run_phoenix_eval.py
"""

import os
import sys
from pathlib import Path

from deepeval.metrics import ConversationCompletenessMetric, KnowledgeRetentionMetric, TurnRelevancyMetric
from deepeval.models import GeminiModel
from deepeval.test_case import ConversationalTestCase, Turn
from dotenv import load_dotenv
from phoenix.client import Client
from phoenix.client.experiments import create_evaluator

# twin/ is a flat app (app.py imports `context`, `tools`, `styles` directly),
# not a package, so put it on sys.path and import app as a top-level module.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import chat  # noqa: E402

load_dotenv(Path(__file__).resolve().parents[2] / ".env", override=True)

PHOENIX_URL = os.getenv("PHOENIX_BASE_URL", "http://localhost:6006")
DATASET_NAME = "twin-conversations"
THRESHOLD = 0.7

judge = GeminiModel(
    model="gemini-3.5-flash-lite",
    api_key=os.getenv("GOOGLE_API_KEY"),
)

client = Client(base_url=PHOENIX_URL)

# 1. Each dataset example is one conversation: the user messages to send in order.
#    The last conversation states facts up front and refers back to them later, so
#    KnowledgeRetentionMetric has something to check.
conversations = [
    {
        "messages": [
            "What are your strongest technical skills?",
            "how to reach out",
        ]
    },
    {
        "messages": [
            "Tell me about your career background.",
            "Which of those roles used AI the most?",
            "Can I get in touch with you about it?",
        ]
    },
    {
        "messages": [
            "Hi, I'm Priya and I'm hiring a senior Python engineer at Acme Robotics.",
            "Which of your skills would fit that kind of role?",
            "Great. Summarise why you'd suit the role I mentioned, and address me by name.",
        ]
    },
]
dataset = client.datasets.create_dataset(name=DATASET_NAME, inputs=conversations)


# 2. The task under test: replay the conversation through the real twin chat
#    function, carrying history between turns, and return the resulting Turns.
def twin_task(input: dict) -> dict:
    turns: list[dict] = []
    for user_message in input["messages"]:
        reply = chat(user_message, turns)
        turns.append({"role": "user", "content": user_message})
        turns.append({"role": "assistant", "content": reply})
    return {"turns": turns}


# 3. Wrap each DeepEval conversational metric as its own Phoenix evaluator, so every
#    metric gets a separate score, label and explanation in the dashboard.
def _conversation(output: dict) -> ConversationalTestCase:
    return ConversationalTestCase(
        turns=[Turn(role=t["role"], content=t["content"]) for t in output["turns"]]
    )


def _score(metric, output: dict) -> tuple[float, str, str]:
    metric.measure(_conversation(output))
    label = "PASS" if metric.is_successful() else "FAIL"
    return metric.score, label, metric.reason


@create_evaluator(name="DeepEval Turn Relevancy")
def deepeval_turn_relevancy(output: dict) -> tuple[float, str, str]:
    return _score(
        TurnRelevancyMetric(threshold=THRESHOLD, async_mode=False), output
    )


@create_evaluator(name="DeepEval Knowledge Retention")
def deepeval_knowledge_retention(output: dict) -> tuple[float, str, str]:
    return _score(
        KnowledgeRetentionMetric(threshold=THRESHOLD, async_mode=False),
        output,
    )

@create_evaluator(name="DeepEval Conversation Completeness")
def deepeval_conversation_completeness(output: dict) -> tuple[float, str, str]:
    return _score(
        ConversationCompletenessMetric(threshold=THRESHOLD, async_mode=False),
        output,
    )

# 4. Run the experiment and push the results to the dashboard.
experiment = client.experiments.run_experiment(
    dataset=dataset,
    task=twin_task,
    evaluators=[deepeval_turn_relevancy, deepeval_knowledge_retention, deepeval_conversation_completeness],
    experiment_name="twin-deepeval-turn-relevancy-and-retention-and-completeness",
)
