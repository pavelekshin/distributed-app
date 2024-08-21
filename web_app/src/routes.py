import logging

from aiohttp import web
from aiohttp.web_exceptions import HTTPException
from aiohttp.web_request import Request
from pydantic import ValidationError

from src.exceptions import NotFoundError
from src.model import Message
from src.service import client, service

logger = logging.getLogger(__name__)


async def healthcheck(request: Request) -> web.json_response:
    return web.json_response(data={"status": "ok"})


async def handle_code_validate(request: Request) -> web.json_response:
    """
    URL validation, receive code via http
    :param request: Request
    :return: web.Response
    """
    logger.info(f"Message receive: {request}")
    code = str(request.match_info["code"])
    if not (row := await service.get_row_by_code(code)):
        raise NotFoundError("Code not found")
    message = Message(**row)
    status = await client.check_resource(message.original_url)
    await service.insert_message(code, message, status)
    raise web.HTTPFound(message.original_url)
