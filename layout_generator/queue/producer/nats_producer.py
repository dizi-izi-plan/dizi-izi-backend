import asyncio
import atexit
import os
import threading
import uuid
from threading import Lock

from nats.aio.client import Client as NATS
from nats.js.api import StreamConfig

from layout_generator.queue.literals import ENV_KEY_NATS_URL, NATS_STREAM_NAME, NATS_SUBJECT_LAYOUT_TASKS
from layout_generator.types import GenerateLayoutRequest, GenerateLayoutResult, TaskStatus


class NATSProducer:
    """
    Implements TaskQueue interface.
    """
    @classmethod
    def get_instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = NATSProducer()
            return cls._instance
        
    def enqueue_task(self, payload: GenerateLayoutRequest) -> str:
        task_id = str(uuid.uuid4())

        coro = self._publish(
            subject=NATS_SUBJECT_LAYOUT_TASKS, 
            message=self._to_message(payload),
            headers={
                "task_id": task_id
            }
        )
        asyncio.run_coroutine_threadsafe(
            coro, 
            self._loop,
        )

        return task_id
    
    def get_task_status(self, task_id: str) -> TaskStatus | None:
        return "PENDING"  # TODO: implement with jetstream
    
    def get_task_results(self, task_id: str) -> GenerateLayoutResult | None:
        pass # TODO: implement with jetstream


    """
    
    ---------- PRIVATE METHODS AND FIELDS ----------
    
    """

    _instance = None
    _lock = Lock()

    def __init__(self):
        """
        Starts a background event loop to run async methods, 
        opens a new NATS connections,
        registers a shutdown callback on interpreter exit.
        """
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

        nats_url = os.environ.get(ENV_KEY_NATS_URL)
        if nats_url is None:
            raise Exception(f"{ENV_KEY_NATS_URL} variable not found in env")
        
        fut = asyncio.run_coroutine_threadsafe(self._setup(nats_url), self._loop)
        try:
            fut.result(timeout=3)
        except TimeoutError:
            raise Exception(f"NATSProducer init, connecting to {ENV_KEY_NATS_URL}: timeout")
        
        atexit.register(self._shutdown)

    def _run_loop(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()
        
    async def _setup(self, nats_url: str):
        self._nc = NATS()
        await self._nc.connect(servers=[nats_url])
        self._js = self._nc.jetstream()
        # Ensure the stream exists
        try:
            await self._js.add_stream(
                StreamConfig(name=NATS_STREAM_NAME, subjects=[NATS_SUBJECT_LAYOUT_TASKS])
            )
        except Exception: # TODO: silently fails if jetstream is disabled, check for Exception type
            pass

    async def _publish(self, subject: str, message: bytes, headers: dict):
        ack = await self._js.publish(subject=subject, payload=message, headers=headers)
        return str(ack.seq)
    
    @staticmethod  # TODO: who owns queue transport config?
    def _to_message(payload: GenerateLayoutRequest) -> bytes:
        return payload.model_dump_json().encode("utf-8")
    
    def _shutdown(self):
        # Step 1: Close the NATS client
        future = asyncio.run_coroutine_threadsafe(self._close_client(), self._loop)
        try:
            future.result(timeout=3)
        except Exception as e:
            print(f"NATS close failed: {e}")

        # Step 2: Stop and close the event loop
        self._loop.call_soon_threadsafe(self._loop.stop)
        self._loop.run_forever()  # allow all callbacks to complete

        self._loop.close()

    async def _close_client(self):
        await self._nc.close()
        