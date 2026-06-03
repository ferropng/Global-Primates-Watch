"""
Global Primates Watch - Aplicação Streamlit
Análise geoespacial e visualização de primatas ameaçados
"""

__version__ = "3.0.0"
__author__ = "Eduardo Ferro"
__description__ = "Monitoramento global de primatas ameaçados com análise geoespacial"

from . import config
from . import components

__all__ = ["config", "components"]
