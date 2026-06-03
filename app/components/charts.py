"""
Módulo para criação de gráficos estatísticos com Plotly.
Mantém Plotly apenas para gráficos de dados, não para mapas.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Optional

from app.config import IUCN_COLORS, IUCN_LABELS


def create_category_distribution_chart(
    category_counts: pd.Series,
    title: str = "Distribuição por Categoria IUCN",
) -> go.Figure:
    """
    Cria gráfico de barras com distribuição por categoria IUCN.
    
    Args:
        category_counts: Series com contagens por categoria
        title: Título do gráfico
        
    Returns:
        Objeto plotly Figure
    """
    fig = px.bar(
        x=category_counts.index,
        y=category_counts.values,
        color=category_counts.index,
        color_discrete_map=IUCN_COLORS,
        labels={"x": "Categoria IUCN", "y": "Número de Espécies"},
        title=title,
    )
    
    fig.update_layout(
        showlegend=False,
        height=400,
        hovermode="x unified",
        template="plotly_white",
        font=dict(family="Arial, sans-serif", size=12),
        title_font_size=16,
    )
    
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Espécies: %{y}<extra></extra>",
    )
    
    return fig


def create_continent_distribution_chart(
    continent_counts: pd.Series,
    title: str = "Distribuição por Continente",
) -> go.Figure:
    """
    Cria gráfico de pizza com distribuição por continente.
    
    Args:
        continent_counts: Series com contagens por continente
        title: Título do gráfico
        
    Returns:
        Objeto plotly Figure
    """
    fig = px.pie(
        values=continent_counts.values,
        names=continent_counts.index,
        title=title,
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    
    fig.update_layout(
        height=400,
        template="plotly_white",
        font=dict(family="Arial, sans-serif", size=12),
        title_font_size=16,
    )
    
    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Espécies: %{value}<br>Percentual: %{percent}<extra></extra>",
    )
    
    return fig


def create_threatened_by_continent_chart(
    threatened_data: pd.DataFrame,
    title: str = "Espécies Ameaçadas por Continente",
) -> go.Figure:
    """
    Cria gráfico de barras com espécies ameaçadas por continente.
    
    Args:
        threatened_data: DataFrame com colunas 'continente' e 'count'
        title: Título do gráfico
        
    Returns:
        Objeto plotly Figure
    """
    fig = px.bar(
        threatened_data,
        x="continente",
        y="count",
        color="continente",
        labels={"count": "Número de Espécies Ameaçadas", "continente": "Continente"},
        title=title,
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    
    fig.update_layout(
        showlegend=False,
        height=400,
        hovermode="x unified",
        template="plotly_white",
        font=dict(family="Arial, sans-serif", size=12),
        title_font_size=16,
    )
    
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Espécies Ameaçadas: %{y}<extra></extra>",
    )
    
    return fig


def create_risk_level_chart(
    risk_counts: pd.Series,
    title: str = "Distribuição por Nível de Risco",
) -> go.Figure:
    """
    Cria gráfico de barras com distribuição por nível de risco.
    
    Args:
        risk_counts: Series com contagens por nível de risco
        title: Título do gráfico
        
    Returns:
        Objeto plotly Figure
    """
    # Definir ordem e cores para níveis de risco
    risk_order = ["Crítico", "Alto Risco", "Médio Risco", "Baixo Risco", "Desconhecido"]
    risk_colors = {
        "Crítico": "#d81e05",
        "Alto Risco": "#fc7f3f",
        "Médio Risco": "#f9e814",
        "Baixo Risco": "#69b342",
        "Desconhecido": "#d3d3d3",
    }
    
    # Reordenar conforme a ordem definida
    risk_counts = risk_counts.reindex(risk_order, fill_value=0)
    
    fig = px.bar(
        x=risk_counts.index,
        y=risk_counts.values,
        color=risk_counts.index,
        color_discrete_map=risk_colors,
        labels={"x": "Nível de Risco", "y": "Número de Espécies"},
        title=title,
    )
    
    fig.update_layout(
        showlegend=False,
        height=400,
        hovermode="x unified",
        template="plotly_white",
        font=dict(family="Arial, sans-serif", size=12),
        title_font_size=16,
    )
    
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Espécies: %{y}<extra></extra>",
    )
    
    return fig


def create_top_threatened_species_chart(
    species_data: pd.DataFrame,
    title: str = "Top 10 Espécies Mais Ameaçadas",
) -> go.Figure:
    """
    Cria gráfico horizontal com as espécies mais ameaçadas.
    
    Args:
        species_data: DataFrame com dados das espécies
        title: Título do gráfico
        
    Returns:
        Objeto plotly Figure
    """
    # Criar coluna de label
    species_data = species_data.copy()
    
    # Se common_name existe, usar sci_name + common_name
    if "common_name" in species_data.columns:
        species_data["label"] = (
            species_data["sci_name"]
            + "<br><i>"
            + species_data["common_name"].fillna("N/A")
            + "</i>"
        )
    else:
        # Caso contrário, usar apenas sci_name
        species_data["label"] = species_data["sci_name"]
    
    # Mapear cores por categoria
    species_data["color"] = species_data["category"].map(IUCN_COLORS)
    
    # Converter range para lista (Plotly não aceita range objects)
    x_values = list(range(len(species_data)))
    
    fig = go.Figure(
        data=[
            go.Bar(
                y=species_data["label"],
                x=x_values,
                orientation="h",
                marker=dict(color=species_data["color"]),
                hovertemplate="<b>%{y}</b><br>Posição: %{x}<extra></extra>",
            )
        ]
    )
    
    fig.update_layout(
        title=title,
        xaxis_title="Ranking de Ameaça",
        yaxis_title="Espécie",
        height=500,
        template="plotly_white",
        font=dict(family="Arial, sans-serif", size=11),
        title_font_size=16,
        hovermode="closest",
    )
    
    return fig


def create_category_comparison_chart(
    df: pd.DataFrame,
    title: str = "Comparação de Categorias por Continente",
) -> go.Figure:
    """
    Cria gráfico de barras agrupadas comparando categorias por continente.
    
    Args:
        df: DataFrame com dados
        title: Título do gráfico
        
    Returns:
        Objeto plotly Figure
    """
    # Criar tabela de contingência
    contingency = pd.crosstab(df["continente"], df["category"])
    
    fig = go.Figure()
    
    for category in contingency.columns:
        fig.add_trace(
            go.Bar(
                name=IUCN_LABELS.get(category, category),
                x=contingency.index,
                y=contingency[category],
                marker_color=IUCN_COLORS.get(category, "#cccccc"),
            )
        )
    
    fig.update_layout(
        title=title,
        xaxis_title="Continente",
        yaxis_title="Número de Espécies",
        barmode="group",
        height=450,
        template="plotly_white",
        font=dict(family="Arial, sans-serif", size=12),
        title_font_size=16,
        hovermode="x unified",
    )
    
    return fig


def create_species_summary_table(
    species_data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Cria tabela resumida de espécies para exibição.
    
    Args:
        species_data: DataFrame com dados de espécies
        
    Returns:
        DataFrame formatado para exibição
    """
    # Selecionar colunas disponíveis
    cols = ["sci_name"]
    if "common_name" in species_data.columns:
        cols.append("common_name")
    cols.extend(["category", "category_pt", "risco", "continente"])
    
    display_df = species_data[cols].copy()
    
    # Renomear colunas
    rename_dict = {
        "sci_name": "Nome Científico",
        "common_name": "Nome Comum",
        "category": "Categoria",
        "category_pt": "Categoria (PT)",
        "risco": "Nível de Risco",
        "continente": "Continente",
    }
    
    display_df.columns = [rename_dict.get(col, col) for col in display_df.columns]
    
    return display_df
