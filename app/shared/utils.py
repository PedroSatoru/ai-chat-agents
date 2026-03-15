import hashlib
import uuid


def generate_hash_id() -> str:
    unique_id = uuid.uuid4().hex
    return hashlib.sha256(unique_id.encode()).hexdigest()[:20]
