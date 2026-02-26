import unittest

from src.backend.app.core.routing import (
    KEYWORD_RULES,
    ROUTING_BY_DOMAIN,
    GENERAL_ROUTING_DECISION,
    KeywordMatcher,
    TaskContext,
    TaskDomain,
    infer_domain,
    route_task,
)


class SwarmLayerTests(unittest.TestCase):
    def test_domain_hint_has_priority(self):
        task = TaskContext(title="General", description="Need help", domain_hint=TaskDomain.insurance)
        self.assertEqual(infer_domain(task), TaskDomain.insurance)

    def test_keyword_routing_tax(self):
        task = TaskContext(title="Tax deductions", description="Need IRS filing checklist")
        decision = route_task(task)
        self.assertEqual(decision.agent_id, "tax_specialist")
        self.assertIn("FINANCIAL_ADVISOR_TAX", decision.required_skills)

    def test_default_route_general(self):
        task = TaskContext(title="Planning", description="Help with goals")
        decision = route_task(task)
        self.assertEqual(decision.agent_id, "general_finance_agent")

    def test_empty_and_punctuation_only_input_routes_general(self):
        empty_task = TaskContext(title="", description="")
        empty_decision = route_task(empty_task)
        self.assertEqual(empty_decision.agent_id, "general_finance_agent")

        punct_task = TaskContext(title="!!!", description="... ---")
        punct_decision = route_task(punct_task)
        self.assertEqual(punct_decision.agent_id, "general_finance_agent")

    def test_keyword_matching_uses_tokens_not_substrings(self):
        task = TaskContext(title="Editor syntax help", description="Need better syntax highlighting")
        decision = route_task(task)
        self.assertEqual(decision.agent_id, "general_finance_agent")

    def test_prefix_keywords_match_declined_word_forms(self):
        task = TaskContext(title="Проверка санкций", description="Нужны шаги AML")
        decision = route_task(task)
        self.assertEqual(decision.agent_id, "compliance_guard")

    def test_suffix_word_forms_match_tax_keywords(self):
        task = TaskContext(title="Filing", description="Need help with deductions and налоги")
        decision = route_task(task)
        self.assertEqual(decision.agent_id, "tax_specialist")

    def test_plural_insurance_terms_route_correctly(self):
        task = TaskContext(title="Policies review", description="Compare premiums and coverage")
        decision = route_task(task)
        self.assertEqual(decision.agent_id, "insurance_specialist")

    def test_tokenization_handles_punctuation_boundaries(self):
        task = TaskContext(title="Tax-help", description="Need: IRS, deductions.")
        decision = route_task(task)
        self.assertEqual(decision.agent_id, "tax_specialist")

    def test_portfolio_keywords_route_to_portfolio_specialist(self):
        task = TaskContext(title="Portfolio rebalance", description="Need allocation check")
        decision = route_task(task)
        self.assertEqual(decision.agent_id, "portfolio_specialist")
        self.assertIn("PORTFOLIO_REBALANCING", decision.required_skills)

    def test_domain_hint_routes_portfolio(self):
        task = TaskContext(title="Anything", description="General", domain_hint=TaskDomain.portfolio)
        decision = route_task(task)
        self.assertEqual(decision.agent_id, "portfolio_specialist")

    def test_route_decision_is_not_shared_mutable_instance(self):
        task = TaskContext(title="Tax deductions", description="Need IRS filing checklist")
        decision = route_task(task)
        decision.required_skills.append("MUTATION")

        decision_again = route_task(task)
        self.assertNotIn("MUTATION", decision_again.required_skills)


    def test_keyword_matching_is_case_insensitive_for_latin_and_cyrillic(self):
        tax_task = TaskContext(title="НАЛОГИ", description="Need IRS help")
        tax_decision = route_task(tax_task)
        self.assertEqual(tax_decision.agent_id, "tax_specialist")

        compliance_task = TaskContext(title="AML CHECK", description="Проверка САНКЦИЙ")
        compliance_decision = route_task(compliance_task)
        self.assertEqual(compliance_decision.agent_id, "compliance_guard")

    def test_keyword_matcher_normalizes_and_deduplicates_prefixes(self):
        matcher = KeywordMatcher.from_keywords({" Tax ", "DEDuction*", "deduction*", "*", ""})
        self.assertIn("tax", matcher.exact_tokens)
        self.assertEqual(matcher.prefix_tokens, ("deduction",))

    def test_rule_priority_prefers_first_matching_domain(self):
        task = TaskContext(title="Tax and insurance", description="Need policy and IRS guidance")
        decision = route_task(task)
        self.assertEqual(decision.agent_id, "tax_specialist")

    def test_all_non_general_domains_have_routing_templates(self):
        expected_domains = {domain for domain in TaskDomain if domain is not TaskDomain.general}
        self.assertEqual(set(ROUTING_BY_DOMAIN.keys()), expected_domains)

    def test_all_non_general_domains_have_keyword_rules(self):
        keyword_domains = {domain for _, domain in KEYWORD_RULES}
        expected_domains = {domain for domain in TaskDomain if domain is not TaskDomain.general}
        self.assertEqual(keyword_domains, expected_domains)

    def test_keyword_rules_have_single_entry_per_domain(self):
        keyword_domains = [domain for _, domain in KEYWORD_RULES]
        self.assertEqual(len(keyword_domains), len(set(keyword_domains)))

    def test_general_route_is_cloned_per_request(self):
        task = TaskContext(title="Unknown", description="No matching keywords")
        decision = route_task(task)
        decision.required_skills.append("MUTATION")

        decision_again = route_task(task)
        self.assertEqual(decision_again.agent_id, GENERAL_ROUTING_DECISION.agent_id)
        self.assertNotIn("MUTATION", decision_again.required_skills)


if __name__ == "__main__":
    unittest.main()
