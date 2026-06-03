"""
Módulo para criar mapas interativos com Folium
Substitui as visualizações Plotly do notebook 03_visualization.ipynb
"""

import folium
from folium.plugins import HeatMap, MarkerCluster, Search
import geopandas as gpd
import pandas as pd
import numpy as np
from pathlib import Path
import streamlit as st

# Cores para categorias IUCN (padrão internacional)
IUCN_COLORS = {
    'EX': '#000000',   # Preto - Extinto
    'EW': '#0d0d0d',   # Cinza muito escuro - Extinto na Natureza
    'CR': '#d81e05',   # Vermelho - Criticamente em Perigo
    'EN': '#fc7f3f',   # Laranja - Em Perigo
    'VU': '#f9e814',   # Amarelo - Vulnerável
    'NT': '#cce2a0',   # Verde claro - Quase Ameaçado
    'LC': '#69b342',   # Verde - Pouco Preocupante
    'DD': '#d3d3d3',   # Cinza - Dados Insuficientes
    'NE': '#ffffff'    # Branco - Não Avaliado
}

IUCN_LABELS = {
    'EX': 'Extinto',
    'EW': 'Extinto na Natureza',
    'CR': 'Criticamente em Perigo',
    'EN': 'Em Perigo',
    'VU': 'Vulnerável',
    'NT': 'Quase Ameaçado',
    'LC': 'Pouco Preocupante',
    'DD': 'Dados Insuficientes',
    'NE': 'Não Avaliado'
}


def create_interactive_map(gdf, df, filter_category=None, filter_continent=None):
    """
    Cria mapa interativo com Folium
    
    Args:
        gdf: GeoDataFrame com geometrias
        df: DataFrame com dados das espécies
        filter_category: Lista de categorias IUCN para filtrar
        filter_continent: Lista de continentes para filtrar
    
    Returns:
        folium.Map object
    """
    # Preparar dados
    gdf_map = gdf.copy()
    gdf_map = gdf_map.merge(
        df[['sci_name', 'category', 'category_pt', 'risco', 'common_name']], 
        on='sci_name', 
        how='left', 
        suffixes=('', '_df')
    )
    
    # Aplicar filtros
    if filter_category and filter_category != ['Todas']:
        gdf_map = gdf_map[gdf_map['category'].isin(filter_category)]
    
    if filter_continent and filter_continent != ['Todos']:
        gdf_map = gdf_map[gdf_map['continente'].isin(filter_continent)]
    
    # Calcular centróides
    gdf_map['lat'] = gdf_map.geometry.centroid.y
    gdf_map['lon'] = gdf_map.geometry.centroid.x
    
    # Criar mapa base
    m = folium.Map(
        location=[0, 20], 
        zoom_start=2, 
        tiles='OpenStreetMap',
        control_scale=True
    )
    
    # Adicionar FeatureGroup para markers
    marker_cluster = MarkerCluster(
        name='Espécies de Primatas',
        overlay=True,
        control=True
    ).add_to(m)
    
    # Adicionar markers para cada espécie
    for idx, row in gdf_map.iterrows():
        if pd.notna(row['lat']) and pd.notna(row['lon']):
            # Criar popup com informações
            common_name = row.get('common_name', 'N/A')
            if pd.isna(common_name):
                common_name = 'Não disponível'
                
            popup_html = f"""
            <div style='font-family: Arial; width: 250px;'>
                <h4 style='margin-bottom: 5px; color: {IUCN_COLORS.get(row['category'], '#333')};'>
                    {row['sci_name']}
                </h4>
                <b>Nome Comum:</b> {common_name}<br>
                <b>Categoria IUCN:</b> {row.get('category_pt', row.get('category', 'N/A'))}<br>
                <b>Nível de Risco:</b> {row.get('risco', 'N/A')}
            </div>
            """
            
            color = IUCN_COLORS.get(row['category'], '#cccccc')
            
            folium.CircleMarker(
                location=[row['lat'], row['lon']],
                radius=6,
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"{row['sci_name']} ({row.get('category', 'N/A')})",
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.7,
                weight=2
            ).add_to(marker_cluster)
    
    # Adicionar camada de densidade (heatmap) para espécies ameaçadas
    threatened = gdf_map[gdf_map['risco'].isin(['Alto Risco', 'Crítico'])]
    if len(threatened) > 0:
        heat_data = [[point.y, point.x] for point in threatened.geometry.centroid]
        HeatMap(
            heat_data,
            name='Hotspots de Espécies Ameaçadas',
            radius=15,
            blur=10,
            gradient={0.4: 'blue', 0.65: 'lime', 1: 'red'}
        ).add_to(m)
    
    # Adicionar controle de camadas
    folium.LayerControl(collapsed=False).add_to(m)
    
    return m


def create_choropleth_map(gdf, df, column='category'):
    """
    Cria mapa coroplético com Folium
    
    Args:
        gdf: GeoDataFrame com geometrias
        df: DataFrame com dados
        column: Coluna para colorir
    
    Returns:
        folium.Map object
    """
    # Simplificar geometrias para melhor performance
    gdf_map = gdf.copy()
    gdf_map['geometry'] = gdf_map.geometry.simplify(tolerance=0.1)
    
    # Criar mapa base
    m = folium.Map(location=[0, 20], zoom_start=2, tiles='CartoDB positron')
    
    # Criar dicionário de cores
    color_mapping = {cat: IUCN_COLORS.get(cat, '#cccccc') for cat in df[column].unique()}
    
    # Adicionar GeoJSON com estilo personalizado
    def style_function(feature):
        category = feature['properties'].get(column, 'NE')
        return {
            'fillColor': color_mapping.get(category, '#cccccc'),
            'color': '#000000',
            'weight': 1,
            'fillOpacity': 0.6,
        }
    
    def highlight_function(feature):
        return {
            'fillColor': '#ffff00',
            'color': '#000000',
            'weight': 3,
            'fillOpacity': 0.8,
        }
    
    folium.GeoJson(
        gdf_map.__geo_interface__,
        style_function=style_function,
        highlight_function=highlight_function,
        tooltip=folium.GeoJsonTooltip(
            fields=['sci_name', 'category_pt', 'risco'],
            aliases=['Espécie:', 'Categoria:', 'Risco:'],
            style=("background-color: white; color: #333333; font-family: Arial; font-size: 12px; padding: 10px;")
        ),
        name='Distribuição de Primatas'
    ).add_to(m)
    
    # Adicionar legenda
    legend_html = f"""
    <div style='position: fixed; 
                bottom: 50px; left: 50px; width: 200px; height: auto; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:12px; padding: 10px;'>
        <b>Status IUCN</b><br>
    """
    for cat, color in IUCN_COLORS.items():
        if cat in df[column].values:
            legend_html += f"""
            <i style='background:{color}; width: 20px; height: 10px; display: inline-block; margin-right: 5px;'></i>
            {IUCN_LABELS.get(cat, cat)}<br>
            """
    legend_html += '</div>'
    m.get_root().html.add_child(folium.Element(legend_html))
    
    return m