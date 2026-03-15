from typing import Annotated

from fastapi import APIRouter, Depends

from app.chat.dependencies import get_chat_service, get_user_id
from app.chat.interfaces.i_chat_service import IChatService
from app.chat.model import SendMessagePayload

router = APIRouter()


@router.post("/chat/send")
async def send_message(
    payload: SendMessagePayload,
    service: Annotated[IChatService, Depends(get_chat_service)],
    user_id: Annotated[str, Depends(get_user_id)],
):
    return await service.send_message(user_id=user_id, payload=payload)


@router.get("/chat/{conversation_id}/history")
async def get_history(
    conversation_id: str,
    service: Annotated[IChatService, Depends(get_chat_service)],
    user_id: Annotated[str, Depends(get_user_id)],
):
    messages = await service.get_history(user_id=user_id, conversation_id=conversation_id)
    return {"conversation_id": conversation_id, "messages": messages}
