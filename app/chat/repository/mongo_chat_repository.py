from datetime import datetime, timezone
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.chat.interfaces.repository.i_chat_repository import IChatRepository
from app.core.config import settings


class MongoChatRepository(IChatRepository):
    def __init__(self, database: AsyncIOMotorDatabase):
        self._conversations = database[settings.MONGO_CONVERSATIONS_COLLECTION]

    async def get_conversation(self, user_id: str, conversation_id: str) -> Optional[dict]:
        doc = await self._conversations.find_one({"_id": conversation_id, "user_id": user_id})
        if not doc:
            return None

        conversation = dict(doc)
        conversation.pop("_id", None)
        return conversation

    async def save_conversation(self, conversation: dict) -> None:
        conversation_id = conversation.get("conversation_id")
        user_id = conversation.get("user_id")
        if not conversation_id or not user_id:
            raise ValueError("conversation must include 'conversation_id' and 'user_id'")

        payload = self._serialize(conversation)
        payload["_id"] = conversation_id
        payload["updated_at"] = datetime.now(timezone.utc).isoformat()

        await self._conversations.update_one(
            {"_id": conversation_id, "user_id": user_id},
            {"$set": payload},
            upsert=True,
        )

    def _serialize(self, value):
        if isinstance(value, dict):
            return {k: self._serialize(v) for k, v in value.items()}
        if isinstance(value, list):
            return [self._serialize(item) for item in value]
        if isinstance(value, datetime):
            return value.isoformat()
        return value
