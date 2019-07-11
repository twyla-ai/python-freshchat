from dataclasses import asdict
from typing import Any, Dict

import pytest

from freshchat.models import User


def user_with_email() -> Dict[Any, Any]:
    return {
        "id": "random_uuid",
        "created_time": "timestamp_is_here",
        "email": "peter.griffin@test.ai",
    }


def user_with_username() -> Dict[Any, Any]:
    return {
        "id": "random_uuid_number_two",
        "created_time": "timestamp_is_here",
        "first_name": "Peter",
        "last_name": "Griffin",
    }


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_data, json_body, output_data",
    [
        (
            {"email": "peter.griffin@test.ai"},
            asdict(User(**{"email": "peter.griffin@test.ai"})),
            asdict(User(**user_with_email())),
        ),
        (
            {"first_name": "Peter", "last_name": "Griffin"},
            asdict(User(**{"first_name": "Peter", "last_name": "Griffin"})),
            asdict(User(**user_with_username())),
        ),
    ],
)
async def test_create_user(
    input_data, json_body, output_data, test_client, mock_aioresponse, base_url
):
    def callback(_, **kwargs):
        assert kwargs.get("json") == json_body

    mock_aioresponse.post(f"{base_url}/users", payload=output_data, callback=callback)

    user = await User.create(client=test_client, **input_data)

    assert asdict(user) == output_data


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_data, output_data",
    [
        ("random_uuid", asdict(User(**user_with_email()))),
        ("random_uuid_number_two", asdict(User(**user_with_username()))),
    ],
)
async def test_get_user_by_id(
    input_data, output_data, test_client, mock_aioresponse, base_url
):
    mock_aioresponse.get(f"{base_url}/users/{input_data}", payload=output_data)
    user = await User.get(client=test_client, user_id=input_data)
    assert asdict(user) == output_data
