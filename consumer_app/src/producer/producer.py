import asyncio
import json
import logging
from datetime import datetime
from uuid import uuid4

import aio_pika
from aio_pika import DeliveryMode

from src import rabbit
from src.main import rabbitmq_connection
from src.settings import settings

logger = logging.getLogger(__name__)


async def data_generator(ids: int, job_id: str) -> list[dict[str, str | int]]:
    """
    Generates data
    :param ids: range
    :param job_id: job uuid
    :return:
    """
    return [
        {
            "id": job_id,
            "ts": datetime.now().isoformat(),
            "link": "https://pypi.org/bcd123",
            "data": {
                "acc_id": str(ids),
                "unsubscribe": False,
                "msg_id": str(ids),
            },
        },
        {
            "id": job_id,
            "ts": datetime.now().isoformat(),
            "link": "https://pypi.org/",
            "data": {
                "acc_id": str(ids),
                "unsubscribe": False,
                "msg_id": str(ids),
            },
        },
    ]


async def producer(queue_name: str) -> None:
    """
    Puts all the requested work into the work queue.
    :param queue_name: producer queue
    """
    async with rabbit.rabbit_client as channel:  # type: aio_pika.abc.AbstractRobustChannel
        for i in range(10):
            job_id = str(uuid4())
            for data in await data_generator(i, job_id):
                message_json = json.dumps(data).encode()
                timestamp = datetime.timestamp(datetime.now())
                ch = await channel.declare_exchange("exchange-common", durable=True)
                await ch.publish(  # publish message to queue
                    aio_pika.Message(
                        body=message_json,
                        timestamp=timestamp,
                        correlation_id=job_id,
                        delivery_mode=DeliveryMode.PERSISTENT,
                        # PERSISTENT messages prevent message lose while RabbitMQ is restarted
                    ),
                    routing_key=queue_name,
                )
                logger.info(f"New Job {job_id} is published!")
                await asyncio.sleep(1)


async def run():
    logger.info("Starting producer")
    async with rabbitmq_connection():
        await producer(settings.COMMON_QUEUE)


if __name__ == "__main__":
    asyncio.run(run())
