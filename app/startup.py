from functools import lru_cache

from app.chat.interfaces.i_chat_service import IChatService
from app.chat.interfaces.repository.i_chat_repository import IChatRepository
from app.chat.repository.mongo_chat_repository import MongoChatRepository
from app.chat.service.chat_service import ChatService
from app.core.config import mongo_db


class Startup:
    @lru_cache
    def get_chat_repository(self) -> IChatRepository:
        return MongoChatRepository(mongo_db)

    def build_chat_service(self) -> IChatService:
        return ChatService(repository=self.get_chat_repository())


startup = Startup()
