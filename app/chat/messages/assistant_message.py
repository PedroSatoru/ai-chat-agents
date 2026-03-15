from dataclasses import dataclass

from app.chat.messages.message import Message


@dataclass
class AssistantMessage(Message):
    role: str = "assistant"
