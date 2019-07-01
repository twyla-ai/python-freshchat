from typing import Dict, AnyStr

import pytest

from python.freshchat.client.client import Operation
from python.freshchat.client.responses import FreshChatResponse


@pytest.fixture
def params() -> Dict[AnyStr, AnyStr]:
    return {"operation": Operation.USERS, "params": None, "headers": None}


@pytest.mark.asyncio
async def test_live_agent_client_request_get(mock_aioresponse, test_client, params):
    mock_aioresponse.get(Operation.USERS, payload={"foo": "bar"})
    resp = await test_client.get(**params)
    data = await resp.json()
    assert isinstance(resp, FreshChatResponse)
    assert {"foo": "bar"} == data


@pytest.mark.asyncio
async def test_live_agent_client_request_post(mock_aioresponse, test_client, params):
    mock_aioresponse.post(Operation.USERS, payload={"foo": "bar"})
    resp = await test_client.post(**params)
    data = await resp.json()
    assert isinstance(resp, FreshChatResponse)
    assert {"foo": "bar"} == data
