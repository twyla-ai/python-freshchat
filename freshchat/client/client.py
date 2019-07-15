from typing import Any, AnyStr, Dict, Optional

import aiohttp
from cafeteria.logging import LoggedObject

from freshchat.client.configuration import FreshChatConfiguration
from freshchat.client.exceptions import HttpResponseCodeError
from freshchat.client.responses import FreshChatResponse


class FreshChatClient(LoggedObject):
    """
    Class represents an HTTP client
    """

    def __init__(self, config: FreshChatConfiguration) -> None:
        self.config = config

    async def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[AnyStr, Any]] = None,
        json: Optional[Dict[AnyStr, Any]] = None,
        headers: Optional[Dict[AnyStr, Any]] = None,
    ) -> FreshChatResponse:
        """

        :param method: http request method
        :param endpoint: Resource endpoint
        :param params: request parameters
        :param json: request json body
        :param headers: Additional request headers
        """
        request_headers = (
            headers.update(self.config.authorization_header)
            if headers
            else self.config.authorization_header
        )

        url = self.config.get_url(endpoint=endpoint)

        self.logger.debug(
            "%s %s \n> params: %s\n> headers: %s%s",
            method,
            url,
            params,
            headers,
            f"\n> body: {json}" if json else "",
        )
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=method,
                url=url,
                params=params,
                json=json,
                headers=request_headers,
            ) as response:
                response = await FreshChatResponse.load(response=response)
                self.logger.debug(
                    "%s %s %d \n< %s", method, url, response.http.status, response.body
                )

                if 200 <= response.http.status < 300:
                    return response
                raise HttpResponseCodeError(response.http.status)

    async def get(
        self,
        endpoint: str,
        params: Optional[Dict[AnyStr, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> FreshChatResponse:
        """
        Method used for the get requests

        :param endpoint: Resource endpoint
        :param params: request parameters
        :param headers: Additional request headers
        """
        return await self.request(
            method="GET", endpoint=endpoint, params=params, headers=headers
        )

    async def post(
        self,
        endpoint: str,
        params: Optional[Dict[AnyStr, Any]] = None,
        json: Optional[Dict[AnyStr, AnyStr]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> FreshChatResponse:
        """
        Method used for the post requests

        :param endpoint: Resource endpoint
        :param params: request parameters
        :param json: request json body
        :param headers: Additional request headers
        """
        return await self.request(
            method="POST", endpoint=endpoint, params=params, json=json, headers=headers
        )

    async def put(
        self,
        endpoint: str,
        params: Optional[Dict[AnyStr, Any]] = None,
        json: Optional[Dict[AnyStr, AnyStr]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> FreshChatResponse:
        """
        Method used for the put requests

        :param endpoint: Resource endpoint
        :param params: request parameters
        :param json: request json body
        :param headers: Additional request headers
        """
        return await self.request(
            method="PUT", endpoint=endpoint, params=params, json=json, headers=headers
        )

    def __repr__(self):
        return (
            f"{self.__class__.__name__}<{hex(id(self))}> (config={repr(self.config)})"
        )
