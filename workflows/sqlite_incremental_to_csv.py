"""
Workflow incremental de SQLite para CSV.

Mantém estado em JSON com o último watermark processado. A query deve receber
um parâmetro posicional para o watermark.
"""

from __future__ import annotations

import argparse
import csv
import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from c_tools.sqlite_tool import execute_sqlite_query


def _read_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"last_watermark": None}
    return json.loads(path.read_text(encoding="utf-8"))


def run_sqlite_incremental_to_csv(
    database_path: str | Path,
    query: str,
    output_path: str | Path,
    state_path: str | Path,
    *,
    initial_watermark: str = "",
    watermark_column: str,
    max_rows: int = 10000,
) -> dict[str, Any]:
    """Executa extração incremental read-only e atualiza estado atomicamente."""
    state_file = Path(state_path)
    output_file = Path(output_path)
    state_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    state = _read_state(state_file)
    watermark = state.get("last_watermark") or initial_watermark
    result = execute_sqlite_query(
        database_path,
        query,
        [watermark],
        allow_write=False,
        max_rows=max_rows,
    )

    rows = result["rows"]
    columns = result["columns"]
    if watermark_column not in columns and rows:
        raise ValueError(f"watermark_column ausente do resultado: {watermark_column}")

    tmp_output = Path(
        tempfile.NamedTemporaryFile(
            prefix=f".{output_file.name}.",
            dir=output_file.parent,
            delete=False,
        ).name
    )
    tmp_state = Path(
        tempfile.NamedTemporaryFile(
            prefix=f".{state_file.name}.",
            dir=state_file.parent,
            delete=False,
        ).name
    )

    try:
        with tmp_output.open("w", encoding="utf-8", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=columns)
            writer.writeheader()
            writer.writerows(rows)

        last_watermark = max((str(row[watermark_column]) for row in rows), default=watermark)
        new_state = {
            "workflow": "sqlite_incremental_to_csv",
            "database_path": str(database_path),
            "output_path": str(output_file),
            "last_watermark": last_watermark,
            "rows": len(rows),
            "executed_at": datetime.now(timezone.utc).isoformat(),
        }
        tmp_state.write_text(
            json.dumps(new_state, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        tmp_output.replace(output_file)
        tmp_state.replace(state_file)
        return new_state
    except Exception:
        tmp_output.unlink(missing_ok=True)
        tmp_state.unlink(missing_ok=True)
        raise


def main() -> None:
    parser = argparse.ArgumentParser(description="Extrai SQLite incremental para CSV.")
    parser.add_argument("--database-path", required=True)
    parser.add_argument("--query", required=True)
    parser.add_argument("--output-path", required=True)
    parser.add_argument("--state-path", required=True)
    parser.add_argument("--watermark-column", required=True)
    parser.add_argument("--initial-watermark", default="")
    args = parser.parse_args()

    result = run_sqlite_incremental_to_csv(
        args.database_path,
        args.query,
        args.output_path,
        args.state_path,
        initial_watermark=args.initial_watermark,
        watermark_column=args.watermark_column,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
