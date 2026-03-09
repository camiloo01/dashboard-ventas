"""
Dashboard de Reportes
Entry point principal de la aplicación Streamlit.
"""

import pandas as pd
import streamlit as st

from src.utils.config import configure_page
from src.utils.data_loader import load_and_clean, detect_columns
from src.utils.filters import render_sidebar_filters, apply_filters
from src.components.kpis import render_kpis
from src.components.charts import render_charts
from src.components.table import render_detail_table
from src.components.export import render_export


def main() -> None:
    configure_page()

    st.markdown("""
        <h1 style='font-family:Syne,sans-serif;font-weight:800;font-size:2rem;color:#e8e8f0;margin-bottom:0'>
            REPORTES<span style='color:#00e5a0'>.</span>
        </h1>
        <p style='color:#6b6b8a;font-size:0.8rem;margin-top:0.3rem'>
            Dashboard de reportes por año
        </p>
    """, unsafe_allow_html=True)

    # ── Cargar archivos desde session_state ──────────────────────────────────
    file_a, file_b = _render_uploaders()

    if not file_a or not file_b:
        st.info("Sube los dos archivos Excel en el panel izquierdo para comenzar.")
        return

    with st.spinner("Cargando y analizando archivos..."):
        df_a = load_and_clean(file_a)
        df_b = load_and_clean(file_b)

    #Filtros (solo se renderizan una vez, con los datos ya cargados)
    period, filters = _render_filters(df_a, df_b)

    fa = apply_filters(df_a, filters)
    fb = apply_filters(df_b, filters)

    st.caption(
        f"Año anterior: **{len(fa):,}** filas | "
        f"Año actual: **{len(fb):,}** filas | "
        f"Filtros activos: **{sum(1 for v in filters.values() if v)}**"
    )

    _show_column_summary(df_a)
    render_kpis(fa, fb)
    render_charts(fa, fb, period)
    table_df = render_detail_table(fa, fb)
    render_export(table_df)


def _render_uploaders():
    """Renderiza los file uploaders en el sidebar. Se llama UNA sola vez."""
    with st.sidebar:
        st.markdown("###Cargar Archivos")
        file_a = st.file_uploader("Año Anterior", type=["xlsx", "xls", "csv"], key="fa")
        file_b = st.file_uploader("Año Actual",   type=["xlsx", "xls", "csv"], key="fb")
    return file_a, file_b


def _render_filters(df_a: pd.DataFrame, df_b: pd.DataFrame):
    """Renderiza periodo y filtros dinámicos en el sidebar. Se llama UNA sola vez."""
    period, filters = render_sidebar_filters(df_a=df_a, df_b=df_b)
    return period, filters


def _show_column_summary(df: pd.DataFrame) -> None:
    col_info = detect_columns(df)
    with st.expander("🔬 Columnas detectadas automáticamente", expanded=False):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown("**📌 Filtros**")
            for c in col_info["filter_cols"]:
                st.markdown(f"- `{c}` ({df[c].nunique()} valores)")
        with c2:
            st.markdown("**📊 Numéricas**")
            for c in col_info["numeric_cols"]:
                st.markdown(f"- `{c}`")
        with c3:
            st.markdown("**📅 Fechas**")
            for c in col_info["date_cols"]:
                st.markdown(f"- `{c}`")
        with c4:
            st.markdown("**🆔 IDs / Texto libre**")
            for c in col_info["id_cols"]:
                st.markdown(f"- `{c}`")


if __name__ == "__main__":
    main()