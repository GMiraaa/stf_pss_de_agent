"""
Ferramenta: executa clustering não supervisionado em dados CSV.

Suporta K-Means e DBSCAN. Retorna os rótulos de cluster atribuídos a cada
observação e as métricas de qualidade (Silhouette Score, Davies-Bouldin).
"""

from __future__ import annotations

import io
import json
from typing import Any

from c_tools.base_tool import BaseTool


class ExecutarClusteringTool(BaseTool):
    """Executa clustering em um dataset CSV e retorna rótulos e métricas."""

    @property
    def name(self) -> str:
        return "executar_clustering"

    @property
    def description(self) -> str:
        return (
            "Executa clustering não supervisionado (K-Means ou DBSCAN) em dados CSV e retorna "
            "o rótulo de cluster de cada amostra, o Silhouette Score e o Davies-Bouldin Index. "
            "Use quando o usuário quiser segmentar ou agrupar observações sem uma variável alvo."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "csv_dados": {
                    "type": "string",
                    "description": "Dados de entrada no formato CSV (cabeçalho obrigatório). Apenas colunas numéricas serão usadas.",
                },
                "algoritmo": {
                    "type": "string",
                    "enum": ["kmeans", "dbscan"],
                    "description": "Algoritmo de clustering: 'kmeans' (padrão) ou 'dbscan'.",
                },
                "n_clusters": {
                    "type": "integer",
                    "description": "Número de clusters para K-Means (padrão: 3). Ignorado pelo DBSCAN.",
                },
                "dbscan_eps": {
                    "type": "number",
                    "description": "Raio de vizinhança para DBSCAN (padrão: 0.5).",
                },
                "dbscan_min_amostras": {
                    "type": "integer",
                    "description": "Mínimo de amostras por vizinhança para DBSCAN (padrão: 5).",
                },
            },
            "required": ["csv_dados"],
        }

    def run(  # type: ignore[override]
        self,
        csv_dados: str,
        algoritmo: str = "kmeans",
        n_clusters: int = 3,
        dbscan_eps: float = 0.5,
        dbscan_min_amostras: int = 5,
    ) -> str:
        try:
            import pandas as pd
            from sklearn.preprocessing import StandardScaler
        except ImportError as exc:
            return f"Dependência ausente: {exc}. Instale com: pip install pandas scikit-learn"

        df = pd.read_csv(io.StringIO(csv_dados))
        numericas = df.select_dtypes(include="number")

        if numericas.empty:
            return "Nenhuma coluna numérica encontrada no dataset."

        X = StandardScaler().fit_transform(numericas.dropna())

        if algoritmo == "dbscan":
            rotulos = self._dbscan(X, dbscan_eps, dbscan_min_amostras)
        else:
            rotulos = self._kmeans(X, n_clusters)

        return self._avaliar(X, rotulos, algoritmo)

    # ------------------------------------------------------------------

    @staticmethod
    def _kmeans(X, n_clusters: int):
        from sklearn.cluster import KMeans

        model = KMeans(n_clusters=n_clusters, random_state=42, n_init="auto")
        return model.fit_predict(X)

    @staticmethod
    def _dbscan(X, eps: float, min_samples: int):
        from sklearn.cluster import DBSCAN

        return DBSCAN(eps=eps, min_samples=min_samples).fit_predict(X)

    @staticmethod
    def _avaliar(X, rotulos, algoritmo: str) -> str:
        import numpy as np
        from sklearn.metrics import davies_bouldin_score, silhouette_score

        n_clusters = len(set(rotulos)) - (1 if -1 in rotulos else 0)
        n_ruido = int(np.sum(rotulos == -1))

        resultado: dict[str, Any] = {
            "algoritmo": algoritmo,
            "n_clusters_encontrados": n_clusters,
            "n_amostras_ruido": n_ruido,
            "distribuicao_clusters": {
                str(k): int(np.sum(rotulos == k))
                for k in sorted(set(rotulos))
            },
        }

        # métricas exigem ao menos 2 clusters e amostras válidas (sem ruído)
        mascara = rotulos != -1
        if n_clusters >= 2 and mascara.sum() > n_clusters:
            resultado["silhouette_score"] = round(
                silhouette_score(X[mascara], rotulos[mascara]), 4
            )
            resultado["davies_bouldin_index"] = round(
                davies_bouldin_score(X[mascara], rotulos[mascara]), 4
            )
        else:
            resultado["aviso"] = (
                "Métricas não calculadas: menos de 2 clusters válidos encontrados. "
                "Tente ajustar os parâmetros (n_clusters, eps, min_amostras)."
            )

        resultado["rotulos"] = rotulos.tolist()
        return json.dumps(resultado, ensure_ascii=False, indent=2)
