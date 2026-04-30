from fastapi import FastAPI

from app.chat.router import router as chat_router
from app.servicos.router import router as servicos_router

app = FastAPI(title="ai-chat-agents | Entrega 1")
app.include_router(chat_router, prefix="/api", tags=["chat"])
app.include_router(servicos_router, prefix="/api", tags=["servicos"])


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
