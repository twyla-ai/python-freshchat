from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, AnyStr, Dict, List

from freshchat.models import Conversation, Actor


@dataclass
class Message:
    """
    Class which represents freshchat new message event
    """

    created_time: str = field(default=None)
    id: str = field(default=None)
    actor_type: str = field(default=None)
    actor_id: str = field(default=None)
    conversation: Conversation = field(default_factory=Conversation)
    message_type: str = field(default=None)
    message_parts: List[Dict[AnyStr, AnyStr]] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.conversation, dict):
            self.conversation = Conversation(**self.conversation)

    @classmethod
    def create(cls, incoming_message: Dict[AnyStr, AnyStr]) -> Message:
        conversation = Conversation(
            conversation_id=incoming_message.pop("conversation_id"),
            channel_id=incoming_message.pop("channel_id"),
            app_id=incoming_message.pop("app_id"),
        )
        incoming_message["conversation"] = asdict(conversation)
        return cls(**incoming_message)


@dataclass
class Reopen:
    """
    Class which represents freshchat conversation reopen event
    """

    reopener: str = field(default=None)
    reopener_id: str = field(default=None)
    conversation: Conversation = field(default_factory=Conversation)

    def __post_init__(self):
        if isinstance(self.conversation, dict):
            self.conversation = Conversation(**self.conversation)


@dataclass
class Resolve:
    """
    Class which represents freshchat conversation resolve event
    """

    resolver: str = field(default=None)
    resolver_id: str = field(default=None)
    conversation: Conversation = field(default_factory=Conversation)

    def __post_init__(self):
        if isinstance(self.conversation, dict):
            self.conversation = Conversation(**self.conversation)


@dataclass
class IncomingEvent:
    """
    Class which accepts an incoming event and based on the type creates the
    corresponding event
    """

    actor: Actor = field(default_factory=Actor)
    action: str = field(default=None)
    action_time: str = field(default=None)
    data: Any = field(default_factory=None)

    def __post_init__(self):
        if isinstance(self.data, dict):
            if "message" in self.data:
                self.data = Message.create(self.data.get("message"))
            elif "resolve" in self.data:
                self.data = Resolve(**self.data.get("resolve"))
            elif "reopen" in self.data:
                self.data = Reopen(**self.data.get("reopen"))
        if isinstance(self.actor, dict):
            self.actor = Actor(**self.actor)
