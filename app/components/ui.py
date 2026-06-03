"""
Módulo para componentes de interface do usuário.
Renderiza headers, filtros, badges, tabelas e outros elementos visuais.
"""

import streamlit as st
import pandas as pd
from typing import Tuple, List, Optional


def render_header() -> None:
    """Renderiza header principal da aplicação."""
    st.markdown(
        """
        <div style='text-align: center; padding: 20px 0;'>
            <p style='color: #7f8c8d; font-size: 16px;'>
                Análise Geoespacial Interativa de Primatas Ameaçados Globalmente
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_filters(df: pd.DataFrame) -> Tuple[str, List[str], List[str], str]:
    """
    Renderiza painel de filtros na sidebar.
    
    Args:
        df: DataFrame com dados de espécies
        
    Returns:
        Tupla (search_query, selected_categories, selected_continents, selected_risk)
    """
    st.sidebar.markdown("## 🔍 Filtros")
    
    # Busca por nome
    search_query = st.sidebar.text_input(
        "Buscar espécie:",
        placeholder="Digite nome científico ou comum...",
        help="Busca em nomes científicos e comuns (se disponível)",
    )
    
    # Categorias IUCN
    categories = sorted(df["category"].unique().tolist())
    selected_categories = st.sidebar.multiselect(
        "Categoria IUCN:",
        options=["Todas"] + categories,
        default=["Todas"],
        help="Selecione categorias de ameaça",
    )
    
    # Continentes
    continents = sorted(df["continente"].unique().tolist())
    selected_continents = st.sidebar.multiselect(
        "Continente:",
        options=["Todos"] + continents,
        default=["Todos"],
        help="Selecione continentes",
    )
    
    # Nível de Risco
    risk_levels = sorted(df["risco"].unique().tolist())
    selected_risk = st.sidebar.selectbox(
        "Nível de Risco:",
        options=["Todos"] + risk_levels,
        help="Selecione nível de risco",
    )
    
    return search_query, selected_categories, selected_continents, selected_risk


def render_metrics(stats: dict) -> None:
    """
    Renderiza cards com métricas principais.
    
    Args:
        stats: Dicionário com estatísticas
    """
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🌍 Total de Espécies",
            stats["total_species"],
            delta=None,
        )
    
    with col2:
        st.metric(
            "⚠️ Ameaçadas",
            stats["threatened"],
            delta=None,
        )
    
    with col3:
        st.metric(
            "🔴 Críticas",
            stats["critical"],
            delta=None,
        )
    
    with col4:
        st.metric(
            "🌏 Continentes",
            stats["continents"],
            delta=None,
        )


def render_species_badge(category: str) -> None:
    """
    Renderiza badge com categoria IUCN.
    
    Args:
        category: Código da categoria (CR, EN, VU, etc)
    """
    from app.config import IUCN_COLORS, IUCN_LABELS
    
    color = IUCN_COLORS.get(category, "#cccccc")
    label = IUCN_LABELS.get(category, "N/A")
    
    st.markdown(
        f"""
        <div style='
            background-color: {color};
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            text-align: center;
            font-weight: bold;
            font-size: 16px;
        '>
            {category} - {label}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_species_info_table(species_details: dict) -> None:
    """
    Renderiza tabela com informações detalhadas de uma espécie.
    
    Args:
        species_details: Dicionário com informações da espécie
    """
    info_data = {
        "Atributo": [
            "Nome Científico",
            "Categoria IUCN",
            "Nível de Risco",
            "Continente",
            "Gênero",
        ],
        "Valor": [
            species_details.get("sci_name", "N/A"),
            species_details.get("category_pt", "N/A"),
            species_details.get("risco", "N/A"),
            species_details.get("continente", "N/A"),
            species_details.get("genus", "N/A"),
        ],
    }
    
    # Adicionar common_name se existir
    if "common_name" in species_details and species_details["common_name"] != "N/A":
        info_data["Atributo"].insert(1, "Nome Comum")
        info_data["Valor"].insert(1, species_details["common_name"])
    
    df_info = pd.DataFrame(info_data)
    st.table(df_info)


def render_footer() -> None:
    """Renderiza footer com informações do projeto."""
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #7f8c8d; font-size: 12px; padding: 20px 0;'>
            <p>
                <b>Global Primates Watch</b> - Análise Geoespacial de Primatas Ameaçados<br>
                Dados: IUCN Red List<br>
                <a href='https://www.iucnredlist.org/' target='_blank'>IUCN Red List</a> | 
                <a href='https://github.com/ferropng/Global-Primates-Watch' target='_blank'>GitHub</a>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_about_section() -> None:
    """Renderiza seção 'Sobre' com informações do projeto."""
    with st.expander("ℹ️ Sobre este Projeto"):
        st.markdown(
            """
            ### Global Primates Watch
            
            Uma plataforma interativa para análise geoespacial de primatas ameaçados globalmente.
            
            **Funcionalidades:**
            - 🗺️ Mapas interativos com Folium
            - 📊 Análises estatísticas com Plotly
            - 🔍 Filtros avançados por categoria, continente e risco
            - 📈 Visualizações de dados em tempo real
            
            **Dados:**
            - Fonte: IUCN Red List
            - Espécies: Primatas globais

            """
        )
