import os
from dataclasses import dataclass, asdict
from enum import Enum
from http import HTTPStatus
from typing import AnyStr, Any, Dict, List
from urllib.parse import urljoin

import aiohttp
from cafeteria.logging import LoggedObject

from freshchat.liveagent.chat.exceptions import (
    FreshChatBadRequest,
    ResourceNotFound,
    ServerSideError,
    FreshChatUnauthorised,
    FreshChatForbidden,
    TooManyRequests,
    ServerUnavailable,
)
from freshchat.liveagent.chat.headers import FreshChatHeaders
from freshchat.liveagent.chat.responses import FreshChatResponse


class Operation(Enum):
    """
    Class which provides the possible endpoints for Freshchat API
    """

    AGENTS = "/agents"
    GROUPS = "/groups"
    USERS = "/users"
    CONVERSATION = "/conversations"
    CHANNELS = "/channels"


@dataclass
class FreshChatConfiguration:
    """
    Class represents the basic URL configuration for Freshchat
    """

    @property
    def url_prefix(self):
        if "ENV" in os.environ and os.environ["ENV"] == "TEST":
            return "http://127.0.0.1:8000/"
        else:
            return f"https://api.freshchat.com/v2/users"

    def get_url(self, *extras: List[Any]):
        """
        Method responsible to build the url using the given extras if exists

        :param extras: List with the extra variables for the url, ex. user/<user_id>
        :return: URL
        """
        return (
            urljoin(self.url_prefix, "/".join(extras).lstrip("/").lstrip("/"))
            if extras
            else self.url_prefix
        )


class FreshChatClient(LoggedObject):
    """
    Class represents an HTTP client
    """

    def __init__(
        self, headers: FreshChatHeaders, config: FreshChatConfiguration
    ) -> None:
        self.headers = headers
        self.config = config

    async def request(
        self,
        method: str,
        operation: Operation,
        url_extras: List = None,
        params: Dict[AnyStr, Any] = None,
        body: Dict[AnyStr, Any] = None,
        headers: Dict[AnyStr, Any] = None,
    ) -> FreshChatResponse:
        """

        :param method: http method can be GET or POST
        :param operation: URL variables
        :param url_extras: URL extra variables
        :param params: request parameters in the case of GET method
        :param body: request body in the case of POST method
        :param headers: extra headers
        :return: The response of the request using the above fields
        """

        request_headers = (
            headers.update(asdict(self.headers)) if headers else asdict(self.headers)
        )

        url = (
            self.config.get_url(operation.value, *url_extras)
            if url_extras
            else self.config.get_url(operation.value)
        )

        self.logger.debug(
            "%s %s \n> params: %s\n> headers: %s%s",
            method,
            url,
            params,
            headers,
            f"\n> body: {body}" if body else "",
        )
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=method,
                url=url,
                params=params,
                json=body,
                headers=request_headers,
            ) as response:
                print(await response.json())
                response = await FreshChatResponse.load(response)
                self.logger.debug(
                    "%s %s %d \n< %s", method, url, response.http.status, response.body
                )

                if response.http.status == HTTPStatus.BAD_REQUEST:
                    raise FreshChatBadRequest(
                        message=response.body, response=response.http
                    )
                elif response.http.status == HTTPStatus.NOT_FOUND:
                    raise ResourceNotFound(
                        message=response.body, response=response.http
                    )
                elif response.http.status == HTTPStatus.INTERNAL_SERVER_ERROR:
                    raise ServerSideError(message=response.body, response=response.http)
                elif response.http.status == HTTPStatus.UNAUTHORIZED:
                    raise FreshChatUnauthorised(
                        message=response.body, response=response.http
                    )
                elif response.http.status == HTTPStatus.FORBIDDEN:
                    raise FreshChatForbidden(
                        message=response.body, response=response.http
                    )
                elif response.http.status == HTTPStatus.TOO_MANY_REQUESTS:
                    raise TooManyRequests(message=response.body, response=response.http)
                elif response.http.status == HTTPStatus.SERVICE_UNAVAILABLE:
                    raise ServerUnavailable(
                        message=response.body, response=response.http
                    )
                return response

    async def get(
        self,
        operation: Operation,
        url_extras: List = None,
        params: Dict[AnyStr, Any] = None,
        headers: Dict[str, Any] = None,
    ) -> FreshChatResponse:
        """
        Method used for the get requests
        :param operation: URL variables
        :param url_extras: URL extra variables
        :param params: request parameters in the case of GET method
        :param headers: extra headers
        :return: The response of the request using the above fields
        :return: FreshChatResponse
        """
        return await self.request(
            method="GET",
            operation=operation,
            url_extras=url_extras,
            params=params,
            headers=headers,
        )

    async def post(
        self,
        operation: Operation,
        url_extras: List = None,
        params: Dict[AnyStr, Any] = None,
        body: Dict[AnyStr, AnyStr] = None,
        headers: Dict[str, Any] = None,
    ) -> FreshChatResponse:
        """
        Method used for the post requests
        :param operation: URL variables
        :param url_extras: URL extra variables
        :param params: request parameters in the case of GET method
        :param body: request body in the case of POST method
        :param headers: extra headers
        :return: The response of the request using the above fields
        :return: FreshChatResponse
        """
        return await self.request(
            method="POST",
            operation=operation,
            url_extras=url_extras,
            params=params,
            body=body,
            headers=headers,
        )
