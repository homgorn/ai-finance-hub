import tempfile
import unittest
from pathlib import Path

from src.backend.app.core.events import SQLiteEventStore


class SQLiteEventStoreTests(unittest.TestCase):
    def test_append_and_list(self):
        with tempfile.TemporaryDirectory() as td:
            db = Path(td) / "events.db"
            store = SQLiteEventStore(str(db))
            store.append("t1", "tenant1", "task_submitted", {"agent": "tax_specialist"})
            store.append("t1", "tenant1", "status_changed", {"status": "queued"})

            events = store.list_by_task("t1")
            self.assertEqual(len(events), 2)
            self.assertEqual(events[0].type, "task_submitted")
            self.assertEqual(store.count(), 2)


if __name__ == "__main__":
    unittest.main()
