"""
Global Primates Watch - Análise Geoespacial de Primatas Ameaçados
"""

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

__version__ = "2.0.0"
__author__ = "Global Primates Watch Team"

__all__ = [
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
    'export_to_geojson'
]
