"""
Configurações centralizadas para o projeto Global Primates Watch.
Define constantes, cores, labels e configurações globais.
"""

from pathlib import Path
from typing import Dict

# ============================================================================
# PATHS - Funciona tanto no sandbox quanto localmente
# ============================================================================
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_RAW = DATA_DIR / "raw"
DATA_PROCESSED = DATA_DIR / "processed"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
ASSETS_DIR = PROJECT_ROOT / "assets"

# Arquivos de dados
GEOJSON_PATH = DATA_PROCESSED / "primates_map.geojson"
CSV_PATH = DATA_PROCESSED / "primates_species_clean.csv"

# Logo
LOGO_PATH = ASSETS_DIR / "logo.png"

# ============================================================================
# CORES IUCN (Padrão Internacional)
# ============================================================================
IUCN_COLORS: Dict[str, str] = {
    "EX": "#000000",      # Preto - Extinto
    "EW": "#0d0d0d",      # Cinza muito escuro - Extinto na Natureza
    "CR": "#d81e05",      # Vermelho vibrante - Criticamente em Perigo
    "EN": "#fc7f3f",      # Laranja - Em Perigo
    "VU": "#f9e814",      # Amarelo - Vulnerável
    "NT": "#cce2a0",      # Verde claro - Quase Ameaçado
    "LC": "#69b342",      # Verde - Pouco Preocupante
    "DD": "#d3d3d3",      # Cinza - Dados Insuficientes
    "NE": "#ffffff",      # Branco - Não Avaliado
}

# ============================================================================
# LABELS IUCN EM PORTUGUÊS
# ============================================================================
IUCN_LABELS: Dict[str, str] = {
    "EX": "Extinto",
    "EW": "Extinto na Natureza",
    "CR": "Criticamente em Perigo",
    "EN": "Em Perigo",
    "VU": "Vulnerável",
    "NT": "Quase Ameaçado",
    "LC": "Pouco Preocupante",
    "DD": "Dados Insuficientes",
    "NE": "Não Avaliado",
}

# Ordem padrão das categorias (da mais crítica para a menos ameaçada)
IUCN_CATEGORY_ORDER = ["EX", "EW", "CR", "EN", "VU", "NT", "LC", "DD", "NE"]

# ============================================================================
# CLASSIFICAÇÃO DE RISCO
# ============================================================================
RISK_CLASSIFICATION: Dict[str, str] = {
    "EX": "Crítico",
    "EW": "Crítico",
    "CR": "Alto Risco",
    "EN": "Alto Risco",
    "VU": "Médio Risco",
    "NT": "Baixo Risco",
    "LC": "Baixo Risco",
    "DD": "Desconhecido",
    "NE": "Desconhecido",
}

# ============================================================================
# CONTINENTES
# ============================================================================
CONTINENTS = ["América", "África", "Ásia", "Oceania"]

# ============================================================================
# CONFIGURAÇÕES DE MAPAS FOLIUM
# ============================================================================
MAP_CONFIG = {
    "center": [0, 20],
    "zoom_start": 2,
    "tiles": "OpenStreetMap",
    "control_scale": True,
    "prefer_canvas": True,
}

# Configurações de heatmap
HEATMAP_CONFIG = {
    "radius": 20,
    "blur": 15,
    "max_zoom": 18,
    "gradient": {0.2: "blue", 0.4: "cyan", 0.6: "lime", 0.8: "yellow", 1.0: "red"},
}

# Configurações de choropleth
CHOROPLETH_CONFIG = {
    "tiles": "CartoDB positron",
    "fill_opacity": 0.6,
    "line_weight": 1,
    "line_color": "#000000",
}

# Configurações de markers
MARKER_CONFIG = {
    "radius": 6,
    "fill_opacity": 0.7,
    "weight": 2,
}

# ============================================================================
# CONFIGURAÇÕES STREAMLIT
# ============================================================================
PAGE_CONFIG = {
    "page_title": "Global Primates Watch",
    "page_icon": "🐒",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# ============================================================================
# NOMES COMUNS DE PRIMATAS (Dataset Padrão)
# ============================================================================
COMMON_NAMES: Dict[str, str] = {
    "Pan troglodytes": "Chimpanzé",
    "Gorilla gorilla": "Gorila Ocidental",
    "Pongo pygmaeus": "Orangotango de Bornéu",
    "Pan paniscus": "Bonobo",
    "Homo sapiens": "Humano",
    "Macaca mulatta": "Macaco Rhesus",
    "Papio anubis": "Babuíno Olive",
    "Alouatta seniculus": "Bugio Vermelho",
    "Ateles geoffroyi": "Macaco-Aranha",
    "Saimiri sciureus": "Macaco de Cheiro",
    "Callithrix jacchus": "Mico Branco",
    "Leontopithecus rosalia": "Mico Leão Dourado",
    "Cebus capucinus": "Capuchinho",
    "Lagothrix lagotricha": "Muriqui",
    "Brachyteles arachnoides": "Muriqui do Sul",
    "Pithecia pithecia": "Saki",
    "Chiropotes satanas": "Caiarara",
    "Callicebus personatus": "Guigó",
    "Saguinus midas": "Mico Preto",
    "Leontocebus fuscicollis": "Sagui de Coleira",
}

# ============================================================================
# ESTILOS CSS PERSONALIZADOS
# ============================================================================
CUSTOM_CSS = """
<style>
    /* Header principal */
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
    }
    
    /* Cards de métricas */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Botões */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] button {
        border-radius: 10px 10px 0 0;
        font-weight: 600;
    }
    
    /* Sidebar */
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    
    /* Containers */
    .stContainer {
        border-radius: 10px;
        padding: 1rem;
    }
</style>
"""
