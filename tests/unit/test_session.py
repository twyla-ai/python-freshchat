from dataclasses import asdict

import pytest

from python.freshchat.client.client import Operation, CONVERSATION_INITIAL_MESSAGE
from python.freshchat.client.models import User, Message


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_data, json_body, output_data",
    [
        (
            {"email": "peter.griffin@test.ai"},
            {
                "id": None,
                "created_time": None,
                "email": "peter.griffin@test.ai",
                "first_name": None,
                "last_name": None,
                "phone": None,
                "avatar": {},
                "social_profiles": [],
                "properties": [],
            },
            {
                "id": "random_uuid",
                "created_time": "timestamp_is_here",
                "email": "peter.griffin@test.ai",
                "first_name": None,
                "last_name": None,
                "phone": None,
                "avatar": {},
                "social_profiles": [],
                "properties": [],
            },
        ),
        (
            {"first_name": "Peter", "last_name": "Griffin"},
            {
                "id": None,
                "created_time": None,
                "email": None,
                "first_name": "Peter",
                "last_name": "Griffin",
                "phone": None,
                "avatar": {},
                "social_profiles": [],
                "properties": [],
            },
            {
                "id": "random_uuid",
                "created_time": "timestamp_is_here",
                "email": None,
                "first_name": "Peter",
                "last_name": "Griffin",
                "phone": None,
                "avatar": {},
                "social_profiles": [],
                "properties": [],
            },
        ),
    ],
)
async def test_create_user(
    input_data, json_body, output_data, test_session, mock_aioresponse
):
    def callback(_, **kwargs):
        assert kwargs.get("json") == json_body

    mock_aioresponse.post(Operation.USERS, payload=output_data, callback=callback)

    user = await test_session.create_user(**input_data)

    assert asdict(user) == output_data


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_data, output_data",
    [
        (
            "random_uuid",
            {
                "id": "random_uuid",
                "created_time": "timestamp_is_here",
                "email": "peter.griffin@test.ai",
                "first_name": None,
                "last_name": None,
                "phone": None,
                "avatar": {},
                "social_profiles": [],
                "properties": [],
            },
        ),
        (
            "random_uuid_number_two",
            {
                "id": "random_uuid_number_two",
                "created_time": "timestamp_is_here",
                "email": None,
                "first_name": "Peter",
                "last_name": "Griffin",
                "phone": None,
                "avatar": {},
                "social_profiles": [],
                "properties": [],
            },
        ),
    ],
)
async def test_get_user_by_id(input_data, output_data, test_session, mock_aioresponse):
    mock_aioresponse.get(Operation.USERS + "/" + input_data, payload=output_data)
    user = await test_session.get_user(input_data)
    assert asdict(user) == output_data


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
                    "first_name": None,
                    "last_name": None,
                    "phone": None,
                    "avatar": {},
                    "social_profiles": [],
                    "properties": [],
                }
            ),
            {
                "conversation_id": None,
                "app_id": "random_uuid",
                "channel_id": "random_uuid",
                "agents": [],
                "status": "new",
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
                        Message.create(
                            **{
                                "app_id": "random_uuid",
                                "actor_id": "random_uuid",
                                "channel_id": "random_uuid",
                                "message_parts": [
                                    {"text": {"content": CONVERSATION_INITIAL_MESSAGE}}
                                ],
                            }
                        )
                    )
                ],
            },
            {
                "conversation_id": "random_uuid",
                "app_id": "random_uuid",
                "channel_id": "random_uuid",
                "status": "new",
                "agents": [],
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
                        Message.create(
                            **{
                                "app_id": "random_uuid",
                                "actor_id": "random_uuid",
                                "channel_id": "random_uuid",
                                "message_parts": [
                                    {"text": {"content": CONVERSATION_INITIAL_MESSAGE}}
                                ],
                            }
                        )
                    )
                ],
            },
        )
    ],
)
async def test_create_conversation(
    user, json_body, output_data, test_session, mock_aioresponse
):
    output_data["app_id"] = test_session.config.app_id
    json_body["app_id"] = test_session.config.app_id
    json_body["messages"][0]["app_id"] = test_session.config.app_id
    output_data["channel_id"] = test_session.config.channel_id
    json_body["channel_id"] = test_session.config.channel_id
    json_body["messages"][0]["channel_id"] = test_session.config.channel_id

    def callback(_, **kwargs):
        assert kwargs.get("json") == json_body

    mock_aioresponse.post(
        Operation.CONVERSATION, payload=output_data, callback=callback
    )
    conversation = await test_session.create_conversation(user=user)
    assert asdict(conversation) == output_data


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "message, json_body, output_data",
    [
        (
            "Hello dude!",
            {
                "created_time": None,
                "id": None,
                "app_id": None,
                "actor_id": "",
                "actor_type": "user",
                "channel_id": None,
                "conversation_id": None,
                "message_type": "normal",
                "message_parts": [{"text": {"content": "Hello dude!"}}],
            },
            {
                "created_time": "current_timestamp",
                "id": "random_uuid",
                "app_id": "",
                "actor_id": "",
                "actor_type": "user",
                "channel_id": "",
                "conversation_id": "random_uuid",
                "message_type": "normal",
                "message_parts": [{"text": {"content": "Hello dude!"}}],
            },
        )
    ],
)
async def test_create_message(
    message, json_body, output_data, test_session, mock_aioresponse
):
    output_data["app_id"] = test_session.config.app_id
    output_data["channel_id"] = test_session.config.channel_id
    output_data["actor_id"] = test_session.session_data.user_id
    json_body["actor_id"] = test_session.session_data.user_id
    output_data["conversation_id"] = test_session.session_data.conversation_id

    def callback(_, **kwargs):
        assert kwargs.get("json") == json_body

    mock_aioresponse.post(
        Operation.CONVERSATION
        + "/"
        + test_session.session_data.conversation_id
        + "/messages",
        payload=output_data,
        callback=callback,
    )
    message_new = await test_session.create_message(message=message)
    assert asdict(message_new) == output_data
