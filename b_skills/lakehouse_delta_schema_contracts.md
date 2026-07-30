# Lakehouse, Delta Lake, Schemas e Contratos

## Metadados
- **id:** `de.skill.lakehouse_delta_schema_contracts`
- **versão:** `1.0.0`
- **categoria:** lakehouse
- **objetivo:** Orientar uso de Data Lake/Lakehouse, Delta Lake open source, schema management e data contracts.
- **entrada esperada:** Arquitetura alvo, camada, formato, schema atual, schema proposto, regras de contrato e operação Delta desejada.
- **saída esperada:** Decisão de arquitetura, plano Delta/schema/contrato, riscos de compatibilidade e guardrails.
- **parâmetros:** `zone`, `table`, `format`, `schema_current`, `schema_expected`, `contract`, `operation`.
- **validações:** Compatibilidade de schema, alteração destrutiva, obrigatoriedade, tipos, particionamento, histórico, retenção e reconciliação.
- **dependências:** Delta Lake opcional quando instalado; Spark para tabelas Delta em escala.
- **exceções:** Funcionalidade Delta não suportada no ambiente, schema incompatível, contrato quebrado, retenção insegura.
- **retry:** Reexecutar operações idempotentes; operações destrutivas exigem política e rollback.
- **idempotência:** Merge/upsert por chave, versionamento de contrato e execução rastreável.
- **efeitos colaterais:** Pode alterar tabelas, schemas, histórico e arquivos quando executada por tool.
- **limitações:** Não declarar recursos proprietários como disponíveis no Delta open source sem verificar ambiente.
- **testes:** `e_tests/test_artifact_catalogs.py`.
- **agentes consumidores:** `de.delta_lake.agent`, `de.schema_contract.agent`, `de.lineage.agent`, `de.orchestrator.agent`.
- **origem:** Implementação original baseada em requisitos do prompt mestre e documentação/conceitos de Delta Lake.
- **licença:** Mesma licença do repositório.

## Lakehouse
Avalie Landing, Raw, Bronze, Silver, Gold, Curated, Trusted, Quarantine e Archive. Não imponha Medallion quando zonas mais simples bastarem.

## Delta Lake
Considere append, overwrite controlado, merge, upsert, delete, update, schema enforcement, schema evolution, time travel, histórico, vacuum, compactação, particionamento, transações e auditoria. Diferencie sempre open source de funcionalidades específicas de plataforma.

## Schema e contratos
Classifique mudanças como compatíveis, potencialmente incompatíveis ou incompatíveis. Contratos devem declarar schema, tipos, obrigatoriedade, SLA, regras de qualidade, proprietário, versão e evidência de validação.

## Guardrails
- Não aplicar remoção/renomeação destrutiva automaticamente.
- Não executar vacuum/retention agressivo sem política.
- Não fazer merge sem chave e regra de resolução de duplicidade.
