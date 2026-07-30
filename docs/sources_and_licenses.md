# Fontes, Licenças e Rastreabilidade

Consulta realizada em 2026-07-30. Nenhum código, prompt ou documentação de terceiros foi copiado. As fontes abaixo foram usadas apenas como referência conceitual e para avaliação de licenças/maturidade.

| Repositório | URL | Licença verificada | Evidências públicas consultadas | Uso no projeto | Decisão |
| --- | --- | --- | --- | --- | --- |
| Great Expectations | https://github.com/great-expectations/great_expectations | Apache-2.0 | README, releases, docs públicas | Referência conceitual para regras de qualidade e validação. | Referência, sem cópia |
| Delta Lake | https://github.com/delta-io/delta | Apache-2.0 | README e metadados do GitHub | Referência conceitual para Delta Lake open source/lakehouse. | Referência, sem cópia |
| OpenLineage | https://github.com/OpenLineage/OpenLineage | Apache-2.0 | README, releases, licença | Referência para linhagem e eventos de execução. | Referência, sem cópia |
| DataHub | https://github.com/datahub-project/datahub | Apache-2.0 | Documentação de integração OpenLineage | Referência para integração de catálogo/linhagem. | Referência, sem cópia |
| Model Context Protocol servers | https://github.com/modelcontextprotocol/servers | MIT | README do servidor filesystem | Referência para guardrails MCP e filesystem. | Referência, sem cópia |
| Model Context Protocol spec | https://github.com/modelcontextprotocol/modelcontextprotocol | MIT | README do protocolo | Referência para MCP. | Referência, sem cópia |
| dbt MCP | https://github.com/dbt-labs/dbt-mcp | Apache-2.0 | README e metadados do GitHub | Referência de MCP aplicável a projetos dbt. | Referência, sem cópia |
| CrewAI | https://github.com/crewAIInc/crewAI | MIT | README e metadados do GitHub | Referência de framework multiagente; não adotado para evitar nova dependência. | Rejeitado como dependência |
| LangChain | https://github.com/langchain-ai/langchain | MIT | README e metadados do GitHub | Referência de agentes; não adotado para preservar arquitetura ReAct atual. | Rejeitado como dependência |
| Microsoft AutoGen | https://github.com/microsoft/autogen | MIT/CC-BY-4.0 conforme repo | README e aviso de manutenção | Rejeitado pela manutenção mode e licença mista em documentação. | Rejeitado |
| LlamaIndex | https://github.com/run-llama/llama_index | MIT | README e metadados do GitHub | Referência de RAG/agentes; baixa aderência direta a pipelines DE. | Rejeitado como dependência |

## Política de uso

- Licenças permissivas não implicam cópia automática.
- Projetos sem aderência direta, dependência proprietária, telemetria relevante ou complexidade operacional foram tratados apenas como referência.
- Qualquer adoção futura deve revalidar licença, versão, dependências, CVEs e compatibilidade local.
