import unittest

from scripts.sync_skills_catalog import RepoSource, classify, discover_entries, parse_sources_yaml


class SkillSyncTests(unittest.TestCase):
    def test_classify(self):
        self.assertEqual(classify("skills/tax/SKILL.md"), "skill")
        self.assertEqual(classify("examples/agent_router.py"), "agent_asset")
        self.assertIsNone(classify("README.md"))

    def test_parse_sources_minimal(self):
        raw = """
providers:
  - name: openai
    repos:
      - owner: openai
        repo: openai-cookbook
        branch: main
        skill_path_hints:
          - examples
"""
        sources = parse_sources_yaml(raw)
        self.assertEqual(len(sources), 1)
        self.assertEqual(sources[0].provider, "openai")
        self.assertEqual(sources[0].owner, "openai")
        self.assertIn("examples", sources[0].skill_path_hints)

    def test_discover_entries_filters_hints(self):
        src = RepoSource(
            provider="openai",
            owner="openai",
            repo="openai-cookbook",
            branch="main",
            skill_path_hints=["examples"],
        )
        entries = discover_entries(src, ["examples/a/SKILL.md", "docs/agent.md", "examples/tools_router.py"])
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0].kind, "skill")


if __name__ == "__main__":
    unittest.main()
