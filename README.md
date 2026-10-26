# Portfólio de Análise de Dados, Machine Learning e Séries Temporais

Repositório de projetos selecionados em **Data Analysis, Data Science, Machine Learning e séries temporais**, desenvolvido como parte da evolução profissional e acadêmica de Álvaro Bonifácio.

O objetivo é reunir estudos reproduzíveis e tecnicamente documentados, com atenção a preparação de dados, validação, prevenção de *data leakage*, comparação com baselines e interpretação responsável dos resultados.

## Projetos

### 1. ETL e análise exploratória de dados clínicos e demográficos
📓 `projetos/01_ETL_EDA_Dados_Clinicos.ipynb`

Case introdutório de engenharia e análise de dados com múltiplas fontes.

Principais tópicos:
- leitura e integração de arquivos CSV;
- identificação de valores ausentes;
- junções entre tabelas;
- organização modular de funções em Python;
- preparação dos dados para análises posteriores.

> Os dados utilizados neste case são dados didáticos do projeto original e não representam prontuários reais.

---

### 2. PETR4 × Brent × OVX — previsão de volatilidade
📓 `projetos/02_MD_PETR4_Brent_OVX.ipynb`

Estudo derivado das atividades de **Mineração de Dados** do Mestrado em Ciência da Computação.

Objetivo:
avaliar se informações externas associadas ao mercado de petróleo acrescentam capacidade preditiva à volatilidade futura da PETR4.

Aspectos metodológicos:
- dados diários de PETR4, Brent e OVX;
- construção temporal de atributos;
- horizonte futuro de cinco pregões;
- comparação com baseline histórico;
- validação *walk-forward*;
- controle explícito de vazamento temporal;
- avaliação por MAE, RMSE e R².

O trabalho evidencia um ponto importante em Ciência de Dados: **relação econômica entre variáveis não implica necessariamente ganho preditivo incremental**.

---

### 3. PETR4 e USD/BRL — Machine Learning para previsão de volatilidade
📓 `projetos/03_AM_PETR4_USDBRL.ipynb`

Trabalho desenvolvido na disciplina de **Aprendizado de Máquina** do PPGCC/UFJF.

O experimento amplia a investigação anterior e compara diferentes representações e modelos para previsão da volatilidade futura.

Principais elementos:
- PETR4 como ativo principal;
- USD/BRL como segunda série econômica e variável externa;
- seleção de atributos exclusivamente no conjunto de desenvolvimento;
- divisão temporal entre desenvolvimento e teste;
- `TimeSeriesSplit` com *gap*;
- regressão linear;
- Support Vector Regression (SVR);
- Random Forest;
- ensembles simples e ponderados;
- análise de importância de atributos;
- testes de sensibilidade a sementes;
- comparação com baseline de volatilidade histórica.

O notebook preserva o conjunto de teste final para avaliação fora da etapa de seleção de modelos.

---

### 4. Pesquisa em andamento — volatilidade intradiária da PETR4

A linha atual de pesquisa do mestrado investiga a **previsão da volatilidade realizada nos próximos 60 minutos de negociação**, utilizando dados intradiários e comparando abordagens estatísticas, econométricas, Machine Learning e Deep Learning.

O projeto permanece em desenvolvimento e, por isso, resultados intermediários ainda não são publicados neste repositório como conclusões definitivas.

Entre os tópicos investigados estão:

- construção e auditoria de dados intradiários;
- volatilidade realizada;
- baselines estatísticos;
- Random Forest e XGBoost;
- Deep Learning;
- modelos híbridos e ensembles;
- validação temporal;
- QLIKE e outras métricas específicas de volatilidade.

---

## Tecnologias

`Python` · `Pandas` · `NumPy` · `Scikit-learn` · `Matplotlib` · `Jupyter Notebook` · `SQL`

Conceitos aplicados:

`EDA` · `ETL` · `Machine Learning` · `Time Series` · `Walk-Forward Validation` · `Feature Engineering` · `Data Leakage Prevention`

## Estrutura

```text
Analise-de-Dados/
├── projetos/
│   ├── 01_ETL_EDA_Dados_Clinicos.ipynb
│   ├── 02_MD_PETR4_Brent_OVX.ipynb
│   └── 03_AM_PETR4_USDBRL.ipynb
├── data/
│   └── raw/
├── src/
│   ├── data_cleaning/
│   └── data_loader/
├── doc/
├── requirements.txt
└── README.md
```

## Boas práticas adotadas nos projetos mais recentes

- separação temporal entre desenvolvimento e teste;
- criação de atributos somente com informações disponíveis no momento da previsão;
- prevenção de *data leakage*;
- uso de baselines;
- comparação de modelos com métricas consistentes;
- reprodutibilidade com sementes e versões documentadas;
- distinção entre associação preditiva e causalidade.

---

Este repositório é atualizado à medida que novos experimentos atingem maturidade suficiente para publicação.
