"""
Defines a TaskQueue interface that is consumed
on producer side.
"""

from typing import Protocol

from layout_generator.queue.producer.nats_producer import NATSProducer
from layout_generator.types import GenerateLayoutRequest, GenerateLayoutResult, TaskStatus


class TaskQueue(Protocol):
    @classmethod
    def get_instance(cls) -> "TaskQueue": ...

    def enqueue_task(self, payload: GenerateLayoutRequest) -> str: ...
    def get_task_status(self, task_id: str) -> TaskStatus | None: ...
    def get_task_results(self, task_id: str) -> GenerateLayoutResult | None: ...


def get_task_queue() -> TaskQueue:
    return NATSProducer.get_instance() # For now do this instead of a proper dependency injection.
