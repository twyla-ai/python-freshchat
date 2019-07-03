from dataclasses import dataclass, field
from typing import Any, AnyStr, Dict, List, ClassVar


@dataclass
class User:
    """
    Class which represents a freshchat user. A user can be an external user or an
    agent
    """

    id: str = field(default=None)
    created_time: str = field(default=None)
    email: str = field(default=None)
    first_name: str = field(default=None)
    last_name: str = field(default=None)
    phone: str = field(default=None)
    avatar: Dict[AnyStr, AnyStr] = field(default_factory=dict)
    social_profiles: List[Dict[AnyStr, AnyStr]] = field(default_factory=list)
    properties: List[Dict[AnyStr, AnyStr]] = field(default_factory=list)
    endpoint: ClassVar[str] = field(default="/users", init=False)

    @property
    def get_endpoint(self):
        return f"{self.endpoint}/{self.id}"


@dataclass
class Message:
    """
    Class which represents freshchat message format
    """

    created_time: str = field(default=None)
    id: str = field(default=None)
    app_id: str = field(default=None)
    actor_type: str = "user"
    actor_id: str = field(default=None)
    channel_id: str = field(default=None)
    conversation_id: str = field(default=None)
    message_type: str = "normal"
    message_parts: List[Dict[AnyStr, AnyStr]] = field(default_factory=list)

    @property
    def endpoint(self) -> str:
        return f"/conversations/{self.conversation_id}/messages"

    # @classmethod
    # def create(cls, **kwargs):
    #     return cls(**kwargs)


@dataclass
class Conversation:
    """
    Class which represents freshchat conversation format
    """

    conversation_id: str = field(default=None)
    app_id: str = field(default=None)
    channel_id: str = field(default=None)
    status: str = field(default="new")
    agents: List[User] = field(default_factory=list)
    users: List[User] = field(default_factory=list)
    messages: List[Message] = field(default_factory=list)
    endpoint: ClassVar[str] = field(default="/conversations", init=False)


@dataclass
class Group:
    """
    Class which represents freshchat group format
    """

    id: str = field(default=None)
    name: str = field(default=None)
    description: str = field(default=None)
    routing_type: str = field(default=None)


@dataclass
class Channel:
    """
    Class which represents freshchat channel object
    """

    id: str = field(default=None)
    icon: Dict[AnyStr, AnyStr] = field(default_factory=dict)
    updated_time: str = field(default=None)
    enabled: bool = field(default=None)
    public: bool = field(default=None)
    name: str = field(default=None)
    tags: List[Any] = field(default_factory=list)
    welcome_message: Dict[Any, Any] = field(default_factory=dict)


@dataclass
class Channels:
    """
    Class which represents freshchat channels. It is the returning
    value of get channels request
    """

    channels: List[Channel] = field(default_factory=list)
    pagination: Dict[AnyStr, AnyStr] = field(default_factory=dict)
    links: Dict[AnyStr, AnyStr] = field(default_factory=dict)
    last_page: Dict[AnyStr, AnyStr] = field(default_factory=dict)
