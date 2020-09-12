from dataclasses import asdict

import pytest

from freshchat.models import Conversation
from freshchat.models import Message as OutgoingMessage
from freshchat.models import User
from freshchat.models.events import IncomingEvent, Message, Reopen, Resolve


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "incoming_event, event_type",
    [
        (
            {
                "actor": "user",
                "action": "message_create",
                "action_time": "time",
                "data": {
                    "message": {
                        "created_time": "created_time",
                        "id": "random_uuid",
                        "actor_type": "user",
                        "actor_id": "random_uuid",
                        "message_type": "",
                        "message_parts": [],
                        "conversation_id": "conversation_uuid",
                        "app_id": "random_uuid",
                        "channel_id": "random_uuid",
                        "conversation": Conversation(
                            **{
                                "conversation_id": "conversation_uuid",
                                "app_id": "random_uuid",
                                "channel_id": "random_uuid",
                                "status": "new",
                                "agents": [],
                                "users": [
                                    User(
                                        **{
                                            "id": "user_random_uuid",
                                            "created_time": "timestamp_is_here",
                                            "email": "peter.griffin@test.ai",
                                        }
                                    )
                                ],
                                "messages": [
                                    asdict(
                                        OutgoingMessage(
                                            **{
                                                "app_id": "random_uuid",
                                                "actor_id": "random_uuid",
                                                "channel_id": "random_uuid",
                                                "message_parts": [
                                                    {"text": {"content": "Hey dude!"}}
                                                ],
                                            }
                                        )
                                    )
                                ],
                            }
                        ),
                    }
                },
            },
            Message,
        ),
        (
            {
                "actor": "user",
                "action": "conversation_resolution",
                "action_time": "time",
                "data": {
                    "resolve": {
                        "resolver": "resolver",
                        "resolver_id": "random_uuid",
                        "conversation": Conversation(
                            **{
                                "conversation_id": "conversation_uuid",
                                "app_id": "random_uuid",
                                "channel_id": "random_uuid",
                                "status": "new",
                                "agents": [],
                                "users": [
                                    User(
                                        **{
                                            "id": "user_random_uuid",
                                            "created_time": "timestamp_is_here",
                                            "email": "peter.griffin@test.ai",
                                        }
                                    )
                                ],
                                "messages": [
                                    asdict(
                                        OutgoingMessage(
                                            **{
                                                "app_id": "random_uuid",
                                                "actor_id": "random_uuid",
                                                "channel_id": "random_uuid",
                                                "message_parts": [
                                                    {"text": {"content": "Hey dude!"}}
                                                ],
                                            }
                                        )
                                    )
                                ],
                            }
                        ),
                    }
                },
            },
            Resolve,
        ),
        (
            {
                "actor": "user",
                "action": "message_create",
                "action_time": "time",
                "data": {
                    "reopen": {
                        "reopener": "reopener",
                        "reopener_id": "random_uuid",
                        "conversation": Conversation(
                            **{
                                "conversation_id": "conversation_uuid",
                                "app_id": "random_uuid",
                                "channel_id": "random_uuid",
                                "status": "new",
                                "agents": [],
                                "users": [
                                    User(
                                        **{
                                            "id": "user_random_uuid",
                                            "created_time": "timestamp_is_here",
                                            "email": "peter.griffin@test.ai",
                                        }
                                    )
                                ],
                                "messages": [
                                    asdict(
                                        OutgoingMessage(
                                            **{
                                                "app_id": "random_uuid",
                                                "actor_id": "random_uuid",
                                                "channel_id": "random_uuid",
                                                "message_parts": [
                                                    {"text": {"content": "Hey dude!"}}
                                                ],
                                            }
                                        )
                                    )
                                ],
                            }
                        ),
                    }
                },
            },
            Reopen,
        ),
    ],
)
async def test_create_message(incoming_event, event_type):
    incoming_event = IncomingEvent(**incoming_event)
    assert isinstance(incoming_event.data, event_type)
