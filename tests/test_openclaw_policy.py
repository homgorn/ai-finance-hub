import unittest

from src.backend.app.core.policy import RiskLevel, evaluate_tool_access


class OpenClawPolicyTests(unittest.TestCase):
    def test_high_risk_is_strict(self):
        policy = evaluate_tool_access(RiskLevel.high, contains_pii=False)
        self.assertFalse(policy.allow_browser)
        self.assertTrue(policy.require_human_approval)

    def test_pii_enables_partial_lockdown(self):
        policy = evaluate_tool_access(RiskLevel.medium, contains_pii=True)
        self.assertTrue(policy.allow_browser)
        self.assertFalse(policy.allow_external_network)
        self.assertTrue(policy.require_human_approval)

    def test_medium_without_pii(self):
        policy = evaluate_tool_access(RiskLevel.medium, contains_pii=False)
        self.assertTrue(policy.allow_external_network)
        self.assertFalse(policy.require_human_approval)


if __name__ == "__main__":
    unittest.main()
