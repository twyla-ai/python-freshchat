import os
from dataclasses import dataclass, field
from typing import AnyStr, Dict, Optional
from urllib.parse import urljoin


@dataclass
class FreshChatConfiguration:
    """
    Class represents the base configuration for Freshchat
    """

    app_id: str
    token: str = field(repr=False)
    default_channel_id: Optional[str] = field(default=None)
    default_initial_message: Optional[str] = field(default=None)
    url: Optional[str] = field(
        default_factory=lambda: os.environ.get(
            "FRESHCHAT_API_URL", "https://api.freshchat.com/v2/"
        )
    )

    @property
    def authorization_header(self) -> Dict[AnyStr, AnyStr]:
        """
        Property which returns the proper format of the authorization header
        """

        return {
            "Authorization": f"Bearer {self.token}"
            if "Bearer" not in self.token
            else self.token
        }

    def get_url(self, endpoint: str) -> str:
        """
        Method responsible to build the url using the given endpoint

        :param endpoint: String with the endpoint which needs to attached to URL
        :return: a string which represents URL
        """
        return urljoin(self.url, endpoint.lstrip("/"))
