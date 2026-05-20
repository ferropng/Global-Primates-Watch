# 🐒 Global Primates Watch — Análise Geoespacial e Machine Learning

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![GeoPandas](https://img.shields.io/badge/GeoPandas-0.14-green.svg)](https://geopandas.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-IUCN_Terms-red.svg)](https://www.iucnredlist.org/resources/terms-of-use)

Este projeto realiza uma análise geoespacial avançada e modelagem preditiva sobre a distribuição global de primatas ameaçados, utilizando dados oficiais da **IUCN Red List of Threatened Species**.

---

## 📁 Estrutura do Repositório

A estrutura do projeto foi totalmente reorganizada para seguir as melhores práticas de engenharia de dados e reprodutibilidade:

```text
Global-Primates-Watch/
├── data/
│   ├── raw/                  # Shapefiles originais da IUCN (MAMMALS_TERRESTRIAL_ONLY)
│   └── processed/            # Dados limpos e processados (CSV, GeoJSON)
├── notebooks/
│   ├── 01_data_cleaning.ipynb # Pipeline de limpeza e preparação de dados
│   ├── 02_eda.ipynb           # Análise exploratória de dados (EDA) avançada
│   ├── 03_visualization.ipynb # Visualizações interativas e estáticas
│   └── 04_machine_learning.ipynb # Modelo preditivo de risco de extinção
├── src/                      # Funções e utilitários reutilizáveis
│   ├── __init__.py
│   └── data_utils.py
├── outputs/                  # Gráficos, mapas interativos e modelos exportados
│   ├── primates_by_category.html
│   ├── primates_by_continent.html
│   ├── primates_density_heatmap.html
│   ├── primates_summary_analysis.png
│   ├── species_threat_predictions.csv
│   └── threat_prediction_model.pkl
├── requirements.txt          # Dependências do projeto
└── README.md                 # Documentação principal
```

---
## ⚠️ Setup Inicial: Baixar Dados

**IMPORTANTE:** As pastas `data/raw/` e `data/processed/` estão vazias. Você precisa baixar os dados da IUCN para executar o projeto.

### **Passo 1: Baixar Dados da IUCN**

1. Acesse https://www.iucnredlist.org/resources/spatial-data-download
2. Faça login (crie uma conta se necessário - é gratuito)
3. Selecione os filtros:
   - **Taxonomy:** Mammalia → Primates
   - **Assessment:** Terrestrial only
   - **Format:** Shapefile
4. Clique em **Download**
5. Aguarde o download (arquivo ~1.8 GB)

### **Passo 2: Extrair e Colocar no Repositório**

```bash
# Extrair o arquivo baixado
unzip MAMMALS_TERRESTRIAL_ONLY.zip

# Mover para a pasta correta
mv MAMMALS_TERRESTRIAL_ONLY/ data/raw/

---
## 📊 Análises e Visualizações

### 1. Distribuição por Categoria IUCN
As espécies foram analisadas e ordenadas de acordo com a gravidade do risco de extinção (da mais crítica para a menos ameaçada), permitindo uma comunicação visual muito mais clara e direta.

### 2. Hotspots de Biodiversidade (Heatmap)
Utilizando coordenadas geográficas dos centroides das distribuições, identificamos as regiões de maior densidade de espécies ameaçadas, fornecendo dados cruciais para tomada de decisão em conservação.

### 3. Análise por Continente
Cruzamos os dados espaciais para entender quais continentes concentram o maior número de espécies criticamente ameaçadas.

---

## 🤖 Machine Learning

Implementamos um modelo de **Random Forest Classifier** para prever se uma espécie está sob ameaça (categorias `CR`, `EN`, `VU`) com base em características geográficas e espaciais:

- **Features Utilizadas**:
  - Área de distribuição ($km^2$)
  - Perímetro da distribuição ($km$)
  - Índice de fragmentação (razão perímetro/área)
  - Coordenadas geográficas (latitude/longitude do centroide)
  - Código do continente
- **Performance do Modelo**:
  - **Acurácia Geral**: ~85% na validação cruzada.
  - **Feature mais importante**: Área de distribuição (espécies com menor área de ocorrência apresentam risco significativamente maior).

---

## 📜 Termos de Uso e Citação de Dados

Este projeto utiliza dados da **IUCN Red List of Threatened Species**. De acordo com os termos de uso oficiais da IUCN:

> **Citação Obrigatória**:
> IUCN (2026). The IUCN Red List of Threatened Species. Version 2026-1. <https://www.iucnredlist.org>

Para mais detalhes sobre as regras de distribuição e uso comercial, consulte o arquivo oficial de termos de uso incluído em `data/raw/MAMMALS_TERRESTRIAL_ONLY/IUCN_Red_List_Terms_and_Conditions_of_Use_v3_1.pdf`.
