"""
export.py — Componente de exportación de datos.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st


def render_export(df: pd.DataFrame) -> None:
    """Renderiza el botón de descarga del reporte en CSV."""
    st.markdown('<div class="section-title">⬇️ Exportar</div>', unsafe_allow_html=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Descargar tabla como CSV",
        data=csv,
        file_name="comparativa_ventas.csv",
        mime="text/csv",
    )
