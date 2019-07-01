from dataclasses import asdict

import pytest


def test_configuration_headers(test_config, auth_header):
    assert asdict(test_config.headers) == {"Authorization": f"Bearer {auth_header}"}


@pytest.mark.parametrize(
    "url, path",
    [
        ("http://127.0.0.1:8000/User/uuid/message", ["User", "uuid", "message"]),
        ("http://127.0.0.1:8000/Conversation", ["Conversation"]),
    ],
)
def test_get_url(url, path, test_config):
    get_url = test_config.get_url(*path)
    assert str(get_url) == str(url)
