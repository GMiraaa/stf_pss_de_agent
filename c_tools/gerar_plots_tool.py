"""
Ferramenta: gera e salva gráficos de avaliação de modelos em arquivos .png.

Cobre regressão, classificação e clustering. Os arquivos são salvos no
diretório especificado e os caminhos são retornados no resultado.
"""

from __future__ import annotations

import io
import json
import os
from typing import Any

from c_tools.base_tool import BaseTool

# Tipos de plot disponíveis por tarefa
_PLOTS_REGRESSAO = ["real_vs_predito", "residuos", "distribuicao_erros"]
_PLOTS_CLASSIFICACAO = ["matriz_confusao", "curva_roc", "precisao_recall"]
_PLOTS_CLUSTERING = ["scatter_2d", "elbow", "silhouette"]


class GerarPlotsTool(BaseTool):
    """Gera e salva gráficos de avaliação de modelos de ML em arquivos .png."""

    @property
    def name(self) -> str:
        return "gerar_plots"

    @property
    def description(self) -> str:
        return (
            "Gera gráficos de avaliação de modelos e salva como arquivos .png. "
            "Regressão: real_vs_predito, residuos, distribuicao_erros. "
            "Classificação: matriz_confusao, curva_roc, precisao_recall. "
            "Clustering: scatter_2d (PCA), elbow, silhouette. "
            "Retorna os caminhos dos arquivos gerados."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "tipo_tarefa": {
                    "type": "string",
                    "enum": ["regressao", "classificacao", "clustering"],
                    "description": "Tipo de tarefa do modelo.",
                },
                "tipo_plot": {
                    "type": "string",
                    "description": (
                        "Gráfico a gerar. "
                        "Regressão: real_vs_predito | residuos | distribuicao_erros. "
                        "Classificação: matriz_confusao | curva_roc | precisao_recall. "
                        "Clustering: scatter_2d | elbow | silhouette."
                    ),
                },
                "valores_reais": {
                    "type": "string",
                    "description": "Lista JSON com valores reais. Regressão e classificação.",
                },
                "valores_preditos": {
                    "type": "string",
                    "description": "Lista JSON com valores preditos. Regressão e classificação.",
                },
                "probabilidades": {
                    "type": "string",
                    "description": (
                        "Lista JSON com probabilidades da classe positiva. "
                        "Necessário para curva_roc e precisao_recall (classificação binária)."
                    ),
                },
                "nomes_classes": {
                    "type": "string",
                    "description": "Lista JSON com nomes das classes para a matriz de confusão.",
                },
                "csv_dados": {
                    "type": "string",
                    "description": "Dados em CSV. Obrigatório para plots de clustering.",
                },
                "rotulos_cluster": {
                    "type": "string",
                    "description": (
                        "Lista JSON com rótulos de cluster. "
                        "Obrigatório para scatter_2d e silhouette."
                    ),
                },
                "max_k": {
                    "type": "integer",
                    "description": "Número máximo de clusters para o gráfico elbow (padrão: 10).",
                },
                "diretorio_saida": {
                    "type": "string",
                    "description": "Diretório onde os arquivos .png serão salvos (padrão: 'plots').",
                },
            },
            "required": ["tipo_tarefa", "tipo_plot"],
        }

    def run(  # type: ignore[override]
        self,
        tipo_tarefa: str,
        tipo_plot: str,
        valores_reais: str | None = None,
        valores_preditos: str | None = None,
        probabilidades: str | None = None,
        nomes_classes: str | None = None,
        csv_dados: str | None = None,
        rotulos_cluster: str | None = None,
        max_k: int = 10,
        diretorio_saida: str = "plots",
    ) -> str:
        try:
            import matplotlib
            matplotlib.use("Agg")  # backend sem janela gráfica
        except ImportError as exc:
            return f"Dependência ausente: {exc}. Instale com: pip install matplotlib"

        os.makedirs(diretorio_saida, exist_ok=True)

        dispatch = {
            ("regressao", "real_vs_predito"): self._reg_real_vs_predito,
            ("regressao", "residuos"): self._reg_residuos,
            ("regressao", "distribuicao_erros"): self._reg_distribuicao_erros,
            ("classificacao", "matriz_confusao"): self._clf_matriz_confusao,
            ("classificacao", "curva_roc"): self._clf_curva_roc,
            ("classificacao", "precisao_recall"): self._clf_precisao_recall,
            ("clustering", "scatter_2d"): self._clu_scatter_2d,
            ("clustering", "elbow"): self._clu_elbow,
            ("clustering", "silhouette"): self._clu_silhouette,
        }

        key = (tipo_tarefa, tipo_plot)
        if key not in dispatch:
            opcoes = [f"{t}/{p}" for t, p in dispatch]
            return f"Combinação inválida '{tipo_tarefa}/{tipo_plot}'. Opções: {opcoes}"

        try:
            caminho = dispatch[key](
                valores_reais=valores_reais,
                valores_preditos=valores_preditos,
                probabilidades=probabilidades,
                nomes_classes=nomes_classes,
                csv_dados=csv_dados,
                rotulos_cluster=rotulos_cluster,
                max_k=max_k,
                diretorio_saida=diretorio_saida,
            )
            return json.dumps({"arquivo_gerado": caminho}, ensure_ascii=False, indent=2)
        except Exception as exc:
            return f"Erro ao gerar plot '{tipo_plot}': {exc}"

    # ------------------------------------------------------------------
    # Regressão
    # ------------------------------------------------------------------

    @staticmethod
    def _reg_real_vs_predito(**kw) -> str:
        import matplotlib.pyplot as plt
        import numpy as np

        y = np.array(json.loads(kw["valores_reais"]), dtype=float)
        yp = np.array(json.loads(kw["valores_preditos"]), dtype=float)

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.scatter(yp, y, alpha=0.6, edgecolors="k", linewidths=0.4)
        lim = [min(y.min(), yp.min()), max(y.max(), yp.max())]
        ax.plot(lim, lim, "r--", linewidth=1.5, label="Perfeito")
        ax.set_xlabel("Valor Predito")
        ax.set_ylabel("Valor Real")
        ax.set_title("Real vs. Predito")
        ax.legend()
        path = os.path.join(kw["diretorio_saida"], "reg_real_vs_predito.png")
        fig.savefig(path, dpi=120, bbox_inches="tight")
        plt.close(fig)
        return path

    @staticmethod
    def _reg_residuos(**kw) -> str:
        import matplotlib.pyplot as plt
        import numpy as np

        y = np.array(json.loads(kw["valores_reais"]), dtype=float)
        yp = np.array(json.loads(kw["valores_preditos"]), dtype=float)
        res = y - yp

        fig, ax = plt.subplots(figsize=(7, 4))
        ax.scatter(yp, res, alpha=0.6, edgecolors="k", linewidths=0.4)
        ax.axhline(0, color="r", linestyle="--", linewidth=1.5)
        ax.set_xlabel("Valor Predito")
        ax.set_ylabel("Resíduo (Real − Predito)")
        ax.set_title("Resíduos vs. Predito")
        path = os.path.join(kw["diretorio_saida"], "reg_residuos.png")
        fig.savefig(path, dpi=120, bbox_inches="tight")
        plt.close(fig)
        return path

    @staticmethod
    def _reg_distribuicao_erros(**kw) -> str:
        import matplotlib.pyplot as plt
        import numpy as np

        y = np.array(json.loads(kw["valores_reais"]), dtype=float)
        yp = np.array(json.loads(kw["valores_preditos"]), dtype=float)
        res = y - yp

        fig, ax = plt.subplots(figsize=(7, 4))
        ax.hist(res, bins="auto", edgecolor="k", alpha=0.75)
        ax.axvline(0, color="r", linestyle="--", linewidth=1.5)
        ax.set_xlabel("Resíduo")
        ax.set_ylabel("Frequência")
        ax.set_title("Distribuição dos Erros")
        path = os.path.join(kw["diretorio_saida"], "reg_distribuicao_erros.png")
        fig.savefig(path, dpi=120, bbox_inches="tight")
        plt.close(fig)
        return path

    # ------------------------------------------------------------------
    # Classificação
    # ------------------------------------------------------------------

    @staticmethod
    def _clf_matriz_confusao(**kw) -> str:
        import matplotlib.pyplot as plt
        from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix

        y = json.loads(kw["valores_reais"])
        yp = json.loads(kw["valores_preditos"])
        classes = json.loads(kw["nomes_classes"]) if kw.get("nomes_classes") else None

        cm = confusion_matrix(y, yp)
        # normaliza por linha para facilitar comparação entre classes de tamanhos diferentes
        cm_norm = cm.astype(float) / cm.sum(axis=1, keepdims=True)

        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        for ax, data, title in zip(
            axes,
            [cm, cm_norm],
            ["Contagem Absoluta", "Normalizada (por linha)"],
        ):
            disp = ConfusionMatrixDisplay(confusion_matrix=data, display_labels=classes)
            disp.plot(ax=ax, colorbar=False, cmap="Blues")
            ax.set_title(f"Matriz de Confusão — {title}")

        path = os.path.join(kw["diretorio_saida"], "clf_matriz_confusao.png")
        fig.savefig(path, dpi=120, bbox_inches="tight")
        plt.close(fig)
        return path

    @staticmethod
    def _clf_curva_roc(**kw) -> str:
        import matplotlib.pyplot as plt
        from sklearn.metrics import RocCurveDisplay, roc_auc_score

        if not kw.get("probabilidades"):
            raise ValueError("probabilidades é obrigatório para a curva ROC.")

        y = json.loads(kw["valores_reais"])
        proba = json.loads(kw["probabilidades"])

        fig, ax = plt.subplots(figsize=(6, 6))
        RocCurveDisplay.from_predictions(y, proba, ax=ax)
        auc = roc_auc_score(y, proba)
        ax.set_title(f"Curva ROC (AUC = {auc:.4f})")
        ax.plot([0, 1], [0, 1], "k--", linewidth=1)
        path = os.path.join(kw["diretorio_saida"], "clf_curva_roc.png")
        fig.savefig(path, dpi=120, bbox_inches="tight")
        plt.close(fig)
        return path

    @staticmethod
    def _clf_precisao_recall(**kw) -> str:
        import matplotlib.pyplot as plt
        from sklearn.metrics import PrecisionRecallDisplay, average_precision_score

        if not kw.get("probabilidades"):
            raise ValueError("probabilidades é obrigatório para a curva Precisão-Recall.")

        y = json.loads(kw["valores_reais"])
        proba = json.loads(kw["probabilidades"])

        fig, ax = plt.subplots(figsize=(6, 6))
        PrecisionRecallDisplay.from_predictions(y, proba, ax=ax)
        ap = average_precision_score(y, proba)
        ax.set_title(f"Curva Precisão-Recall (AP = {ap:.4f})")
        path = os.path.join(kw["diretorio_saida"], "clf_precisao_recall.png")
        fig.savefig(path, dpi=120, bbox_inches="tight")
        plt.close(fig)
        return path

    # ------------------------------------------------------------------
    # Clustering
    # ------------------------------------------------------------------

    @staticmethod
    def _clu_scatter_2d(**kw) -> str:
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
        from sklearn.decomposition import PCA
        from sklearn.preprocessing import StandardScaler

        if not kw.get("csv_dados") or not kw.get("rotulos_cluster"):
            raise ValueError("csv_dados e rotulos_cluster são obrigatórios para scatter_2d.")

        df = pd.read_csv(io.StringIO(kw["csv_dados"]))
        X = StandardScaler().fit_transform(df.select_dtypes(include="number").dropna())
        labels = np.array(json.loads(kw["rotulos_cluster"]))

        coords = PCA(n_components=2).fit_transform(X)

        fig, ax = plt.subplots(figsize=(7, 6))
        for label in sorted(set(labels)):
            mask = labels == label
            nome = "Ruído" if label == -1 else f"Cluster {label}"
            marker = "x" if label == -1 else "o"
            ax.scatter(coords[mask, 0], coords[mask, 1], label=nome, marker=marker, alpha=0.7)

        ax.set_xlabel("PC1")
        ax.set_ylabel("PC2")
        ax.set_title("Clusters — Projeção PCA 2D")
        ax.legend(loc="best")
        path = os.path.join(kw["diretorio_saida"], "clu_scatter_2d.png")
        fig.savefig(path, dpi=120, bbox_inches="tight")
        plt.close(fig)
        return path

    @staticmethod
    def _clu_elbow(**kw) -> str:
        import matplotlib.pyplot as plt
        import pandas as pd
        from sklearn.cluster import KMeans
        from sklearn.preprocessing import StandardScaler

        if not kw.get("csv_dados"):
            raise ValueError("csv_dados é obrigatório para o gráfico elbow.")

        df = pd.read_csv(io.StringIO(kw["csv_dados"]))
        X = StandardScaler().fit_transform(df.select_dtypes(include="number").dropna())
        max_k = max(2, kw.get("max_k") or 10)

        ks = range(1, min(max_k + 1, len(X)))
        inercias = [
            KMeans(n_clusters=k, random_state=42, n_init="auto").fit(X).inertia_
            for k in ks
        ]

        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(list(ks), inercias, "o-", linewidth=2)
        ax.set_xlabel("Número de Clusters (k)")
        ax.set_ylabel("Inércia (WCSS)")
        ax.set_title("Método do Cotovelo (Elbow)")
        ax.grid(True, linestyle="--", alpha=0.5)
        path = os.path.join(kw["diretorio_saida"], "clu_elbow.png")
        fig.savefig(path, dpi=120, bbox_inches="tight")
        plt.close(fig)
        return path

    @staticmethod
    def _clu_silhouette(**kw) -> str:
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
        from sklearn.metrics import silhouette_samples, silhouette_score
        from sklearn.preprocessing import StandardScaler

        if not kw.get("csv_dados") or not kw.get("rotulos_cluster"):
            raise ValueError("csv_dados e rotulos_cluster são obrigatórios para silhouette.")

        df = pd.read_csv(io.StringIO(kw["csv_dados"]))
        X = StandardScaler().fit_transform(df.select_dtypes(include="number").dropna())
        labels = np.array(json.loads(kw["rotulos_cluster"]))

        # remove amostras de ruído (-1) para o cálculo
        mask = labels != -1
        Xv, lv = X[mask], labels[mask]

        if len(set(lv)) < 2:
            raise ValueError("Pelo menos 2 clusters válidos são necessários para o silhouette plot.")

        sample_scores = silhouette_samples(Xv, lv)
        media_global = silhouette_score(Xv, lv)

        fig, ax = plt.subplots(figsize=(8, max(4, len(set(lv)) * 1.5)))
        y_lower = 10
        for label in sorted(set(lv)):
            valores = np.sort(sample_scores[lv == label])
            tamanho = len(valores)
            y_upper = y_lower + tamanho
            ax.barh(
                range(y_lower, y_upper),
                valores,
                height=1.0,
                label=f"Cluster {label}",
            )
            ax.text(-0.05, (y_lower + y_upper) / 2, str(label), ha="right", va="center")
            y_lower = y_upper + 10

        ax.axvline(media_global, color="red", linestyle="--", linewidth=1.5,
                   label=f"Média global = {media_global:.4f}")
        ax.set_xlabel("Coeficiente Silhouette")
        ax.set_ylabel("Amostras por cluster")
        ax.set_title("Silhouette Plot")
        ax.legend(loc="lower right")
        path = os.path.join(kw["diretorio_saida"], "clu_silhouette.png")
        fig.savefig(path, dpi=120, bbox_inches="tight")
        plt.close(fig)
        return path
