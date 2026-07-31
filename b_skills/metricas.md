# Métricas de Avaliação de Modelos

## Regressão

Usadas quando a saída do modelo é um valor contínuo (ex.: preço, temperatura, demanda).

| Métrica | Fórmula | Interpretação |
|---------|---------|---------------|
| **MAE** (Mean Absolute Error) | $\frac{1}{n}\sum|y_i - \hat{y}_i|$ | Erro médio absoluto; mesma unidade do alvo; robusto a outliers |
| **RMSE** (Root Mean Squared Error) | $\sqrt{\frac{1}{n}\sum(y_i - \hat{y}_i)^2}$ | Penaliza erros grandes; sensível a outliers; mesma unidade do alvo |
| **R²** (Coeficiente de Determinação) | $1 - \frac{SS_{res}}{SS_{tot}}$ | Proporção da variância explicada; 1 = perfeito, 0 = modelo constante, <0 = pior que média |
| **MAPE** (Mean Absolute Percentage Error) | $\frac{100}{n}\sum\left|\frac{y_i - \hat{y}_i}{y_i}\right|$ | Erro percentual; interpretável entre datasets; problemático se y ≈ 0 |

**Quando usar cada uma:**
- Prefira **RMSE** quando erros grandes são inaceitáveis.
- Prefira **MAE** quando a distribuição de erros tem outliers.
- Use **R²** para comparar modelos em um mesmo dataset.
- Use **MAPE** quando a escala do alvo varia muito entre amostras.

---

## Classificação

Usadas quando a saída é uma categoria (ex.: fraude/não-fraude, tipo de contrato).

### Métricas básicas (derivadas da matriz de confusão)

```
              Predito Positivo   Predito Negativo
Real Positivo       TP                FN
Real Negativo       FP                TN
```

| Métrica | Fórmula | Foco |
|---------|---------|------|
| **Acurácia** | $(TP+TN)/(TP+TN+FP+FN)$ | Fração total de acertos; enganosa em classes desbalanceadas |
| **Precisão** | $TP/(TP+FP)$ | Dos classificados como positivo, quantos realmente são? |
| **Recall (Sensibilidade)** | $TP/(TP+FN)$ | Dos positivos reais, quantos foram detectados? |
| **F1-Score** | $2 \cdot \frac{P \cdot R}{P+R}$ | Média harmônica entre precisão e recall; equilíbrio entre os dois |
| **Especificidade** | $TN/(TN+FP)$ | Capacidade de identificar negativos corretamente |

### Métricas baseadas em probabilidade

- **AUC-ROC**: área sob a curva TPR vs FPR. Varia de 0 a 1; 0.5 = aleatório; 1 = perfeito. Independe do limiar de decisão.
- **AUC-PR** (Precision-Recall): mais informativa que ROC em datasets muito desbalanceados.
- **Log-Loss** (Cross-Entropy): penaliza predições confiantes e erradas.

### Para problemas multiclasse
- **macro**: média simples entre classes (trata todas igualmente).
- **weighted**: média ponderada pelo suporte de cada classe.
- **micro**: agrega TP/FP/FN de todas as classes antes de calcular.

---

## Clustering

Usadas para avaliar qualidade dos grupos sem rótulos verdadeiros (métricas internas).

| Métrica | Intervalo | Objetivo | O que mede |
|---------|-----------|----------|------------|
| **Silhouette Score** | [-1, 1] | Maximizar | Coesão intra-cluster e separação inter-cluster; 1 = perfeito, 0 = sobreposição, -1 = atribuição errada |
| **Davies-Bouldin Index** | [0, ∞) | Minimizar | Razão entre dispersão intra-cluster e distância inter-cluster; 0 = perfeito |
| **Calinski-Harabasz Index** | [0, ∞) | Maximizar | Razão entre variância inter e intra-cluster; quanto maior, mais densos e separados os clusters |
| **Inércia (WCSS)** | [0, ∞) | Minimizar | Soma das distâncias ao quadrado de cada ponto ao seu centróide; usada no método do cotovelo |

### Métricas externas (quando há rótulos verdadeiros para validação)

| Métrica | Intervalo | O que mede |
|---------|-----------|------------|
| **ARI** (Adjusted Rand Index) | [-1, 1] | Concordância entre clustering e rótulos, corrigida para acaso |
| **NMI** (Normalized Mutual Information) | [0, 1] | Informação mútua normalizada entre clusters e classes verdadeiras |
| **Homogeneidade** | [0, 1] | Cada cluster contém apenas membros de uma única classe |
| **Completude** | [0, 1] | Todos os membros de uma classe estão no mesmo cluster |
| **V-Measure** | [0, 1] | Média harmônica entre homogeneidade e completude |

### Método do cotovelo (Elbow Method)
- Plote a inércia para k = 1 até k = 10 (ou mais).
- O ponto onde a curva "dobra" (cotovelo) indica o k ideal.
- Combine com Silhouette Score para confirmar a escolha.
