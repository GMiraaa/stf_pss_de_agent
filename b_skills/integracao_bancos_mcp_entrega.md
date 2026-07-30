# Integração com Bancos, MCP e Entrega de Dados

## Metadados
- **id:** `de.skill.integracao_bancos_mcp_entrega`
- **versão:** `1.0.0`
- **categoria:** integração
- **objetivo:** Orientar conexão segura com bancos, APIs, MCP e entrega técnica para consumidores como Power BI.
- **entrada esperada:** Tipo de origem/destino, credenciais por variável de ambiente, query/API, modo incremental, consumidor e SLA.
- **saída esperada:** Plano de integração, guardrails de segurança, estratégia incremental, reconciliação e contrato de entrega.
- **parâmetros:** `connection_ref`, `query`, `api_endpoint`, `incremental_key`, `target`, `consumer`, `mcp_server`.
- **validações:** Menor privilégio, query parametrizada, paginação/chunking, timeout, retry, reconciliação, ausência de segredos em logs.
- **dependências:** Driver ou MCP aplicável; secret manager ou variáveis de ambiente.
- **exceções:** Credencial ausente, permissão negada, timeout, rate limit, schema divergente, destino indisponível.
- **retry:** Retry com backoff para falhas transitórias; não repetir escrita sem idempotência.
- **idempotência:** Chaves incrementais, watermarks, transações, upsert/merge e controle de lote.
- **efeitos colaterais:** Pode ler/escrever bancos, chamar APIs, preparar datasets e publicar metadados.
- **limitações:** MCPs não são instalados por padrão; cada integração requer avaliação de permissão e licença.
- **testes:** `e_tests/test_artifact_catalogs.py`.
- **agentes consumidores:** `de.database.agent`, `de.delivery.agent`, `de.orchestrator.agent`, `de.lineage.agent`.
- **origem:** Implementação original baseada em requisitos do prompt mestre e referências conceituais MCP.
- **licença:** Mesma licença do repositório.

## Bancos e APIs
- Usar variáveis de ambiente ou secret manager; nunca hardcode de senha/token.
- Preferir queries parametrizadas.
- Usar paginação, chunking e limites de concorrência.
- Registrar reconciliação entre origem e destino.
- Exigir confirmação/política para `DROP`, `TRUNCATE`, `DELETE` e overwrite.

## MCP
Avalie MCPs para filesystem, SQL, dbt, catálogos, documentação e repositórios. Restrinja permissões ao mínimo necessário e documente operações read/write/destrutivas.

## Entrega
Preparar dados confiáveis, contratos, freshness e reconciliação para consumo técnico. Power BI é consumidor possível; dashboards de negócio pertencem ao repositório de Data Analytics.
