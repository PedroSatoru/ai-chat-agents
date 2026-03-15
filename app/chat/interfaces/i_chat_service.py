from abc import ABC, abstractmethod
from app.chat.model import SendMessagePayload


class IChatService(ABC):
    @abstractmethod
    async def send_message(self, user_id: str, payload: SendMessagePayload) -> dict:
        raise NotImplementedError()

    @abstractmethod
    async def get_history(self, user_id: str, conversation_id: str) -> list[dict]:
        raise NotImplementedError()
