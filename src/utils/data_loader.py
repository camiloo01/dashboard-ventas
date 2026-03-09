"""
data_loader.py — Carga y limpieza calibrada para el archivo de ventas.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

MAX_UNIQUE_FOR_FILTER  = 200
MIN_UNIQUE_FOR_NUMERIC = 10

# Columnas que son filtros conocidos
FILTER_COLS = [
    "Fabricante", "Canal", "Region", "Tipo de Venta",
    "Gama", "Contado/Financiado2", "Kit/Post",
    "Descripción Centro", "Ce", "Ref_Template",
]

# Columnas a ignorar
IGNORE_COLS = [
    "Destinatario", "Cuotas", "Nombre solicitante",
    "Expr1016", "Observa_Ref", "Número de serie",
    "Referencia", "Factura",
]


@st.cache_data(show_spinner=False)
def load_and_clean(file) -> pd.DataFrame:
    df = _read_file(file)
    df = _normalize_text(df)
    df = _clean_ingreso(df)
    df = _clean_cantidad(df)
    df = _parse_dates(df)
    return df


@st.cache_data(show_spinner=False)
def detect_columns(df: pd.DataFrame) -> dict:
    present_filters  = [c for c in FILTER_COLS if c in df.columns]
    present_numerics = [c for c in ["Ingreso", "Cantidad"] if c in df.columns]
    present_dates    = [c for c in ["Fecha_doc"] if c in df.columns]
    present_ids      = [c for c in IGNORE_COLS if c in df.columns]

    return {
        "filter_cols":  present_filters,
        "numeric_cols": present_numerics,
        "date_cols":    present_dates,
        "id_cols":      present_ids,
    }


# ── Lectura ───────────────────────────────────────────────────────────────────

def _read_file(file) -> pd.DataFrame:
    if file.name.endswith(".csv"):
        return pd.read_csv(file, low_memory=False)
    try:
        return pd.read_excel(
            file,
            sheet_name="Data",
            engine="calamine",  # mucho mas rapido que openpyxl
            dtype=str
        )
    except Exception:
        # Fallback a openpyxl si calamine falla
        return pd.read_excel(
            file,
            sheet_name="Data",
            engine="openpyxl",
            dtype=str
        )

# ── Ingreso ───────────────────────────────────────────────────────────────────

def _clean_ingreso(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "Ingreso" in df.columns:
        df["_ingreso"] = (
            df["Ingreso"].astype(str)
            .str.replace(r"[\$\s,]", "", regex=True)
            .str.replace(r"\.(?=\d{3}(\D|$))", "", regex=True)
            .pipe(pd.to_numeric, errors="coerce")
            .fillna(0)
        )
    else:
        df["_ingreso"] = 0.0
    return df

def _normalize_text(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza columnas de texto: elimina espacios extra
    y estandariza mayúsculas para evitar duplicados como
    'SAMSUNG' vs 'Samsung' o 'Puntos directos' vs 'PUNTOS DIRECTOS'.
    """
    df = df.copy()
    for col in FILTER_COLS:
        if col in df.columns:
            df[col] = (
                df[col].astype(str)
                .str.strip()                # quita espacios al inicio y final
                .str.title()               # Primera Letra En Mayuscula
            )
    return df


# ── Cantidad ──────────────────────────────────────────────────────────────────

def _clean_cantidad(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "Cantidad" in df.columns:
        df["Cantidad"] = pd.to_numeric(df["Cantidad"], errors="coerce").fillna(1)
    return df


# ── Fechas ────────────────────────────────────────────────────────────────────

def _parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Parsea Fecha_doc en cualquier formato:
      - dd/mm/yyyy  (año anterior)
      - yyyy-mm-dd  (año actual)
    """
    df = df.copy()
    if "Fecha_doc" not in df.columns:
        return df

    df["_fecha"] = pd.to_datetime(df["Fecha_doc"], errors="coerce")

    # Fallback con dayfirst si falló
    mask_failed = df["_fecha"].isna()
    if mask_failed.any():
        df.loc[mask_failed, "_fecha"] = pd.to_datetime(
            df.loc[mask_failed, "Fecha_doc"], dayfirst=True, errors="coerce"
        )

    df["_mes"]    = df["_fecha"].dt.to_period("M").astype(str)
    df["_semana"] = df["_fecha"].dt.to_period("W").astype(str)
    df["_dia"]    = df["_fecha"].dt.date.astype(str)
    return df


# ── Periodo ───────────────────────────────────────────────────────────────────

PERIOD_COL = {"Mensual": "_mes", "Semanal": "_semana", "Diario": "_dia"}

def get_period_col(period: str) -> str:
    return PERIOD_COL.get(period, "_mes")