"""
Ferramentas de arquivo, CSV e validação simples de schema.

As implementações usam apenas biblioteca padrão para manter execução local leve.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from c_tools.base_tool import BaseTool


SUPPORTED_TYPES = {"string", "integer", "float", "boolean"}


@dataclass(frozen=True)
class CsvValidationResult:
    source_path: str
    delimiter: str
    encoding: str
    total_rows: int
    valid_rows: int
    rejected_rows: int
    columns: list[str]
    required_columns: list[str]
    errors: list[dict[str, Any]]

    def as_dict(self) -> dict[str, Any]:
        return {
            "source_path": self.source_path,
            "delimiter": self.delimiter,
            "encoding": self.encoding,
            "total_rows": self.total_rows,
            "valid_rows": self.valid_rows,
            "rejected_rows": self.rejected_rows,
            "columns": self.columns,
            "required_columns": self.required_columns,
            "errors": self.errors,
        }


def parse_schema(schema: str | dict[str, Any] | None) -> dict[str, str]:
    """Converte schema JSON/dict para mapeamento coluna -> tipo."""
    if not schema:
        return {}
    raw_schema = json.loads(schema) if isinstance(schema, str) else schema
    if not isinstance(raw_schema, dict):
        raise ValueError("schema deve ser um objeto JSON com coluna -> tipo")

    parsed: dict[str, str] = {}
    for column, type_name in raw_schema.items():
        if not isinstance(column, str) or not column:
            raise ValueError("schema possui nome de coluna inválido")
        if not isinstance(type_name, str) or type_name not in SUPPORTED_TYPES:
            raise ValueError(
                f"tipo inválido para {column!r}: use {sorted(SUPPORTED_TYPES)}"
            )
        parsed[column] = type_name
    return parsed


def detect_csv_dialect(path: Path, encoding: str = "utf-8") -> csv.Dialect:
    """Detecta dialect de CSV a partir de uma amostra."""
    sample = path.read_text(encoding=encoding)[:8192]
    if not sample.strip():
        raise ValueError("arquivo CSV vazio")
    try:
        return csv.Sniffer().sniff(sample, delimiters=",;\t|")
    except csv.Error:
        return csv.get_dialect("excel")


def coerce_value(value: str | None, type_name: str) -> Any:
    """Valida e converte um valor textual para tipo simples."""
    if value is None or value == "":
        raise ValueError("valor obrigatório ausente")
    if type_name == "string":
        return value
    if type_name == "integer":
        return int(value)
    if type_name == "float":
        return float(value.replace(",", "."))
    if type_name == "boolean":
        normalized = value.strip().lower()
        if normalized in {"true", "1", "yes", "y", "sim"}:
            return True
        if normalized in {"false", "0", "no", "n", "nao", "não"}:
            return False
        raise ValueError("booleano inválido")
    raise ValueError(f"tipo não suportado: {type_name}")


def validate_csv_file(
    source_path: str | Path,
    schema: str | dict[str, Any] | None = None,
    *,
    encoding: str = "utf-8",
    delimiter: str | None = None,
    max_errors: int = 50,
) -> CsvValidationResult:
    """Valida existência, header, tipos simples e linhas corrompidas de um CSV."""
    path = Path(source_path)
    if not path.exists():
        raise FileNotFoundError(f"arquivo não encontrado: {path}")
    if not path.is_file():
        raise ValueError(f"origem não é arquivo: {path}")

    parsed_schema = parse_schema(schema)
    dialect = detect_csv_dialect(path, encoding=encoding)
    detected_delimiter = delimiter or dialect.delimiter

    errors: list[dict[str, Any]] = []
    total_rows = 0
    valid_rows = 0

    with path.open("r", encoding=encoding, newline="") as file_obj:
        reader = csv.DictReader(file_obj, delimiter=detected_delimiter)
        columns = list(reader.fieldnames or [])
        missing_columns = [column for column in parsed_schema if column not in columns]
        if missing_columns:
            errors.append(
                {
                    "row_number": 0,
                    "error": "missing_columns",
                    "columns": missing_columns,
                }
            )

        for row_number, row in enumerate(reader, start=2):
            total_rows += 1
            row_errors = []
            for column, type_name in parsed_schema.items():
                if column not in row:
                    continue
                try:
                    coerce_value(row[column], type_name)
                except ValueError as exc:
                    row_errors.append(
                        {"column": column, "type": type_name, "error": str(exc)}
                    )
            if row_errors:
                if len(errors) < max_errors:
                    errors.append({"row_number": row_number, "errors": row_errors})
            else:
                valid_rows += 1

    if not columns:
        errors.append({"row_number": 0, "error": "missing_header"})

    return CsvValidationResult(
        source_path=str(path),
        delimiter=detected_delimiter,
        encoding=encoding,
        total_rows=total_rows,
        valid_rows=valid_rows,
        rejected_rows=total_rows - valid_rows,
        columns=columns,
        required_columns=list(parsed_schema),
        errors=errors,
    )


class ValidarCsvTool(BaseTool):
    """Valida um arquivo CSV pequeno ou médio com schema explícito opcional."""

    @property
    def name(self) -> str:
        return "validar_csv"

    @property
    def description(self) -> str:
        return (
            "Valida arquivo CSV local: existência, dialect, header, schema simples, "
            "contagens e amostra de rejeições."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "source_path": {"type": "string", "description": "Caminho do CSV."},
                "schema": {
                    "type": "string",
                    "description": "JSON opcional coluna->tipo: string, integer, float, boolean.",
                },
                "encoding": {"type": "string", "description": "Encoding do arquivo."},
                "delimiter": {
                    "type": "string",
                    "description": "Delimitador opcional. Se ausente, tenta detectar.",
                },
            },
            "required": ["source_path"],
        }

    def run(
        self,
        source_path: str,
        schema: str | None = None,
        encoding: str = "utf-8",
        delimiter: str | None = None,
    ) -> dict[str, Any]:
        result = validate_csv_file(
            source_path,
            schema=schema,
            encoding=encoding,
            delimiter=delimiter,
        )
        return result.as_dict()
