"""
Utilitários para processamento de dados de primatas.
Funções reutilizáveis para limpeza, transformação e análise.
"""

import geopandas as gpd
import pandas as pd
from pathlib import Path
from typing import Tuple, Dict, List


def load_shapefile(shapefile_path: str) -> gpd.GeoDataFrame:
    """
    Carrega um shapefile e retorna um GeoDataFrame.
    
    Args:
        shapefile_path: Caminho para o arquivo .shp
        
    Returns:
        GeoDataFrame com os dados geoespaciais
    """
    return gpd.read_file(shapefile_path)


def find_column(columns: List[str], keywords: List[str]) -> str:
    """
    Encontra uma coluna pelo nome, procurando por palavras-chave.
    
    Args:
        columns: Lista de nomes de colunas
        keywords: Lista de palavras-chave para buscar
        
    Returns:
        Nome da coluna encontrada ou None
    """
    for col in columns:
        lc = col.lower()
        if any(k in lc for k in keywords):
            return col
    return None


def normalize_text_columns(gdf: gpd.GeoDataFrame, columns: List[str]) -> gpd.GeoDataFrame:
    """
    Normaliza colunas de texto (maiúsculas e remove espaços extras).
    
    Args:
        gdf: GeoDataFrame
        columns: Lista de nomes de colunas para normalizar
        
    Returns:
        GeoDataFrame com colunas normalizadas
    """
    gdf_copy = gdf.copy()
    for col in columns:
        if col in gdf_copy.columns:
            gdf_copy[col] = gdf_copy[col].astype(str).str.upper().str.strip()
    return gdf_copy


def filter_primates(gdf: gpd.GeoDataFrame, order_col: str = 'order_') -> gpd.GeoDataFrame:
    """
    Filtra apenas registros de primatas.
    
    Args:
        gdf: GeoDataFrame
        order_col: Nome da coluna com a ordem taxonômica
        
    Returns:
        GeoDataFrame filtrado apenas com primatas
    """
    return gdf[gdf[order_col] == 'PRIMATES'].copy()


def deduplicate_species(gdf: gpd.GeoDataFrame, species_col: str = 'sci_name') -> gpd.GeoDataFrame:
    """
    Remove duplicatas mantendo o primeiro registro de cada espécie.
    
    Args:
        gdf: GeoDataFrame
        species_col: Nome da coluna com nome científico
        
    Returns:
        GeoDataFrame sem duplicatas
    """
    return gdf.drop_duplicates(subset=[species_col], keep='first').copy()


def translate_categories(df: pd.DataFrame, category_col: str = 'category') -> pd.DataFrame:
    """
    Traduz categorias IUCN para português brasileiro.
    
    Args:
        df: DataFrame
        category_col: Nome da coluna com categorias
        
    Returns:
        DataFrame com coluna adicional 'category_pt'
    """
    translation_map = {
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
    
    df_copy = df.copy()
    df_copy['category_pt'] = df_copy[category_col].map(translation_map)
    
    return df_copy


def classify_risk_level(df: pd.DataFrame, category_col: str = 'category') -> pd.DataFrame:
    """
    Classifica o nível de risco baseado na categoria IUCN.
    
    Args:
        df: DataFrame
        category_col: Nome da coluna com categorias
        
    Returns:
        DataFrame com coluna adicional 'risco'
    """
    risk_map = {
        'EX': 'Crítico',
        'EW': 'Crítico',
        'CR': 'Alto Risco',
        'EN': 'Alto Risco',
        'VU': 'Médio Risco',
        'NT': 'Baixo Risco',
        'LC': 'Baixo Risco',
        'DD': 'Desconhecido',
        'NE': 'Desconhecido'
    }
    
    df_copy = df.copy()
    df_copy['risco'] = df_copy[category_col].map(risk_map)
    
    return df_copy


def get_statistics_by_category(df: pd.DataFrame, category_col: str = 'category') -> pd.DataFrame:
    """
    Calcula estatísticas por categoria IUCN.
    
    Args:
        df: DataFrame
        category_col: Nome da coluna com categorias
        
    Returns:
        DataFrame com contagens por categoria
    """
    stats = df[category_col].value_counts().sort_index()
    return stats


def get_statistics_by_continent(gdf: gpd.GeoDataFrame) -> Dict[str, int]:
    """
    Calcula estatísticas de espécies por continente (baseado em geometria).
    
    Args:
        gdf: GeoDataFrame com geometrias
        
    Returns:
        Dicionário com contagens por continente
    """
    # Aproximação: usa a longitude do centroide para classificar continentes
    continents = {}
    
    for idx, row in gdf.iterrows():
        if row.geometry is None:
            continue
            
        lon = row.geometry.centroid.x
        
        if -180 <= lon < -60:
            continent = 'América'
        elif -60 <= lon < 40:
            continent = 'África'
        elif 40 <= lon < 100:
            continent = 'Ásia'
        elif 100 <= lon <= 180:
            continent = 'Oceania'
        else:
            continent = 'Desconhecido'
        
        continents[continent] = continents.get(continent, 0) + 1
    
    return continents


def export_to_csv(df: pd.DataFrame, output_path: str) -> None:
    """
    Exporta DataFrame para CSV.
    
    Args:
        df: DataFrame
        output_path: Caminho do arquivo de saída
    """
    df.to_csv(output_path, index=False)
    print(f"✓ Arquivo exportado: {output_path}")


def export_to_geojson(gdf: gpd.GeoDataFrame, output_path: str) -> None:
    """
    Exporta GeoDataFrame para GeoJSON.
    
    Args:
        gdf: GeoDataFrame
        output_path: Caminho do arquivo de saída
    """
    gdf.to_file(output_path, driver='GeoJSON')
    print(f"✓ Arquivo exportado: {output_path}")
