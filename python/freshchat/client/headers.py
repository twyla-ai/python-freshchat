from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from cafeteria.logging import LoggedObject


@dataclass
class FreshChatHeaders(LoggedObject):
    """
    Class which represents the headers for requesting freshchat API
    """

    Authorization: Optional[str] = field(default=None)

    def __post_init__(self):
        self.Authorization = f"Bearer {self.Authorization}"
