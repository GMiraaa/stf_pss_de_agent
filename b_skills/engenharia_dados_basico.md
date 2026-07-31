# Engenharia de Dados — Conceitos Fundamentais

## Metadados
- **id:** `de.skill.fundamentos`
- **versão:** `1.0.0`
- **categoria:** fundamentos
- **objetivo:** Fornecer vocabulário e decisões-base para conversas de Engenharia de Dados.
- **entrada esperada:** Pergunta conceitual, dúvida de arquitetura ou solicitação de orientação inicial.
- **saída esperada:** Explicação objetiva em português, com limites entre Data Engineering, Analytics e Science.
- **parâmetros:** Nenhum.
- **validações:** Verificar se a resposta permanece no escopo de Engenharia de Dados.
- **dependências:** Nenhuma.
- **exceções:** Não substitui documentação operacional específica do projeto.
- **retry:** Não aplicável.
- **idempotência:** Determinística como referência textual.
- **efeitos colaterais:** Nenhum.
- **limitações:** Não executa pipelines nem valida dados reais.
- **testes:** `e_tests/test_artifact_catalogs.py`.
- **agentes consumidores:** `de.orchestrator.agent` e todos os agentes especializados quando precisarem de contexto base.
- **origem:** Implementação original do projeto.
- **licença:** Mesma licença do repositório.

## Pipelines de dados
- **ETL** (Extract, Transform, Load): extrai dados da fonte, transforma e carrega no destino.
- **ELT** (Extract, Load, Transform): carrega os dados brutos primeiro e transforma no destino.
- Ferramentas comuns: Apache Airflow, dbt, Spark, Kafka.

## Armazenamento
- **Data Warehouse**: armazenamento analítico estruturado (ex.: BigQuery, Redshift, Snowflake).
- **Data Lake**: armazenamento de dados brutos em qualquer formato (ex.: S3, GCS, ADLS).
- **Data Lakehouse**: combina as vantagens dos dois (ex.: Delta Lake, Apache Iceberg).

## Qualidade de dados
- Verificações de schema, nulidade, unicidade e integridade referencial.
- Ferramentas: Great Expectations, dbt tests, Soda.

## SQL relevante para Engenharia de Dados
- CTEs (`WITH`), window functions, particionamento de tabelas, índices.
- `EXPLAIN ANALYZE` para otimização de queries.
