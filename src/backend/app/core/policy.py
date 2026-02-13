from dataclasses import dataclass
from enum import Enum


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


@dataclass
class OpenClawPolicy:
    allow_shell: bool
    allow_browser: bool
    allow_external_network: bool
    max_tool_calls: int
    require_human_approval: bool


def evaluate_tool_access(agent_risk: RiskLevel, contains_pii: bool) -> OpenClawPolicy:
    if agent_risk is RiskLevel.high:
        return OpenClawPolicy(False, False, False, 2, True)

    if contains_pii:
        return OpenClawPolicy(False, True, False, 3, True)

    return OpenClawPolicy(False, True, True, 6, False)
