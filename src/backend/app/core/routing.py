from dataclasses import dataclass
from enum import Enum
import re


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
    ({"tax", "irs", "deduction*", "налог*", "ндфл"}, TaskDomain.tax),
    ({"insurance", "policy", "policies", "premium*", "страхов*"}, TaskDomain.insurance),
    ({"portfolio", "rebalance", "allocation"}, TaskDomain.portfolio),
    ({"kyc", "aml", "compliance", "санкц*"}, TaskDomain.compliance),
]

_TOKEN_RE = re.compile(r"\w+")


@dataclass(frozen=True)
class KeywordMatcher:
    exact_tokens: frozenset[str]
    prefix_tokens: tuple[str, ...]

    @classmethod
    def from_keywords(cls, keywords: set[str]) -> "KeywordMatcher":
        exact_tokens: set[str] = set()
        prefix_tokens: list[str] = []

        for raw_keyword in keywords:
            keyword = raw_keyword.lower().strip()
            if not keyword:
                continue
            if keyword.endswith("*"):
                prefix = keyword[:-1]
                if prefix:
                    prefix_tokens.append(prefix)
                continue
            exact_tokens.add(keyword)

        return cls(
            exact_tokens=frozenset(exact_tokens),
            prefix_tokens=tuple(sorted(set(prefix_tokens), key=len, reverse=True)),
        )

    def matches(self, tokens: set[str]) -> bool:
        if tokens & self.exact_tokens:
            return True
        if not self.prefix_tokens:
            return False
        return any(token.startswith(self.prefix_tokens) for token in tokens)


ROUTING_BY_DOMAIN: dict[TaskDomain, RoutingDecision] = {
    TaskDomain.tax: RoutingDecision(
        agent_id="tax_specialist",
        reason="Tax intent identified via domain hint/keywords.",
        required_skills=["FINANCIAL_ADVISOR_TAX", "PROMPT_SECURITY_AUDIT"],
    ),
    TaskDomain.insurance: RoutingDecision(
        agent_id="insurance_specialist",
        reason="Insurance intent identified via domain hint/keywords.",
        required_skills=["OPERATOR_WEB_AUTOMATION", "PROMPT_SECURITY_AUDIT"],
    ),
    TaskDomain.compliance: RoutingDecision(
        agent_id="compliance_guard",
        reason="Compliance-sensitive task routed to stricter agent.",
        required_skills=["SECURE_CODE_REVIEW", "PROMPT_SECURITY_AUDIT"],
    ),
    TaskDomain.portfolio: RoutingDecision(
        agent_id="portfolio_specialist",
        reason="Portfolio intent identified via domain hint/keywords.",
        required_skills=["PORTFOLIO_REBALANCE", "PROMPT_SECURITY_AUDIT"],
    ),
}

GENERAL_ROUTING_DECISION = RoutingDecision(
    agent_id="general_finance_agent",
    reason="No strong domain signal; routed to general agent.",
    required_skills=["PROMPT_SECURITY_AUDIT"],
)




def _validate_routing_decision(decision: RoutingDecision, label: str) -> None:
    if not decision.agent_id:
        raise ValueError(f"Routing decision '{label}' must define a non-empty agent_id")
    if not decision.reason:
        raise ValueError(f"Routing decision '{label}' must define a non-empty reason")
    if not decision.required_skills:
        raise ValueError(f"Routing decision '{label}' must define at least one required skill")
    if len(decision.required_skills) != len(set(decision.required_skills)):
        raise ValueError(f"Routing decision '{label}' contains duplicate required skills")
    if "PROMPT_SECURITY_AUDIT" not in decision.required_skills:
        raise ValueError(
            f"Routing decision '{label}' must include PROMPT_SECURITY_AUDIT in required_skills"
        )


def _validate_routing_configuration() -> None:
    _validate_routing_decision(GENERAL_ROUTING_DECISION, "general")
    for domain, decision in ROUTING_BY_DOMAIN.items():
        _validate_routing_decision(decision, domain.value)

    expected_domains = {domain for domain in TaskDomain if domain is not TaskDomain.general}
    configured_domains = set(ROUTING_BY_DOMAIN)

    missing_domains = expected_domains - configured_domains
    if missing_domains:
        missing = ", ".join(sorted(domain.value for domain in missing_domains))
        raise ValueError(f"Missing routing decisions for domains: {missing}")

    extra_domains = configured_domains - expected_domains
    if extra_domains:
        extra = ", ".join(sorted(domain.value for domain in extra_domains))
        raise ValueError(f"Unexpected routing decisions for unsupported domains: {extra}")

    keyword_domains_list = [domain for _, domain in KEYWORD_RULES]
    keyword_domains = set(keyword_domains_list)
    if len(keyword_domains_list) != len(keyword_domains):
        raise ValueError("KEYWORD_RULES must define at most one rule entry per domain")

    missing_keyword_domains = expected_domains - keyword_domains
    if missing_keyword_domains:
        missing = ", ".join(sorted(domain.value for domain in missing_keyword_domains))
        raise ValueError(f"Missing keyword rules for domains: {missing}")

    exact_keyword_owners: dict[str, TaskDomain] = {}
    for keywords, domain in KEYWORD_RULES:
        matcher = KeywordMatcher.from_keywords(keywords)
        if not matcher.exact_tokens and not matcher.prefix_tokens:
            raise ValueError(f"Keyword rule for domain '{domain.value}' is empty after normalization")
        for keyword in matcher.exact_tokens:
            owner = exact_keyword_owners.get(keyword)
            if owner is not None and owner is not domain:
                raise ValueError(
                    f"Exact keyword '{keyword}' is assigned to multiple domains: {owner.value}, {domain.value}"
                )
            exact_keyword_owners[keyword] = domain


_validate_routing_configuration()


def _tokenize(text: str) -> set[str]:
    return set(_TOKEN_RE.findall(text.lower()))


def _compile_keyword_rules() -> tuple[tuple[KeywordMatcher, TaskDomain], ...]:
    return tuple((KeywordMatcher.from_keywords(keywords), domain) for keywords, domain in KEYWORD_RULES)


COMPILED_KEYWORD_RULES: tuple[tuple[KeywordMatcher, TaskDomain], ...] = _compile_keyword_rules()


def infer_domain(task: TaskContext) -> TaskDomain:
    if task.domain_hint:
        return task.domain_hint

    tokens = _tokenize(f"{task.title} {task.description}")
    if not tokens:
        return TaskDomain.general

    for matcher, domain in COMPILED_KEYWORD_RULES:
        if matcher.matches(tokens):
            return domain
    return TaskDomain.general


def _clone_decision(decision: RoutingDecision) -> RoutingDecision:
    return RoutingDecision(
        agent_id=decision.agent_id,
        reason=decision.reason,
        required_skills=list(decision.required_skills),
    )


def route_task(task: TaskContext) -> RoutingDecision:
    domain = infer_domain(task)
    return _clone_decision(ROUTING_BY_DOMAIN.get(domain, GENERAL_ROUTING_DECISION))
