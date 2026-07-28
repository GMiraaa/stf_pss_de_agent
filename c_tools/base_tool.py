"""
Classe base para todas as ferramentas do agente.

Uma ferramenta é uma função que o agente pode chamar para interagir com o
mundo externo (executar SQL, fazer chamadas HTTP, ler arquivos, etc.).

Para adicionar uma nova ferramenta:
1. Crie um arquivo em `c_tools/` (ex.: `sql_tool.py`).
2. Herde de `BaseTool`.
3. Implemente `name`, `description`, `parameters` e `run()`.
4. Registre no `main.py` com `agent.register_tool(MinhaFerramenta())`.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseTool(ABC):
    """Interface que toda ferramenta deve implementar."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Identificador único da ferramenta (ex.: 'executar_sql')."""

    @property
    @abstractmethod
    def description(self) -> str:
        """Descrição clara do que a ferramenta faz (usada pelo LLM para decidir quando chamá-la)."""

    @property
    @abstractmethod
    def parameters(self) -> dict[str, Any]:
        """
        Schema JSON dos parâmetros da ferramenta no formato OpenAI:

        {
            "type": "object",
            "properties": {
                "param1": {"type": "string", "description": "..."},
            },
            "required": ["param1"],
        }
        """

    @abstractmethod
    def run(self, **kwargs: Any) -> Any:
        """Executa a ferramenta com os parâmetros fornecidos e retorna o resultado."""

    def schema(self) -> dict[str, Any]:
        """Retorna a declaração da função (nome, descrição e parâmetros)."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Tool name={self.name!r}>"
