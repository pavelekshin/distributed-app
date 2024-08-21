import logging

import aiohttp

logger = logging.getLogger(__name__)


async def check_resource(url: str) -> bool:
    """
    HTTP client for checking provided http url
    :param url: http url
    :return: bool
    """
    async with aiohttp.ClientSession() as session:
        logger.info(f"Make request to {url}")
        async with session.get(url) as resp:
            return resp.ok
