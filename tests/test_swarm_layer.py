import unittest

from src.backend.app.core.routing import TaskContext, TaskDomain, infer_domain, route_task


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


if __name__ == "__main__":
    unittest.main()
