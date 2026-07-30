# Workflows

Workflows executáveis locais e idempotentes.

## CSV para Bronze

```bash
python3 -m workflows.csv_to_bronze \
  --source-path examples/input.csv \
  --output-dir data/bronze/input \
  --schema '{"id":"integer","nome":"string","valor":"float"}'
```

Saídas:

- `data.jsonl`
- `quarantine.jsonl`
- `metadata.json`

## SQLite Incremental para CSV

```bash
python3 -m workflows.sqlite_incremental_to_csv \
  --database-path data/source.db \
  --query "select id, updated_at, amount from events where updated_at > ? order by updated_at" \
  --output-path data/export/events.csv \
  --state-path data/state/events.json \
  --watermark-column updated_at
```

Guardrails:

- Queries destrutivas são bloqueadas pela tool SQL.
- Estado e outputs são escritos de forma atômica.
- Reexecução com a mesma entrada preserva consistência.
