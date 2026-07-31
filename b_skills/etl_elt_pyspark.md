# ETL, ELT e PySpark

## Metadados
- **id:** `de.skill.etl_elt_pyspark`
- **versão:** `1.0.0`
- **categoria:** processamento
- **objetivo:** Orientar desenho e implementação de pipelines ETL/ELT, batch, incremental e PySpark.
- **entrada esperada:** Fonte, destino, volume, frequência, latência, transformações, estratégia incremental e restrições de ambiente.
- **saída esperada:** Plano de pipeline, escolha ETL/ELT, estratégia Spark, validações, métricas e critérios de rollback.
- **parâmetros:** `source`, `target`, `load_type`, `keys`, `watermark`, `spark_conf`, `partitions`, `write_mode`.
- **validações:** Schema de entrada, contagem antes/depois, chaves, duplicidades, nulos críticos, reconciliação e plano de execução quando Spark for usado.
- **dependências:** Spark/PySpark quando volume ou paralelismo justificarem; Python local para dados pequenos.
- **exceções:** Falha de conexão, schema incompatível, chave incremental ausente, shuffle excessivo, skew crítico, destino indisponível.
- **retry:** Retry com backoff em extração/carga transitória; transformações determinísticas devem ser reexecutáveis pelo mesmo lote.
- **idempotência:** Controlar lote, checkpoint, merge/upsert por chave, watermark e escrita temporária antes de promover dados.
- **efeitos colaterais:** Pode escrever dados processados, checkpoints, logs e métricas.
- **limitações:** Não executa Spark sem tool ou ambiente configurado.
- **testes:** `e_tests/test_artifact_catalogs.py`.
- **agentes consumidores:** `de.etl_elt.agent`, `de.spark.agent`, `de.batch.agent`, `de.transformation.agent`.
- **origem:** Implementação original baseada em requisitos do prompt mestre e boas práticas de Spark.
- **licença:** Mesma licença do repositório.

## Decisão ETL ou ELT
- Use ETL quando a transformação antes da carga reduz risco, custo ou exposição de dados.
- Use ELT quando o destino possui capacidade analítica adequada, governança e custo aceitável.
- Use batch para janelas discretas e latência tolerante.
- Use micro-batch/streaming quando freshness e continuidade forem requisitos reais.

## PySpark
- Prefira funções nativas a UDF.
- Evite `collect` para grandes volumes.
- Avalie cardinalidade antes de particionar.
- Use broadcast join apenas quando o lado pequeno for comprovadamente pequeno.
- Analise `explain` para shuffle, full scan, skew e filtros não empurrados.
- Defina estratégia contra small files em escrita distribuída.

## Guardrails
- Overwrite destrutivo exige confirmação ou política documentada.
- Otimização exige baseline, métrica e comparação.
- Cache exige motivo e escopo.
- Reprocessamento deve preservar rastreabilidade do lote original.
