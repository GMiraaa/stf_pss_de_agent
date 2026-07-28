"""
Configurações centralizadas do agente.

Os valores são lidos de variáveis de ambiente (arquivo `.env` na raiz).
Copie `.env.example` para `.env` e preencha as variáveis.
"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # LLM
    google_api_key: str = Field(..., description="Chave de API do Google AI Studio.")
    model: str = Field("gemini-1.5-flash", description="Modelo Gemini a ser utilizado.")
    temperature: float = Field(0.2, description="Temperatura de geração do LLM (0–2).")

    # Agente
    max_iterations: int = Field(10, description="Número máximo de iterações do loop ReAct.")


settings = Settings()  # type: ignore[call-arg]
