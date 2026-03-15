from typing import Annotated
from pydantic import BaseModel, Field, field_validator


class SendMessagePayload(BaseModel):
    chat_id: str | None = None
    prompt: str
    model: str = "openai/gpt-4.1-mini"
    max_tokens: int = 512
    temperature: Annotated[float, Field(ge=0.0, le=1.0)] = 0.7
    title: str | None = None

    @field_validator("temperature", mode="before")
    @classmethod
    def round_temperature(cls, value: float) -> float:
        return round(float(value), 1)
