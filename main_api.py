"""
Servidor HTTP do agente — necessário para o chat participant do VS Code.

Execute antes de abrir o chat no VS Code:
    uvicorn main_api:app --port 8765 --reload
"""

from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from main import build_agent

app = FastAPI(title="STF DE Agent API", version="0.1.0")

# Instância única do agente reutilizada entre requisições
_agent = build_agent()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """Envia uma mensagem ao agente e retorna a resposta."""
    reply = _agent.run(request.message)
    return ChatResponse(response=reply)


@app.post("/reset")
def reset() -> dict[str, str]:
    """Limpa o histórico de conversa do agente."""
    _agent.reset()
    return {"status": "ok"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
