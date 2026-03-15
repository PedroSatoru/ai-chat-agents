from typing import Annotated

from fastapi import Depends, Header

from app.chat.interfaces.i_chat_service import IChatService
from app.startup import startup


def get_current_user_id(x_user_id: Annotated[str, Header()]) -> str:
    return x_user_id


def get_chat_service() -> IChatService:
    return startup.build_chat_service()


def get_user_id(user_id: Annotated[str, Depends(get_current_user_id)]) -> str:
    return user_id
