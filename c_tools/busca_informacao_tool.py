"""
Ferramenta de exemplo: busca em memória (mock).

Substitua pela implementação real (ex.: consulta a banco de dados,
chamada HTTP a uma API, leitura de arquivo, etc.).
"""

from __future__ import annotations

from typing import Any

from c_tools.base_tool import BaseTool


class BuscaInformacaoTool(BaseTool):
    """Busca uma informação em uma base de conhecimento simulada."""

    @property
    def name(self) -> str:
        return "buscar_informacao"

    @property
    def description(self) -> str:
        return (
            "Busca informações sobre Engenharia de Dados na base de conhecimento interna. "
            "Use quando precisar de detalhes técnicos ou definições."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "consulta": {
                    "type": "string",
                    "description": "Termo ou pergunta a ser buscada.",
                }
            },
            "required": ["consulta"],
        }

    def run(self, consulta: str) -> str:  # type: ignore[override]
        # Substitua esta implementação por uma busca real (vetorial, SQL, etc.)
        return (
            f"[mock] Resultado para '{consulta}': "
            "Informação não encontrada na base de conhecimento simulada. "
            "Implemente a busca real em `c_tools/busca_informacao_tool.py`."
        )
