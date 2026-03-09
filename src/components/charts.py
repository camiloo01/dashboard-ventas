"""
charts.py — Componente de gráficos comparativos.
"""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.utils.config import PLOTLY_LAYOUT
from src.utils.data_loader import get_period_col
from src.utils.helpers import pct_change

COLOR_A      = "rgba(123,97,255,0.75)"
COLOR_B      = "rgba(0,229,160,0.75)"
COLOR_A_LINE = "#7b61ff"
COLOR_B_LINE = "#00e5a0"


def render_charts(fa: pd.DataFrame, fb: pd.DataFrame, period: str) -> None:
    _render_timeline(fa, fb, period)
    _render_bar_row(fa, fb, "🗺️ Ventas por Región y Fabricante",
                   [("Region", 10), ("Fabricante", 8)])
    _render_bar_row(fa, fb, "🏪 Tiendas y Gama",
                   [("Descripción Centro", 12), ("Gama", 10)])
    _render_growth_by_region(fa, fb)


# ── Layout base sin yaxis ─────────────────────────────────────────────────────

def _base_layout(**extra):
    """Construye el layout base sin duplicar yaxis."""
    layout = {k: v for k, v in PLOTLY_LAYOUT.items() if k != "yaxis"}
    layout.update(extra)
    return layout


# ── Timeline ──────────────────────────────────────────────────────────────────

def _render_timeline(fa: pd.DataFrame, fb: pd.DataFrame, period: str) -> None:
    st.markdown('<div class="section-title">📊 Evolución de Ingresos</div>', unsafe_allow_html=True)

    col = get_period_col(period)
    if col not in fa.columns:
        st.warning("No se encontró columna de fecha para graficar la evolución.")
        return

    g_a = fa.groupby(col)["_ingreso"].sum().reset_index()
    g_b = fb.groupby(col)["_ingreso"].sum().reset_index()
    g_a.columns = ["periodo", "ingreso"]
    g_b.columns = ["periodo", "ingreso"]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=g_a["periodo"], y=g_a["ingreso"], name="Año Anterior",
        line=dict(color=COLOR_A_LINE, width=2),
        fill="tozeroy", fillcolor="rgba(123,97,255,0.08)"
    ))
    fig.add_trace(go.Scatter(
        x=g_b["periodo"], y=g_b["ingreso"], name="Año Actual",
        line=dict(color=COLOR_B_LINE, width=2),
        fill="tozeroy", fillcolor="rgba(0,229,160,0.08)"
    ))
    fig.update_layout(
        **_base_layout(height=320, hovermode="x unified"),
        yaxis=dict(tickformat=",.0f", gridcolor="#1c1c28")
    )
    st.plotly_chart(fig, width="stretch")


# ── Barras ────────────────────────────────────────────────────────────────────

def _grouped_bar(fa: pd.DataFrame, fb: pd.DataFrame, field: str, top: int) -> go.Figure | None:
    if field not in fa.columns:
        return None

    agg_a = fa.groupby(field)["_ingreso"].sum().nlargest(top)
    agg_b = fb.groupby(field)["_ingreso"].sum()
    keys  = agg_a.index.tolist()

    fig = go.Figure()
    fig.add_bar(
        name="Año Ant.", x=keys,
        y=[agg_a.get(k, 0) for k in keys],
        marker_color=COLOR_A, marker_line_width=0
    )
    fig.add_bar(
        name="Año Act.", x=keys,
        y=[agg_b.get(k, 0) for k in keys],
        marker_color=COLOR_B, marker_line_width=0
    )
    fig.update_layout(
        **_base_layout(height=300, barmode="group"),
        yaxis=dict(tickformat=",.0f", gridcolor="#1c1c28")
    )
    return fig


def _render_bar_row(fa, fb, title: str, fields: list[tuple]) -> None:
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    cols = st.columns(len(fields))
    for col, (field, top) in zip(cols, fields):
        with col:
            fig = _grouped_bar(fa, fb, field, top)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(f"Columna `{field}` no encontrada.")


# ── Crecimiento % ─────────────────────────────────────────────────────────────

def _render_growth_by_region(fa: pd.DataFrame, fb: pd.DataFrame) -> None:
    region_col = _find_col(fa, ["Region", "Zona", "Area"])
    if not region_col:
        return

    st.markdown('<div class="section-title">📉 Crecimiento % por Región</div>', unsafe_allow_html=True)

    reg_a   = fa.groupby(region_col)["_ingreso"].sum()
    reg_b   = fb.groupby(region_col)["_ingreso"].sum()
    regions = sorted(set(reg_a.index) | set(reg_b.index))
    growths = [pct_change(reg_a.get(r, 0), reg_b.get(r, 0)) for r in regions]

    fig = go.Figure(go.Bar(
        x=regions, y=growths,
        marker_color=["#00e5a0" if g >= 0 else "#ff4d6d" for g in growths],
        marker_line_width=0,
        text=[f"{g:+.1f}%" for g in growths],
        textposition="outside",
        textfont=dict(color="#e8e8f0", size=11),
    ))
    fig.update_layout(
        **_base_layout(height=280),
        yaxis=dict(ticksuffix="%", gridcolor="#1c1c28")
    )
    st.plotly_chart(fig, use_container_width=True)


def _find_col(df: pd.DataFrame, candidates: list[str]) -> str | None:
    for c in candidates:
        if c in df.columns:
            return c
    return None