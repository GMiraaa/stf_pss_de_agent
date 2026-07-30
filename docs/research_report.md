# Relatório da Pesquisa

## Objetivo

Pesquisar projetos open source aplicáveis a agentes, skills, MCP e práticas de Engenharia de Dados, selecionando apenas referências seguras e úteis para orientar artefatos locais.

## Estratégia

Termos usados: `data engineering agent`, `ETL agent`, `PySpark agent`, `MCP data engineering`, `MCP database`, `MCP filesystem`, `data quality`, `Delta Lake`, `OpenLineage`, `data observability`, `multi-agent framework`.

Foram analisados 11 repositórios/fontes públicas. Nenhum artefato externo foi copiado.

## Critérios e pesos

| Critério | Peso |
| --- | ---: |
| Relevância para Data Engineering | 15% |
| Qualidade técnica | 15% |
| Compatibilidade com o projeto | 15% |
| Cobertura dos requisitos | 15% |
| Licença | 10% |
| Modularidade | 8% |
| Segurança | 7% |
| Testes | 5% |
| Documentação | 5% |
| Atividade recente | 3% |
| Execução local | 2% |

## Ranking dos candidatos

| Repositório | URL | Licença | Atividade observada | Pontuação | Decisão | Justificativa |
| --- | --- | --- | --- | ---: | --- | --- |
| Great Expectations | https://github.com/great-expectations/great_expectations | Apache-2.0 | Releases em 2026 e docs ativas | 4.4 | Referência | Forte para qualidade; adoção direta exigiria dependência nova. |
| Delta Lake | https://github.com/delta-io/delta | Apache-2.0 | Release 4.2.0 em 2026 nas fontes consultadas | 4.3 | Referência | Forte aderência a Lakehouse; execução depende de Spark/Delta instalados. |
| OpenLineage | https://github.com/OpenLineage/OpenLineage | Apache-2.0 | Release 1.48.0 em 2026 nas fontes consultadas | 4.2 | Referência | Padrão adequado para linhagem; não necessário incorporar cliente agora. |
| Model Context Protocol servers | https://github.com/modelcontextprotocol/servers | MIT | Projeto amplo, issues/PRs ativos | 4.0 | Referência | Útil para filesystem MCP; requer controle forte de permissões. |
| DataHub | https://github.com/datahub-project/datahub | Apache-2.0 | Docs de OpenLineage consultadas | 3.9 | Referência | Catálogo robusto, mas pesado para execução local inicial. |
| dbt MCP | https://github.com/dbt-labs/dbt-mcp | Apache-2.0 | Releases em 2026 nas fontes consultadas | 3.7 | Referência | Útil quando dbt entrar no escopo; não é foco atual. |
| LangChain | https://github.com/langchain-ai/langchain | MIT | Alta atividade | 3.4 | Rejeitado como dependência | Framework genérico; arquitetura local já resolve loop básico. |
| CrewAI | https://github.com/crewAIInc/crewAI | MIT | Alta atividade | 3.2 | Rejeitado como dependência | Multiagente genérico, com possível telemetria configurável e dependência grande. |
| LlamaIndex | https://github.com/run-llama/llama_index | MIT | Alta atividade | 3.0 | Rejeitado como dependência | Foco maior em RAG/documentos do que execução de pipelines. |
| Microsoft AutoGen | https://github.com/microsoft/autogen | MIT/CC-BY-4.0 | Fonte consultada informa maintenance mode | 2.5 | Rejeitado | Risco de adoção nova e licença mista/documentação. |
| Marquez | https://github.com/MarquezProject/marquez | Apache-2.0 conforme projeto OpenLineage/Marquez | Fonte consultada indica compatibilidade OpenLineage | 3.6 | Referência | Boa opção futura para backend de linhagem; pesado para MVP local. |

## Duplicidades identificadas

- `Data Quality Agent` e `Data Observability Agent` compartilham métricas, mas foram separados porque qualidade decide conformidade de dados e observabilidade monitora execução.
- `Delta Lake Agent` e `Schema and Contract Agent` compartilham schema evolution, mas foram separados porque Delta trata armazenamento/transações e contrato trata compatibilidade/SLAs.
- `File Processing Agent` e `Data Ingestion Agent` compartilham leitura de arquivos; file processing é executor especializado, ingestion coordena origem, metadados e idempotência.

## Capacidades implementadas originalmente

Skills Markdown de ingestão, ETL/PySpark, qualidade/observabilidade, lakehouse/contratos, integração/MCP/entrega e batch/streaming/orquestração.

## Lacunas restantes

- Tools reais para Spark, SQL, arquivos e métricas ainda não foram implementadas.
- Testes atuais validam integridade dos artefatos, não execução de pipeline real.
- MCPs não foram instalados por decisão de escopo e segurança.
