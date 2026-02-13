import unittest

from src.backend.app.core.lifecycle import TaskStatus, can_transition


class LifecycleTests(unittest.TestCase):
    def test_valid_transition_chain(self):
        self.assertTrue(can_transition(TaskStatus.submitted, TaskStatus.routed))
        self.assertTrue(can_transition(TaskStatus.routed, TaskStatus.queued))
        self.assertTrue(can_transition(TaskStatus.queued, TaskStatus.processing))
        self.assertTrue(can_transition(TaskStatus.processing, TaskStatus.completed))

    def test_retry_transitions(self):
        self.assertTrue(can_transition(TaskStatus.processing, TaskStatus.queued))
        self.assertTrue(can_transition(TaskStatus.failed, TaskStatus.queued))

    def test_invalid_transition(self):
        self.assertFalse(can_transition(TaskStatus.submitted, TaskStatus.completed))


if __name__ == "__main__":
    unittest.main()
