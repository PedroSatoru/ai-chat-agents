from dataclasses import asdict, dataclass, field
from datetime import datetime

from app.shared.utils import generate_hash_id


@dataclass(kw_only=True)
class Message:
    text: str
    conversation_id: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    message_id: str = field(default_factory=generate_hash_id)

    def as_dict(self) -> dict:
        return asdict(self)
