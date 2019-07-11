from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, AnyStr, Dict, List, ClassVar, Optional

from freshchat.client.client import FreshChatClient


@dataclass
class User:
    """
    Class which represents a freshchat user. A user can be an external user or an
    agent
    """

    id: Optional[str] = field(default=None)
    created_time: Optional[str] = field(default=None)
    email: Optional[str] = field(default=None)
    first_name: Optional[str] = field(default=None)
    last_name: Optional[str] = field(default=None)
    phone: Optional[str] = field(default=None)
    avatar: Optional[Dict[AnyStr, AnyStr]] = field(default_factory=dict)
    social_profiles: Optional[List[Dict[AnyStr, AnyStr]]] = field(default_factory=list)
    properties: Optional[List[Dict[AnyStr, AnyStr]]] = field(default_factory=list)
    endpoint: ClassVar[str] = "/users"

    @property
    def get_endpoint(self) -> str:
        return f"{self.endpoint}/{self.id}"

    @classmethod
    async def create(cls, client: FreshChatClient, **kwargs) -> User:
        """
        Creates a new user instance with the given kwargs
        """
        user = cls(**kwargs)
        response = await client.post(endpoint=user.endpoint, json=asdict(user))
        return cls(**response.body)

    @classmethod
    async def get(cls, client: FreshChatClient, user_id: str) -> User:
        """
        Returns an existing user based on the given user_id
        """
        user = cls(id=user_id)
        response = await client.get(user.get_endpoint)
        return cls(**response.body)


@dataclass
class Message:
    """
    Class which represents freshchat message format
    """

    created_time: Optional[str] = field(default=None)
    id: Optional[str] = field(default=None)
    app_id: str = field(default=None)
    actor_type: Optional[str] = "user"
    actor_id: str = field(default=None)
    channel_id: Optional[str] = field(default=None)
    conversation_id: Optional[str] = field(default=None)
    message_type: str = "normal"
    message_parts: List[Dict[AnyStr, AnyStr]] = field(default_factory=list)

    @property
    def endpoint(self) -> str:
        return f"/conversations/{self.conversation_id}/messages"


@dataclass
class Conversation:
    """
    Class which represents freshchat conversation format
    """

    conversation_id: Optional[str] = field(default=None)
    app_id: str = field(default=None)
    channel_id: str = field(default=None)
    status: Optional[str] = field(default="new")
    agents: Optional[List[User]] = field(default_factory=list)
    users: List[User] = field(default_factory=list)
    messages: List[Message] = field(default_factory=list)
    endpoint: ClassVar[str] = "/conversations"

    @property
    def get_endpoint(self):
        return f"{self.endpoint}/{self.conversation_id}"

    @property
    def user_id(self):
        return self.users[0].id

    @classmethod
    async def create(
        cls,
        client: FreshChatClient,
        user_id: str,
        channel_id: str,
        init_message: str = None,
    ) -> Conversation:
        """
        Create a new conversation instance
        """
        user = await User().get(client=client, user_id=user_id)
        conversation_body = {
            "app_id": client.config.app_id,
            "channel_id": channel_id,
            "users": [asdict(user)],
            "messages": [
                asdict(
                    Message(
                        **{
                            "app_id": client.config.app_id,
                            "actor_id": user.id,
                            "channel_id": channel_id,
                            "message_parts": [{"text": {"content": init_message}}],
                        }
                    )
                )
            ],
        }

        conversation = cls(**conversation_body)

        response = await client.post(
            endpoint=conversation.endpoint, json=asdict(conversation)
        )
        conversation = cls(**response.body)
        conversation.users = [user]
        return conversation

    @classmethod
    async def get(
        cls, client: FreshChatClient, conversation_id: str, user_id: str
    ) -> Conversation:
        """
        Return an existing conversation based on the conversation_id
        """

        user = await User().get(client=client, user_id=user_id)
        conversation = cls(conversation_id=conversation_id)
        response = await client.get(conversation.get_endpoint)
        conversation = cls(**response.body)
        conversation.users = [user]
        return conversation

    async def send(self, client: FreshChatClient, message: str) -> Message:
        """
        Sends a message to an existing conversation
        """

        message_model = Message(
            **{
                "conversation_id": self.conversation_id,
                "actor_id": self.user_id,
                "message_parts": [{"text": {"content": message}}],
            }
        )
        response = await client.post(
            endpoint=message_model.endpoint, json=asdict(message_model)
        )
        return Message(**response.body)


@dataclass
class Group:
    """
    Class which represents freshchat group format
    """

    id: Optional[str] = field(default=None)
    name: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None)
    routing_type: Optional[str] = field(default=None)


@dataclass
class Channel:
    """
    Class which represents freshchat channel object
    """

    id: Optional[str] = field(default=None)
    icon: Optional[Dict[AnyStr, AnyStr]] = field(default_factory=dict)
    updated_time: Optional[str] = field(default=None)
    enabled: Optional[bool] = field(default=None)
    public: Optional[bool] = field(default=None)
    name: Optional[str] = field(default=None)
    tags: Optional[List[Any]] = field(default_factory=list)
    welcome_message: Optional[Dict[Any, Any]] = field(default_factory=dict)


@dataclass
class Channels:
    """
    Class which represents freshchat channels. It is the returning
    value of get channels request
    """

    channels: List[Channel] = field(default_factory=list)
    pagination: Optional[Dict[AnyStr, AnyStr]] = field(default_factory=dict)
    links: Optional[Dict[AnyStr, AnyStr]] = field(default_factory=dict)
    last_page: Optional[Dict[AnyStr, AnyStr]] = field(default_factory=dict)
    endpoint: ClassVar[str] = "/channels"

    @classmethod
    async def get(cls, client: FreshChatClient) -> List:
        """
        Returns a list of Channel
        """
        response = await client.get(Channels().endpoint)
        return Channels(**response.body).channels


@dataclass
class Actor:
    actor_type: Optional[str] = field(default=None)
    actor_id: Optional[str] = field(default=None)
