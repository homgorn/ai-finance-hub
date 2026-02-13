from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass
class Event:
    task_id: str
    tenant_id: str
    type: str
    data: dict[str, Any]
    created_at: str


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
