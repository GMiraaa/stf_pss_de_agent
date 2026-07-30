from __future__ import annotations

import csv
import json
import sqlite3
from pathlib import Path

import pytest

from c_tools.file_csv_tool import ValidarCsvTool, validate_csv_file
from c_tools.pyspark_tool import run_pyspark_csv_profile
from c_tools.sqlite_tool import execute_sqlite_query, validate_sql
from workflows.csv_to_bronze import run_csv_to_bronze
from workflows.sqlite_incremental_to_csv import run_sqlite_incremental_to_csv


def _write_csv(path: Path) -> None:
    with path.open("w", encoding="utf-8", newline="") as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=["id", "name", "amount"])
        writer.writeheader()
        writer.writerow({"id": "1", "name": "alpha", "amount": "10.5"})
        writer.writerow({"id": "bad", "name": "beta", "amount": "20.0"})


def test_validate_csv_reports_rejections(tmp_path: Path) -> None:
    source = tmp_path / "input.csv"
    _write_csv(source)

    result = validate_csv_file(
        source,
        schema={"id": "integer", "name": "string", "amount": "float"},
    )

    assert result.total_rows == 2
    assert result.valid_rows == 1
    assert result.rejected_rows == 1
    assert result.columns == ["id", "name", "amount"]
    assert result.errors


def test_validar_csv_tool_returns_dict(tmp_path: Path) -> None:
    source = tmp_path / "input.csv"
    _write_csv(source)

    result = ValidarCsvTool().run(
        str(source),
        schema=json.dumps({"id": "integer", "name": "string"}),
    )

    assert result["total_rows"] == 2
    assert result["rejected_rows"] == 1


def test_sqlite_tool_allows_parametrized_select(tmp_path: Path) -> None:
    db_path = tmp_path / "source.db"
    with sqlite3.connect(db_path) as conn:
        conn.execute("create table events (id integer, amount real)")
        conn.executemany("insert into events values (?, ?)", [(1, 10.0), (2, 20.0)])

    result = execute_sqlite_query(
        db_path,
        "select id, amount from events where amount > ? order by id",
        [10],
    )

    assert result["columns"] == ["id", "amount"]
    assert result["rows"] == [{"id": 2, "amount": 20.0}]


def test_sqlite_tool_blocks_destructive_sql() -> None:
    with pytest.raises(ValueError, match="destrutivo"):
        validate_sql("drop table events")

    with pytest.raises(ValueError, match="somente SELECT"):
        validate_sql("insert into events values (1)")


def test_csv_to_bronze_writes_data_quarantine_and_metadata(tmp_path: Path) -> None:
    source = tmp_path / "input.csv"
    output = tmp_path / "bronze" / "input"
    _write_csv(source)

    metadata = run_csv_to_bronze(
        source,
        output,
        schema={"id": "integer", "name": "string", "amount": "float"},
    )

    assert metadata["valid_rows"] == 1
    assert metadata["rejected_rows"] == 1
    assert (output / "data.jsonl").exists()
    assert (output / "quarantine.jsonl").exists()
    assert (output / "metadata.json").exists()

    data_lines = (output / "data.jsonl").read_text(encoding="utf-8").splitlines()
    quarantine_lines = (output / "quarantine.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(data_lines) == 1
    assert len(quarantine_lines) == 1


def test_sqlite_incremental_to_csv_updates_state(tmp_path: Path) -> None:
    db_path = tmp_path / "source.db"
    output_path = tmp_path / "extract.csv"
    state_path = tmp_path / "state.json"
    with sqlite3.connect(db_path) as conn:
        conn.execute("create table events (id integer, updated_at text, amount real)")
        conn.executemany(
            "insert into events values (?, ?, ?)",
            [(1, "2026-01-01", 10.0), (2, "2026-01-02", 20.0)],
        )

    state = run_sqlite_incremental_to_csv(
        db_path,
        "select id, updated_at, amount from events where updated_at > ? order by updated_at",
        output_path,
        state_path,
        initial_watermark="2026-01-01",
        watermark_column="updated_at",
    )

    assert state["rows"] == 1
    assert state["last_watermark"] == "2026-01-02"
    assert output_path.read_text(encoding="utf-8").splitlines()[1].startswith("2,")


def test_pyspark_profile_reports_missing_optional_dependency(tmp_path: Path) -> None:
    source = tmp_path / "input.csv"
    _write_csv(source)

    try:
        result = run_pyspark_csv_profile(source)
    except RuntimeError as exc:
        assert "PySpark não está instalado" in str(exc)
    else:
        assert result["rows"] == 2
        assert result["columns"] == ["id", "name", "amount"]
