from opik.evaluation.metrics import Hallucination, Equals
from opik.evaluation import evaluate
from opik import Opik
from opik.evaluation.metrics.llm_judges.hallucination.template import generate_query
from typing import Dict


# Define the evaluation task
def evaluation_task(x: Dict):
    metric = Hallucination()
    try:
        metric_score = metric.score(input=x["input"], output=x["llm_output"])
        hallucination_score = metric_score.value
        hallucination_reason = metric_score.reason
    except Exception as e:
        print(e)
        hallucination_score = None
        hallucination_reason = str(e)

    return {
        "hallucination_score": "yes" if hallucination_score == 1 else "no",
        "hallucination_reason": hallucination_reason,
    }


# Get the dataset
client = Opik()
dataset = client.get_dataset(name="HaluEval")

# Define the scoring metric
check_hallucinated_metric = Equals(name="Correct hallucination score")

# Add the prompt template as an experiment configuration
experiment_config = {
    "prompt_template": generate_query(
        input="{input}", context="{context}", output="{output}", few_shot_examples=[]
    )
}

res = evaluate(
    dataset=dataset,
    task=evaluation_task,
    scoring_metrics=[check_hallucinated_metric],
    experiment_config=experiment_config,
    scoring_key_mapping={
        "reference": "expected_hallucination_label",
        "output": "hallucination_score",
    },
)
