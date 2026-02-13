from dataclasses import dataclass
from enum import Enum


class TaskDomain(str, Enum):
    tax = "tax"
    insurance = "insurance"
    portfolio = "portfolio"
    compliance = "compliance"
    general = "general"


@dataclass
class TaskContext:
    title: str
    description: str
    domain_hint: TaskDomain | None = None


@dataclass
class RoutingDecision:
    agent_id: str
    reason: str
    required_skills: list[str]


KEYWORD_RULES: list[tuple[set[str], TaskDomain]] = [
    ({"tax", "irs", "deduction", "налог", "ндфл"}, TaskDomain.tax),
    ({"insurance", "policy", "premium", "страхов"}, TaskDomain.insurance),
    ({"portfolio", "rebalance", "allocation"}, TaskDomain.portfolio),
    ({"kyc", "aml", "compliance", "санкц"}, TaskDomain.compliance),
]


def infer_domain(task: TaskContext) -> TaskDomain:
    if task.domain_hint:
        return task.domain_hint

    haystack = f"{task.title} {task.description}".lower()
    for keywords, domain in KEYWORD_RULES:
        if any(token in haystack for token in keywords):
            return domain
    return TaskDomain.general


def route_task(task: TaskContext) -> RoutingDecision:
    domain = infer_domain(task)
    if domain is TaskDomain.tax:
        return RoutingDecision(
            agent_id="tax_specialist",
            reason="Tax intent identified via domain hint/keywords.",
            required_skills=["FINANCIAL_ADVISOR_TAX", "PROMPT_SECURITY_AUDIT"],
        )
    if domain is TaskDomain.insurance:
        return RoutingDecision(
            agent_id="insurance_specialist",
            reason="Insurance intent identified via domain hint/keywords.",
            required_skills=["OPERATOR_WEB_AUTOMATION", "PROMPT_SECURITY_AUDIT"],
        )
    if domain is TaskDomain.compliance:
        return RoutingDecision(
            agent_id="compliance_guard",
            reason="Compliance-sensitive task routed to stricter agent.",
            required_skills=["SECURE_CODE_REVIEW", "PROMPT_SECURITY_AUDIT"],
        )
    return RoutingDecision(
        agent_id="general_finance_agent",
        reason="No strong domain signal; routed to general agent.",
        required_skills=["PROMPT_SECURITY_AUDIT"],
    )
