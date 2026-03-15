from abc import ABC, abstractmethod
from typing import Optional


class IChatRepository(ABC):
    @abstractmethod
    async def get_conversation(self, user_id: str, conversation_id: str) -> Optional[dict]:
        raise NotImplementedError()

    @abstractmethod
    async def save_conversation(self, conversation: dict) -> None:
        raise NotImplementedError()
