from dataclasses import asdict
from typing import Dict, AnyStr

import pytest

from python.freshchat.client.client import CONVERSATION_INITIAL_MESSAGE
from python.freshchat.client.models import User, Message
from python.freshchat.client.responses import FreshChatResponse


@pytest.fixture
def params() -> Dict[AnyStr, AnyStr]:
    return {"endpoint": "/users", "params": None, "headers": None}


def test_configuration_headers(test_config, auth_header):
    assert test_config.authorization_header == {
        "Authorization": f"Bearer {auth_header}"
    }


@pytest.mark.asyncio
async def test_live_agent_client_request_get(mock_aioresponse, test_client, params):
    mock_aioresponse.get("/users", payload={"foo": "bar"})
    resp = await test_client.get(**params)
    data = await resp.json()
    assert isinstance(resp, FreshChatResponse)
    assert {"foo": "bar"} == data


@pytest.mark.asyncio
async def test_live_agent_client_request_post(mock_aioresponse, test_client, params):
    mock_aioresponse.post("/users", payload={"foo": "bar"})
    resp = await test_client.post(**params)
    data = await resp.json()
    assert isinstance(resp, FreshChatResponse)
    assert {"foo": "bar"} == data


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
    input_data, json_body, output_data, test_client, mock_aioresponse
):
    def callback(_, **kwargs):
        assert kwargs.get("json") == json_body

    mock_aioresponse.post("/users", payload=output_data, callback=callback)

    user = await test_client.create_user(**input_data)

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
async def test_get_user_by_id(input_data, output_data, test_client, mock_aioresponse):
    mock_aioresponse.get("/users" + "/" + input_data, payload=output_data)
    user = await test_client.get_user(user_id=input_data)
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
                        Message(
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
                        Message(
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
    user, json_body, output_data, test_client, mock_aioresponse
):
    output_data["app_id"] = test_client.config.app_id
    json_body["app_id"] = test_client.config.app_id
    json_body["messages"][0]["app_id"] = test_client.config.app_id
    output_data["channel_id"] = test_client.config.channel_id
    json_body["channel_id"] = test_client.config.channel_id
    json_body["messages"][0]["channel_id"] = test_client.config.channel_id

    def callback(_, **kwargs):
        assert kwargs.get("json") == json_body

    mock_aioresponse.post("/conversations", payload=output_data, callback=callback)
    conversation = await test_client.create_conversation(user=user)
    assert asdict(conversation) == output_data


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "message, user_id, conversation_id, json_body, output_data",
    [
        (
            "Hello dude!",
            "user_uuid",
            "conversation_uuid",
            {
                "created_time": None,
                "id": None,
                "app_id": None,
                "actor_id": "user_uuid",
                "actor_type": "user",
                "channel_id": None,
                "conversation_id": "conversation_uuid",
                "message_type": "normal",
                "message_parts": [{"text": {"content": "Hello dude!"}}],
            },
            {
                "created_time": "current_timestamp",
                "id": "random_uuid",
                "app_id": "",
                "actor_id": "user_uuid",
                "actor_type": "user",
                "channel_id": "",
                "conversation_id": "conversation_uuid",
                "message_type": "normal",
                "message_parts": [{"text": {"content": "Hello dude!"}}],
            },
        )
    ],
)
async def test_create_message(
    message,
    user_id,
    conversation_id,
    json_body,
    output_data,
    test_client,
    mock_aioresponse,
):
    output_data["app_id"] = test_client.config.app_id
    output_data["channel_id"] = test_client.config.channel_id

    def callback(_, **kwargs):
        assert kwargs.get("json") == json_body

    mock_aioresponse.post(
        "/conversations" + "/" + conversation_id + "/messages",
        payload=output_data,
        callback=callback,
    )
    message_new = await test_client.create_message(
        message=message, conversation_id=conversation_id, user_id=user_id
    )
    assert asdict(message_new) == output_data
