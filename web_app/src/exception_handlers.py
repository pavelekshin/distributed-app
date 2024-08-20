from aiohttp import web

from src.exceptions import (
    InvalidRequestError,
    NotFoundError,
)


async def not_found_error_exception_handler(
    request, exception: NotFoundError
) -> web.json_response:
    """
    Return response for NotFoundError exception.
    Used for error middleware.
    :param request: request
    :param exception: exception
    :return: web.Response
    """
    return web.json_response(
        status=404,
        data={
            "error_code": exception.error_code,
            "error_message": exception.error_message,
            "detail": exception.error_detail,
        },
    )


async def invalid_request_error_exception_handler(
    request, exception: InvalidRequestError
) -> web.json_response:
    """
    Return response for InvalidRequest exception.
    Used for error middleware.
    :param request: request
    :param exception: exception
    :return: web.Response
    """
    return web.json_response(
        status=400,
        data={
            "error_code": exception.error_code,
            "error_message": exception.error_message,
            "detail": exception.error_detail,
        },
    )


async def base_exception_handler(
    status_code: int, exception: Exception
) -> web.json_response:
    """
    Returns a Response for any unhandled exception.
    Used for error middleware.
    :param status_code: status_code
    :param exception: exception
    :return: web.Response
    """
    return web.json_response(
        status=status_code,
        data={
            "error_code": "Internal Server Error",
            "error_message": str(exception),
        },
    )
