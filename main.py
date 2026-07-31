"""
Ponto de entrada do agente STF PSS — Data Engineering Agent.

Uso interativo:
    python main.py

O agente inicia um loop de chat no terminal.
"""

from __future__ import annotations

from a_agent import Agent
from c_tools.avaliar_modelo_tool import AvaliarModeloTool
from c_tools.busca_informacao_tool import BuscaInformacaoTool
from c_tools.calcular_metricas_tool import CalcularMetricasTool
from c_tools.executar_clustering_tool import ExecutarClusteringTool
from c_tools.gerar_plots_tool import GerarPlotsTool
from c_tools.treinar_predicao_tool import TreinarPredicaoTool
from c_tools.file_csv_tool import ValidarCsvTool
from c_tools.pyspark_tool import PerfilCsvPySparkTool
from c_tools.sqlite_tool import ExecutarSqliteTool


def build_agent() -> Agent:
    """Monta e retorna o agente com todas as skills e ferramentas registradas."""
    agent = Agent()

    # Carrega todas as skills em b_skills/*.md automaticamente
    agent.load_skills_from_dir("b_skills")

    # Ferramentas — adicione novas ferramentas aqui
    agent.register_tool(BuscaInformacaoTool())
    agent.register_tool(TreinarPredicaoTool())
    agent.register_tool(ExecutarClusteringTool())
    agent.register_tool(AvaliarModeloTool())
    agent.register_tool(CalcularMetricasTool())
    agent.register_tool(GerarPlotsTool())
    agent.register_tool(ValidarCsvTool())
    agent.register_tool(ExecutarSqliteTool())
    agent.register_tool(PerfilCsvPySparkTool())

    return agent


def main() -> None:
    print("=" * 60)
    print("  STF PSS — Data Engineering Agent")
    print("  Digite 'sair' para encerrar | 'reset' para limpar contexto")
    print("=" * 60)

    agent = build_agent()

    while True:
        try:
            user_input = input("\nVocê: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAté logo!")
            break

        if not user_input:
            continue

        if user_input.lower() == "sair":
            print("Até logo!")
            break

        if user_input.lower() == "reset":
            agent.reset()
            print("Contexto limpo.")
            continue

        response = agent.run(user_input)
        print(f"\nAgente: {response}")


if __name__ == "__main__":
    main()
