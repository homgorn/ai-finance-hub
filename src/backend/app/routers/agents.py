from fastapi import APIRouter

router = APIRouter(prefix="/agents", tags=["agents"])


@router.get("")
def list_agents():
    return [
        {
            "id": "general_finance_agent",
            "role": "general",
            "risk_level": "medium",
            "allowed_domains": ["general", "portfolio"],
        },
        {
            "id": "tax_specialist",
            "role": "tax",
            "risk_level": "high",
            "allowed_domains": ["tax"],
        },
        {
            "id": "insurance_specialist",
            "role": "insurance",
            "risk_level": "medium",
            "allowed_domains": ["insurance"],
        },
        {
            "id": "compliance_guard",
            "role": "compliance",
            "risk_level": "high",
            "allowed_domains": ["compliance"],
        },
    ]
