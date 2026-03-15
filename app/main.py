from fastapi import FastAPI

from app.chat.router import router as chat_router

app = FastAPI(title="ai-chat-agents | Entrega 1")
app.include_router(chat_router, prefix="/api", tags=["chat"])


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
