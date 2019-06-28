from dataclasses import asdict, dataclass, field

from python.freshchat.client.client import (
    CONVERSATION_INITIAL_MESSAGE,
    FreshChatClient,
    Operation,
)
from python.freshchat.client.models import Conversation, Message, User


@dataclass
class SessionData:
    conversation_id: str = None
    user_id: str = None
    channel_user_id: str = None


@dataclass
class FreshChatSession:
    session_data: SessionData = field(default_factory=SessionData)
    client: FreshChatClient = field(default_factory=FreshChatClient)

    async def create_user(self, **kwargs) -> User:
        response = await self.client.post(operation=Operation.USERS, body=kwargs)
        user = User(**response.body)
        self.session_data.user_id = user.id
        return user

    async def create_conversation(self, user: User) -> Conversation:
        conversation_body = {
            "app_id": self.client.config.app_id,
            "channel_id": self.client.config.channel_id,
            "users": [asdict(user)],
            "messages": [
                asdict(
                    Message.create(
                        **{
                            "app_id": self.client.config.app_id,
                            "actor_id": user.id,
                            "channel_id": self.client.config.channel_id,
                            "message_parts": [
                                {"text": {"content": CONVERSATION_INITIAL_MESSAGE}}
                            ],
                        }
                    )
                )
            ],
        }
        conversation = Conversation(**conversation_body)
        response = await self.client.post(
            operation=Operation.CONVERSATION, body=asdict(conversation)
        )
        conversation = Conversation(**response.body)
        self.session_data.conversation_id = conversation.conversation_id
        return conversation

    async def create_message(self, message: str) -> Message:
        message_body = asdict(
            Message.create(
                **{
                    "actor_id": self.session_data.user_id,
                    "message_parts": [{"text": {"content": message}}],
                }
            )
        )
        response = await self.client.post(
            Operation.CONVERSATION,
            path=[self.session_data.conversation_id, "messages"],
            body=message_body,
        )
        return Message(**response.body)

    async def get_user(self) -> User:
        response = await self.client.get(
            Operation.USERS, path=[self.session_data.user_id]
        )
        return User(**response.body)
