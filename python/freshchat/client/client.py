import os
from dataclasses import asdict, dataclass, field
from typing import Any, AnyStr, Dict
from urllib.parse import urljoin

import aiohttp
from cafeteria.logging import LoggedObject

from python.freshchat.client.exceptions import HttpResponseCodeError
from python.freshchat.client.models import Conversation, Message, User
from python.freshchat.client.responses import FreshChatResponse

CONVERSATION_INITIAL_MESSAGE = os.environ.get(
    "CONVERSATION_INITIAL_MESSAGE", "hey dude!"
)


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
    token: str = None

    @property
    def authorization_header(self) -> Dict[AnyStr, AnyStr]:
        return {
            "Authorization": f"Bearer {self.token}"
            if "Bearer" not in self.token
            else self.token
        }

    def get_url(self, endpoint: str):
        """
        Method responsible to build the url using the given extras if exists

        :param endpoint: List with the extra variables for the url, ex. user/<user_id>
        :return: URL
        """
        return urljoin(self.url, endpoint.lstrip("/"))


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
        params: Dict[AnyStr, Any] = None,
        body: Dict[AnyStr, Any] = None,
        headers: Dict[AnyStr, Any] = None,
    ) -> FreshChatResponse:
        """

        :param method: http method can be GET or POST
        :param endpoint: URL variables
        :param params: request parameters in the case of GET method
        :param body: request body in the case of POST method
        :param headers: extra headers
        :return: The response of the request using the above fields
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
        endpoint: str,
        params: Dict[AnyStr, Any] = None,
        headers: Dict[str, Any] = None,
    ) -> FreshChatResponse:
        """
        Method used for the get requests

        :param endpoint: URL variables
        :param params: request parameters in the case of GET method
        :param headers: extra headers
        :return: The response of the request using the above fields
        :return: FreshChatResponse
        """
        return await self.request(
            method="GET", endpoint=endpoint, params=params, headers=headers
        )

    async def post(
        self,
        endpoint: str,
        params: Dict[AnyStr, Any] = None,
        body: Dict[AnyStr, AnyStr] = None,
        headers: Dict[str, Any] = None,
    ) -> FreshChatResponse:
        """
        Method used for the post requests
        :param endpoint: URL variables
        :param params: request parameters in the case of GET method
        :param body: request body in the case of POST method
        :param headers: extra headers
        :return: The response of the request using the above fields
        :return: FreshChatResponse
        """
        return await self.request(
            method="POST", endpoint=endpoint, params=params, body=body, headers=headers
        )

    async def create_user(self, **kwargs) -> User:
        user = User(**kwargs)
        response = await self.post(endpoint=user.endpoint, body=asdict(user))
        user = User(**response.body)
        return user

    async def create_conversation(self, user: User) -> Conversation:
        conversation_body = {
            "app_id": self.config.app_id,
            "channel_id": self.config.channel_id,
            "users": [asdict(user)],
            "messages": [
                asdict(
                    Message(
                        **{
                            "app_id": self.config.app_id,
                            "actor_id": user.id,
                            "channel_id": self.config.channel_id,
                            "message_parts": [
                                {"text": {"content": CONVERSATION_INITIAL_MESSAGE}}
                            ],
                        }
                    )
                )
            ],
        }
        conversation = Conversation(**conversation_body)
        response = await self.post(
            endpoint=conversation.endpoint, body=asdict(conversation)
        )
        conversation = Conversation(**response.body)
        return conversation

    async def create_message(
        self, conversation_id: str, user_id: str, message: str
    ) -> Message:
        message_model = Message(
            **{
                "conversation_id": conversation_id,
                "actor_id": user_id,
                "message_parts": [{"text": {"content": message}}],
            }
        )

        response = await self.post(
            endpoint=message_model.endpoint, body=asdict(message_model)
        )
        return Message(**response.body)

    async def get_user(self, user_id: str = None) -> User:
        user = User(id=user_id)
        response = await self.get(user.get_endpoint)
        return User(**response.body)

    def __repr__(self):
        return f"{self.__class__.__name__}<{hex(id(self))}> (config={self.config})"
