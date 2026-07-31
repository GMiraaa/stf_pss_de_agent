"""
Ferramenta SQL segura para SQLite local.

Por padrão permite apenas consultas de leitura. Escritas precisam de
`allow_write=True` e comandos destrutivos seguem bloqueados.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from c_tools.base_tool import BaseTool


READ_ONLY_PREFIXES = ("select", "with", "pragma")
DESTRUCTIVE_KEYWORDS = {
    "drop",
    "truncate",
    "delete",
    "alter",
    "vacuum",
    "attach",
    "detach",
    "reindex",
}


def _first_token(sql: str) -> str:
    stripped = sql.strip().lower()
    if not stripped:
        raise ValueError("query SQL vazia")
    return stripped.split(None, 1)[0].rstrip(";")


def validate_sql(sql: str, *, allow_write: bool = False) -> None:
    """Aplica guardrails simples contra SQL destrutivo e multi-statement."""
    normalized = sql.strip().lower()
    if ";" in normalized.rstrip(";"):
        raise ValueError("multi-statement não é permitido")

    first = _first_token(sql)
    if first in DESTRUCTIVE_KEYWORDS:
        raise ValueError(f"comando SQL destrutivo bloqueado: {first}")
    if not allow_write and not normalized.startswith(READ_ONLY_PREFIXES):
        raise ValueError("somente SELECT/WITH/PRAGMA são permitidos sem allow_write")


def execute_sqlite_query(
    database_path: str | Path,
    query: str,
    parameters: list[Any] | None = None,
    *,
    allow_write: bool = False,
    max_rows: int = 100,
) -> dict[str, Any]:
    """Executa SQL parametrizado em SQLite com limite de linhas retornadas."""
    validate_sql(query, allow_write=allow_write)

    db_path = Path(database_path)
    if not db_path.exists():
        raise FileNotFoundError(f"banco SQLite não encontrado: {db_path}")
    if not db_path.is_file():
        raise ValueError(f"database_path não é arquivo: {db_path}")

    params = parameters or []
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(query, params)
        if cursor.description is None:
            conn.commit()
            return {"rowcount": cursor.rowcount, "columns": [], "rows": []}

        rows = cursor.fetchmany(max_rows)
        columns = [column[0] for column in cursor.description]
        return {
            "rowcount": len(rows),
            "columns": columns,
            "rows": [dict(row) for row in rows],
            "truncated": len(rows) == max_rows,
        }


class ExecutarSqliteTool(BaseTool):
    """Executa SQL parametrizado em SQLite com bloqueio destrutivo."""

    @property
    def name(self) -> str:
        return "executar_sqlite"

    @property
    def description(self) -> str:
        return (
            "Executa SQL em banco SQLite local. Por padrão aceita apenas leitura "
            "e bloqueia comandos destrutivos."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "database_path": {"type": "string", "description": "Arquivo SQLite."},
                "query": {"type": "string", "description": "Query SQL parametrizada."},
                "parameters": {
                    "type": "array",
                    "description": "Parâmetros posicionais da query.",
                    "items": {"type": "string"},
                },
                "allow_write": {
                    "type": "boolean",
                    "description": "Permite escrita não destrutiva quando true.",
                },
                "max_rows": {
                    "type": "integer",
                    "description": "Máximo de linhas retornadas.",
                },
            },
            "required": ["database_path", "query"],
        }

    def run(
        self,
        database_path: str,
        query: str,
        parameters: list[Any] | None = None,
        allow_write: bool = False,
        max_rows: int = 100,
    ) -> dict[str, Any]:
        return execute_sqlite_query(
            database_path,
            query,
            parameters,
            allow_write=allow_write,
            max_rows=max_rows,
        )
