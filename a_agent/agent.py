"""
Core Agent — loop de raciocínio e ação (ReAct) sobre o Google Gemini.

O agente recebe uma tarefa, raciocina sobre ela, decide quais ferramentas
usar e retorna uma resposta final ao usuário.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import google.generativeai as genai

from d_config.settings import settings


class Agent:
    """Agente de Engenharia de Dados baseado em Gemini com suporte a ferramentas e skills."""

    def __init__(self) -> None:
        genai.configure(api_key=settings.google_api_key)
        self._tools: dict[str, Any] = {}
        self._skills: list[str] = []
        self._model: genai.GenerativeModel | None = None
        self._chat: genai.ChatSession | None = None
        self._rebuild()

    # ------------------------------------------------------------------
    # Registro de ferramentas e skills
    # ------------------------------------------------------------------

    def register_tool(self, tool: Any) -> None:
        """Registra uma ferramenta disponível para o agente."""
        self._tools[tool.name] = tool
        self._rebuild()

    def register_skill(self, content: str) -> None:
        """Registra uma skill a partir de uma string de conteúdo (Markdown)."""
        self._skills.append(content)
        self._rebuild()

    def load_skills_from_dir(self, path: str | Path = "b_skills") -> None:
        """Lê todos os arquivos .md de um diretório e registra como skills."""
        for md_file in sorted(Path(path).glob("*.md")):
            self._skills.append(md_file.read_text(encoding="utf-8"))
        self._rebuild()

    # ------------------------------------------------------------------
    # Construção interna
    # ------------------------------------------------------------------

    def _build_system_prompt(self) -> str:
        skill_block = "\n\n---\n\n".join(self._skills) if self._skills else ""
        return (
            "Você é um agente especialista em Engenharia de Dados do STF PSS. "
            "Responda sempre em português do Brasil. "
            "Pense passo a passo antes de responder. "
            "Use as ferramentas disponíveis sempre que necessário.\n\n"
            + (f"## Conhecimentos disponíveis\n\n{skill_block}" if skill_block else "")
        ).strip()

    def _build_google_tools(self) -> list[dict] | None:
        if not self._tools:
            return None
        return [
            {
                "function_declarations": [
                    {
                        "name": t.name,
                        "description": t.description,
                        "parameters": t.parameters,
                    }
                    for t in self._tools.values()
                ]
            }
        ]

    def _rebuild(self) -> None:
        """Reconstrói o modelo e inicia uma nova sessão de chat."""
        self._model = genai.GenerativeModel(
            model_name=settings.model,
            system_instruction=self._build_system_prompt(),
            tools=self._build_google_tools(),
            generation_config=genai.GenerationConfig(
                temperature=settings.temperature,
            ),
        )
        self._chat = self._model.start_chat()

    # ------------------------------------------------------------------
    # Execução
    # ------------------------------------------------------------------

    def run(self, user_message: str) -> str:
        """Executa o loop ReAct para uma mensagem do usuário e retorna a resposta."""
        response = self._chat.send_message(user_message)

        for _ in range(settings.max_iterations):
            # Coleta todas as chamadas de ferramenta na resposta atual
            fn_calls = [
                part.function_call
                for part in response.parts
                if part.function_call.name
            ]

            if not fn_calls:
                return response.text

            # Executa cada ferramenta e monta as respostas
            result_parts = []
            for fn in fn_calls:
                tool_name = fn.name
                tool_args = dict(fn.args)

                if tool_name not in self._tools:
                    result = f"Ferramenta '{tool_name}' não encontrada."
                else:
                    try:
                        result = self._tools[tool_name].run(**tool_args)
                    except Exception as exc:  # noqa: BLE001
                        result = f"Erro ao executar '{tool_name}': {exc}"

                result_parts.append(
                    genai.protos.Part(
                        function_response=genai.protos.FunctionResponse(
                            name=tool_name,
                            response={"result": str(result)},
                        )
                    )
                )

            response = self._chat.send_message(result_parts)

        return "Limite de iterações atingido. Tente reformular a pergunta."

    def reset(self) -> None:
        """Inicia uma nova sessão de chat (limpa o histórico de conversa)."""
        self._chat = self._model.start_chat()

