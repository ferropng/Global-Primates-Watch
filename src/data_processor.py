"""
Módulo para processamento e transformação de dados.
Responsável por filtros, agregações e transformações de dados.
"""

import geopandas as gpd
import pandas as pd
from typing import List, Optional, Dict


def apply_filters(
    gdf: gpd.GeoDataFrame,
    df: pd.DataFrame,
    search_query: Optional[str] = None,
    categories: Optional[List[str]] = None,
    continents: Optional[List[str]] = None,
    risk_levels: Optional[List[str]] = None,
) -> tuple[gpd.GeoDataFrame, pd.DataFrame]:
    """
    Aplica múltiplos filtros aos dados.
    
    Args:
        gdf: GeoDataFrame original
        df: DataFrame original
        search_query: Texto para buscar em nomes científicos/comuns
        categories: Lista de categorias IUCN
        continents: Lista de continentes
        risk_levels: Lista de níveis de risco
        
    Returns:
        Tupla (GeoDataFrame filtrado, DataFrame filtrado)
    """
    filtered_df = df.copy()
    filtered_gdf = gdf.copy()
    
    # Filtro de pesquisa
    if search_query and search_query.strip():
        search_lower = search_query.lower()
        mask = filtered_df["sci_name"].str.lower().str.contains(search_lower, na=False)
        
        # Se common_name existe, buscar também nele
        if "common_name" in filtered_df.columns:
            mask = mask | filtered_df["common_name"].str.lower().str.contains(search_lower, na=False)
        
        filtered_df = filtered_df[mask]
        filtered_gdf = filtered_gdf[filtered_gdf["sci_name"].isin(filtered_df["sci_name"])]
    
    # Filtro por categoria IUCN
    if categories and "Todas" not in categories:
        filtered_df = filtered_df[filtered_df["category"].isin(categories)]
        filtered_gdf = filtered_gdf[filtered_gdf["category"].isin(categories)]
    
    # Filtro por continente
    if continents and "Todos" not in continents:
        filtered_df = filtered_df[filtered_df["continente"].isin(continents)]
        filtered_gdf = filtered_gdf[filtered_gdf["continente"].isin(continents)]
    
    # Filtro por nível de risco
    if risk_levels and "Todos" not in risk_levels:
        filtered_df = filtered_df[filtered_df["risco"].isin(risk_levels)]
        filtered_gdf = filtered_gdf[filtered_gdf["risco"].isin(risk_levels)]
    
    return filtered_gdf, filtered_df


def get_statistics(
    df: pd.DataFrame,
) -> Dict[str, int]:
    """
    Calcula estatísticas principais dos dados.
    
    Args:
        df: DataFrame com dados de espécies
        
    Returns:
        Dicionário com estatísticas
    """
    stats = {
        "total_species": len(df),
        "threatened": len(df[df["risco"].isin(["Alto Risco", "Crítico"])]),
        "critical": len(df[df["category"] == "CR"]),
        "endangered": len(df[df["category"] == "EN"]),
        "vulnerable": len(df[df["category"] == "VU"]),
        "continents": df["continente"].nunique(),
    }
    
    return stats


def get_category_distribution(df: pd.DataFrame) -> pd.Series:
    """
    Retorna distribuição de espécies por categoria IUCN.
    
    Args:
        df: DataFrame com dados
        
    Returns:
        Series com contagens por categoria
    """
    from app.config import IUCN_CATEGORY_ORDER
    
    counts = df["category"].value_counts()
    # Reordenar conforme ordem padrão
    counts = counts.reindex(IUCN_CATEGORY_ORDER, fill_value=0)
    
    return counts


def get_continent_distribution(df: pd.DataFrame) -> pd.Series:
    """
    Retorna distribuição de espécies por continente.
    
    Args:
        df: DataFrame com dados
        
    Returns:
        Series com contagens por continente
    """
    return df["continente"].value_counts()


def get_threatened_by_continent(df: pd.DataFrame) -> pd.DataFrame:
    """
    Retorna número de espécies ameaçadas por continente.
    
    Args:
        df: DataFrame com dados
        
    Returns:
        DataFrame com contagens
    """
    threatened = df[df["risco"].isin(["Alto Risco", "Crítico"])]
    result = threatened.groupby("continente").size().reset_index(name="count")
    
    return result.sort_values("count", ascending=False)


def get_species_details(
    df: pd.DataFrame,
    gdf: gpd.GeoDataFrame,
    species_name: str,
) -> Optional[Dict]:
    """
    Retorna detalhes completos de uma espécie.
    
    Args:
        df: DataFrame com dados
        gdf: GeoDataFrame com geometrias
        species_name: Nome científico da espécie
        
    Returns:
        Dicionário com detalhes ou None se não encontrada
    """
    species_data = df[df["sci_name"] == species_name]
    
    if species_data.empty:
        return None
    
    row = species_data.iloc[0]
    
    details = {
        "sci_name": row.get("sci_name", "N/A"),
        "common_name": row.get("common_name", "N/A") if "common_name" in row.index else "N/A",
        "category": row.get("category", "NE"),
        "category_pt": row.get("category_pt", "N/A"),
        "risco": row.get("risco", "N/A"),
        "continente": row.get("continente", "N/A"),
        "genus": row.get("genus", "N/A"),
    }
    
    # Adicionar informações geográficas
    species_gdf = gdf[gdf["sci_name"] == species_name]
    if not species_gdf.empty:
        geom_row = species_gdf.iloc[0]
        details["area_km2"] = geom_row.geometry.area if hasattr(geom_row.geometry, "area") else "N/A"
        details["lat"] = geom_row.get("lat", "N/A")
        details["lon"] = geom_row.get("lon", "N/A")
    
    return details


def get_top_threatened_species(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    Retorna as N espécies mais ameaçadas.
    
    Args:
        df: DataFrame com dados
        n: Número de espécies a retornar
        
    Returns:
        DataFrame com as espécies mais ameaçadas
    """
    from app.config import IUCN_CATEGORY_ORDER
    
    # Criar mapa de prioridade (mais crítico = menor número)
    priority_map = {cat: i for i, cat in enumerate(IUCN_CATEGORY_ORDER)}
    df_copy = df.copy()
    df_copy["priority"] = df_copy["category"].map(priority_map)
    
    # Selecionar colunas disponíveis
    cols = ["sci_name", "category", "category_pt", "continente"]
    if "common_name" in df_copy.columns:
        cols.insert(1, "common_name")
    
    return df_copy.nsmallest(n, "priority")[cols]
