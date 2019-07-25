from typing import Any, AnyStr, Dict
from uuid import uuid4

import pytest
from aioresponses import aioresponses

from freshchat.client.client import FreshChatClient
from freshchat.client.configuration import FreshChatConfiguration

BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture(autouse=True)
def set_environ_vars(monkeypatch):
    monkeypatch.setenv("FRESHCHAT_API_URL", BASE_URL)


@pytest.fixture
def mock_aioresponse():
    with aioresponses() as m:
        yield m


@pytest.fixture
def base_url():
    return BASE_URL


@pytest.fixture(scope="module")
def token():
    return str(uuid4())


@pytest.fixture
def test_config(token) -> FreshChatConfiguration:
    return FreshChatConfiguration(
        **{
            "app_id": str(uuid4()),
            "default_channel_id": str(uuid4()),
            "token": token,
            "public_key": "-----BEGIN RSA PUBLIC KEY-----*****-----END RSA PUBLIC KEY-----",
        }
    )


@pytest.fixture(scope="module")
def session_data() -> Dict[AnyStr, Any]:
    return {
        "session_data": {
            "conversation_id": str(uuid4()),
            "user_id": str(uuid4()),
            "channel_user_id": str(uuid4()),
        }
    }


@pytest.fixture
def test_client(test_config) -> FreshChatClient:
    return FreshChatClient(config=test_config)
