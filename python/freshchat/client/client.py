import os
from dataclasses import asdict, dataclass, field
from typing import Any, AnyStr, Dict, List, Union
from urllib.parse import urljoin

import aiohttp
from cafeteria.logging import LoggedObject

from python.freshchat.client.exceptions import HttpResponseCodeError
from python.freshchat.client.headers import FreshChatHeaders
from python.freshchat.client.responses import FreshChatResponse

CONVERSATION_INITIAL_MESSAGE = os.environ.get(
    "CONVERSATION_INITIAL_MESSAGE", "hey dude!"
)


@dataclass(frozen=True)
class Operation:
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

    url: str = field(
        default_factory=lambda: os.environ.get(
            "FRESHCHAT_API_URL", "https://api.freshchat.com/v2/"
        )
    )
    app_id: str = None
    channel_id: str = None
    headers: FreshChatHeaders = field(default_factory=FreshChatHeaders)

    def __post_init__(self):
        if isinstance(self.headers, dict):
            self.headers = FreshChatHeaders(self.headers.get("Authorization"))

    def get_url(self, *path: str):
        """
        Method responsible to build the url using the given extras if exists

        :param path: List with the extra variables for the url, ex. user/<user_id>
        :return: URL
        """
        return (
            (
                urljoin(self.url, "/".join((str(x) for x in path)).lstrip("/"))
                if not isinstance(path, str)
                else urljoin(self.url, path.lstrip("/"))
            )
            if path
            else self.url
        )


class FreshChatClient(LoggedObject):
    """
    Class represents an HTTP client
    """

    def __init__(self, config: FreshChatConfiguration) -> None:
        self.config = config

    async def request(
        self,
        method: str,
        operation: str,
        path: Union[str, List] = None,
        params: Dict[AnyStr, Any] = None,
        body: Dict[AnyStr, Any] = None,
        headers: Dict[AnyStr, Any] = None,
    ) -> FreshChatResponse:
        """

        :param method: http method can be GET or POST
        :param operation: URL variables
        :param path: URL extra variables
        :param params: request parameters in the case of GET method
        :param body: request body in the case of POST method
        :param headers: extra headers
        :return: The response of the request using the above fields
        """
        request_headers = (
            headers.update(asdict(self.config.headers))
            if headers
            else asdict(self.config.headers)
        )

        url = (
            (
                self.config.get_url(operation, path)
                if isinstance(path, str)
                else self.config.get_url(operation, *path)
            )
            if path
            else self.config.get_url(operation)
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
                response = await FreshChatResponse.load(response)
                self.logger.debug(
                    "%s %s %d \n< %s", method, url, response.http.status, response.body
                )

                if 200 <= response.http.status < 300:
                    return response
                raise HttpResponseCodeError(response.http.status)

    async def get(
        self,
        operation: str,
        path: Union[str, List] = None,
        params: Dict[AnyStr, Any] = None,
        headers: Dict[str, Any] = None,
    ) -> FreshChatResponse:
        """
        Method used for the get requests

        :param operation: URL variables
        :param path: URL extra variables
        :param params: request parameters in the case of GET method
        :param headers: extra headers
        :return: The response of the request using the above fields
        :return: FreshChatResponse
        """
        return await self.request(
            method="GET", operation=operation, path=path, params=params, headers=headers
        )

    async def post(
        self,
        operation: str,
        path: Union[str, List] = None,
        params: Dict[AnyStr, Any] = None,
        body: Dict[AnyStr, AnyStr] = None,
        headers: Dict[str, Any] = None,
    ) -> FreshChatResponse:
        """
        Method used for the post requests
        :param operation: URL variables
        :param path: URL extra variables
        :param params: request parameters in the case of GET method
        :param body: request body in the case of POST method
        :param headers: extra headers
        :return: The response of the request using the above fields
        :return: FreshChatResponse
        """
        return await self.request(
            method="POST",
            operation=operation,
            path=path,
            params=params,
            body=body,
            headers=headers,
        )

    def __repr__(self):
        return f"{self.__class__.__name__}<{hex(id(self))}> (config={self.config})"
