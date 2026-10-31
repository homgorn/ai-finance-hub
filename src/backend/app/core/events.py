from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol


@dataclass
class Event:
    task_id: str
    tenant_id: str
    type: str
    data: dict[str, Any]
    created_at: str


class EventStore(Protocol):
    def append(self, task_id: str, tenant_id: str, event_type: str, data: dict[str, Any]) -> None: ...

    def list_by_task(self, task_id: str) -> list[Event]: ...

    def count(self) -> int: ...


class InMemoryEventStore:
    def __init__(self) -> None:
        self._events: list[Event] = []

    def append(self, task_id: str, tenant_id: str, event_type: str, data: dict[str, Any]) -> None:
        self._events.append(
            Event(
                task_id=task_id,
                tenant_id=tenant_id,
                type=event_type,
                data=data,
                created_at=datetime.now(timezone.utc).isoformat(),
            )
        )

    def list_by_task(self, task_id: str) -> list[Event]:
        return [e for e in self._events if e.task_id == task_id]

    def count(self) -> int:
        return len(self._events)


class SQLiteEventStore:
    def __init__(self, db_path: str = ".runtime/events.db") -> None:
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
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT NOT NULL,
                    tenant_id TEXT NOT NULL,
                    type TEXT NOT NULL,
                    data_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def append(self, task_id: str, tenant_id: str, event_type: str, data: dict[str, Any]) -> None:
        with self._connection() as conn:
            conn.execute(
                "INSERT INTO events(task_id, tenant_id, type, data_json, created_at) VALUES (?, ?, ?, ?, ?)",
                (
                    task_id,
                    tenant_id,
                    event_type,
                    json.dumps(data, ensure_ascii=False),
                    datetime.now(timezone.utc).isoformat(),
                ),
            )
            conn.commit()

    def list_by_task(self, task_id: str) -> list[Event]:
        with self._connection() as conn:
            rows = conn.execute(
                "SELECT task_id, tenant_id, type, data_json, created_at FROM events WHERE task_id = ? ORDER BY id",
                (task_id,),
            ).fetchall()
        return [
            Event(task_id=r[0], tenant_id=r[1], type=r[2], data=json.loads(r[3]), created_at=r[4])
            for r in rows
        ]

    def count(self) -> int:
        with self._connection() as conn:
            row = conn.execute("SELECT COUNT(*) FROM events").fetchone()
        return int(row[0]) if row else 0
