from pydantic import BaseModel, Field

from ..core.policy import RiskLevel


class AgentDescriptor(BaseModel):
    id: str = Field(min_length=2)
    role: str
    risk_level: RiskLevel = RiskLevel.medium
    allowed_domains: list[str] = []
