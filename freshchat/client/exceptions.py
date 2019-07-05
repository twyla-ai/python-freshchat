from http import HTTPStatus
from typing import Dict, Type

from aiohttp import ClientResponse

from freshchat.client.responses import FreshChatResponseBody


class FreshChatClientException(Exception):
    """
    Class to customize exceptions of the library
    """

    DEFAULT_MESSAGE = "Encountered a live agent client error"

    def __init__(
        self,
        message: FreshChatResponseBody = None,
        response: ClientResponse = None,
        *args,
    ) -> None:
        message = message or self.DEFAULT_MESSAGE
        super().__init__(message, *args)
        self._message = message
        self._response = response

    @property
    def message(self) -> FreshChatResponseBody:
        return self._message

    @property
    def response(self) -> ClientResponse:
        return self._response


class FreshChatUnauthorised(FreshChatClientException):
    DEFAULT_MESSAGE = "Access to the requested resource is unauthorised"


class FreshChatForbidden(FreshChatClientException):
    DEFAULT_MESSAGE = "Access to the requested resource  is not permitted"


class FreshChatNotAllowed(FreshChatClientException):
    DEFAULT_MESSAGE = "Access to the requested resource  is not allowed"


class FreshChatBadRequest(FreshChatClientException):
    DEFAULT_MESSAGE = (
        "Bad request, probably due to invalid syntax or missing required " "fields "
    )


class TooManyRequests(FreshChatClientException):
    DEFAULT_MESSAGE = "Too many requests. Requests overcame the proper time limit"


class ServerUnavailable(FreshChatClientException):
    DEFAULT_MESSAGE = (
        "The server is currently unable to handle the request due to a "
        "temporary overload or scheduled maintenance"
    )


class ResourceNotFound(FreshChatClientException):
    DEFAULT_MESSAGE = "The requested resource was not found"


class ServerSideError(FreshChatClientException):
    DEFAULT_MESSAGE = "Something went wrong on the server side"


class Conflict(FreshChatClientException):
    DEFAULT_MESSAGE = "The request causes data inconsistencies"


RESPONSE_CODE_TO_ERROR_MAPPING: Dict[int, Type[FreshChatClientException]] = {
    HTTPStatus.BAD_REQUEST: FreshChatBadRequest,
    HTTPStatus.NOT_FOUND: ResourceNotFound,
    HTTPStatus.INTERNAL_SERVER_ERROR: ServerSideError,
    HTTPStatus.UNAUTHORIZED: FreshChatUnauthorised,
    HTTPStatus.FORBIDDEN: FreshChatForbidden,
    HTTPStatus.METHOD_NOT_ALLOWED: FreshChatNotAllowed,
    HTTPStatus.TOO_MANY_REQUESTS: TooManyRequests,
    HTTPStatus.SERVICE_UNAVAILABLE: ServerUnavailable,
    HTTPStatus.CONFLICT: Conflict,
}


class HttpResponseCodeError:
    def __new__(cls, code) -> FreshChatClientException:
        return RESPONSE_CODE_TO_ERROR_MAPPING.get(code, FreshChatClientException)()
