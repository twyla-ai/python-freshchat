from dataclasses import asdict

import pytest

from freshchat.models import User, Conversation, Message


def message_init():
    return Message(
        **{
            "actor_id": "random_uuid",
            "actor_type": "user",
            "conversation_id": "random_uuid",
            "message_type": "normal",
            "message_parts": [{"text": {"content": "Hello dude!"}}],
        }
    )


def message_response():
    return Message(
        **{
            "created_time": "current_timestamp",
            "id": "random_uuid",
            "actor_id": "random_uuid",
            "actor_type": "user",
            "conversation_id": "random_uuid",
            "message_type": "normal",
            "message_parts": [{"text": {"content": "Hello dude!"}}],
        }
    )


def conversation_response() -> Conversation:
    return Conversation(
        **{
            "conversation_id": "random_uuid",
            "app_id": "random_uuid",
            "channel_id": "random_uuid",
            "users": [
                User(
                    **{
                        "id": "random_uuid",
                        "created_time": "timestamp_is_here",
                        "email": "peter.griffin@test.ai",
                    }
                )
            ],
            "messages": [
                asdict(
                    Message(
                        **{
                            "app_id": "random_uuid",
                            "actor_id": "random_uuid",
                            "channel_id": "random_uuid",
                            "message_parts": [{"text": {"content": "Hey dude!"}}],
                        }
                    )
                )
            ],
        }
    )


def conversation_init() -> Conversation:
    return Conversation(
        **{
            "app_id": "random_uuid",
            "channel_id": "random_uuid",
            "users": [
                asdict(
                    User(
                        **{
                            "id": "random_uuid",
                            "created_time": "timestamp_is_here",
                            "email": "peter.griffin@test.ai",
                        }
                    )
                )
            ],
            "messages": [
                asdict(
                    Message(
                        **{
                            "app_id": "random_uuid",
                            "actor_id": "random_uuid",
                            "channel_id": "random_uuid",
                            "message_parts": [{"text": {"content": "Hey dude!"}}],
                        }
                    )
                )
            ],
        }
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user, json_body, output_data",
    [
        (
            User(
                **{
                    "id": "random_uuid",
                    "created_time": "timestamp_is_here",
                    "email": "peter.griffin@test.ai",
                }
            ),
            asdict(conversation_init()),
            asdict(conversation_response()),
        )
    ],
)
async def test_create_conversation(
    user, json_body, output_data, test_client, mock_aioresponse, base_url
):
    output_data["app_id"] = test_client.config.app_id
    json_body["app_id"] = test_client.config.app_id
    json_body["messages"][0]["app_id"] = test_client.config.app_id
    output_data["channel_id"] = test_client.config.default_channel_id
    json_body["channel_id"] = test_client.config.default_channel_id
    json_body["messages"][0]["channel_id"] = test_client.config.default_channel_id

    def callback(_, **kwargs):
        assert kwargs.get("json") == json_body

    mock_aioresponse.get(f"{base_url}/users/{user.id}", payload=asdict(user))
    mock_aioresponse.post(
        f"{base_url}/conversations", payload=output_data, callback=callback
    )
    conversation = await Conversation.create(
        client=test_client,
        user_id=user.id,
        channel_id=test_client.config.default_channel_id,
        init_message="Hey dude!",
    )
    assert asdict(conversation) == output_data


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "message, conversation, json_body, output_data",
    [
        (
            "Hello dude!",
            conversation_response(),
            asdict(message_init()),
            asdict(message_response()),
        )
    ],
)
async def test_create_message(
    message,
    conversation,
    json_body,
    output_data,
    test_client,
    mock_aioresponse,
    base_url,
):
    output_data["app_id"] = test_client.config.app_id
    output_data["channel_id"] = test_client.config.default_channel_id

    def callback(_, **kwargs):
        assert kwargs.get("json") == json_body

    mock_aioresponse.post(
        f"{base_url}/conversations/{conversation.conversation_id}/messages",
        payload=output_data,
        callback=callback,
    )

    message_new = await conversation.send(client=test_client, message=message)
    assert asdict(message_new) == output_data
