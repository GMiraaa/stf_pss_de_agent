# Batch, Streaming e Orquestração

## Metadados
- **id:** `de.skill.batch_streaming_orquestracao`
- **versão:** `1.0.0`
- **categoria:** orquestração
- **objetivo:** Orientar workflows batch, streaming, micro-batch, backfill, reprocessamento e orquestração.
- **entrada esperada:** Frequência, latência, dependências, janela, fonte, destino, estado, SLA e ferramenta de orquestração disponível.
- **saída esperada:** Plano operacional com dependências, retry, checkpoint, backfill, alertas e recuperação de falhas.
- **parâmetros:** `schedule`, `dependencies`, `checkpoint`, `state_store`, `sla`, `retry_policy`, `orchestrator`.
- **validações:** Estado, offsets, janelas, watermark, duplicidade, late data, SLAs, bloqueio de concorrência e reprocessamento.
- **dependências:** Airflow, Dagster, Prefect, cron, Spark Structured Streaming, Kafka ou equivalente quando aplicável.
- **exceções:** Checkpoint corrompido, offset inválido, dependência indisponível, falha de SLA, destino inconsistente.
- **retry:** Retry com backoff e limite; backfill/replay só com intervalo, lote e destino definidos.
- **idempotência:** Checkpoints, locks, controle de lote, deduplicação e escrita transacional quando disponível.
- **efeitos colaterais:** Pode disparar execuções, registrar estado e publicar alertas quando conectado a tools.
- **limitações:** Não garante exactly-once sem verificar fonte, processamento, sink e checkpoint.
- **testes:** `e_tests/test_artifact_catalogs.py`.
- **agentes consumidores:** `de.batch.agent`, `de.streaming.agent`, `de.etl_elt.agent`, `de.orchestrator.agent`.
- **origem:** Implementação original baseada em requisitos do prompt mestre.
- **licença:** Mesma licença do repositório.

## Batch
Defina agenda, dependências, janela, modo full/incremental, retry, backoff, checkpoint, idempotência, bloqueio de concorrência, SLA e auditoria.

## Streaming
Defina event time, processing time, watermark, trigger, checkpoint, offset, late data, semântica de entrega, dead-letter queue e monitoramento.

## Orquestração
Avalie Airflow, Dagster, Prefect, Luigi, Argo ou execução local simples conforme complexidade. Não acople o repositório a uma ferramenta única sem necessidade.

## Guardrails
- Exactly-once só deve ser declarado após verificar toda a cadeia.
- Backfill não deve sobrescrever dados fora do intervalo solicitado.
- Reprocessamento deve ser auditável e reversível quando possível.
