# Catálogo de Workflows

| Workflow | Origem | Destino | Agentes | Skills | Qualidade e observabilidade | Status |
| --- | --- | --- | --- | --- | --- | --- |
| CSV para Bronze/Lakehouse | CSV local | Bronze JSONL local | Ingestion, Files, Quality | Ingestão, Lakehouse, Qualidade | Schema, encoding, volume, rejeições, metadados | Executável |
| Batch ETL PySpark | Arquivos, banco ou API | Silver/Gold técnico | ETL/ELT, Spark, Transformation, Quality | ETL/PySpark, Qualidade, Batch | Contagem, reconciliação, duração, logs | Documentado |
| Carga incremental de banco | SQLite local | CSV de entrega | Database, ETL/ELT, Quality | Integração, ETL/PySpark, Qualidade | Watermark, chave, volume, reconciliação | Executável |
| Validação de qualidade | Dataset processado | Relatório, métricas e quarentena | Quality, Observability | Qualidade | Severidade, evidência, histórico, drift | Documentado |
| Migração de schema/contrato | Schema atual | Schema versionado | Schema Contract, Delta | Lakehouse/Contratos | Compatibilidade, impacto, rollback | Documentado |
| Streaming técnico | Eventos/Kafka equivalente | Bronze/Silver stream | Streaming, Observability, Quality | Batch/Streaming, Qualidade | Checkpoint, offset, late data, latência | Documentado |
| Backfill e reprocessamento | Lotes históricos | Destino original versionado | Batch, ETL/ELT, Quality | Batch/Streaming, ETL/PySpark | Janela, idempotência, reconciliação | Documentado |
| Entrega para Power BI | Camada confiável | Dataset/arquivo/tabela de consumo | Delivery, Quality | Integração/Entrega, Qualidade | Freshness, contrato, reconciliação | Documentado |

## Convenção

Workflows são sequências reproduzíveis. CSV local e SQLite incremental já possuem execução local. Spark, Delta, orquestração externa e MCP ainda dependem de tools/ambiente específicos.
