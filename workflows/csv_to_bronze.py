"""
Workflow idempotente de CSV para Bronze local.

Saídas:
- `data.jsonl`: registros válidos em JSON Lines.
- `quarantine.jsonl`: registros rejeitados com motivo.
- `metadata.json`: contagens, schema, origem e checksum.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from c_tools.file_csv_tool import coerce_value, detect_csv_dialect, parse_schema


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file_obj:
        for chunk in iter(lambda: file_obj.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_csv_to_bronze(
    source_path: str | Path,
    output_dir: str | Path,
    schema: str | dict[str, Any] | None = None,
    *,
    encoding: str = "utf-8",
    delimiter: str | None = None,
) -> dict[str, Any]:
    """Lê CSV, valida schema simples e escreve Bronze em JSONL de forma atômica."""
    source = Path(source_path)
    output = Path(output_dir)
    if not source.exists():
        raise FileNotFoundError(f"arquivo não encontrado: {source}")
    if not source.is_file():
        raise ValueError(f"source_path não é arquivo: {source}")

    parsed_schema = parse_schema(schema)
    dialect = detect_csv_dialect(source, encoding=encoding)
    effective_delimiter = delimiter or dialect.delimiter

    output.parent.mkdir(parents=True, exist_ok=True)
    tmp_dir = Path(tempfile.mkdtemp(prefix=f".{output.name}.", dir=output.parent))
    data_path = tmp_dir / "data.jsonl"
    quarantine_path = tmp_dir / "quarantine.jsonl"
    metadata_path = tmp_dir / "metadata.json"

    total_rows = 0
    valid_rows = 0
    rejected_rows = 0
    columns: list[str] = []

    try:
        with (
            source.open("r", encoding=encoding, newline="") as src,
            data_path.open("w", encoding="utf-8") as data_file,
            quarantine_path.open("w", encoding="utf-8") as quarantine_file,
        ):
            reader = csv.DictReader(src, delimiter=effective_delimiter)
            columns = list(reader.fieldnames or [])
            missing_columns = [column for column in parsed_schema if column not in columns]
            if missing_columns:
                raise ValueError(f"colunas obrigatórias ausentes: {missing_columns}")

            for row_number, row in enumerate(reader, start=2):
                total_rows += 1
                converted = dict(row)
                errors: list[dict[str, str]] = []

                for column, type_name in parsed_schema.items():
                    try:
                        converted[column] = coerce_value(row.get(column), type_name)
                    except ValueError as exc:
                        errors.append(
                            {"column": column, "type": type_name, "error": str(exc)}
                        )

                if errors:
                    rejected_rows += 1
                    quarantine_file.write(
                        json.dumps(
                            {
                                "row_number": row_number,
                                "errors": errors,
                                "raw": row,
                            },
                            ensure_ascii=False,
                        )
                        + "\n"
                    )
                    continue

                valid_rows += 1
                data_file.write(json.dumps(converted, ensure_ascii=False) + "\n")

        metadata = {
            "workflow": "csv_to_bronze",
            "source_path": str(source),
            "source_sha256": file_sha256(source),
            "output_dir": str(output),
            "executed_at": datetime.now(timezone.utc).isoformat(),
            "encoding": encoding,
            "delimiter": effective_delimiter,
            "columns": columns,
            "schema": parsed_schema,
            "total_rows": total_rows,
            "valid_rows": valid_rows,
            "rejected_rows": rejected_rows,
            "idempotency_key": f"{source.name}:{file_sha256(source)}",
        }
        metadata_path.write_text(
            json.dumps(metadata, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        if output.exists():
            shutil.rmtree(output)
        tmp_dir.replace(output)
        return metadata
    except Exception:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        raise


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingere CSV em Bronze JSONL local.")
    parser.add_argument("--source-path", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--schema", default=None, help="JSON coluna->tipo")
    parser.add_argument("--encoding", default="utf-8")
    parser.add_argument("--delimiter", default=None)
    args = parser.parse_args()

    result = run_csv_to_bronze(
        args.source_path,
        args.output_dir,
        schema=args.schema,
        encoding=args.encoding,
        delimiter=args.delimiter,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
