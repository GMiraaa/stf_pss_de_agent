# Limitações

- Há execução local para validação CSV, SQLite seguro, CSV para Bronze JSONL e SQLite incremental para CSV.
- A tool `buscar_informacao` continua mock.
- PySpark é opcional e só funciona quando `pyspark` e Java estiverem disponíveis no ambiente.
- Não há ainda execução real de Delta Lake, MCP, Airflow, Dagster, Prefect ou Kafka.
- Integrações com Airflow, Dagster, Prefect, Kafka, Delta, OpenLineage, DataHub, bancos externos e Power BI não foram instaladas nem executadas.
- Estatística, clustering, classificação e previsão são tratados apenas como suporte técnico a qualidade, observabilidade e capacidade.
- Dados sensíveis, credenciais e operações destrutivas exigem implementação futura com guardrails adicionais.
