"""
Service interface for submitting layout generation tasks and retrieving their status and results.


Provides the following functions:
    - create_task: Submit a layout generation request.
    - get_task_status: Check the current status of a task.
    - get_task_results: Retrieve the result of a completed task.
"""


from layout_generator.queue.producer.interface import get_task_queue
from layout_generator.types import GenerateLayoutRequest, GenerateLayoutResult, TaskStatus


def create_task(room_description: GenerateLayoutRequest) -> str:
    """
    Creates and enqueues a layout generation task using the given room description.
    Returns a unique task ID.
    """
    
    q = get_task_queue()
    return q.enqueue_task(payload=room_description)


def get_task_status(task_id: str) -> TaskStatus | None:
    """
    Checks the status of a layout generation task.
    Returns the current task status or None if not found.
    """ 

    q = get_task_queue()
    return q.get_task_status(task_id)


def get_task_results(task_id: str) -> GenerateLayoutResult | None:
    """
    Retrieves the result of a completed layout generation task.
    Returns either the layout result or None if task is not successfully completed 
    or doesn't exist.
    """

    q = get_task_queue()
    return q.get_task_results(task_id)
