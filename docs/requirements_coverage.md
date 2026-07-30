# Matriz de Cobertura de Requisitos

| Requisito | Agente principal | Skill | Workflow | Teste | Status |
| --- | --- | --- | --- | --- | --- |
| Ingestão de dados | Data Ingestion Agent | Ingestão de Arquivos e CSV | CSV para Bronze/Lakehouse | `test_validate_csv_reports_rejections` | Implementado local |
| ETL e ELT | ETL/ELT Agent | ETL, ELT e PySpark | Batch ETL PySpark | `test_skills_have_required_metadata` | Coberto por skill |
| Apache Spark e PySpark | Spark/PySpark Agent | ETL, ELT e PySpark | Batch ETL PySpark | `test_core_docs_exist` | Coberto por skill |
| Clean-up de dados | Data Cleaning Agent | ETL, ELT e PySpark | Batch ETL PySpark | `test_agent_catalog_lists_expected_agents` | Coberto por agente |
| Mapping | Data Mapping Agent | ETL, ELT e PySpark | Batch ETL PySpark | `test_agent_catalog_lists_expected_agents` | Coberto por agente |
| Transformation | Data Transformation Agent | ETL, ELT e PySpark | Batch ETL PySpark | `test_agent_catalog_lists_expected_agents` | Coberto por agente |
| Grouping e agregações | Spark/PySpark Agent | ETL, ELT e PySpark | Batch ETL PySpark | `test_core_docs_exist` | Coberto por skill |
| Qualidade de dados | Data Quality Agent | Qualidade, Profiling e Observabilidade | Validação de qualidade | `test_skills_have_required_metadata` | Coberto por skill |
| Estatísticas básicas | Data Quality Agent | Qualidade, Profiling e Observabilidade | Validação de qualidade | `test_core_docs_exist` | Coberto por skill |
| Profiling técnico | Data Quality Agent | Qualidade, Profiling e Observabilidade | Validação de qualidade | `test_core_docs_exist` | Coberto por skill |
| Boxplot/distribuição/outliers | Data Observability Agent | Qualidade, Profiling e Observabilidade | Validação de qualidade | `test_core_docs_exist` | Coberto conceitualmente |
| Covariância/correlação/heatmap | Data Observability Agent | Qualidade, Profiling e Observabilidade | Validação de qualidade | `test_core_docs_exist` | Coberto conceitualmente |
| Testes estatísticos técnicos | Performance Optimization Agent | Qualidade, Profiling e Observabilidade | Validação de qualidade | `test_core_docs_exist` | Coberto conceitualmente |
| A/B técnico | Performance Optimization Agent | ETL, ELT e PySpark | Batch ETL PySpark | `test_core_docs_exist` | Coberto conceitualmente |
| Variância operacional | Data Observability Agent | Qualidade, Profiling e Observabilidade | Validação de qualidade | `test_core_docs_exist` | Coberto conceitualmente |
| Tendência/sazonalidade/ruído | Data Observability Agent | Qualidade, Profiling e Observabilidade | Validação de qualidade | `test_core_docs_exist` | Coberto conceitualmente |
| Previsão de capacidade | Data Observability Agent | Qualidade, Profiling e Observabilidade | Validação de qualidade | `test_core_docs_exist` | Coberto conceitualmente |
| Classificação técnica | Data Quality Agent | Qualidade, Profiling e Observabilidade | Validação de qualidade | `test_core_docs_exist` | Coberto conceitualmente |
| Clustering técnico | Performance Optimization Agent | Qualidade, Profiling e Observabilidade | Validação de qualidade | `test_core_docs_exist` | Coberto conceitualmente |
| Delta Lake | Delta Lake Agent | Lakehouse, Delta Lake, Schemas e Contratos | CSV para Bronze/Lakehouse | `test_core_docs_exist` | Coberto por skill |
| Data Lake e Lakehouse | Delta Lake Agent | Lakehouse, Delta Lake, Schemas e Contratos | CSV para Bronze/Lakehouse | `test_core_docs_exist` | Coberto por skill |
| CSV | File Processing Agent | Ingestão de Arquivos e CSV | CSV para Bronze/Lakehouse | `test_csv_to_bronze_writes_data_quarantine_and_metadata` | Implementado local |
| Bancos de dados | Database Integration Agent | Integração com Bancos, MCP e Entrega | Carga incremental de banco | `test_sqlite_tool_allows_parametrized_select` | Implementado para SQLite |
| Processamento batch | Batch Processing Agent | Batch, Streaming e Orquestração | Backfill e reprocessamento | `test_core_docs_exist` | Coberto por skill |
| Processamento streaming | Streaming Agent | Batch, Streaming e Orquestração | Streaming técnico | `test_core_docs_exist` | Coberto por skill |
| Orquestração | Data Engineering Orchestrator Agent | Batch, Streaming e Orquestração | Todos | `test_agent_catalog_lists_expected_agents` | Coberto por agente |
| Observabilidade | Data Observability Agent | Qualidade, Profiling e Observabilidade | Validação de qualidade | `test_core_docs_exist` | Coberto por skill |
| Logging | Data Observability Agent | Qualidade, Profiling e Observabilidade | Todos | `test_core_docs_exist` | Coberto por skill |
| Linhagem e metadados | Data Lineage and Metadata Agent | Lakehouse/Contratos; Integração/MCP | Todos | `test_agent_catalog_lists_expected_agents` | Coberto por agente |
| Schema management | Schema and Contract Agent | Lakehouse, Delta Lake, Schemas e Contratos | Migração de schema/contrato | `test_core_docs_exist` | Coberto por skill |
| Particionamento | Spark/PySpark Agent | ETL, ELT e PySpark | Batch ETL PySpark | `test_core_docs_exist` | Coberto por skill |
| Performance | Performance Optimization Agent | ETL, ELT e PySpark | Batch ETL PySpark | `test_agent_catalog_lists_expected_agents` | Coberto por agente |
| Segurança e privacidade | Database Integration Agent | Integração com Bancos, MCP e Entrega | Todos | `test_security_doc_mentions_guardrails` | Coberto por doc/skill |
| Data contracts | Schema and Contract Agent | Lakehouse, Delta Lake, Schemas e Contratos | Migração de schema/contrato | `test_core_docs_exist` | Coberto por skill |
| DataViz operacional/Power BI | Data Delivery Agent | Integração com Bancos, MCP e Entrega | Entrega para Power BI | `test_core_docs_exist` | Coberto por skill |

## Observação

O status "Coberto conceitualmente" indica que o agente possui orientação e guardrails, mas ainda não há tool executora dedicada. "Implementado local" indica execução com biblioteca padrão e datasets pequenos/sintéticos.
