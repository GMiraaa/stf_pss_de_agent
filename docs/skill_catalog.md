# Catálogo de Skills

| Skill | ID | Finalidade | Agentes consumidores | Status |
| --- | --- | --- | --- | --- |
| Engenharia de Dados - Conceitos Fundamentais | `de.skill.fundamentos` | Vocabulário e limites de escopo. | Todos | Implementada |
| Ingestão de Arquivos e CSV | `de.skill.ingestao_arquivos_csv` | Ingestão de arquivos, CSV, JSON, Parquet, encoding, quarentena e idempotência. | Ingestion, Files, Orchestrator | Implementada |
| ETL, ELT e PySpark | `de.skill.etl_elt_pyspark` | Decisão ETL/ELT, pipelines batch/incrementais e práticas PySpark. | ETL/ELT, Spark, Transformation, Batch | Implementada |
| Qualidade, Profiling e Observabilidade | `de.skill.qualidade_observabilidade` | Regras de qualidade, profiling técnico, estatística operacional e métricas. | Quality, Observability, Delivery | Implementada |
| Lakehouse, Delta Lake, Schemas e Contratos | `de.skill.lakehouse_delta_schema_contracts` | Zonas, Delta open source, schema evolution e data contracts. | Delta, Schema Contract, Lineage | Implementada |
| Integração com Bancos, MCP e Entrega de Dados | `de.skill.integracao_bancos_mcp_entrega` | Bancos, APIs, MCP, segurança e entrega técnica para consumo. | Database, Delivery, Lineage | Implementada |
| Batch, Streaming e Orquestração | `de.skill.batch_streaming_orquestracao` | Batch, streaming, checkpoint, backfill, reprocessamento e orquestração. | Batch, Streaming, ETL/ELT | Implementada |

## Contrato mínimo

Cada skill em `b_skills/*.md` deve conter seção `## Metadados` com identificador, versão, categoria, objetivo, entrada esperada, saída esperada, parâmetros, validações, dependências, exceções, retry, idempotência, efeitos colaterais, limitações, testes, agentes consumidores, origem e licença.
