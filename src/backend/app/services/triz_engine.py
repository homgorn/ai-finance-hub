from ..models.triz import TrizProblem


def generate_triz_seed(problem: TrizProblem) -> dict:
    return {
        "contradiction": problem.contradiction,
        "desired_outcome": problem.desired_outcome,
        "principle_hint": "Segmentation",
    }
