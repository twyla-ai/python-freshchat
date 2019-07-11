from typing import AnyStr, Dict

import pytest

from freshchat.client.client import FreshChatClient
from freshchat.client.responses import FreshChatResponse


@pytest.fixture
def user_request_params() -> Dict[AnyStr, AnyStr]:
    return {"endpoint": "/users", "params": None, "headers": None}


@pytest.fixture
def client_get(mock_aioresponse, test_config, base_url):
    mock_aioresponse.get(f"{base_url}/users", payload={"foo": "bar"})
    return FreshChatClient(config=test_config)


@pytest.fixture
def client_post(mock_aioresponse, test_config, base_url):
    mock_aioresponse.post(f"{base_url}/users", payload={"foo": "bar"})
    return FreshChatClient(config=test_config)


def test_configuration_headers(test_config, token):
    assert test_config.authorization_header == {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_client_request_get(client_get, user_request_params):
    resp = await client_get.get(**user_request_params)
    data = await resp.json()
    assert isinstance(resp, FreshChatResponse)
    assert {"foo": "bar"} == data


@pytest.mark.asyncio
async def test_client_request_post(client_post, user_request_params):
    resp = await client_post.post(**user_request_params)
    data = await resp.json()
    assert isinstance(resp, FreshChatResponse)
    assert {"foo": "bar"} == data
