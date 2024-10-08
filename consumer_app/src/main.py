import asyncio
import logging
import socket
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import aio_pika

from src import rabbit
from src.settings import settings
from src.worker import worker

RABBIT_URL = str(settings.RABBIT_URL)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def rabbitmq_connection() -> AsyncGenerator:
    connection = await aio_pika.connect_robust(RABBIT_URL)
    rabbit.rabbit_client = await connection.channel()
    yield
    await connection.channel().close()
    await connection.close()


async def run() -> None:
    logger.info("Starting workers")
    async with rabbitmq_connection():
        hostname = socket.gethostname()
        await worker.worker(settings.COMMON_QUEUE, f"Worker-{hostname}")
    logger.info("Connection closed")


if __name__ == "__main__":
    asyncio.run(run())
