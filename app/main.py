"""
🐒 Global Primates Watch - Aplicação Principal Streamlit
Análise geoespacial interativa de primatas ameaçados globalmente.

Versão 2.0 - Refatorada com arquitetura profissional
"""

import streamlit as st
import sys
from pathlib import Path

# Adicionar paths - Funciona tanto no sandbox quanto localmente
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Importações
from app.config import PAGE_CONFIG, CUSTOM_CSS
from app.components import (
    render_header,
    render_filters,
    render_metrics,
    render_species_badge,
    render_species_info_table,
    render_footer,
    render_about_section,
    create_interactive_map,
    create_choropleth_map,
    create_heatmap_density,
    create_species_detail_map,
    create_category_distribution_chart,
    create_continent_distribution_chart,
    create_threatened_by_continent_chart,
    create_risk_level_chart,
    create_top_threatened_species_chart,
    create_category_comparison_chart,
)
from src.data_loader import load_data, add_geographic_info, validate_data
from src.data_processor import (
    apply_filters,
    get_statistics,
    get_category_distribution,
    get_continent_distribution,
    get_threatened_by_continent,
    get_species_details,
    get_top_threatened_species,
)
from app.config import GEOJSON_PATH, CSV_PATH
from streamlit_folium import st_folium

DATA_PROCESSING_VERSION = "continent-classification-v2"


# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================
st.set_page_config(**PAGE_CONFIG)

# Aplicar CSS personalizado
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================
@st.cache_data
def load_and_process_data(cache_version: str = DATA_PROCESSING_VERSION):
    """Carrega e processa dados com cache."""
    try:
        gdf, df = load_data(GEOJSON_PATH, CSV_PATH)
        gdf, df = add_geographic_info(gdf, df)
        
        if not validate_data(gdf, df):
            st.error("⚠️ Dados inválidos ou incompletos!")
            st.stop()
        
        return gdf, df
    except FileNotFoundError as e:
        st.error(f"❌ Erro ao carregar dados: {str(e)}")
        st.info("Execute o notebook 01_data_cleaning.ipynb para processar os dados.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Erro inesperado: {str(e)}")
        st.stop()


def render_logo_header():
    """Renderiza header com logo do projeto."""

    col1, col2, col3 = st.columns([2, 3, 2])

    with col2:
        logo_path = project_root / "assets" / "logo.png"

        if logo_path.exists():
            st.image(str(logo_path))
        else:
            st.warning("⚠️ Logo não encontrada em assets/logo.png")


# ============================================================================
# MAIN
# ============================================================================
def main():
    """Função principal da aplicação."""
    
    # Logo e Header
    render_logo_header()
    render_header()
    
    # Carregar dados
    with st.spinner("📦 Carregando dados..."):
        gdf, df = load_and_process_data()
    
    # Sidebar - Filtros
    search_query, selected_categories, selected_continents, selected_risk = render_filters(df)
    
    # Aplicar filtros
    filtered_gdf, filtered_df = apply_filters(
        gdf,
        df,
        search_query=search_query,
        categories=selected_categories,
        continents=selected_continents,
        risk_levels=[selected_risk] if selected_risk != "Todos" else None,
    )
    
    # Métricas principais
    stats = get_statistics(filtered_df)
    render_metrics(stats)
    
    # Tabs principais
    tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Mapas", "📊 Análises", "🔍 Detalhes", "ℹ️ Sobre"])
    
    # ========================================================================
    # TAB 1: MAPAS
    # ========================================================================
    with tab1:
        st.subheader("🗺️ Visualizações Geoespaciais")
        st.markdown("Explore a distribuição global de primatas com mapas interativos.")
        
        map_type = st.radio(
            "Selecione o tipo de visualização:",
            [
                "🎨 Mapa Coroplético",
                "🔥 Heatmap de Densidade",
            ],
            horizontal=True,
        )
        
        if map_type == "🎨 Mapa Coroplético":
            st.markdown("#### Distribuição por Categoria IUCN")
            st.info(
                "💡 Clique nos pontos para ver detalhes da espécie. Os clusters se expandem ao dar zoom."
            )
            m = create_choropleth_map(filtered_gdf, filtered_df)
            st_folium(m, width=None, height=700, returned_objects=[])
        
        else:  # Heatmap
            st.markdown("#### Hotspots de Espécies Ameaçadas")
            st.info(
                "💡 Cores mais quentes indicam maior concentração de espécies ameaçadas."
            )
            threatened_count = len(
                filtered_df[filtered_df["risco"].isin(["Alto Risco", "Crítico"])]
            )
            if threatened_count > 0:
                m = create_heatmap_density(filtered_gdf, filtered_df)
                st_folium(m, width=None, height=700, returned_objects=[])
            else:
                st.warning("⚠️ Nenhuma espécie ameaçada encontrada com os filtros atuais.")
    
    # ========================================================================
    # TAB 2: ANÁLISES
    # ========================================================================
    with tab2:
        st.subheader("📊 Análises e Gráficos Estatísticos")
        st.markdown("Visualize tendências e padrões nos dados de conservação.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Distribuição por Categoria IUCN")
            category_counts = get_category_distribution(filtered_df)
            fig_cat = create_category_distribution_chart(category_counts)
            st.plotly_chart(fig_cat, use_container_width=True, config={'responsive': True})
        
        with col2:
            st.markdown("#### Distribuição por Continente")
            continent_counts = get_continent_distribution(filtered_df)
            fig_cont = create_continent_distribution_chart(continent_counts)
            st.plotly_chart(fig_cont, use_container_width=True, config={'responsive': True})
        
        # Gráfico de risco por continente
        st.markdown("#### Espécies Ameaçadas por Continente")
        threatened_by_cont = get_threatened_by_continent(filtered_df)
        
        if len(threatened_by_cont) > 0:
            fig_risk = create_threatened_by_continent_chart(threatened_by_cont)
            st.plotly_chart(fig_risk, use_container_width=True, config={'responsive': True})
        else:
            st.info("ℹ️ Nenhuma espécie ameaçada encontrada com os filtros atuais.")
        
        # Gráfico de nível de risco
        st.markdown("#### Distribuição por Nível de Risco")
        risk_counts = filtered_df["risco"].value_counts()
        fig_risk_level = create_risk_level_chart(risk_counts)
        st.plotly_chart(fig_risk_level, use_container_width=True, config={'responsive': True})
        
        # Comparação de categorias por continente
        st.markdown("#### Comparação: Categorias por Continente")
        fig_comparison = create_category_comparison_chart(filtered_df)
        st.plotly_chart(fig_comparison, use_container_width=True, config={'responsive': True})
    
    # ========================================================================
    # TAB 3: DETALHES
    # ========================================================================
    with tab3:
        st.subheader("🔍 Informações Detalhadas de Espécies")
        
        # Top espécies ameaçadas
        st.markdown("#### 🔴 Top 10 Espécies Mais Ameaçadas")
        top_threatened = get_top_threatened_species(filtered_df, n=10)
        if len(top_threatened) > 0:
            fig_top = create_top_threatened_species_chart(top_threatened)
            st.plotly_chart(fig_top, use_container_width=True, config={'responsive': True})
        else:
            st.info("ℹ️ Nenhuma espécie ameaçada encontrada.")
        
        # Seleção de espécie individual
        st.markdown("---")
        st.markdown("#### Detalhes de Espécie Individual")
        
        species_list = sorted(filtered_df["sci_name"].tolist())
        if species_list:
            selected_species = st.selectbox(
                "Selecione uma espécie:",
                options=species_list,
            )
            
            if selected_species:
                species_details = get_species_details(
                    filtered_df, filtered_gdf, selected_species
                )
                
                if species_details:
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"### {species_details['sci_name']}")
                        render_species_info_table(species_details)
                    
                    with col2:
                        render_species_badge(species_details["category"])
                    
                    # Mapa da espécie
                    st.markdown("#### 📍 Distribuição Geográfica")
                    m_species = create_species_detail_map(
                        filtered_gdf,
                        filtered_df,
                        selected_species,
                        species_details["category"],
                    )
                    st_folium(m_species, width=None, height=500, returned_objects=[])
        else:
            st.warning("⚠️ Nenhuma espécie encontrada com os filtros atuais.")
    
    # ========================================================================
    # TAB 4: SOBRE
    # ========================================================================
    with tab4:
        render_about_section()
    
    # Footer
    render_footer()


if __name__ == "__main__":
    main()
