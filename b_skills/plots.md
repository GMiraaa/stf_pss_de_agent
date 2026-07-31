# Visualizações para Modelos de Machine Learning

## Regressão

| Gráfico | Eixos | O que revela |
|---------|-------|-------------|
| **Real vs. Predito** | x = valor predito, y = valor real | Pontos na diagonal = modelo perfeito; desvios indicam viés sistemático |
| **Resíduos vs. Predito** | x = valor predito, y = resíduo $(y - \hat{y})$ | Resíduos aleatórios em torno de 0 = bom; padrões indicam heterocedasticidade ou não-linearidade |
| **Distribuição dos Erros** | histograma dos resíduos | Deve ser aproximadamente normal e centrada em 0; caudas pesadas indicam outliers |
| **Feature Importance** | barras horizontais por feature | Identifica as variáveis mais influentes na predição |

**Boas práticas:**
- Sempre plote resíduos; um RMSE baixo pode esconder padrões sistemáticos.
- Transformações como `log(y)` podem corrigir heterocedasticidade.

---

## Classificação

| Gráfico | O que revela |
|---------|-------------|
| **Matriz de Confusão** | Heatmap de TP, FP, FN, TN; identifica quais classes são confundidas entre si |
| **Curva ROC** | TPR vs FPR para todos os limiares; AUC resume a capacidade discriminativa; útil para comparar modelos |
| **Curva Precisão-Recall** | Precisão vs Recall; preferível à ROC em datasets muito desbalanceados |
| **Feature Importance** | Variáveis mais relevantes para a decisão do modelo |
| **Curva de Aprendizado** | Score vs tamanho do dataset de treino; diagnóstica overfitting/underfitting |

**Boas práticas:**
- Em classes muito desbalanceadas, a curva ROC pode ser otimista — prefira a curva Precisão-Recall.
- A matriz de confusão normalizada (por linha) facilita a comparação entre classes de tamanhos diferentes.
- O limiar padrão (0.5) raramente é o ideal; a curva ROC/PR ajuda a escolher o limiar correto.

---

## Clustering

| Gráfico | O que revela |
|---------|-------------|
| **Scatter 2D (PCA/UMAP)** | Distribuição espacial dos clusters em 2 dimensões; evidencia separação e sobreposição |
| **Gráfico do Cotovelo (Elbow)** | Inércia vs k; o "joelho" da curva indica o número ideal de clusters para K-Means |
| **Silhouette Plot** | Coeficiente silhouette de cada amostra por cluster; clusters homogêneos têm barras longas e uniformes |
| **Dendrograma** | Hierarquia de fusões no clustering aglomerativo; cortar em uma altura define o número de clusters |
| **Heatmap de Centroides** | Valores médios das features por cluster; facilita a interpretação e nomeação dos grupos |

**Boas práticas:**
- Sempre reduza dimensionalidade (PCA ou UMAP) antes de plotar scatter — não use features brutas com alta dimensão.
- No silhouette plot, clusters com muitas amostras abaixo do score médio global são mal formados.
- Use o dendrograma apenas com datasets pequenos a médios (até ~1000 amostras) para manter legibilidade.
- Combine elbow + silhouette para escolha do k — o cotovelo indica um intervalo, o silhouette confirma.

---

## Bibliotecas Python recomendadas

| Biblioteca | Uso principal |
|-----------|--------------|
| **matplotlib** | Base para todos os gráficos; controle total do layout |
| **seaborn** | Gráficos estatísticos elegantes com menos código (heatmap, histplot, scatterplot) |
| **scikit-learn** | `ConfusionMatrixDisplay`, `RocCurveDisplay`, `PrecisionRecallDisplay` prontos para uso |
| **plotly** | Gráficos interativos; ideal para exploração e dashboards |
| **yellowbrick** | Visualizações específicas para ML: elbow, silhouette, curva de aprendizado |
