# Predição — Conceitos e Técnicas

## O que é predição (aprendizado supervisionado)
- Tarefa de estimar um valor ou classe para novas observações a partir de dados históricos rotulados.
- Divide-se em **regressão** (saída contínua) e **classificação** (saída categórica).

## Fluxo padrão de modelagem preditiva
1. Coleta e limpeza dos dados.
2. Análise exploratória (EDA) — distribuições, correlações, outliers.
3. Engenharia de features — criação, transformação e seleção de variáveis.
4. Divisão treino/validação/teste (`train_test_split`, validação cruzada `k-fold`).
5. Treinamento do modelo.
6. Avaliação com métricas adequadas.
7. Ajuste de hiperparâmetros (`GridSearchCV`, `RandomizedSearchCV`, Optuna).
8. Deploy e monitoramento de desvio de dados (*data drift*).

## Principais algoritmos

### Regressão
| Algoritmo | Uso típico |
|-----------|-----------|
| Regressão Linear / Ridge / Lasso | Relações lineares; regularização previne overfitting |
| Árvore de Decisão | Interpretável; sensível a outliers |
| Random Forest | Ensemble robusto; lida bem com features categóricas |
| Gradient Boosting (XGBoost, LightGBM, CatBoost) | Alta performance; competições e produção |
| Redes Neurais (MLP) | Relações muito complexas e grandes volumes |

### Classificação
| Algoritmo | Uso típico |
|-----------|-----------|
| Regressão Logística | Baseline; probabilidades calibradas |
| SVM | Margem máxima; eficaz em alta dimensão |
| KNN | Simples; custoso em inferência |
| Gradient Boosting (XGBoost, LightGBM) | Padrão-ouro para dados tabulares |
| Redes Neurais (CNN, Transformer) | Imagens, texto, séries temporais |

## Métricas de avaliação

### Regressão
- **MAE** (Mean Absolute Error): erro médio absoluto; mesma unidade do alvo.
- **RMSE** (Root Mean Squared Error): penaliza erros grandes; sensível a outliers.
- **R²** (coeficiente de determinação): proporção da variância explicada (1 = perfeito).
- **MAPE**: erro percentual médio absoluto; útil quando a escala varia.

### Classificação
- **Acurácia**: fração de acertos; enganosa em classes desbalanceadas.
- **Precisão / Recall / F1-Score**: equilíbrio entre falsos positivos e falsos negativos.
- **ROC-AUC**: capacidade discriminativa do modelo (1 = perfeito).
- **Matriz de confusão**: visão detalhada de acertos e erros por classe.

## Overfitting e underfitting
- **Overfitting**: modelo memoriza o treino mas não generaliza → regularização, mais dados, dropout.
- **Underfitting**: modelo muito simples → aumentar complexidade, adicionar features.
- Monitorar a diferença entre erro de treino e validação é o sinal principal.

## Séries temporais
- Validação deve respeitar a ordem cronológica (sem *data leakage*): `TimeSeriesSplit`.
- Modelos clássicos: ARIMA, SARIMA, Prophet.
- Modelos modernos: LSTM, Temporal Fusion Transformer, N-BEATS.
- Features úteis: lag, rolling mean/std, diferenciação, variáveis sazonais.

## Ferramentas Python comuns
- **scikit-learn**: pipeline completo de ML (pré-processamento → modelo → avaliação).
- **XGBoost / LightGBM / CatBoost**: Gradient Boosting de alta performance.
- **statsmodels**: modelos estatísticos e séries temporais.
- **Prophet**: séries temporais com sazonalidade e feriados.
- **MLflow / DVC**: rastreamento de experimentos e versionamento de modelos.
- **SHAP / LIME**: explicabilidade de modelos (*explainable AI*).
