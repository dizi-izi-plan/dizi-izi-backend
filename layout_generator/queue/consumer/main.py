import asyncio
import json

from nats.aio.client import Client as NATS

from layout_generator.queue.literals import NATS_STREAM_NAME, NATS_SUBJECT_LAYOUT_TASKS
from layout_generator.types import GenerateLayoutRequest

DURABLE_NAME = "vile_vincenzo"


async def mock_handler(msg):
    try:
        data = json.loads(msg.data.decode())
        print(f"Received task: {data}")
        

        # Validate message schema
        _ = GenerateLayoutRequest(**data)

        # Simulate processing
        # Algorithm goes here ->
        await asyncio.sleep(1)

        # Store results in jetstream

        print(f"Processed task: {data}")

    except Exception as e:
        print(f"Failed to process message: {e}")

    await msg.ack()


async def main():
    nc = NATS()
    await nc.connect()

    js = nc.jetstream()

    # Ensure the stream exists — optional if already created by producer
    # Not sure if calling this on existing stream will throw an exception
    await js.add_stream(name=NATS_STREAM_NAME, subjects=[NATS_SUBJECT_LAYOUT_TASKS])

    await js.subscribe(
        subject=NATS_SUBJECT_LAYOUT_TASKS,
        durable=DURABLE_NAME,
        stream=NATS_STREAM_NAME,
        cb=mock_handler,
        manual_ack=True
    )

    print(f"worker durable_name={DURABLE_NAME} listening on {NATS_SUBJECT_LAYOUT_TASKS} subject")
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())