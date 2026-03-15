from dataclasses import dataclass

from app.chat.messages.message import Message


@dataclass
class UserMessage(Message):
    user_id: str
    model: str
    max_tokens: int
    temperature: float
