from datetime import datetime, timezone

from app.chat.interfaces.i_chat_service import IChatService
from app.chat.interfaces.repository.i_chat_repository import IChatRepository
from app.chat.messages.assistant_message import AssistantMessage
from app.chat.messages.user_message import UserMessage
from app.chat.model import SendMessagePayload
from app.shared.utils import generate_hash_id


class ChatService(IChatService):
    def __init__(self, repository: IChatRepository):
        self._repository = repository

    async def send_message(self, user_id: str, payload: SendMessagePayload) -> dict:
        conversation_id = payload.chat_id or generate_hash_id()
        conversation = await self._repository.get_conversation(
            user_id=user_id,
            conversation_id=conversation_id,
        )

        now = datetime.now(timezone.utc)
        if not conversation:
            conversation = {
                "conversation_id": conversation_id,
                "user_id": user_id,
                "title": payload.title or "Nova conversa",
                "created_at": now,
                "messages": [],
            }

        user_message = UserMessage(
            text=payload.prompt,
            conversation_id=conversation_id,
            user_id=user_id,
            model=payload.model,
            max_tokens=payload.max_tokens,
            temperature=payload.temperature,
        )
        conversation["messages"].append({"role": "user", **user_message.as_dict()})

        assistant = AssistantMessage(
            text=f"[entrega-1] Mensagem recebida com sucesso: {payload.prompt}",
            conversation_id=conversation_id,
        )
        conversation["messages"].append(assistant.as_dict())

        conversation["updated_at"] = now
        await self._repository.save_conversation(conversation)

        return {
            "conversation_id": conversation_id,
            "messages": conversation["messages"],
        }

    async def get_history(self, user_id: str, conversation_id: str) -> list[dict]:
        conversation = await self._repository.get_conversation(
            user_id=user_id,
            conversation_id=conversation_id,
        )
        if not conversation:
            return []
        return conversation.get("messages", [])
