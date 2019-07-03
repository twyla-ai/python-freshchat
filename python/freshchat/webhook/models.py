from dataclasses import asdict, dataclass, field
from typing import Any, AnyStr, Dict, List

LIVEAGENT_INTEGRATION_NAME = "freshchat-liveagent"


@dataclass
class Actor:
    actor_type: str = None
    actor_id: str = None


@dataclass
class Conversation:
    conversation_id: str = None
    app_id: str = None
    status: str = None
    channel_id: str = None


@dataclass
class Message:
    """
    Class which represents freshchat message format
    """

    created_time: str = None
    id: str = None
    actor_type: str = None
    actor_id: str = None
    conversation: Conversation = field(default_factory=Conversation)
    message_type: str = None
    message_parts: List[Dict[AnyStr, AnyStr]] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.conversation, dict):
            self.conversation = Conversation(**self.conversation)

    @classmethod
    def create(cls, incoming_message):
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
    Class which represents freshchat message format
    """

    reopener: str = None
    reopener_id: str = None
    conversation: Conversation = field(default_factory=Conversation)

    def __post_init__(self):
        if isinstance(self.conversation, dict):
            self.conversation = Conversation(**self.conversation)


@dataclass
class Resolve:
    """
    Class which represents freshchat message format
    """

    resolver: str = None
    resolver_id: str = None
    conversation: Conversation = field(default_factory=Conversation)

    def __post_init__(self):
        if isinstance(self.conversation, dict):
            self.conversation = Conversation(**self.conversation)


@dataclass
class IncomingEvent:
    actor: Actor = field(default_factory=Actor)
    action: str = None
    action_time: str = None
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
