# Observabilidade

## Métricas mínimas

- Status, início, fim e duração.
- Volume de entrada, saída, rejeições e duplicidades.
- Taxa de erro, throughput, latência e freshness.
- Quantidade de partições e tamanho de arquivos.
- Resultado de regras de qualidade e severidade.
- SLA e custo quando disponível.

## Logs

Logs devem ser estruturados e correlacionáveis por `run_id`, `pipeline_id`, `stage`, `source`, `target` e `environment`.

## Linhagem

Registrar origem, destino, schema, transformação, versão, dependências, qualidade e proprietário. OpenLineage/DataHub/Marquez são referências futuras, não dependências instaladas neste momento.

## Alertas

Alertas devem depender de severidade e política. Nem toda falha de qualidade deve interromper todos os pipelines.
