import sys
from pathlib import Path

from deepeval.test_case import ConversationalTestCase, Turn
from deepeval import evaluate
from deepeval.metrics import TurnRelevancyMetric


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import chat  # noqa: E402
turns = []
history = []

for user_query in [
    "What are your strongest technical skills?",
    "how to reach out"
]:
    response = chat(user_query, history)
    turns.append(Turn(role="user", content=user_query))
    turns.append(Turn(role="assistant", content=response))

test_cases = ConversationalTestCase(
    turns=turns
)
turn_relevance_metric = TurnRelevancyMetric(threshold=0.7)

evaluate(test_cases = [test_cases], metrics=[turn_relevance_metric])
