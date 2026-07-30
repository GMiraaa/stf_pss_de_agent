# Catálogo de Agentes

Todos os agentes abaixo são perfis operacionais do `Agent` atual em `a_agent/agent.py`. Eles são materializados por skills Markdown carregadas de `b_skills/`, tools registradas em `main.py` e workflows executáveis em `workflows/`.

| Agente | ID | Responsabilidade principal | Skills | Tools | Status |
| --- | --- | --- | --- | --- | --- |
| Data Engineering Orchestrator Agent | `de.orchestrator.agent` | Classificar objetivo, selecionar agentes/skills, consolidar plano, riscos e limitações. | Todas | `buscar_informacao`, `validar_csv`, `executar_sqlite`, `perfil_csv_pyspark` | Implementado |
| Data Ingestion Agent | `de.ingestion.agent` | Validar origem, formato, schema, metadados, quarentena e idempotência. | `de.skill.ingestao_arquivos_csv` | `validar_csv` | Implementado |
| File Processing Agent | `de.files.agent` | Processar CSV, JSON, Parquet, compactados, encoding e conversão para formatos colunares. | `de.skill.ingestao_arquivos_csv` | `validar_csv` | Implementado parcialmente |
| ETL/ELT Agent | `de.etl_elt.agent` | Definir ETL/ELT, carga full/incremental, reprocessamento, validação e auditoria. | `de.skill.etl_elt_pyspark`, `de.skill.batch_streaming_orquestracao` | `executar_sqlite`, `perfil_csv_pyspark` | Implementado parcialmente |
| Data Cleaning Agent | `de.cleaning.agent` | Tratar nulos, duplicidades, strings, tipos, datas e rejeições com rastreabilidade. | `de.skill.etl_elt_pyspark`, `de.skill.qualidade_observabilidade` | `buscar_informacao` | Documentado |
| Data Mapping Agent | `de.mapping.agent` | Mapear origem-destino, colunas, tipos, códigos, regras e versões. | `de.skill.etl_elt_pyspark`, `de.skill.lakehouse_delta_schema_contracts` | `buscar_informacao` | Documentado |
| Data Transformation Agent | `de.transformation.agent` | Aplicar filtros, joins, derivações, agregações, flatten, pivot/unpivot e validação. | `de.skill.etl_elt_pyspark` | `buscar_informacao` | Documentado |
| Spark/PySpark Agent | `de.spark.agent` | Configurar Spark, analisar plano, evitar anti-patterns e orientar performance. | `de.skill.etl_elt_pyspark` | `perfil_csv_pyspark` | Implementado parcialmente |
| Data Quality Agent | `de.quality.agent` | Executar regras, classificar falhas, gerar evidências, quarentena e histórico. | `de.skill.qualidade_observabilidade` | `buscar_informacao` | Documentado |
| Data Observability Agent | `de.observability.agent` | Monitorar status, volume, duração, erros, freshness, SLA, drift e métricas técnicas. | `de.skill.qualidade_observabilidade` | `buscar_informacao` | Documentado |
| Delta Lake Agent | `de.delta_lake.agent` | Orientar append, merge, schema enforcement/evolution, time travel, compactação e retenção. | `de.skill.lakehouse_delta_schema_contracts` | `buscar_informacao` | Documentado |
| Schema and Contract Agent | `de.schema_contract.agent` | Validar schema, contratos, compatibilidade e alterações destrutivas. | `de.skill.lakehouse_delta_schema_contracts` | `buscar_informacao` | Documentado |
| Batch Processing Agent | `de.batch.agent` | Planejar agenda, janelas, retry, backfill, checkpoint, lock e SLA. | `de.skill.batch_streaming_orquestracao` | `buscar_informacao` | Documentado |
| Streaming Agent | `de.streaming.agent` | Planejar checkpoint, offset, watermark, late data, DLQ e semântica de entrega. | `de.skill.batch_streaming_orquestracao` | `buscar_informacao` | Documentado |
| Performance Optimization Agent | `de.performance.agent` | Diagnosticar shuffle, skew, small files, particionamento, cache e baseline. | `de.skill.etl_elt_pyspark`, `de.skill.qualidade_observabilidade` | `buscar_informacao` | Documentado |
| Data Lineage and Metadata Agent | `de.lineage.agent` | Registrar origem, destino, schema, transformação, versão, qualidade e dependências. | `de.skill.lakehouse_delta_schema_contracts`, `de.skill.integracao_bancos_mcp_entrega` | `buscar_informacao` | Documentado |
| Database Integration Agent | `de.database.agent` | Conexão segura, leitura/escrita, chunking, CDC/incremental, transação e reconciliação. | `de.skill.integracao_bancos_mcp_entrega` | `executar_sqlite` | Implementado parcialmente |
| Data Delivery Agent | `de.delivery.agent` | Preparar entrega técnica, contratos, reconciliação, freshness e consumo Power BI. | `de.skill.integracao_bancos_mcp_entrega`, `de.skill.qualidade_observabilidade` | `buscar_informacao` | Documentado |

## Guardrails comuns

- Não executar operação destrutiva sem política explícita.
- Não registrar credenciais, tokens, strings completas de conexão ou dados pessoais desnecessários.
- Não declarar compatibilidade com Spark, Delta, MCP ou exatamente-uma-vez sem verificar o ambiente.
- Não transformar o repositório em Data Analytics ou Data Science; estatística e visualização são usadas para operação, qualidade e observabilidade.
