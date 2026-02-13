from fastapi import APIRouter, Query

from ..core.policy import RiskLevel, evaluate_tool_access

router = APIRouter(prefix="/security", tags=["security"])


@router.get("/policy")
def policy(
    risk: RiskLevel = Query(default=RiskLevel.medium),
    contains_pii: bool = Query(default=False),
):
    return evaluate_tool_access(risk, contains_pii).__dict__
