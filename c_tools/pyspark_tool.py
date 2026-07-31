"""
Ferramenta PySpark opcional.

O import de PySpark é feito dentro da execução para não tornar a dependência
obrigatória nos testes e no uso básico do agente.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from c_tools.base_tool import BaseTool


def run_pyspark_csv_profile(
    source_path: str | Path,
    *,
    header: bool = True,
    infer_schema: bool = False,
) -> dict[str, Any]:
    """Cria SparkSession local e retorna perfil simples de um CSV."""
    try:
        from pyspark.sql import SparkSession
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "PySpark não está instalado. Instale a dependência opcional `pyspark` "
            "e garanta Java disponível para usar esta tool."
        ) from exc

    path = Path(source_path)
    if not path.exists():
        raise FileNotFoundError(f"arquivo não encontrado: {path}")

    spark = (
        SparkSession.builder.master("local[*]")
        .appName("stf-pss-de-agent-profile")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")
    try:
        df = (
            spark.read.option("header", str(header).lower())
            .option("inferSchema", str(infer_schema).lower())
            .csv(str(path))
        )
        return {
            "source_path": str(path),
            "rows": df.count(),
            "columns": df.columns,
            "schema": df.schema.simpleString(),
            "partitions": df.rdd.getNumPartitions(),
        }
    finally:
        spark.stop()


class PerfilCsvPySparkTool(BaseTool):
    """Gera perfil técnico de CSV com PySpark quando a dependência está disponível."""

    @property
    def name(self) -> str:
        return "perfil_csv_pyspark"

    @property
    def description(self) -> str:
        return (
            "Gera perfil simples de CSV usando Spark local opcional: linhas, colunas, "
            "schema e partições."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "source_path": {"type": "string", "description": "Caminho do CSV."},
                "header": {"type": "boolean", "description": "CSV possui header."},
                "infer_schema": {
                    "type": "boolean",
                    "description": "Inferir schema. Evite em produção sem justificativa.",
                },
            },
            "required": ["source_path"],
        }

    def run(
        self,
        source_path: str,
        header: bool = True,
        infer_schema: bool = False,
    ) -> dict[str, Any]:
        return run_pyspark_csv_profile(
            source_path,
            header=header,
            infer_schema=infer_schema,
        )
