"""
Módulo para carregamento e cache de dados.
Responsável por ler GeoJSON e CSV com tratamento de erros robusto.
"""

import streamlit as st
import geopandas as gpd
import pandas as pd
from pathlib import Path
from typing import Tuple, Optional
import logging
import os

logger = logging.getLogger(__name__)


@st.cache_data
def load_data(
    geojson_path: Path,
    csv_path: Path,
) -> Tuple[gpd.GeoDataFrame, pd.DataFrame]:
    """
    Carrega dados processados de GeoJSON e CSV com cache.
    
    Args:
        geojson_path: Caminho para o arquivo GeoJSON
        csv_path: Caminho para o arquivo CSV
        
    Returns:
        Tupla (GeoDataFrame, DataFrame)
        
    Raises:
        FileNotFoundError: Se os arquivos não forem encontrados
        ValueError: Se os dados estiverem inválidos
    """
    # Converter para Path se necessário
    geojson_path = Path(geojson_path)
    csv_path = Path(csv_path)
    
    # Debug: Mostrar caminhos
    print(f"[DEBUG] Procurando GeoJSON em: {geojson_path}")
    print(f"[DEBUG] Procurando CSV em: {csv_path}")
    print(f"[DEBUG] GeoJSON existe: {geojson_path.exists()}")
    print(f"[DEBUG] CSV existe: {csv_path.exists()}")
    
    # Validar existência dos arquivos
    if not geojson_path.exists():
        raise FileNotFoundError(f"Arquivo GeoJSON não encontrado: {geojson_path}")
    if not csv_path.exists():
        raise FileNotFoundError(f"Arquivo CSV não encontrado: {csv_path}")
    
    try:
        # Carregar GeoJSON
        gdf = gpd.read_file(str(geojson_path))
        print(f"[DEBUG] GeoJSON carregado: {len(gdf)} registros")
        print(f"[DEBUG] Colunas GeoJSON: {gdf.columns.tolist()}")
        logger.info(f"✓ GeoJSON carregado: {len(gdf)} registros")
        
        # Carregar CSV
        df = pd.read_csv(str(csv_path))
        print(f"[DEBUG] CSV carregado: {len(df)} espécies")
        print(f"[DEBUG] Colunas CSV: {df.columns.tolist()}")
        logger.info(f"✓ CSV carregado: {len(df)} espécies")
        
        # Validações básicas
        if len(gdf) == 0 or len(df) == 0:
            raise ValueError("Dados carregados estão vazios")
        
        return gdf, df
        
    except Exception as e:
        logger.error(f"Erro ao carregar dados: {str(e)}")
        print(f"[DEBUG] Erro: {str(e)}")
        raise


def add_geographic_info(
    gdf: gpd.GeoDataFrame,
    df: pd.DataFrame,
) -> Tuple[gpd.GeoDataFrame, pd.DataFrame]:
    """
    Adiciona informações geográficas derivadas (centroide, continente).
    
    Args:
        gdf: GeoDataFrame
        df: DataFrame
        
    Returns:
        Tupla (GeoDataFrame, DataFrame) com informações adicionadas
    """
    gdf = gdf.copy()
    df = df.copy()
    
    # Calcular coordenadas do centroide
    gdf["lat"] = gdf.geometry.centroid.y
    gdf["lon"] = gdf.geometry.centroid.x
    
    # Classificar continentes baseado em longitude
    def classify_continent(lon: float) -> str:
        """Classifica continente pela longitude do centroide."""
        if -180 <= lon < -60:
            return "América"
        elif -60 <= lon < 40:
            return "África"
        elif 40 <= lon < 100:
            return "Ásia"
        elif 100 <= lon <= 180:
            return "Oceania"
        return "Desconhecido"
    
    gdf["continente"] = gdf["lon"].apply(classify_continent)
    
    # Sincronizar continente no DataFrame
    if "sci_name" in gdf.columns and "sci_name" in df.columns:
        continent_map = dict(zip(gdf["sci_name"], gdf["continente"]))
        df["continente"] = df["sci_name"].map(continent_map)
    
    print(f"[DEBUG] Continentes únicos em GeoDataFrame: {gdf['continente'].unique().tolist()}")
    print(f"[DEBUG] Continentes únicos em DataFrame: {df['continente'].unique().tolist()}")
    
    return gdf, df


def validate_data(gdf: gpd.GeoDataFrame, df: pd.DataFrame) -> bool:
    """
    Valida integridade dos dados carregados.
    
    Args:
        gdf: GeoDataFrame
        df: DataFrame
        
    Returns:
        True se válido, False caso contrário
    """
    required_gdf_cols = ["geometry", "sci_name"]
    required_df_cols = ["sci_name", "category"]
    
    # Verificar colunas obrigatórias
    if not all(col in gdf.columns for col in required_gdf_cols):
        logger.error("GeoDataFrame faltam colunas obrigatórias")
        print(f"[DEBUG] Colunas GeoDataFrame: {gdf.columns.tolist()}")
        return False
    
    if not all(col in df.columns for col in required_df_cols):
        logger.error("DataFrame faltam colunas obrigatórias")
        print(f"[DEBUG] Colunas DataFrame: {df.columns.tolist()}")
        return False
    
    # Verificar geometrias válidas
    if gdf.geometry.isnull().any():
        logger.warning(f"GeoDataFrame contém {gdf.geometry.isnull().sum()} geometrias nulas")
    
    print(f"[DEBUG] Validação passou! GeoDataFrame: {len(gdf)} registros, DataFrame: {len(df)} registros")
    return True
