from src.constants import ErrorCode, ErrorMessage


class DetailedError(Exception):
    error_message = ErrorMessage.INTERNAL_SERVER_ERROR
    error_code = ErrorCode.INTERNAL_SERVER_ERROR
    error_detail = None

    def __init__(self, detail=None):
        self.error_detail = detail


class NotFoundError(DetailedError):
    error_code = ErrorCode.INTERNAL_SERVER_ERROR
    error_message = ErrorMessage.CODE_NOT_FOUND


class InvalidRequestError(DetailedError):
    error_code = ErrorCode.INVALID_REQUEST
    error_message = ErrorMessage.INVALID_REQUEST
