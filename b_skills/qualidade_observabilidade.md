# Qualidade, Profiling e Observabilidade

## Metadados
- **id:** `de.skill.qualidade_observabilidade`
- **versão:** `1.0.0`
- **categoria:** qualidade
- **objetivo:** Definir regras de qualidade, profiling técnico, estatísticas operacionais e observabilidade de pipelines.
- **entrada esperada:** Dataset, schema, regras, severidades, métricas históricas, SLA e política de falha.
- **saída esperada:** Plano de validação, evidências, classificação de falhas, métricas operacionais e recomendações.
- **parâmetros:** `dataset`, `rules`, `severity_policy`, `metrics`, `history_window`, `sla`.
- **validações:** Completude, unicidade, validade, consistência, integridade, volume, distribuição, freshness, duplicidade e drift.
- **dependências:** Tool de leitura/execução, biblioteca de qualidade opcional e armazenamento de métricas quando disponível.
- **exceções:** Regra mal definida, coluna ausente, histórico insuficiente, métrica indisponível.
- **retry:** Recalcular validações determinísticas; não mascarar falhas reais como transientes.
- **idempotência:** A mesma entrada e regra devem produzir a mesma evidência.
- **efeitos colaterais:** Pode gerar relatórios, métricas, logs e registros em quarentena.
- **limitações:** Estatística aqui é operacional; modelagem avançada pertence a Data Science.
- **testes:** `e_tests/test_artifact_catalogs.py`.
- **agentes consumidores:** `de.quality.agent`, `de.observability.agent`, `de.orchestrator.agent`, `de.delivery.agent`.
- **origem:** Implementação original baseada em requisitos do prompt mestre e referências conceituais de qualidade/linhagem.
- **licença:** Mesma licença do repositório.

## Regras de qualidade
Cada regra deve registrar: nome, identificador, descrição, entidade/coluna, severidade, tipo, limiar, resultado esperado, ação em falha, destino de inválidos, evidência, métrica, histórico e responsável.

## Profiling técnico
Calcule contagens, tipos, cardinalidade, nulos, duplicidades, valores frequentes, mínimo/máximo, padrões, outliers técnicos, possíveis chaves e possíveis dados sensíveis. Não transformar esse profiling em análise de negócio.

## Estatística operacional
Use média, mediana, moda, variância, desvio padrão, percentis, covariância e correlação para qualidade, drift, comparação de execuções e diagnóstico. Declare que correlação não implica causalidade.

## Observabilidade
Monitore início, fim, duração, status, volume de entrada/saída, rejeições, duplicidades, taxa de erro, throughput, latência, partições, tamanho de arquivos, freshness, SLA, qualidade e custo quando disponível.

## Guardrails
- Falhas críticas podem bloquear; falhas informativas devem alertar ou registrar.
- Outliers não devem ser removidos automaticamente.
- Logs não devem conter senhas, tokens, strings completas de conexão ou dados pessoais desnecessários.
