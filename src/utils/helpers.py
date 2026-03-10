"""
helpers.py — Funciones utilitarias de formato y cálculo.
"""

from __future__ import annotations


def fmt_cop(value: float) -> str:
    """Formatea moneda COP en escala colombiana correcta."""
    abs_val = abs(value)
    if abs_val >= 1_000_000_000_000:
        return f"$ {value / 1_000_000_000_000:.2f} Bill."
    if abs_val >= 1_000_000_000:
        return f"$ {value / 1_000_000_000:.2f} Mil M."
    if abs_val >= 1_000_000:
        return f"$ {value / 1_000_000:.2f} M."
    if abs_val >= 1_000:
        return f"$ {value / 1_000:.2f} K"
    return f"$ {value:,.0f}"

def fmt_number(value: float) -> str:
    """Formatea un número entero con separadores de miles."""
    return f"{value:,.0f}"


def pct_change(base: float, current: float) -> float:
    """
    Calcula el porcentaje de cambio entre base y current.
    Retorna 0.0 si base es cero para evitar división por cero.
    """
    if base == 0:
        return 100.0 if current > 0 else 0.0
    return round((current - base) / base * 100, 1)


def sign(value: float) -> str:
    """Devuelve '+' si el valor es positivo, '' si negativo."""
    return "+" if value >= 0 else ""
