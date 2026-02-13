from __future__ import annotations

from enum import Enum


class TaskStatus(str, Enum):
    submitted = "submitted"
    routed = "routed"
    queued = "queued"
    processing = "processing"
    completed = "completed"
    failed = "failed"
    rejected = "rejected"


ALLOWED_TRANSITIONS: dict[TaskStatus, set[TaskStatus]] = {
    TaskStatus.submitted: {TaskStatus.routed, TaskStatus.rejected},
    TaskStatus.routed: {TaskStatus.queued, TaskStatus.rejected},
    TaskStatus.queued: {TaskStatus.processing, TaskStatus.failed},
    TaskStatus.processing: {TaskStatus.completed, TaskStatus.failed},
    TaskStatus.completed: set(),
    TaskStatus.failed: set(),
    TaskStatus.rejected: set(),
}


def can_transition(current: TaskStatus, target: TaskStatus) -> bool:
    return target in ALLOWED_TRANSITIONS[current]
