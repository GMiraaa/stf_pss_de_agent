"""
Ferramenta: calculadora centralizada de métricas de avaliação.

Cobre regressão, classificação e clustering a partir de dados fornecidos
como listas JSON ou CSV — sem treinar nenhum modelo.
"""

from __future__ import annotations

import json
from typing import Any

from c_tools.base_tool import BaseTool


class CalcularMetricasTool(BaseTool):
    """Calcula métricas de avaliação para regressão, classificação ou clustering."""

    @property
    def name(self) -> str:
        return "calcular_metricas"

    @property
    def description(self) -> str:
        return (
            "Calcula métricas de avaliação de modelos de ML. "
            "Para regressão: MAE, RMSE, R², MAPE. "
            "Para classificação: acurácia, precisão, recall, F1, AUC-ROC, AUC-PR. "
            "Para clustering: Silhouette Score, Davies-Bouldin, Calinski-Harabasz. "
            "Use quando quiser avaliar resultados já obtidos sem treinar um novo modelo."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "tipo_tarefa": {
                    "type": "string",
                    "enum": ["regressao", "classificacao", "clustering"],
                    "description": "Tipo de tarefa do modelo a ser avaliado.",
                },
                "valores_reais": {
                    "type": "string",
                    "description": (
                        "Lista JSON com os valores reais do alvo. "
                        "Obrigatório para regressão e classificação."
                    ),
                },
                "valores_preditos": {
                    "type": "string",
                    "description": (
                        "Lista JSON com os valores preditos pelo modelo. "
                        "Obrigatório para regressão e classificação."
                    ),
                },
                "probabilidades": {
                    "type": "string",
                    "description": (
                        "Lista JSON com probabilidades da classe positiva "
                        "(classificação binária). Necessário para AUC-ROC e AUC-PR."
                    ),
                },
                "csv_dados": {
                    "type": "string",
                    "description": "Dados originais em CSV. Obrigatório para clustering.",
                },
                "rotulos_cluster": {
                    "type": "string",
                    "description": (
                        "Lista JSON com os rótulos de cluster atribuídos a cada amostra. "
                        "Obrigatório para clustering. Use -1 para amostras classificadas como ruído."
                    ),
                },
                "rotulos_verdadeiros": {
                    "type": "string",
                    "description": (
                        "Lista JSON com rótulos verdadeiros das amostras (opcional para clustering). "
                        "Quando fornecido, calcula métricas externas: ARI, NMI, V-Measure."
                    ),
                },
            },
            "required": ["tipo_tarefa"],
        }

    def run(  # type: ignore[override]
        self,
        tipo_tarefa: str,
        valores_reais: str | None = None,
        valores_preditos: str | None = None,
        probabilidades: str | None = None,
        csv_dados: str | None = None,
        rotulos_cluster: str | None = None,
        rotulos_verdadeiros: str | None = None,
    ) -> str:
        if tipo_tarefa == "regressao":
            return self._regressao(valores_reais, valores_preditos)
        if tipo_tarefa == "classificacao":
            return self._classificacao(valores_reais, valores_preditos, probabilidades)
        if tipo_tarefa == "clustering":
            return self._clustering(csv_dados, rotulos_cluster, rotulos_verdadeiros)
        return f"tipo_tarefa inválido: '{tipo_tarefa}'. Use regressao, classificacao ou clustering."

    # ------------------------------------------------------------------
    # Regressão
    # ------------------------------------------------------------------

    @staticmethod
    def _regressao(valores_reais: str | None, valores_preditos: str | None) -> str:
        if not valores_reais or not valores_preditos:
            return "Parâmetros obrigatórios ausentes: valores_reais e valores_preditos."
        try:
            import math
            import numpy as np
            from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
        except ImportError as exc:
            return f"Dependência ausente: {exc}"

        y = json.loads(valores_reais)
        yp = json.loads(valores_preditos)

        if len(y) != len(yp):
            return f"Tamanhos incompatíveis: reais={len(y)}, preditos={len(yp)}."

        y_arr, yp_arr = np.array(y, dtype=float), np.array(yp, dtype=float)

        # MAPE evita divisão por zero mascarando zeros
        with np.errstate(divide="ignore", invalid="ignore"):
            mape_vals = np.where(y_arr != 0, np.abs((y_arr - yp_arr) / y_arr), np.nan)
            mape = float(np.nanmean(mape_vals) * 100)

        result = {
            "MAE": round(mean_absolute_error(y_arr, yp_arr), 4),
            "RMSE": round(math.sqrt(mean_squared_error(y_arr, yp_arr)), 4),
            "R2": round(r2_score(y_arr, yp_arr), 4),
            "MAPE_%": round(mape, 4),
            "n_amostras": len(y),
        }
        return json.dumps(result, ensure_ascii=False, indent=2)

    # ------------------------------------------------------------------
    # Classificação
    # ------------------------------------------------------------------

    @staticmethod
    def _classificacao(
        valores_reais: str | None,
        valores_preditos: str | None,
        probabilidades: str | None,
    ) -> str:
        if not valores_reais or not valores_preditos:
            return "Parâmetros obrigatórios ausentes: valores_reais e valores_preditos."
        try:
            from sklearn.metrics import (
                accuracy_score,
                average_precision_score,
                classification_report,
                f1_score,
                precision_score,
                recall_score,
                roc_auc_score,
            )
        except ImportError as exc:
            return f"Dependência ausente: {exc}"

        y = json.loads(valores_reais)
        yp = json.loads(valores_preditos)

        if len(y) != len(yp):
            return f"Tamanhos incompatíveis: reais={len(y)}, preditos={len(yp)}."

        binario = len(set(y)) == 2
        media = "binary" if binario else "weighted"

        result: dict[str, Any] = {
            "acuracia": round(accuracy_score(y, yp), 4),
            "precisao": round(precision_score(y, yp, average=media, zero_division=0), 4),
            "recall": round(recall_score(y, yp, average=media, zero_division=0), 4),
            "f1_score": round(f1_score(y, yp, average=media, zero_division=0), 4),
            "n_amostras": len(y),
            "relatorio_classificacao": classification_report(y, yp, zero_division=0),
        }

        if probabilidades and binario:
            proba = json.loads(probabilidades)
            try:
                result["auc_roc"] = round(roc_auc_score(y, proba), 4)
                result["auc_pr"] = round(average_precision_score(y, proba), 4)
            except Exception as exc:
                result["auc_erro"] = str(exc)

        return json.dumps(result, ensure_ascii=False, indent=2)

    # ------------------------------------------------------------------
    # Clustering
    # ------------------------------------------------------------------

    @staticmethod
    def _clustering(
        csv_dados: str | None,
        rotulos_cluster: str | None,
        rotulos_verdadeiros: str | None,
    ) -> str:
        if not csv_dados or not rotulos_cluster:
            return "Parâmetros obrigatórios ausentes: csv_dados e rotulos_cluster."
        try:
            import io
            import numpy as np
            import pandas as pd
            from sklearn.metrics import (
                adjusted_rand_score,
                calinski_harabasz_score,
                davies_bouldin_score,
                normalized_mutual_info_score,
                silhouette_score,
                v_measure_score,
            )
            from sklearn.preprocessing import StandardScaler
        except ImportError as exc:
            return f"Dependência ausente: {exc}"

        df = pd.read_csv(io.StringIO(csv_dados))
        X = StandardScaler().fit_transform(df.select_dtypes(include="number").dropna())
        labels = np.array(json.loads(rotulos_cluster))

        mascara = labels != -1
        n_clusters = len(set(labels[mascara]))
        n_ruido = int(np.sum(labels == -1))

        result: dict[str, Any] = {
            "n_clusters": n_clusters,
            "n_amostras_ruido": n_ruido,
            "distribuicao": {str(k): int(np.sum(labels == k)) for k in sorted(set(labels))},
        }

        if n_clusters >= 2 and mascara.sum() > n_clusters:
            Xv, lv = X[mascara], labels[mascara]
            result["silhouette_score"] = round(silhouette_score(Xv, lv), 4)
            result["davies_bouldin_index"] = round(davies_bouldin_score(Xv, lv), 4)
            result["calinski_harabasz_index"] = round(calinski_harabasz_score(Xv, lv), 4)
        else:
            result["aviso_metricas_internas"] = (
                "Métricas internas não calculadas: menos de 2 clusters válidos."
            )

        if rotulos_verdadeiros:
            yt = json.loads(rotulos_verdadeiros)
            result["ari"] = round(adjusted_rand_score(yt, labels), 4)
            result["nmi"] = round(normalized_mutual_info_score(yt, labels), 4)
            result["v_measure"] = round(v_measure_score(yt, labels), 4)

        return json.dumps(result, ensure_ascii=False, indent=2)
