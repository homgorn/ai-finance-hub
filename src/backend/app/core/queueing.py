from __future__ import annotations

from dataclasses import dataclass
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
