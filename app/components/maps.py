"""
MÃ³dulo para criaÃ§Ã£o de mapas interativos com Folium.
CÃ³digo simplificado, funcional e bonito com clustering.
"""

import folium
from folium.plugins import HeatMap, MarkerCluster
import geopandas as gpd
import pandas as pd
from typing import Optional, List
import logging

from app.config import (
    IUCN_COLORS,
    IUCN_LABELS,
    MAP_CONFIG,
    HEATMAP_CONFIG,
)

logger = logging.getLogger(__name__)
NOT_INFORMED = "Não informado"


def _display_value(value: object, fallback: str = NOT_INFORMED) -> str:
    if pd.isna(value) or str(value).strip() == "":
        return fallback

    return str(value)


def _add_species_attributes(
    gdf: gpd.GeoDataFrame,
    df: pd.DataFrame,
    columns: List[str],
) -> gpd.GeoDataFrame:
    """Add CSV attributes to a GeoDataFrame without duplicate merge suffixes."""
    if "sci_name" not in gdf.columns or "sci_name" not in df.columns:
        return gdf.copy()

    gdf = gdf.copy()
    available_columns = [column for column in columns if column in df.columns]

    if not available_columns:
        return gdf

    attributes = (
        df[["sci_name", *available_columns]]
        .drop_duplicates(subset=["sci_name"])
        .set_index("sci_name")
    )

    for column in available_columns:
        mapped_values = gdf["sci_name"].map(attributes[column])

        if column in gdf.columns:
            gdf[column] = gdf[column].where(gdf[column].notna(), mapped_values)
        else:
            gdf[column] = mapped_values

    duplicate_suffix_columns = [
        column
        for column in gdf.columns
        if column.endswith("_df") and column[:-3] in available_columns
    ]

    if duplicate_suffix_columns:
        gdf = gdf.drop(columns=duplicate_suffix_columns)

    return gdf


def create_base_map(
    center: Optional[List[float]] = None,
    zoom_start: Optional[int] = None,
    tiles: Optional[str] = None,
) -> folium.Map:
    """Cria um mapa base."""
    center = center or MAP_CONFIG["center"]
    zoom_start = zoom_start or MAP_CONFIG["zoom_start"]
    tiles = tiles or MAP_CONFIG["tiles"]
    
    m = folium.Map(
        location=center,
        zoom_start=zoom_start,
        tiles=None,
        control_scale=MAP_CONFIG["control_scale"],
        prefer_canvas=MAP_CONFIG["prefer_canvas"],
    )

    folium.TileLayer(
        tiles=tiles,
        name="Mapa base",
        control=True,
    ).add_to(m)

    _localize_leaflet_controls(m)
    
    return m


def create_interactive_map(gdf: gpd.GeoDataFrame, df: pd.DataFrame) -> folium.Map:
    """Cria mapa interativo com clustering e popups clicÃ¡veis."""

    if "lat" not in gdf.columns or "lon" not in gdf.columns:
        gdf = gdf.copy()
        gdf["lat"] = gdf.geometry.centroid.y
        gdf["lon"] = gdf.geometry.centroid.x

    gdf = _add_species_attributes(
        gdf,
        df,
        ["category", "category_pt", "risco", "common_name", "continente"],
    )

    gdf_unique = gdf.drop_duplicates(subset=["sci_name"], keep="first")

    logger.info(f"Renderizando {len(gdf_unique)} espÃ©cies")

    m = folium.Map(
        location=MAP_CONFIG["center"],
        zoom_start=MAP_CONFIG["zoom_start"],
        tiles=None,
        control_scale=True,
        prefer_canvas=False,
    )

    folium.TileLayer(
        tiles=MAP_CONFIG["tiles"],
        name="Mapa base",
        control=True,
    ).add_to(m)

    marker_cluster = MarkerCluster(
        name="Espécies de primatas",
        show=True,
    ).add_to(m)

    for _, row in gdf_unique.iterrows():

        if pd.isna(row["lat"]) or pd.isna(row["lon"]):
            continue

        sci_name = _display_value(row.get("sci_name"))

        # Nome comum vindo diretamente da coluna common_name
        common_name = _display_value(row.get("common_name", None))

        category = row.get("category", "NE")
        color = IUCN_COLORS.get(category, "#cccccc")
        category_label = IUCN_LABELS.get(category, NOT_INFORMED)

        risco = _display_value(row.get("risco"))
        continente = _display_value(row.get("continente"))

        html = f"""
        <div style="width:280px;font-family:Arial,sans-serif;">
            <h4 style="
                color:{color};
                margin:0 0 10px 0;
                border-bottom:2px solid {color};
                padding-bottom:8px;
            ">
                {sci_name}
            </h4>

            <p><b>Nome comum:</b> {common_name}</p>
            <p><b>Categoria IUCN:</b> {category_label}</p>
            <p><b>Nível de risco:</b> {risco}</p>
            <p><b>Continente:</b> {continente}</p>
        </div>
        """

        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=8,
            color=color,
            weight=2,
            fill=True,
            fill_color=color,
            fill_opacity=0.85,
            popup=folium.Popup(html, max_width=320),
            tooltip=folium.Tooltip(
                f"{common_name} ({sci_name})",
                sticky=True
            ),
        ).add_to(marker_cluster)

    threatened = gdf[
        gdf["risco"].isin(
            ["Alto Risco", "Crítico"]
        )
    ]

    if not threatened.empty:

        heat_data = [
            [row["lat"], row["lon"]]
            for _, row in threatened.iterrows()
            if pd.notna(row["lat"]) and pd.notna(row["lon"])
        ]

        if heat_data:

            HeatMap(
                heat_data,
                name="Áreas de maior ameaça",
                overlay=True,
                control=True,
                **HEATMAP_CONFIG,
            ).add_to(m)

    folium.LayerControl(
        collapsed=False
    ).add_to(m)

    _add_legend(m)
    _localize_leaflet_controls(m)

    return m


def create_choropleth_map(gdf: gpd.GeoDataFrame, df: pd.DataFrame) -> folium.Map:
    """Cria mapa coroplÃ©tico com clustering bonito."""
    return create_interactive_map(gdf, df)


def create_heatmap_density(gdf: gpd.GeoDataFrame, df: pd.DataFrame) -> folium.Map:
    """Cria heatmap de densidade."""
    
    if "lat" not in gdf.columns or "lon" not in gdf.columns:
        gdf = gdf.copy()
        gdf["lat"] = gdf.geometry.centroid.y
        gdf["lon"] = gdf.geometry.centroid.x
    
    gdf = _add_species_attributes(
        gdf,
        df,
        ["risco"],
    )
    
    m = create_base_map()
    
    # EspÃ©cies ameaÃ§adas
    threatened = gdf[gdf["risco"].isin(["Alto Risco", "Crítico"])]
    
    if len(threatened) > 0:
        heat_data = [
            [row["lat"], row["lon"]]
            for idx, row in threatened.iterrows()
            if pd.notna(row["lat"]) and pd.notna(row["lon"])
        ]
        
        if heat_data:
            HeatMap(
                heat_data,
                name="Densidade de espécies ameaçadas",
                overlay=True,
                control=True,
                **HEATMAP_CONFIG,
            ).add_to(m)
    
    folium.LayerControl().add_to(m)
    _localize_leaflet_controls(m)
    return m


def create_species_detail_map(gdf: gpd.GeoDataFrame, df: pd.DataFrame, species_name: str, category: str) -> folium.Map:
    """Cria mapa de detalhe para uma espÃ©cie."""
    
    gdf = _add_species_attributes(
        gdf,
        df,
        ["category"],
    )
    
    species_gdf = gdf[gdf["sci_name"] == species_name]
    
    if species_gdf.empty:
        return create_base_map()
    
    bounds = species_gdf.total_bounds
    center_lat = (bounds[1] + bounds[3]) / 2
    center_lon = (bounds[0] + bounds[2]) / 2
    
    m = create_base_map(center=[center_lat, center_lon], zoom_start=4)
    
    color = IUCN_COLORS.get(category, "#cccccc")
    
    for idx, row in species_gdf.iterrows():
        folium.GeoJson(
            row.geometry.__geo_interface__,
            style_function=lambda x, color=color: {
                "fillColor": color,
                "color": "#000000",
                "weight": 2,
                "fillOpacity": 0.7,
            },
            popup=f"<b>Espécie:</b> {species_name}",
            name=f"Distribuição de {species_name}",
        ).add_to(m)
    
    folium.LayerControl().add_to(m)
    _localize_leaflet_controls(m)
    return m


def _add_legend(m: folium.Map) -> None:
    """Adiciona legenda."""

    legend_html = """
    <div style="
        position: fixed;
        bottom: 50px;
        left: 50px;
        width: 220px;
        background-color: grey;
        border: 2px solid #333;
        z-index: 1000;
        pointer-events: none;
        font-size: 12px;
        padding: 12px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,.15);
    ">
        <b style="
            font-size:14px;
            display:block;
            margin-bottom:8px;
        ">
            Categorias IUCN
        </b>
    """

    for category, label in IUCN_LABELS.items():

        color = IUCN_COLORS.get(
            category,
            "#cccccc"
        )

        legend_html += f"""
        <div style="margin-bottom:6px;">
            <span style="
                display:inline-block;
                width:16px;
                height:16px;
                background-color:{color};
                border:1px solid #333;
                margin-right:8px;
                border-radius:3px;
            "></span>

            <span>{category} - {label}</span>
        </div>
        """

    legend_html += "</div>"

    m.get_root().html.add_child(
        folium.Element(legend_html)
    )


def _localize_leaflet_controls(m: folium.Map) -> None:
    """Traduz rótulos dos controles padrão do Leaflet."""
    script = """
    <script>
    document.addEventListener("DOMContentLoaded", function () {
        const zoomIn = document.querySelector(".leaflet-control-zoom-in");
        const zoomOut = document.querySelector(".leaflet-control-zoom-out");

        if (zoomIn) {
            zoomIn.title = "Aproximar";
            zoomIn.setAttribute("aria-label", "Aproximar");
        }

        if (zoomOut) {
            zoomOut.title = "Afastar";
            zoomOut.setAttribute("aria-label", "Afastar");
        }
    });
    </script>
    """

    m.get_root().html.add_child(folium.Element(script))

