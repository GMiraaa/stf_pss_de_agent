"""
Testes básicos do agente.

Execute com: pytest e_tests/
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from c_tools.base_tool import BaseTool


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_FAKE_SKILL_CONTENT = "## Fake Skill\nConteúdo de teste."


class _FakeTool(BaseTool):
    @property
    def name(self) -> str:
        return "fake_tool"

    @property
    def description(self) -> str:
        return "Ferramenta de teste."

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {"entrada": {"type": "string"}},
            "required": ["entrada"],
        }

    def run(self, entrada: str) -> str:  # type: ignore[override]
        return f"resultado: {entrada}"


# ---------------------------------------------------------------------------
# Testes de Tool
# ---------------------------------------------------------------------------


def test_tool_schema_format() -> None:
    tool = _FakeTool()
    schema = tool.schema()
    assert schema["name"] == "fake_tool"
    assert "parameters" in schema


def test_tool_run() -> None:
    tool = _FakeTool()
    assert tool.run(entrada="teste") == "resultado: teste"


# ---------------------------------------------------------------------------
# Testes do Agente (com mock da API)
# ---------------------------------------------------------------------------


@patch("a_agent.agent.genai")
def test_agent_run_simple_response(mock_genai: MagicMock) -> None:
    """O agente deve retornar a resposta do LLM quando não há tool calls."""
    from a_agent.agent import Agent

    mock_part = MagicMock()
    mock_part.function_call.name = ""  # sem chamada de ferramenta

    mock_response = MagicMock()
    mock_response.parts = [mock_part]
    mock_response.text = "Resposta simulada."

    mock_chat = MagicMock()
    mock_chat.send_message.return_value = mock_response
    mock_genai.GenerativeModel.return_value.start_chat.return_value = mock_chat

    agent = Agent()
    response = agent.run("Olá, como você pode me ajudar?")

    assert response == "Resposta simulada."


@patch("a_agent.agent.genai")
def test_agent_register_skill(mock_genai: MagicMock) -> None:
    """Skills registradas devem aparecer no prompt de sistema."""
    from a_agent.agent import Agent

    agent = Agent()
    agent.register_skill(_FAKE_SKILL_CONTENT)

    assert "Fake Skill" in agent._build_system_prompt()


@patch("a_agent.agent.genai")
def test_agent_register_tool(mock_genai: MagicMock) -> None:
    """Ferramentas registradas devem estar disponíveis no agente."""
    from a_agent.agent import Agent

    agent = Agent()
    agent.register_tool(_FakeTool())

    assert "fake_tool" in agent._tools


@patch("a_agent.agent.genai")
def test_agent_reset(mock_genai: MagicMock) -> None:
    """Reset deve criar uma nova sessão de chat."""
    from a_agent.agent import Agent

    agent = Agent()
    old_chat = agent._chat
    mock_genai.GenerativeModel.return_value.start_chat.return_value = MagicMock()
    agent.reset()

    assert agent._chat is not None
