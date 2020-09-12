from http import HTTPStatus
from typing import Dict, Type

from freshchat.client.responses import FreshChatResponse


class FreshChatClientException(Exception):
    """
    Class to customize exceptions of the library with attribute DEFAULT_MESSAGE
    to be returned if message isn't provided
    """

    DEFAULT_MESSAGE = "Encountered a live agent client error"

    def __init__(
        self,
        response: FreshChatResponse,
        *args,
    ) -> None:
        message: str = self.DEFAULT_MESSAGE
        if isinstance(response.body, dict):
            message = response.body.get("message")
        elif isinstance(response.body, str):
            message = response.body

        super().__init__(message, *args)
        self._message = message
        self._response = response

    @property
    def message(self) -> str:
        return self._message

    @property
    def response(self) -> FreshChatResponse:
        return self._response


class FreshChatUnauthorised(FreshChatClientException):
    """
    Class inherits from FreshChatClientException represents Unauthorized exception and
    sets DEFAULT_MESSAGE to `Access to the requested resource is unauthorised`
    """

    DEFAULT_MESSAGE = "Access to the requested resource is unauthorised"


class FreshChatForbidden(FreshChatClientException):
    """
    Class inherits from FreshChatClientException represents Forbidden access exception
    and sets DEFAULT_MESSAGE to `Access to the requested resource  is not permitted`
    """

    DEFAULT_MESSAGE = "Access to the requested resource  is not permitted"


class FreshChatNotAllowed(FreshChatClientException):
    """
    Class inherits from FreshChatClientException represents Not Allowed exception
    and sets DEFAULT_MESSAGE to `Access to the requested resource  is not allowed`
    """

    DEFAULT_MESSAGE = "Access to the requested resource  is not allowed"


class FreshChatBadRequest(FreshChatClientException):
    """
    Class inherits from FreshChatClientException represents Bad Request exception
    and sets DEFAULT_MESSAGE to `Bad request, probably due to invalid syntax or
    missing required " "fields`
    """

    DEFAULT_MESSAGE = (
        "Bad request, probably due to invalid syntax or missing required " "fields "
    )


class TooManyRequests(FreshChatClientException):
    """
    Class inherits from FreshChatClientException represents Too Many Requests exception
    and sets DEFAULT_MESSAGE to `Too many requests. Requests overcame the
    proper time limit`
    """

    DEFAULT_MESSAGE = "Too many requests. Requests overcame the proper time limit"


class ServerUnavailable(FreshChatClientException):
    """
    Class inherits from FreshChatClientException represents Unavailable Server exception
    and sets DEFAULT_MESSAGE to `The server is currently unable to handle the request
    due to a temporary overload or scheduled maintenance"`
    """

    DEFAULT_MESSAGE = (
        "The server is currently unable to handle the request due to a "
        "temporary overload or scheduled maintenance"
    )


class ResourceNotFound(FreshChatClientException):
    """
    Class inherits from FreshChatClientException represents Resource Not Found exception
    and sets DEFAULT_MESSAGE to `The requested resource was not found`
    """

    DEFAULT_MESSAGE = "The requested resource was not found"


class ServerSideError(FreshChatClientException):
    """
    Class inherits from FreshChatClientException represents Server Side Error exception
    and sets DEFAULT_MESSAGE to `Something went wrong on the server side`
    """

    DEFAULT_MESSAGE = "Something went wrong on the server side"


class Conflict(FreshChatClientException):
    """
    Class inherits from FreshChatClientException represents Conflict exception
    and sets DEFAULT_MESSAGE to `The request causes data inconsistencies`
    """

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
    """
    Class responsible to return the proper exception based on the response status code
    """

    def __new__(cls, response: FreshChatResponse) -> FreshChatClientException:
        return RESPONSE_CODE_TO_ERROR_MAPPING.get(
            response.status, FreshChatClientException
        )(response=response)
