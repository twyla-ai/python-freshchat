from __future__ import annotations

import json
from json import JSONDecodeError
from typing import Union, Dict, AnyStr, Any

from aiohttp import ClientResponse

FreshChatResponseBody = Union[str, Dict[AnyStr, Any]]


class FreshChatResponse:
    """
    Class represent http response
    """

    def __init__(
        self, response: ClientResponse, body: FreshChatResponseBody = None
    ) -> None:
        self._response = response
        self._body: FreshChatResponseBody = body

    @property
    def http(self) -> ClientResponse:
        """
        Property returns aiohttp.ClientResponse
        """
        return self._response

    @property
    def body(self) -> FreshChatResponseBody:
        """
        Property returns FreshChatResponseBody which can be either a String or a
        Dictionary
        """
        return self._body

    @staticmethod
    def _decode(body: str):
        try:
            return json.loads(body)
        except JSONDecodeError:
            return body

    @classmethod
    async def load(cls, response: ClientResponse) -> FreshChatResponse:
        """
        Class method creates and returns an instance of the class given
        an aiohttp.ClientResponse
        """
        if response.content_type != "application/json":
            return cls(response, await response.text())
        return cls(response, await response.json(loads=cls._decode))

    def __getattr__(self, attr):
        return getattr(self.http, attr)

    def __repr__(self):
        return f"{self.__class__.__name__}<{hex(id(self))}>(body={self.body})"
