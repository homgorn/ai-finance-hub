from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from queue import Empty, Queue
from typing import Protocol


@dataclass
class TaskMessage:
    task_id: str
    tenant_id: str
    idempotency_key: str


class TaskQueue(Protocol):
    def publish(self, msg: TaskMessage) -> None: ...

    def consume_nowait(self) -> TaskMessage | None: ...

    def lag(self) -> int: ...


class InMemoryTaskQueue:
    def __init__(self) -> None:
        self._q: Queue[TaskMessage] = Queue()

    def publish(self, msg: TaskMessage) -> None:
        self._q.put(msg)

    def consume_nowait(self) -> TaskMessage | None:
        try:
            return self._q.get_nowait()
        except Empty:
            return None

    def lag(self) -> int:
        return self._q.qsize()


class SQLiteTaskQueue:
    def __init__(self, db_path: str = ".runtime/queue.db") -> None:
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._ensure_schema()

    def _conn(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    @contextmanager
    def _connection(self):
        """Yield a connection and always release its OS file handle."""
        conn = self._conn()
        try:
            yield conn
        finally:
            conn.close()

    def _ensure_schema(self) -> None:
        with self._connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS task_queue (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT NOT NULL,
                    tenant_id TEXT NOT NULL,
                    idempotency_key TEXT NOT NULL,
                    consumed INTEGER NOT NULL DEFAULT 0
                )
                """
            )
            conn.commit()

    def publish(self, msg: TaskMessage) -> None:
        with self._connection() as conn:
            conn.execute(
                "INSERT INTO task_queue(task_id, tenant_id, idempotency_key, consumed) VALUES (?, ?, ?, 0)",
                (msg.task_id, msg.tenant_id, msg.idempotency_key),
            )
            conn.commit()

    def consume_nowait(self) -> TaskMessage | None:
        with self._connection() as conn:
            # Serialize the claim so two local workers cannot consume one row.
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute(
                "SELECT id, task_id, tenant_id, idempotency_key FROM task_queue WHERE consumed = 0 ORDER BY id LIMIT 1"
            ).fetchone()
            if not row:
                conn.rollback()
                return None
            updated = conn.execute(
                "UPDATE task_queue SET consumed = 1 WHERE id = ? AND consumed = 0", (row[0],)
            )
            if updated.rowcount != 1:
                conn.rollback()
                return None
            conn.commit()
            return TaskMessage(task_id=row[1], tenant_id=row[2], idempotency_key=row[3])

    def lag(self) -> int:
        with self._connection() as conn:
            row = conn.execute("SELECT COUNT(*) FROM task_queue WHERE consumed = 0").fetchone()
        return int(row[0]) if row else 0


def build_task_queue(backend: str, sqlite_path: str) -> TaskQueue:
    if backend == "sqlite":
        return SQLiteTaskQueue(sqlite_path)
    if backend == "inmemory":
        return InMemoryTaskQueue()
    raise ValueError(f"Unsupported queue backend: {backend}")
