"""
Componentes da aplicação Global Primates Watch.
Inclui mapas, gráficos e componentes de UI.
"""

from .maps import (
    create_base_map,
    create_interactive_map,
    create_choropleth_map,
    create_heatmap_density,
    create_species_detail_map,
)
from .charts import (
    create_category_distribution_chart,
    create_continent_distribution_chart,
    create_threatened_by_continent_chart,
    create_risk_level_chart,
    create_top_threatened_species_chart,
    create_category_comparison_chart,
    create_species_summary_table,
)
from .ui import (
    render_header,
    render_filters,
    render_metrics,
    render_species_badge,
    render_species_info_table,
    render_footer,
    render_about_section,
)

__all__ = [
    # Maps
    "create_base_map",
    "create_interactive_map",
    "create_choropleth_map",
    "create_heatmap_density",
    "create_species_detail_map",
    # Charts
    "create_category_distribution_chart",
    "create_continent_distribution_chart",
    "create_threatened_by_continent_chart",
    "create_risk_level_chart",
    "create_top_threatened_species_chart",
    "create_category_comparison_chart",
    "create_species_summary_table",
    # UI
    "render_header",
    "render_filters",
    "render_metrics",
    "render_species_badge",
    "render_species_info_table",
    "render_footer",
    "render_about_section",
]
