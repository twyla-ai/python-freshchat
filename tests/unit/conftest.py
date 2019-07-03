import urllib.parse
from typing import Any, AnyStr, Dict
from uuid import uuid4

import pytest
from aioresponses import aioresponses

from python.freshchat.client.client import FreshChatClient, FreshChatConfiguration

BASE_URL = "http://127.0.0.1:8000/"


@pytest.fixture(autouse=True)
def set_environ_vars(monkeypatch):
    monkeypatch.setenv("FRESHCHAT_API_URL", BASE_URL)


class MockResp(aioresponses):
    def __init__(self, base_url, **kwargs):
        self.base_url = base_url
        super().__init__(**kwargs)

    def get(self, operation: str, params: dict = None, **kwargs):
        url = self.base_url + operation.lstrip("/")
        if params:
            url += "?" + urllib.parse.urlencode(params)
        super().get(url=url, **kwargs)

    def post(self, operation: str, **kwargs):
        url = self.base_url + operation.lstrip("/")
        super().post(url=url, **kwargs)


@pytest.fixture
def mock_aioresponse() -> MockResp:
    with MockResp(BASE_URL) as m:
        yield m


@pytest.fixture(scope="module")
def auth_header():
    return str(uuid4())


@pytest.fixture
def test_config(auth_header) -> FreshChatConfiguration:
    return FreshChatConfiguration(
        **{"app_id": str(uuid4()), "channel_id": str(uuid4()), "token": auth_header}
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
