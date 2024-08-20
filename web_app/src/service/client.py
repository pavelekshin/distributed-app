import logging

import aiohttp

logger = logging.getLogger(__name__)


async def client(url) -> bool:
    """
    HTTP client for checking provided http url
    :param url: http url
    :return: bool
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return resp.ok
