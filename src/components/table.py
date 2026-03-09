"""
table.py — Componente de tabla detallada.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.utils.helpers import pct_change, sign

# Columnas preferidas para agrupar la tabla
GROUP_CANDIDATES = ["Fabricante", "Marca", "Proveedor", "Producto", "Categoría"]


def render_detail_table(fa: pd.DataFrame, fb: pd.DataFrame) -> pd.DataFrame:
    group_col = _find_col(fa, GROUP_CANDIDATES)

    if not group_col:
        st.warning("No se encontró columna de agrupación para la tabla.")
        return pd.DataFrame()

    st.markdown(f'<div class="section-title">📋 Detalle por {group_col}</div>', unsafe_allow_html=True)
    df = _build_table(fa, fb, group_col)
    _display(df)
    return df


def _build_table(fa: pd.DataFrame, fb: pd.DataFrame, group_col: str) -> pd.DataFrame:
    cant_col = _find_col(fa, ["Cantidad", "cantidad", "Qty", "Units"])

    agg_dict = {"ingreso": ("_ingreso", "sum")}
    if cant_col:
        agg_dict["cant"] = (cant_col, "sum")

    agg_a = fa.groupby(group_col).agg(**agg_dict)
    agg_b = fb.groupby(group_col).agg(**agg_dict)
    items = sorted(set(agg_a.index) | set(agg_b.index))

    rows = []
    for item in items:
        ia = agg_a.loc[item, "ingreso"] if item in agg_a.index else 0
        ib = agg_b.loc[item, "ingreso"] if item in agg_b.index else 0
        ca = agg_a.loc[item, "cant"]    if (cant_col and item in agg_a.index) else "-"
        cb = agg_b.loc[item, "cant"]    if (cant_col and item in agg_b.index) else "-"
        dp = pct_change(ia, ib)

        rows.append({
            group_col:       item,
            "Ing. Año Ant.": f"$ {ia:,.0f}",
            "Ing. Año Act.": f"$ {ib:,.0f}",
            "Variación $":   f"{sign(ib - ia)}$ {ib - ia:,.0f}",
            "Variación %":   f"{sign(dp)}{dp}%",
            "Unid. Ant.": str(int(ca)) if ca != "-" else "-",
            "Unid. Act.": str(int(cb)) if cb != "-" else "-",
        })

    return pd.DataFrame(rows).sort_values("Ing. Año Act.", ascending=False).reset_index(drop=True)


def _display(df: pd.DataFrame) -> None:
    var_cols = [c for c in ["Variación $", "Variación %"] if c in df.columns]
    styled = df.style.map(_color_delta, subset=var_cols)
    st.dataframe(styled, use_container_width=True, hide_index=True, height=400)


def _color_delta(val: str) -> str:
    return "color: #00e5a0" if "+" in str(val) else "color: #ff4d6d"


def _find_col(df: pd.DataFrame, candidates: list[str]) -> str | None:
    for c in candidates:
        if c in df.columns:
            return c
    return None