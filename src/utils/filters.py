"""
filters.py — Detección automática de filtros y renderizado del sidebar.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.utils.data_loader import detect_columns

EXCLUDE_FROM_FILTERS = {
    "Factura", "Número de serie", "Expr1016", "Nombre solicitante",
    "Ref_Template", "Referencia", "Observa_Ref", "Entrega",
    "Cuotas", "Destinatario",
}

FilterDict = dict[str, list]


def render_sidebar_filters(df_a: pd.DataFrame, df_b: pd.DataFrame):
    """
    Renderiza periodo y filtros dinámicos en el sidebar.
    Los file uploaders están en app.py — esta función NO los toca.

    Returns: (period, filters_dict)
    """
    with st.sidebar:
        st.markdown("---")
        period = st.radio("📅 Período", ["Mensual", "Semanal", "Diario"], index=0)

        # selector de fecha
        date_filter = _render_date_filter(df_a, df_b)

        st.markdown("---")
        st.markdown("### 🔍 Filtros detectados")
        filters = _build_auto_filters(df_a, df_b)

    return period, filters, date_filter


def _build_auto_filters(df_a: pd.DataFrame, df_b: pd.DataFrame) -> FilterDict:
    combined = pd.concat([df_a, df_b], ignore_index=True)
    col_info = detect_columns(combined)
    filter_cols = [
        c for c in col_info["filter_cols"]
        if c not in EXCLUDE_FROM_FILTERS
    ]

    if not filter_cols:
        st.info("No se detectaron columnas categóricas para filtrar.")
        return {}

    filters: FilterDict = {}
    for col in filter_cols:
        options = _sorted_unique(combined, col)
        if not options:
            continue
        with st.expander(f"📌 {col} ({len(options)} valores)", expanded=_is_priority(col)):
            selected = st.multiselect(
                label=col,
                options=options,
                default=options,
                key=f"filter_{col}",
                label_visibility="collapsed",
            )
            filters[col] = selected

    return filters


def _is_priority(col: str) -> bool:
    priority = {"Region", "Canal", "Fabricante", "Gama", "Tipo de Venta",
                "Descripción Centro", "Contado/Financiado"}
    return col in priority


def apply_filters(df: pd.DataFrame, filters: FilterDict) -> pd.DataFrame:
    if not filters:
        return df
    mask = pd.Series(True, index=df.index)
    for col, values in filters.items():
        if col in df.columns and values is not None:
            mask &= df[col].isin(values)
    return df[mask]

def _render_date_filter(df_a: pd.DataFrame, df_b: pd.DataFrame) -> dict | None:
    """
    Selector de fecha específica para comparar un día del año anterior
    vs un día del año actual.
    """
    st.markdown("---")
    usar_fecha = st.checkbox("📆 Filtrar por día específico", value=False)

    if not usar_fecha:
        return None

    # Detectar rango de fechas disponibles en cada archivo
    fechas_a = pd.to_datetime(df_a["_fecha"], errors="coerce").dropna()
    fechas_b = pd.to_datetime(df_b["_fecha"], errors="coerce").dropna()

    min_a = fechas_a.min().date()
    max_a = fechas_a.max().date()
    min_b = fechas_b.min().date()
    max_b = fechas_b.max().date()

    st.markdown("**Año Anterior:**")
    fecha_a = st.date_input(
        "Selecciona el día",
        value=max_a,
        min_value=min_a,
        max_value=max_a,
        key="fecha_a"
    )

    st.markdown("**Año Actual:**")
    fecha_b = st.date_input(
        "Selecciona el día",
        value=max_b,
        min_value=min_b,
        max_value=max_b,
        key="fecha_b"
    )

    return {"fecha_a": fecha_a, "fecha_b": fecha_b}


def _sorted_unique(df: pd.DataFrame, col: str) -> list:
    return sorted(df[col].dropna().unique().tolist(), key=str)

    