"""
config.py — Configuración global de la página y estilos CSS.
"""

import streamlit as st


def configure_page() -> None:
    st.set_page_config(
        page_title="Dashboard de Ventas",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    _inject_styles()


def _inject_styles() -> None:
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Mono&display=swap');

    html, body, [class*="css"] { font-family: 'DM Mono', monospace; }

    .metric-card {
        background: #13131a;
        border: 1px solid #2a2a3d;
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1rem;
        position: relative;
        overflow: hidden;
    }
    .metric-label  { font-size:.65rem; color:#6b6b8a; text-transform:uppercase; letter-spacing:.12em; margin-bottom:.5rem; }
    .metric-value  { font-family:'Syne',sans-serif; font-size:1.8rem; font-weight:800; color:#e8e8f0; line-height:1; }
    .metric-delta-up   { font-size:.82rem; color:#00e5a0; margin-top:.4rem; }
    .metric-delta-down { font-size:.82rem; color:#ff4d6d; margin-top:.4rem; }
    .metric-sub    { font-size:.68rem; color:#6b6b8a; margin-top:.2rem; }
    .metric-bar    { height:2px; position:absolute; bottom:0; left:0; right:0; }
    .bar-up   { background:#00e5a0; }
    .bar-down { background:#ff4d6d; }

    .section-title {
        font-family:'Syne',sans-serif;
        font-size:1.1rem; font-weight:700;
        color:#e8e8f0;
        margin:1.5rem 0 .8rem;
        padding-bottom:.5rem;
        border-bottom:1px solid #2a2a3d;
    }
    </style>
    """, unsafe_allow_html=True)


# ── Constantes de diseño compartidas ─────────────────────────────────────────
CHART_COLORS = [
    "#00e5a0", "#7b61ff", "#ff4d6d", "#ffd166",
    "#06d6a0", "#118ab2", "#ef476f", "#ffc8dd",
]

PLOTLY_LAYOUT = dict(
    paper_bgcolor="#13131a",
    plot_bgcolor="#13131a",
    font=dict(family="DM Mono", color="#6b6b8a", size=11),
    xaxis=dict(gridcolor="#1c1c28", linecolor="#2a2a3d"),
    yaxis=dict(gridcolor="#1c1c28", linecolor="#2a2a3d"),
    legend=dict(bgcolor="#13131a", bordercolor="#2a2a3d", borderwidth=1),
    margin=dict(l=10, r=10, t=30, b=10),
)