"""
Ferramenta: avalia métricas de um modelo já executado externamente.

Recebe os valores reais e preditos (como JSON ou CSV) e calcula as
métricas adequadas ao tipo de tarefa (regressão ou classificação).
"""

from __future__ import annotations

import json
from typing import Any

from c_tools.base_tool import BaseTool


class AvaliarModeloTool(BaseTool):
    """Calcula métricas de avaliação dado vetores de valores reais e preditos."""

    @property
    def name(self) -> str:
        return "avaliar_modelo"

    @property
    def description(self) -> str:
        return (
            "Calcula métricas de avaliação de um modelo preditivo a partir de valores reais "
            "e preditos fornecidos como listas JSON. Para regressão: MAE, RMSE, R². "
            "Para classificação: acurácia, precisão, recall, F1 e AUC-ROC (se probabilidades "
            "forem fornecidas). Use quando o usuário já tiver as predições e quiser avaliá-las."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "valores_reais": {
                    "type": "string",
                    "description": "Lista JSON com os valores reais. Ex.: [1.2, 3.4, 2.1]",
                },
                "valores_preditos": {
                    "type": "string",
                    "description": "Lista JSON com os valores preditos pelo modelo.",
                },
                "tipo_tarefa": {
                    "type": "string",
                    "enum": ["regressao", "classificacao"],
                    "description": "Tipo de tarefa do modelo.",
                },
                "probabilidades": {
                    "type": "string",
                    "description": (
                        "Opcional. Lista JSON com probabilidades da classe positiva "
                        "(apenas para classificação binária, necessário para calcular AUC-ROC)."
                    ),
                },
            },
            "required": ["valores_reais", "valores_preditos", "tipo_tarefa"],
        }

    def run(  # type: ignore[override]
        self,
        valores_reais: str,
        valores_preditos: str,
        tipo_tarefa: str,
        probabilidades: str | None = None,
    ) -> str:
        try:
            y_real = json.loads(valores_reais)
            y_pred = json.loads(valores_preditos)
        except json.JSONDecodeError as exc:
            return f"Erro ao interpretar JSON: {exc}"

        if len(y_real) != len(y_pred):
            return (
                f"Tamanhos incompatíveis: valores_reais={len(y_real)}, "
                f"valores_preditos={len(y_pred)}."
            )

        if tipo_tarefa == "regressao":
            return self._metricas_regressao(y_real, y_pred)

        proba = None
        if probabilidades:
            try:
                proba = json.loads(probabilidades)
            except json.JSONDecodeError:
                pass

        return self._metricas_classificacao(y_real, y_pred, proba)

    # ------------------------------------------------------------------

    @staticmethod
    def _metricas_regressao(y_real, y_pred) -> str:
        try:
            import math
            from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
        except ImportError as exc:
            return f"Dependência ausente: {exc}"

        metricas = {
            "MAE": round(mean_absolute_error(y_real, y_pred), 4),
            "RMSE": round(math.sqrt(mean_squared_error(y_real, y_pred)), 4),
            "R2": round(r2_score(y_real, y_pred), 4),
            "n_amostras": len(y_real),
        }
        return json.dumps(metricas, ensure_ascii=False, indent=2)

    @staticmethod
    def _metricas_classificacao(y_real, y_pred, proba) -> str:
        try:
            from sklearn.metrics import (
                accuracy_score,
                classification_report,
                f1_score,
                precision_score,
                recall_score,
                roc_auc_score,
            )
        except ImportError as exc:
            return f"Dependência ausente: {exc}"

        media = "binary" if len(set(y_real)) == 2 else "weighted"

        metricas: dict[str, Any] = {
            "acuracia": round(accuracy_score(y_real, y_pred), 4),
            "precisao": round(precision_score(y_real, y_pred, average=media, zero_division=0), 4),
            "recall": round(recall_score(y_real, y_pred, average=media, zero_division=0), 4),
            "f1_score": round(f1_score(y_real, y_pred, average=media, zero_division=0), 4),
            "n_amostras": len(y_real),
            "relatorio": classification_report(y_real, y_pred, zero_division=0),
        }

        if proba is not None and media == "binary":
            try:
                metricas["auc_roc"] = round(roc_auc_score(y_real, proba), 4)
            except Exception as exc:
                metricas["auc_roc"] = f"Não calculado: {exc}"

        return json.dumps(metricas, ensure_ascii=False, indent=2)
