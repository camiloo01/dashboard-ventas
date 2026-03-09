"""
kpis.py — Componente de tarjetas KPI con comparativa año vs año.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.utils.helpers import fmt_cop, fmt_number, pct_change


def render_kpis(fa: pd.DataFrame, fb: pd.DataFrame) -> None:
    st.markdown('<div class="section-title">📈 Indicadores Clave</div>', unsafe_allow_html=True)
    metrics = _compute_metrics(fa, fb)
    cols = st.columns(4)
    for col, m in zip(cols, metrics):
        with col:
            _metric_card(**m)


# ── Cálculo ──────────────────────────────────────────────────────────────────

def _get_cantidad(df: pd.DataFrame) -> pd.Series:
    """
    Busca la columna de cantidad de forma flexible.
    Si no existe ninguna, retorna una serie de unos.
    """
    candidates = ["Cantidad", "cantidad", "Qty", "Units", "units", "Unidades"]
    for c in candidates:
        if c in df.columns:
            return pd.to_numeric(df[c], errors="coerce").fillna(1)
    # Fallback: contar filas como unidades
    return pd.Series(1, index=df.index)


def _compute_metrics(fa: pd.DataFrame, fb: pd.DataFrame) -> list[dict]:
    tot_a = fa["_ingreso"].sum()
    tot_b = fb["_ingreso"].sum()
    uni_a = _get_cantidad(fa).sum()
    uni_b = _get_cantidad(fb).sum()
    ticket_a = tot_a / uni_a if uni_a else 0
    ticket_b = tot_b / uni_b if uni_b else 0
    tiendas_col = _find_col(fa, ["Descripción Centro", "Tienda", "Centro", "Sucursal", "Punto de Venta"])
    tiendas_a = fa[tiendas_col].nunique() if tiendas_col else 0
    tiendas_b = fb[tiendas_col].nunique() if tiendas_col else 0

    return [
        dict(label="Ingresos Totales",  val_a=tot_a,     val_b=tot_b,     fmt=fmt_cop),
        dict(label="Unidades Vendidas", val_a=uni_a,     val_b=uni_b,     fmt=fmt_number),
        dict(label="Ticket Promedio",   val_a=ticket_a,  val_b=ticket_b,  fmt=fmt_cop),
        dict(label="Tiendas Activas",   val_a=tiendas_a, val_b=tiendas_b, fmt=lambda v: str(int(v))),
    ]


def _find_col(df: pd.DataFrame, candidates: list[str]) -> str | None:
    """Retorna la primera columna que exista en el DataFrame."""
    for c in candidates:
        if c in df.columns:
            return c
    return None


# ── Renderizado ──────────────────────────────────────────────────────────────

def _metric_card(label: str, val_a: float, val_b: float, fmt) -> None:
    delta = pct_change(val_a, val_b)
    is_up = delta >= 0
    arrow       = "▲" if is_up else "▼"
    delta_class = "metric-delta-up" if is_up else "metric-delta-down"
    bar_class   = "bar-up" if is_up else "bar-down"

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{fmt(val_b)}</div>
        <div class="{delta_class}">{arrow} {abs(delta)}% vs año anterior</div>
        <div class="metric-sub">Año ant.: {fmt(val_a)}</div>
        <div class="metric-bar {bar_class}"></div>
    </div>
    """, unsafe_allow_html=True)