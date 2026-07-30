"""
Ferramenta: treinar e avaliar um modelo preditivo (regressão ou classificação).

Recebe dados no formato CSV (como string), o nome da coluna alvo e o tipo de
tarefa, treina um modelo Gradient Boosting e devolve as métricas de avaliação.
"""

from __future__ import annotations

import io
import json
from typing import Any

from c_tools.base_tool import BaseTool


class TreinarPredicaoTool(BaseTool):
    """Treina um modelo preditivo supervisionado e retorna métricas de avaliação."""

    @property
    def name(self) -> str:
        return "treinar_modelo_predicao"

    @property
    def description(self) -> str:
        return (
            "Treina um modelo preditivo (regressão ou classificação) a partir de dados CSV "
            "e retorna as métricas de avaliação (RMSE/R² para regressão; acurácia/F1/AUC "
            "para classificação). Use quando o usuário fornecer um dataset e quiser prever "
            "uma variável alvo."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "csv_dados": {
                    "type": "string",
                    "description": (
                        "Dados de entrada no formato CSV (cabeçalho obrigatório). "
                        "Todas as colunas, exceto a coluna alvo, serão usadas como features."
                    ),
                },
                "coluna_alvo": {
                    "type": "string",
                    "description": "Nome da coluna que deve ser prevista.",
                },
                "tipo_tarefa": {
                    "type": "string",
                    "enum": ["regressao", "classificacao"],
                    "description": (
                        "Tipo de tarefa: 'regressao' para saída contínua, "
                        "'classificacao' para saída categórica."
                    ),
                },
                "proporcao_teste": {
                    "type": "number",
                    "description": "Fração dos dados reservada para teste (padrão: 0.2).",
                },
            },
            "required": ["csv_dados", "coluna_alvo", "tipo_tarefa"],
        }

    def run(  # type: ignore[override]
        self,
        csv_dados: str,
        coluna_alvo: str,
        tipo_tarefa: str,
        proporcao_teste: float = 0.2,
    ) -> str:
        try:
            import pandas as pd
            from sklearn.model_selection import train_test_split
        except ImportError as exc:
            return f"Dependência ausente: {exc}. Instale com: pip install pandas scikit-learn"

        df = pd.read_csv(io.StringIO(csv_dados))

        if coluna_alvo not in df.columns:
            return f"Coluna alvo '{coluna_alvo}' não encontrada. Colunas disponíveis: {list(df.columns)}"

        X = pd.get_dummies(df.drop(columns=[coluna_alvo]))
        y = df[coluna_alvo]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=proporcao_teste, random_state=42
        )

        if tipo_tarefa == "regressao":
            return self._regressao(X_train, X_test, y_train, y_test)
        return self._classificacao(X_train, X_test, y_train, y_test)

    # ------------------------------------------------------------------

    @staticmethod
    def _regressao(X_train, X_test, y_train, y_test) -> str:
        try:
            from sklearn.ensemble import GradientBoostingRegressor
            from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
        except ImportError as exc:
            return f"Dependência ausente: {exc}"

        import math

        model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        metricas = {
            "MAE": round(mean_absolute_error(y_test, preds), 4),
            "RMSE": round(math.sqrt(mean_squared_error(y_test, preds)), 4),
            "R2": round(r2_score(y_test, preds), 4),
            "amostras_treino": len(X_train),
            "amostras_teste": len(X_test),
        }
        return json.dumps(metricas, ensure_ascii=False, indent=2)

    @staticmethod
    def _classificacao(X_train, X_test, y_train, y_test) -> str:
        try:
            from sklearn.ensemble import GradientBoostingClassifier
            from sklearn.metrics import (
                accuracy_score,
                classification_report,
                roc_auc_score,
            )
        except ImportError as exc:
            return f"Dependência ausente: {exc}"

        model = GradientBoostingClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        auc: float | str = "N/A"
        try:
            if len(set(y_test)) == 2:
                proba = model.predict_proba(X_test)[:, 1]
                auc = round(roc_auc_score(y_test, proba), 4)
        except Exception:
            pass

        metricas = {
            "acuracia": round(accuracy_score(y_test, preds), 4),
            "auc_roc": auc,
            "relatorio": classification_report(y_test, preds),
            "amostras_treino": len(X_train),
            "amostras_teste": len(X_test),
        }
        return json.dumps(metricas, ensure_ascii=False, indent=2)
