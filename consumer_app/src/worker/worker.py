import asyncio
import json
import logging
from json import JSONDecodeError

import aio_pika  # noqa
from aio_pika.abc import AbstractIncomingMessage, AbstractQueue, AbstractRobustChannel
from pydantic import ValidationError

from src import rabbit
from src.model import UserData
from src.settings import settings
from src.worker import service
from src.worker.client import Client

logger = logging.getLogger(__name__)


async def process_message(msg: AbstractIncomingMessage) -> None:
    """
    Process messages retrieved from queue
    :param msg: AbstractIncomingMessage
    """
    async with msg.process(ignore_processed=True):
        try:
            logger.info(
                f"Message received: message_id={msg.message_id}, from={msg.consumer_tag}"
            )
            body = json.loads(msg.body.decode())
            data = UserData(**body.get("data"))
        except JSONDecodeError as err:
            logger.error(f"Error occurred: {err=}")
            await msg.reject(requeue=False)
            return
        except ValidationError as err:
            logger.error(f"Error occurred: {err=}")
            await msg.reject(requeue=False)
            return
        else:
            if not (link := body.get("link")):
                logger.error("Error occurred: 'link' not exists in received data")
                await msg.reject(requeue=False)
                return
            if row := await service.insert_message(url=link, data=data):
                client = Client()
                logger.info(f"Data saved: {row}")
                await client.url_validation(code=row.get("code"))
                await msg.ack()
            await msg.reject(requeue=True)

async def initialize_dlx_exchange(channel: AbstractRobustChannel) -> None:
    """
    Initialize DLX exchange and queue
    :param channel: channel
    :return:
    """
    dlx_exchange = await channel.declare_exchange(
        name=settings.DLX_EXCHANGE, durable=True
    )
    dlx_queue = await channel.declare_queue(name=settings.DLX_QUEUE, durable=True)
    await dlx_queue.bind(dlx_exchange)


async def initialize_common_exchange(
        channel: AbstractRobustChannel, queue_name: str
) -> AbstractQueue:
    """
    Initialize common exchange and queue
    :param channel: channel
    :param queue_name: queue name
    :return:
    """
    queue_exchange = await channel.declare_exchange(
        name=settings.COMMON_EXCHANGE, durable=True
    )
    queue = await channel.declare_queue(
        name=queue_name,
        durable=True,  # Durable queue survive broker restart
        auto_delete=False,
        arguments={
            "x-dead-letter-exchange": settings.DLX_EXCHANGE,
            "x-dead-letter-routing-key": settings.DLX_QUEUE,
            "x-message-ttl": settings.MESSAGE_TTL,
        },
    )
    await queue.bind(queue_exchange)
    return queue


async def worker(queue_name: str, name: str) -> None:
    """
    Consumes items from the RabbitMQ queue
    :param name: worker name
    :param queue_name: worker queue
    """
    async with rabbit.rabbit_client as channel:  # type: AbstractRobustChannel
        await channel.set_qos(prefetch_count=1)  # number of messages per worker
        await initialize_dlx_exchange(channel)
        queue = await initialize_common_exchange(channel, queue_name)
        logger.info(f"Worker connected to queue={queue_name}")
        await queue.consume(process_message, consumer_tag=name)
        logger.info("Waiting messages")
        await asyncio.Future()
