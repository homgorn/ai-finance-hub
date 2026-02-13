from pydantic import BaseModel


class TrizProblem(BaseModel):
    contradiction: str
    desired_outcome: str
