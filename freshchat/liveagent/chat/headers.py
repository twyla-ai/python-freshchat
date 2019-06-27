from dataclasses import dataclass
from enum import Enum
from typing import Dict, AnyStr

from cafeteria.logging import LoggedObject


class HeaderKey(Enum):
    """
    Class which provides the required header fields for freshchat api requests
    """

    AUTHORIZATION = "Authorization"


@dataclass
class FreshChatHeaders(LoggedObject):
    """
    Class which represents the headers for requesting freshchat API
    """

    Authorization: str = ""

    @classmethod
    def load(cls, data: Dict[AnyStr, AnyStr]) -> "FreshChatHeaders":
        return cls(Authorization=f"Bearer {data.get('Authorization')}")
