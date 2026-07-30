# Clustering — Conceitos e Técnicas

## O que é clustering (aprendizado não supervisionado)
- Agrupa observações semelhantes sem rótulos pré-definidos.
- O objetivo é maximizar a similaridade intra-cluster e a dissimilaridade inter-clusters.
- Aplicações: segmentação de clientes, detecção de anomalias, redução de dimensionalidade, análise exploratória.

## Fluxo padrão de clustering
1. Coleta e limpeza dos dados.
2. Pré-processamento: normalização/padronização (`StandardScaler`, `MinMaxScaler`).
3. Redução de dimensionalidade opcional (PCA, UMAP, t-SNE) — melhora qualidade e visualização.
4. Escolha do algoritmo e dos hiperparâmetros (ex.: número de clusters *k*).
5. Ajuste do modelo e atribuição de rótulos.
6. Avaliação com métricas internas e interpretação dos clusters.

## Principais algoritmos

| Algoritmo | Tipo | Quando usar |
|-----------|------|-------------|
| **K-Means** | Particionamento | Clusters esféricos, número *k* conhecido ou estimado |
| **K-Medoids (PAM)** | Particionamento | Mais robusto a outliers que K-Means |
| **DBSCAN** | Baseado em densidade | Clusters de forma arbitrária; detecta ruído/outliers |
| **HDBSCAN** | Hierárquico + densidade | Clusters de densidades variáveis; mais estável que DBSCAN |
| **Agglomerative Clustering** | Hierárquico | Dendrogramas; não exige *k* a priori |
| **Gaussian Mixture Models (GMM)** | Probabilístico | Clusters sobrepostos; fornece probabilidades de pertença |
| **Mean Shift** | Baseado em densidade | Detecta *k* automaticamente; custoso em grandes datasets |
| **Spectral Clustering** | Baseado em grafos | Clusters não convexos; computacionalmente pesado |

## Escolha do número de clusters (K-Means)
- **Método do cotovelo (Elbow)**: plotar inércia × *k*; o "joelho" da curva indica o *k* ideal.
- **Silhouette Score**: mede coesão e separação (-1 a 1); maximizar.
- **Davies-Bouldin Index**: razão de dispersão intra vs. inter-cluster; minimizar.
- **Calinski-Harabasz Index**: razão variância inter/intra; maximizar.

## Métricas de avaliação

### Métricas internas (sem rótulos verdadeiros)
- **Silhouette Score**: `sklearn.metrics.silhouette_score` — quanto maior, melhor.
- **Davies-Bouldin Index**: `davies_bouldin_score` — quanto menor, melhor.
- **Inércia (Within-Cluster Sum of Squares)**: soma das distâncias ao centróide; usada no método do cotovelo.

### Métricas externas (com rótulos verdadeiros — para validação)
- **Adjusted Rand Index (ARI)**: concordância corrigida para acaso.
- **Normalized Mutual Information (NMI)**: similaridade de informação entre clusters e classes.
- **Homogeneidade, Completude, V-Measure**: decomposição da qualidade dos clusters.

## Pré-processamento essencial
- Variáveis em escalas muito diferentes distorcem distâncias → **sempre normalizar**.
- Variáveis categóricas: One-Hot Encoding ou distância de Gower.
- Alta dimensionalidade degrada métricas de distância (*curse of dimensionality*) → reduzir com PCA ou UMAP antes de clusterizar.

## Redução de dimensionalidade para clustering
- **PCA**: linear; preserva variância máxima; rápido.
- **UMAP**: não-linear; preserva estrutura local e global; ótimo para visualização 2D/3D.
- **t-SNE**: não-linear; apenas para visualização (não recomendado como pré-processamento).

## Detecção de anomalias via clustering
- Pontos classificados como ruído pelo DBSCAN/HDBSCAN são candidatos a anomalias.
- Observações com Silhouette Score muito baixo dentro do cluster podem ser outliers.
- Alternativas dedicadas: Isolation Forest, Local Outlier Factor (LOF), Autoencoder.

## Ferramentas Python comuns
- **scikit-learn**: K-Means, DBSCAN, Agglomerative, GMM, métricas de avaliação.
- **hdbscan**: implementação eficiente do HDBSCAN.
- **umap-learn**: UMAP para redução dimensional.
- **yellowbrick**: visualizações de ML, incluindo elbow e silhouette plots.
- **scipy**: dendrogramas para clustering hierárquico.
- **plotly / seaborn / matplotlib**: visualização dos clusters em 2D/3D.
