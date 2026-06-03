"""
Módulo de utilitários e processamento de dados
Global Primates Watch - Versão 2.0
"""

# Manter compatibilidade com data_utils antigo
from .data_utils import (
    load_shapefile,
    find_column,
    normalize_text_columns,
    filter_primates,
    deduplicate_species,
    translate_categories,
    classify_risk_level,
    get_statistics_by_category,
    get_statistics_by_continent,
    export_to_csv,
    export_to_geojson
)

# Novos módulos
from . import data_loader
from . import data_processor

__version__ = "2.0.0"
__author__ = "Global Primates Watch Team"

__all__ = [
    # Legacy
    'load_shapefile',
    'find_column',
    'normalize_text_columns',
    'filter_primates',
    'deduplicate_species',
    'translate_categories',
    'classify_risk_level',
    'get_statistics_by_category',
    'get_statistics_by_continent',
    'export_to_csv',
    'export_to_geojson',
    # New
    'data_loader',
    'data_processor',
]
