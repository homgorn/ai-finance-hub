from __future__ import annotations

from dataclasses import dataclass
from queue import Empty, Queue


@dataclass
class TaskMessage:
    task_id: str
    tenant_id: str
    idempotency_key: str


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
