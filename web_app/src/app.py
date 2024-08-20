from asyncio.log import logger

from aiohttp import web

from src.exception_handlers import (
    base_exception_handler,
    invalid_request_error_exception_handler,
    not_found_error_exception_handler,
)
from src.routes import handle_code_validate, healthcheck


async def init_app() -> web.Application:
    """
    Init application settings
    :return:
    """
    # Create webapp
    app = web.Application()
    # init webapp routes
    setup_routes(app)
    # init middlewares handlers
    setup_middlewares(app)
    return app


def create_error_middleware(overrides):
    """
    Custom middleware error handler
    :param overrides: dict with exception handlers
    :return:
    """

    @web.middleware
    async def error_middleware(request, handler):
        try:
            return await handler(request)
        except web.HTTPException as ex:
            override = overrides.get(ex.status)
            if override:
                return await override(request, ex)
            raise
        except Exception as ex:
            override = overrides.get(ex.__class__.__name__)
            if override:
                logger.error(f"Error handling {request=}")
                return await override(request, ex)
            logger.error(f"Error handling {request=}")
            return await base_exception_handler(500, ex)

    return error_middleware


def setup_routes(app: web.Application):
    app.router.add_routes(
        [
            web.post("/{code}/validate", handle_code_validate),
            web.get("/healthcheck", healthcheck),
        ]
    )


def setup_middlewares(app):
    error_middleware = create_error_middleware(
        {
            "NotFoundError": not_found_error_exception_handler,
            "InvalidRequestError": invalid_request_error_exception_handler,
        }
    )
    app.middlewares.append(error_middleware)
