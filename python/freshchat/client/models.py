from dataclasses import dataclass, field
from typing import Any, AnyStr, Dict, List


@dataclass
class User:
    """
    Class which represents a freshchat user. A user can be an external user or an
    agent
    """

    id: str = None
    created_time: str = None
    email: str = None
    first_name: str = None
    last_name: str = None
    phone: str = None
    avatar: Dict[AnyStr, AnyStr] = field(default_factory=dict)
    social_profiles: List[Dict[AnyStr, AnyStr]] = field(default_factory=list)
    properties: List[Dict[AnyStr, AnyStr]] = field(default_factory=list)


@dataclass
class Message:
    """
    Class which represents freshchat message format
    """

    created_time: str = None
    id: str = None
    app_id: str = None
    actor_type: str = "user"
    actor_id: str = None
    channel_id: str = None
    conversation_id: str = None
    message_type: str = "normal"
    message_parts: List[Dict[AnyStr, AnyStr]] = field(default_factory=list)

    @classmethod
    def create(cls, **kwargs):
        return cls(**kwargs)


@dataclass
class Conversation:
    """
    Class which represents freshchat conversation format
    """

    conversation_id: str = None
    app_id: str = None
    channel_id: str = None
    status: str = "new"
    agents: List[User] = field(default_factory=list)
    users: List[User] = field(default_factory=list)
    messages: List[Message] = field(default_factory=list)


@dataclass
class Group:
    """
    Class which represents freshchat group format
    """

    id: str = None
    name: str = None
    description: str = None
    routing_type: str = None


@dataclass
class Channel:
    """
    Class which represents freshchat channel object
    """

    id: str = None
    icon: Dict[AnyStr, AnyStr] = field(default_factory=dict)
    updated_time: str = None
    enabled: bool = None
    public: bool = None
    name: str = None
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
