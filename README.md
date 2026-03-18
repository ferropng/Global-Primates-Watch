# 🐒 Global Primates Watch

Projeto de Análise de Dados focado na situação atual das espécies de primatas no mundo, utilizando dados geoespaciais oficiais da IUCN (Red List).

## 📊 Sobre o projeto

Este projeto tem como objetivo analisar a distribuição geográfica, o status de conservação e os riscos de extinção das espécies de primatas globalmente.

A análise é baseada em dados geoespaciais (shapefiles), permitindo explorar não apenas informações tabulares, mas também a dimensão espacial da biodiversidade.

## 🎯 Objetivos

* Identificar quantas espécies de primatas estão ameaçadas de extinção
* Analisar a distribuição geográfica global das espécies
* Avaliar a proporção de espécies por categoria de risco (IUCN)
* Criar visualizações claras e interativas para apoio à análise
* Construir uma base sólida para futuras aplicações de Machine Learning

## 🧠 Metodologia

O projeto segue um pipeline de análise de dados:

1. **Coleta de dados**

   * Dados oficiais da IUCN (Red List)
   * Shapefiles com distribuição geográfica das espécies

2. **Tratamento e preparação**

   * Limpeza de dados
   * Padronização de colunas
   * Remoção de duplicidades (nível espécie vs. área geográfica)

3. **Feature Engineering**

   * Tradução das categorias de risco
   * Criação de agrupamentos de risco (baixo, médio, alto)
   * Criação de variáveis derivadas

4. **Análise Exploratória**

   * Distribuição de espécies por categoria
   * Contagem de espécies únicas
   * Identificação de padrões globais

5. **Visualização**

   * Gráficos de distribuição
   * Mapas interativos com Plotly

## 🌍 Categorias de Conservação (IUCN)

* LC — Pouco Preocupante
* NT — Quase Ameaçado
* VU — Vulnerável
* EN — Em Perigo
* CR — Criticamente Ameaçado
* DD — Dados Insuficientes
* EX — Extinto

## 🛠️ Tecnologias utilizadas

* Python
* Pandas
* GeoPandas
* Matplotlib
* Plotly
* Shapely

## 🔮 Próximos passos

* Integração com dados de desmatamento (Our World in Data)
* Criação de dashboards interativos (Power BI / Streamlit)
* Modelos de Machine Learning para previsão de risco de extinção
* Análise temporal da perda de habitat

