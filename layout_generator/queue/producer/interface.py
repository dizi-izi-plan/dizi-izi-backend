"""
Defines a TaskQueue interface that is consumed
on producer side.
"""

from typing import Protocol

from layout_generator.types import GenerateLayoutRequest, GenerateLayoutResult, TaskStatus


class TaskQueue(Protocol):
    @classmethod
    def get_instance(cls) -> "TaskQueue": ...

    def enqueue_task(self, payload: GenerateLayoutRequest) -> str: ...
    def get_task_status(self, task_id: str) -> TaskStatus | None: ...
    def get_task_results(self, task_id: str) -> GenerateLayoutResult | None: ...