# Engenharia de Dados — Conceitos Fundamentais

## Pipelines de dados
- **ETL** (Extract, Transform, Load): extrai dados da fonte, transforma e carrega no destino.
- **ELT** (Extract, Load, Transform): carrega os dados brutos primeiro e transforma no destino.
- Ferramentas comuns: Apache Airflow, dbt, Spark, Kafka.

## Armazenamento
- **Data Warehouse**: armazenamento analítico estruturado (ex.: BigQuery, Redshift, Snowflake).
- **Data Lake**: armazenamento de dados brutos em qualquer formato (ex.: S3, GCS, ADLS).
- **Data Lakehouse**: combina as vantagens dos dois (ex.: Delta Lake, Apache Iceberg).

## Qualidade de dados
- Verificações de schema, nulidade, unicidade e integridade referencial.
- Ferramentas: Great Expectations, dbt tests, Soda.

## SQL relevante para Engenharia de Dados
- CTEs (`WITH`), window functions, particionamento de tabelas, índices.
- `EXPLAIN ANALYZE` para otimização de queries.
