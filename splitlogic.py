# PROYEK 2: SplitLogic

# ─────────────────────────────────────────────
#  LIBRARY
# ─────────────────────────────────────────────

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
from PIL import Image

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
logo_path = "assets/splitlogic.png"
try:
    logo = Image.open(logo_path)
    st.set_page_config(layout="wide", page_title="SplitLogic", page_icon=logo)
except FileNotFoundError:
    st.set_page_config(layout="wide", page_title="SplitLogic", page_icon="⚡")
    logo = None

# ─────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

  /* ── Root & Background ── */
  :root {
    --amber:   #E8963C;
    --amber-d: #C47420;
    --amber-l: #F5B96B;
    --navy:    #0D1B2A;
    --navy-2:  #12243A;
    --navy-3:  #1A3050;
    --slate:   #2C4A6E;
    --text:    #E8EEF4;
    --muted:   #8BA3BC;
    --card-bg: rgba(18, 36, 58, 0.85);
    --border:  rgba(232, 150, 60, 0.18);
    --radius:  12px;
  }

  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
  }

  /* dark background with subtle grid */
  .stApp {
    background:
      linear-gradient(rgba(232,150,60,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(232,150,60,0.03) 1px, transparent 1px),
      linear-gradient(160deg, #0D1B2A 0%, #12243A 50%, #0D1B2A 100%);
    background-size: 48px 48px, 48px 48px, 100% 100%;
  }

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {
    background: var(--navy-2) !important;
    border-right: 1px solid var(--border) !important;
  }
  [data-testid="stSidebar"] .stSelectbox label,
  [data-testid="stSidebar"] .stNumberInput label,
  [data-testid="stSidebar"] .stRadio label,
  [data-testid="stSidebar"] p,
  [data-testid="stSidebar"] span {
    color: var(--text) !important;
  }

  /* ── Headers ── */
  h1, h2, h3, h4 {
    font-family: 'Syne', sans-serif !important;
    color: var(--text) !important;
  }

  /* ── Metric cards ── */
  [data-testid="stMetric"] {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px 24px !important;
    backdrop-filter: blur(8px);
  }
  [data-testid="stMetric"] label {
    color: var(--muted) !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }
  [data-testid="stMetricValue"] {
    color: var(--amber) !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
  }
  [data-testid="stMetricDelta"] { color: var(--amber-l) !important; }

  /* ── Dataframe ── */
  [data-testid="stDataFrame"] {
    border-radius: var(--radius);
    border: 1px solid var(--border);
  }

  /* ── Selectbox / Number input ── */
  .stSelectbox > div > div,
  .stNumberInput > div > div > input {
    background: var(--navy-3) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
  }
  .stSelectbox > div > div:hover,
  .stNumberInput > div > div > input:focus {
    border-color: var(--amber) !important;
  }

  /* ── Buttons ── */
  .stButton > button {
    background: linear-gradient(135deg, var(--amber), var(--amber-d)) !important;
    color: #0D1B2A !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 2rem !important;
    letter-spacing: 0.04em;
    transition: transform 0.15s, box-shadow 0.15s !important;
  }
  .stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(232,150,60,0.35) !important;
  }

  /* ── Divider ── */
  hr { border-color: var(--border) !important; }

  /* ── Tabs ── */
  .stTabs [data-baseweb="tab-list"] {
    background: var(--navy-2);
    border-radius: var(--radius) var(--radius) 0 0;
    gap: 4px;
    padding: 6px 8px;
  }
  .stTabs [data-baseweb="tab"] {
    background: transparent;
    color: var(--muted) !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif;
    font-weight: 600;
  }
  .stTabs [aria-selected="true"] {
    background: var(--amber) !important;
    color: #0D1B2A !important;
  }

  /* ── Expander ── */
  [data-testid="stExpander"] {
    background: var(--card-bg);
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
  }
  [data-testid="stExpander"] summary {
    color: var(--text) !important;
    font-family: 'Syne', sans-serif;
    font-weight: 600;
  }

  /* ── Info / Success box ── */
  .stAlert {
    border-radius: var(--radius) !important;
  }

  /* ── Radio ── */
  .stRadio label { color: var(--text) !important; }
  .stRadio [data-baseweb="radio"] div {
    border-color: var(--amber) !important;
  }

  /* ── Custom card helper ── */
  .sl-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 24px;
    backdrop-filter: blur(8px);
    margin-bottom: 16px;
  }
  .sl-section-tag {
    display: inline-block;
    background: rgba(232,150,60,0.15);
    color: var(--amber);
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 4px;
    margin-bottom: 10px;
  }
  .sl-result-bar {
    height: 10px;
    border-radius: 5px;
    background: linear-gradient(90deg, #1A3050, #0D1B2A);
    margin: 8px 0;
    overflow: hidden;
  }
  .sl-result-bar-fill-gov {
    height: 100%;
    background: linear-gradient(90deg, #2C4A6E, #3A6090);
    border-radius: 5px 0 0 5px;
    transition: width 1s ease;
  }
  .hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2rem, 4vw, 3.2rem);
    font-weight: 800;
    letter-spacing: -0.02em;
    line-height: 1.1;
    color: #E8EEF4;
  }
  .hero-sub {
    font-size: 0.9rem;
    color: var(--muted);
    line-height: 1.6;
    margin-top: 8px;
  }
  .badge {
    display: inline-block;
    background: rgba(232,150,60,0.12);
    border: 1px solid rgba(232,150,60,0.3);
    color: var(--amber-l);
    font-size: 0.72rem;
    font-family: 'Syne', sans-serif;
    font-weight: 600;
    letter-spacing: 0.08em;
    padding: 3px 10px;
    border-radius: 20px;
    margin-right: 6px;
  }
  .footer-text {
    font-size: 0.75rem;
    color: var(--muted);
    text-align: center;
    padding: 32px 0 16px;
    border-top: 1px solid var(--border);
    margin-top: 40px;
  }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  GROSS SPLIT CALCULATION ENGINE
# ─────────────────────────────────────────────

BASE_SPLIT = {
    "Minyak Bumi": {"gov": 57.0, "cont": 43.0},
    "Gas Bumi":    {"gov": 52.0, "cont": 48.0},
}

def calc_field_status(status: str) -> float:
    return {"POD I": 5.0, "POD II": 3.0, "No POD": 0.0}.get(status, 0.0)

def calc_field_location(depth_m: float, is_offshore: bool) -> float:
    if not is_offshore:
        return 0.0
    if depth_m <= 20:   return 8.0
    if depth_m <= 50:   return 10.0
    if depth_m <= 150:  return 12.0
    if depth_m <= 1000: return 14.0
    return 16.0

def calc_reservoir_depth(depth_m: float) -> float:
    return 1.0 if depth_m > 2500 else 0.0

def calc_infrastructure(infra: str) -> float:
    return {"Well Developed": 0.0, "New Frontier Offshore": 2.0, "New Frontier Onshore": 4.0}.get(infra, 0.0)

def calc_reservoir_type(rtype: str) -> float:
    return {"Konvensional (Sandstone / Limestone / Carbonate)": 0.0,
            "Non-Konvensional (Shale / CBM)": 15.0}.get(rtype, 0.0)

def calc_co2(pct: float) -> float:
    if pct < 5:   return 0.0
    if pct < 10:  return 0.5
    if pct < 20:  return 1.0
    if pct < 40:  return 1.5
    if pct < 60:  return 2.0
    return 4.0

def calc_h2s(ppm: float) -> float:
    if ppm < 100:   return 0.0
    if ppm < 1000:  return 1.0
    if ppm < 2000:  return 2.0
    if ppm < 3000:  return 3.0
    if ppm < 4000:  return 4.0
    return 5.0

def calc_sg(api: float) -> float:
    return 1.0 if api < 25 else 0.0

def calc_tkdn(pct: float) -> float:
    if pct < 30:  return 0.0
    if pct < 50:  return 2.0
    if pct < 70:  return 3.0
    return 4.0

def calc_prod_stage(stage: str) -> float:
    return {"Primary": 0.0,
            "Sekunder (Injeksi Air / Gas)": 6.0,
            "Tersier (EOR)": 10.0}.get(stage, 0.0)

# Progressive components
def calc_oil_price(icp: float) -> float:
    if icp >= 85:  return 0.0
    return (85 - icp) * 0.25

def calc_gas_price(price: float) -> float:
    if price < 7:   return (7 - price) * 2.5
    if price < 10:  return 0.0
    return (price - 10) * 2.5

def calc_nett_prod(mmboe: float) -> float:
    if mmboe < 30:   return 10.0
    if mmboe < 60:   return 9.0
    if mmboe < 90:   return 8.0
    if mmboe < 125:  return 6.0
    if mmboe < 175:  return 4.0
    return 0.0

def calculate_gross_split(params: dict) -> dict:
    """Main calculation function. Returns full breakdown dict."""

    commodity  = params["commodity"]
    base       = BASE_SPLIT[commodity]

    # ── Fixed components ──
    fc = {
        "Status Lapangan":        calc_field_status(params["field_status"]),
        "Lokasi Lapangan":        calc_field_location(params["water_depth"], params["is_offshore"]),
        "Kedalaman Reservoir":    calc_reservoir_depth(params["reservoir_depth"]),
        "Infrastruktur":          calc_infrastructure(params["infrastructure"]),
        "Jenis Reservoir":        calc_reservoir_type(params["reservoir_type"]),
        "Kandungan CO₂":          calc_co2(params["co2_pct"]),
        "Kandungan H₂S":          calc_h2s(params["h2s_ppm"]),
        "SG (API)":               calc_sg(params["api"]),
        "TKDN":                   calc_tkdn(params["tkdn_pct"]),
        "Tahapan Produksi":       calc_prod_stage(params["prod_stage"]),
    }

    # ── Progressive components ──
    pc = {}
    if commodity == "Minyak Bumi":
        pc["Harga Minyak (ICP)"] = calc_oil_price(params.get("icp_price", 85))
    else:
        pc["Harga Gas Bumi"]     = calc_gas_price(params.get("gas_price", 8))

    pc["Kumulatif Produksi (MMBOE)"] = calc_nett_prod(params["nett_prod"])

    # ── Ministerial discretion (Pasal 7) ──
    ministerial = params.get("ministerial_adj", 0.0)

    total_correction = sum(fc.values()) + sum(pc.values()) + ministerial

    final_cont = base["cont"] + total_correction
    final_gov  = 100.0 - final_cont

    return {
        "commodity":       commodity,
        "base_gov":        base["gov"],
        "base_cont":       base["cont"],
        "fixed_comps":     fc,
        "progressive_comps": pc,
        "ministerial_adj": ministerial,
        "total_correction": total_correction,
        "final_cont":      final_cont,
        "final_gov":       final_gov,
    }


# ─────────────────────────────────────────────
#  PLOTLY CHARTS
# ─────────────────────────────────────────────

AMBER = "#E8963C"
NAVY  = "#1A3050"
SLATE = "#2C4A6E"
MUTED = "#8BA3BC"
BG    = "rgba(0,0,0,0)"
PAPER = "rgba(18,36,58,0.0)"

def plotly_layout(title="", height=380):
    return dict(
        title=dict(text=title, font=dict(family="Syne", size=14, color="#E8EEF4")),
        height=height,
        plot_bgcolor=BG,
        paper_bgcolor=PAPER,
        font=dict(family="DM Sans", color="#8BA3BC"),
        margin=dict(l=16, r=16, t=40, b=16),
        legend=dict(
            bgcolor="rgba(13,27,42,0.7)",
            bordercolor="rgba(232,150,60,0.2)",
            borderwidth=1,
            font=dict(size=11, color="#E8EEF4"),
        ),
    )

def donut_chart(gov_pct: float, cont_pct: float, label: str = "Final Split"):
    fig = go.Figure(go.Pie(
        labels=["Pemerintah", "Kontraktor"],
        values=[round(gov_pct, 4), round(cont_pct, 4)],
        hole=0.65,
        marker=dict(
            colors=[SLATE, AMBER],
            line=dict(color="rgba(13,27,42,1)", width=3),
        ),
        textfont=dict(family="Syne", size=13, color="#E8EEF4"),
        hovertemplate="<b>%{label}</b><br>%{value:.2f}%<extra></extra>",
    ))
    fig.add_annotation(
        text=f"<b>{label}</b>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(family="Syne", size=12, color=MUTED),
        align="center",
    )
    fig.update_layout(**plotly_layout(height=320))
    return fig

def waterfall_chart(result: dict):
    labels = (
        ["Base (Kontraktor)"]
        + list(result["fixed_comps"].keys())
        + list(result["progressive_comps"].keys())
        + (["Diskresi Menteri"] if result["ministerial_adj"] != 0 else [])
        + ["Final (Kontraktor)"]
    )
    values = (
        [result["base_cont"]]
        + list(result["fixed_comps"].values())
        + list(result["progressive_comps"].values())
        + ([result["ministerial_adj"]] if result["ministerial_adj"] != 0 else [])
        + [result["final_cont"]]
    )
    measure = (
        ["absolute"]
        + ["relative"] * (len(labels) - 2)
        + ["total"]
    )
    colors = []
    for i, (m, v) in enumerate(zip(measure, values)):
        if m == "absolute":   colors.append(SLATE)
        elif m == "total":    colors.append(AMBER)
        else:                 colors.append("#5DA897" if v >= 0 else "#C05050")

    fig = go.Figure(go.Waterfall(
        orientation="v",
        measure=measure,
        x=labels,
        y=values,
        text=[f"{v:+.2f}%" if m == "relative" else f"{v:.2f}%" for m, v in zip(measure, values)],
        textposition="outside",
        textfont=dict(family="DM Sans", size=10, color="#E8EEF4"),
        connector=dict(line=dict(color=MUTED, width=1, dash="dot")),
        increasing=dict(marker=dict(color="#5DA897")),
        decreasing=dict(marker=dict(color="#C05050")),
        totals=dict(marker=dict(color=AMBER)),
        hovertemplate="<b>%{x}</b><br>%{y:.4f}%<extra></extra>",
    ))
    fig.update_layout(
        **plotly_layout("Waterfall – Koreksi Split Kontraktor", height=440),
        xaxis=dict(tickangle=-35, tickfont=dict(size=10, color=MUTED), gridcolor="rgba(255,255,255,0.04)"),
        yaxis=dict(title="Split Kontraktor (%)", gridcolor="rgba(255,255,255,0.04)"),
        showlegend=False,
    )
    return fig

def bar_comparison(result: dict):
    cats = list(result["fixed_comps"].keys()) + list(result["progressive_comps"].keys())
    if result["ministerial_adj"] != 0:
        cats.append("Diskresi Menteri")
    vals = (list(result["fixed_comps"].values())
            + list(result["progressive_comps"].values())
            + ([result["ministerial_adj"]] if result["ministerial_adj"] != 0 else []))

    colors = [AMBER if v > 0 else "#C05050" for v in vals]

    fig = go.Figure(go.Bar(
        x=cats, y=vals,
        marker=dict(color=colors, line=dict(color="rgba(0,0,0,0.3)", width=1)),
        text=[f"{v:+.2f}%" for v in vals],
        textposition="outside",
        textfont=dict(family="DM Sans", size=10, color="#E8EEF4"),
        hovertemplate="<b>%{x}</b><br>Koreksi: %{y:.4f}%<extra></extra>",
    ))
    fig.update_layout(
        **plotly_layout("Koreksi per Komponen (% Split Kontraktor)", height=400),
        xaxis=dict(tickangle=-35, tickfont=dict(size=10, color=MUTED), gridcolor="rgba(255,255,255,0.04)"),
        yaxis=dict(title="Koreksi (%)", gridcolor="rgba(255,255,255,0.04)"),
        showlegend=False,
    )
    return fig


# ─────────────────────────────────────────────
#  SIDEBAR – INPUT PARAMETERS
# ─────────────────────────────────────────────

with st.sidebar:
    # ── Logo ──
    logo_path = os.path.join("assets", "splitlogic.png")
    if os.path.exists(logo_path):
        st.image(logo_path, use_column_width=True)
    else:
        st.markdown("""
        <div style="text-align:center;padding:20px 0 8px;">
          <span style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;
                       color:#E8963C;letter-spacing:-0.02em;">⚡ SplitLogic</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;margin-bottom:24px;">
      <span class="badge">TM3203</span>
      <span class="badge">ITB</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Commodity ──
    st.markdown('<div class="sl-section-tag">Komoditas</div>', unsafe_allow_html=True)
    commodity = st.radio("Jenis Komoditas", ["Minyak Bumi", "Gas Bumi"], horizontal=True)

    st.markdown("---")
    st.markdown('<div class="sl-section-tag">Fixed Components</div>', unsafe_allow_html=True)

    field_status = st.selectbox(
        "1 · Status Lapangan (Field Status)",
        ["No POD", "POD I", "POD II"],
    )

    is_offshore = st.radio("Lokasi Lapangan", ["Onshore", "Offshore"], horizontal=True) == "Offshore"

    water_depth = 0.0
    if is_offshore:
        water_depth = st.number_input(
            "2 · Kedalaman Air (m)", min_value=0.0, value=30.0, step=1.0,
            help="Kedalaman air laut dalam meter"
        )
    else:
        st.markdown("**2 · Lokasi:** Onshore → Koreksi **0%**")

    reservoir_depth = st.number_input(
        "3 · Kedalaman Reservoir (m)", min_value=0.0, value=2600.0, step=50.0,
        help="> 2500 m → +1%"
    )

    infrastructure = st.selectbox(
        "4 · Infrastruktur",
        ["Well Developed", "New Frontier Offshore", "New Frontier Onshore"],
    )

    reservoir_type = st.selectbox(
        "5 · Jenis Reservoir",
        ["Konvensional (Sandstone / Limestone / Carbonate)",
         "Non-Konvensional (Shale / CBM)"],
    )

    co2_pct = st.number_input(
        "6 · Kandungan CO₂ (%)", min_value=0.0, max_value=100.0, value=5.0, step=0.5
    )

    h2s_ppm = st.number_input(
        "7 · Kandungan H₂S (ppm)", min_value=0.0, value=50.0, step=10.0
    )

    api = st.number_input(
        "8 · Specific Gravity (°API)", min_value=0.0, max_value=70.0, value=30.0, step=0.5
    )

    tkdn_pct = st.number_input(
        "9 · TKDN (%)", min_value=0.0, max_value=100.0, value=55.0, step=1.0
    )

    prod_stage = st.selectbox(
        "10 · Tahapan Produksi",
        ["Primary", "Sekunder (Injeksi Air / Gas)", "Tersier (EOR)"],
    )

    st.markdown("---")
    st.markdown('<div class="sl-section-tag">Progressive Components</div>', unsafe_allow_html=True)

    if commodity == "Minyak Bumi":
        icp_price = st.number_input(
            "11 · Harga Minyak ICP (US$/BBL)", min_value=0.0, value=75.0, step=1.0,
            help="< 85: koreksi = (85 − ICP) × 0.25%"
        )
        gas_price = 8.0
    else:
        gas_price = st.number_input(
            "11 · Harga Gas Bumi (US$/MMBTU)", min_value=0.0, value=7.0, step=0.1,
            help="< 7: (7−x)×2.5% | 7–10: 0% | >10: (x−10)×2.5%"
        )
        icp_price = 85.0

    nett_prod = st.number_input(
        "12 · Kumulatif Produksi (MMBOE)", min_value=0.0, value=25.0, step=1.0
    )

    st.markdown("---")
    st.markdown('<div class="sl-section-tag">Pasal 7 – Diskresi Menteri</div>', unsafe_allow_html=True)
    ministerial_adj = st.number_input(
        "Tambahan / Pengurangan Split Kontraktor (%)",
        value=0.0, step=0.5,
        help="Positif = tambahan untuk Kontraktor | Negatif = tambahan untuk Negara"
    )

    st.markdown("---")
    calc_btn = st.button("Hitung Gross Split", use_container_width=True)


# ─────────────────────────────────────────────
#  MAIN AREA
# ─────────────────────────────────────────────

# ── Hero ──
col_logo, col_hero = st.columns([1, 4])
with col_logo:
    if os.path.exists(logo_path):
        st.image(logo_path, width=110)
    else:
        st.markdown(
            '<div style="font-size:4rem;text-align:center;padding-top:8px;">⚡</div>',
            unsafe_allow_html=True,
        )
with col_hero:
    st.markdown("""
    <div class="hero-title">SplitLogic</div>
    <div class="hero-sub">
      Kalkulator Bagi Hasil <strong style="color:#E8963C">Gross Split</strong> — Permen ESDM No. 8 Tahun 2017<br>
      <span class="badge" style="margin-top:8px;display:inline-block;">TM3203 · Manajemen & Keekonomian Proyek</span>
      <span class="badge">Teknik Perminyakan ITB</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────────
tab_calc, tab_ref, tab_about = st.tabs(["Kalkulator", "Tabel Referensi", "Tentang"])

# ══════════════════════════════════════════════
#  TAB 1 – KALKULATOR
# ══════════════════════════════════════════════
with tab_calc:
    if not calc_btn:
        st.markdown("""
        <div class="sl-card" style="text-align:center;padding:48px 24px;">
          <div style="font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:700;
                      color:#E8EEF4;margin-bottom:8px;">
            SplitLogic
          </div>
          <div style="color:#8BA3BC;font-size:0.9rem;max-width:480px;margin:0 auto;">
            Isi seluruh parameter di sidebar kiri, lalu klik
            <strong style="color:#E8963C">Hitung Gross Split</strong> untuk memulai kalkulasi.
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        params = dict(
            commodity=commodity,
            field_status=field_status,
            is_offshore=is_offshore,
            water_depth=water_depth,
            reservoir_depth=reservoir_depth,
            infrastructure=infrastructure,
            reservoir_type=reservoir_type,
            co2_pct=co2_pct,
            h2s_ppm=h2s_ppm,
            api=api,
            tkdn_pct=tkdn_pct,
            prod_stage=prod_stage,
            icp_price=icp_price,
            gas_price=gas_price,
            nett_prod=nett_prod,
            ministerial_adj=ministerial_adj,
        )
        res = calculate_gross_split(params)

        # ── Alert if final > 100 or < 0 ──
        if res["final_cont"] > 100 or res["final_gov"] < 0:
            st.warning("⚠️ Split Kontraktor melebihi 100% — periksa kembali input parameter.")
        elif res["final_gov"] < 0:
            st.warning("⚠️ Split Pemerintah bernilai negatif — periksa kembali input parameter.")

        # ── KPI Row ──
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Base Split – Kontraktor", f"{res['base_cont']:.2f}%", f"Komoditas: {commodity}")
        k2.metric("Total Koreksi", f"+{res['total_correction']:.4f}%",
                  f"{len(res['fixed_comps'])} fixed + {len(res['progressive_comps'])} progressive")
        k3.metric("Final – Kontraktor", f"{res['final_cont']:.4f}%",
                  f"+{res['total_correction']:.4f}% dari base")
        k4.metric("Final – Pemerintah", f"{res['final_gov']:.4f}%",
                  f"{res['base_gov']:.0f}% base")

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Charts Row ──
        c_donut, c_bar = st.columns([1, 2])
        with c_donut:
            st.plotly_chart(
                donut_chart(res["final_gov"], res["final_cont"]),
                use_container_width=True,
            )
        with c_bar:
            st.plotly_chart(bar_comparison(res), use_container_width=True)

        # ── Waterfall ──
        st.plotly_chart(waterfall_chart(res), use_container_width=True)

        # ── Breakdown Table ──
        st.markdown("###Rincian Komponen")
        rows = []
        for comp, val in res["fixed_comps"].items():
            rows.append({"Komponen": comp, "Tipe": "Fixed", "Koreksi Split Kontraktor (%)": f"+{val:.2f}%"})
        for comp, val in res["progressive_comps"].items():
            rows.append({"Komponen": comp, "Tipe": "Progressive", "Koreksi Split Kontraktor (%)": f"+{val:.4f}%"})
        if res["ministerial_adj"] != 0:
            rows.append({
                "Komponen": "Diskresi Menteri (Pasal 7)",
                "Tipe": "Ministerial",
                "Koreksi Split Kontraktor (%)": f"{res['ministerial_adj']:+.2f}%",
            })

        df = pd.DataFrame(rows)
        df.index = df.index + 1
        st.dataframe(df, use_container_width=True)

        # ── Summary Box ──
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="sl-card" style="border-color:rgba(232,150,60,0.4);">
          <div class="sl-section-tag">Ringkasan Final</div>
          <table style="width:100%;border-collapse:collapse;margin-top:12px;">
            <thead>
              <tr style="border-bottom:1px solid rgba(232,150,60,0.2);">
                <th style="text-align:left;padding:8px 0;font-family:'Syne',sans-serif;
                           font-size:0.75rem;letter-spacing:0.1em;text-transform:uppercase;
                           color:#8BA3BC;">Parameter</th>
                <th style="text-align:right;padding:8px 0;font-family:'Syne',sans-serif;
                           font-size:0.75rem;letter-spacing:0.1em;text-transform:uppercase;
                           color:#8BA3BC;">Pemerintah</th>
                <th style="text-align:right;padding:8px 0;font-family:'Syne',sans-serif;
                           font-size:0.75rem;letter-spacing:0.1em;text-transform:uppercase;
                           color:#8BA3BC;">Kontraktor</th>
              </tr>
            </thead>
            <tbody>
              <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                <td style="padding:10px 0;color:#8BA3BC;">Base Split</td>
                <td style="text-align:right;padding:10px 0;">{res['base_gov']:.2f}%</td>
                <td style="text-align:right;padding:10px 0;">{res['base_cont']:.2f}%</td>
              </tr>
              <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                <td style="padding:10px 0;color:#8BA3BC;">Total Koreksi</td>
                <td style="text-align:right;padding:10px 0;color:#8BA3BC;">−{res['total_correction']:.4f}%</td>
                <td style="text-align:right;padding:10px 0;color:#5DA897;">+{res['total_correction']:.4f}%</td>
              </tr>
              <tr>
                <td style="padding:12px 0;font-family:'Syne',sans-serif;font-weight:700;font-size:1rem;">
                  Final Split
                </td>
                <td style="text-align:right;padding:12px 0;font-family:'Syne',sans-serif;
                           font-weight:700;font-size:1.2rem;color:#2C6EA3;">
                  {res['final_gov']:.4f}%
                </td>
                <td style="text-align:right;padding:12px 0;font-family:'Syne',sans-serif;
                           font-weight:800;font-size:1.4rem;color:#E8963C;">
                  {res['final_cont']:.4f}%
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  TAB 2 – TABEL REFERENSI
# ══════════════════════════════════════════════
with tab_ref:
    st.markdown("###Tabel Komponen Gross Split")
    st.markdown("Berdasarkan **Peraturan Menteri ESDM No. 8 Tahun 2017** tentang Kontrak Bagi Hasil Gross Split.")

    # Base split
    with st.expander("Base Split", expanded=True):
        st.dataframe(pd.DataFrame({
            "Komoditas":          ["Minyak Bumi", "Gas Bumi"],
            "Pemerintah (%)":     [57, 52],
            "Kontraktor (%)":     [43, 48],
        }), use_container_width=True, hide_index=True)

    # Fixed components tables
    with st.expander("Fixed Components (10 Komponen)", expanded=False):
        tables = {
            "1. Field Status": pd.DataFrame({
                "Parameter": ["POD I", "POD II", "No POD"],
                "Koreksi Kontrak. (%)": [5, 3, 0],
            }),
            "2. Lokasi Lapangan": pd.DataFrame({
                "Parameter": [
                    "Onshore",
                    "Offshore (0 < h ≤ 20 m)",
                    "Offshore (20 < h ≤ 50 m)",
                    "Offshore (50 < h ≤ 150 m)",
                    "Offshore (150 < h ≤ 1000 m)",
                    "Offshore (h > 1000 m)",
                ],
                "Koreksi Kontrak. (%)": [0, 8, 10, 12, 14, 16],
            }),
            "3. Kedalaman Reservoir": pd.DataFrame({
                "Parameter": ["< 2500 m", "> 2500 m"],
                "Koreksi Kontrak. (%)": [0, 1],
            }),
            "4. Infrastruktur": pd.DataFrame({
                "Parameter": ["Well Developed", "New Frontier Offshore", "New Frontier Onshore"],
                "Koreksi Kontrak. (%)": [0, 2, 4],
            }),
            "5. Jenis Reservoir": pd.DataFrame({
                "Parameter": ["Konvensional (Sandstone, Limestone, Carbonate)", "Non-Konvensional (Shale, CBM)"],
                "Koreksi Kontrak. (%)": [0, 15],
            }),
            "6. CO₂ (%)": pd.DataFrame({
                "Parameter": ["x < 5", "5 ≤ x < 10", "10 ≤ x < 20", "20 ≤ x < 40", "40 ≤ x < 60", "x ≥ 60"],
                "Koreksi Kontrak. (%)": [0, 0.5, 1, 1.5, 2, 4],
            }),
            "7. H₂S (ppm)": pd.DataFrame({
                "Parameter": ["x < 100", "100 ≤ x < 1000", "1000 ≤ x < 2000",
                              "2000 ≤ x < 3000", "3000 ≤ x < 4000", "x ≥ 4000"],
                "Koreksi Kontrak. (%)": [0, 1, 2, 3, 4, 5],
            }),
            "8. SG / API": pd.DataFrame({
                "Parameter": ["API < 25", "API ≥ 25"],
                "Koreksi Kontrak. (%)": [1, 0],
            }),
            "9. TKDN (%)": pd.DataFrame({
                "Parameter": ["x < 30", "30 ≤ x < 50", "50 ≤ x < 70", "x ≥ 70"],
                "Koreksi Kontrak. (%)": [0, 2, 3, 4],
            }),
            "10. Tahapan Produksi": pd.DataFrame({
                "Parameter": ["Primary", "Sekunder (Injeksi Air/Gas)", "Tersier (EOR)"],
                "Koreksi Kontrak. (%)": [0, 6, 10],
            }),
        }
        for title, df_t in tables.items():
            st.markdown(f"**{title}**")
            st.dataframe(df_t, use_container_width=True, hide_index=True)
            st.markdown("")

    with st.expander("Progressive Components (3 Komponen)", expanded=False):
        st.markdown("**11a. Harga Minyak Bumi / ICP (US$/BBL)**")
        st.dataframe(pd.DataFrame({
            "Parameter":              ["ICP ≥ 85", "ICP < 85"],
            "Koreksi Kontrak. (%)":   ["0%", "(85 − ICP) × 0.25%"],
        }), use_container_width=True, hide_index=True)

        st.markdown("**11b. Harga Gas Bumi (US$/MMBTU)**")
        st.dataframe(pd.DataFrame({
            "Parameter":              ["x < 7", "7 ≤ x < 10", "x ≥ 10"],
            "Koreksi Kontrak. (%)":   ["(7 − x) × 2.5%", "0%", "(x − 10) × 2.5%"],
        }), use_container_width=True, hide_index=True)

        st.markdown("**12. Kumulatif Produksi (MMBOE)**")
        st.dataframe(pd.DataFrame({
            "Parameter": ["x < 30", "30 ≤ x < 60", "60 ≤ x < 90",
                          "90 ≤ x < 125", "125 ≤ x < 175", "x ≥ 175"],
            "Koreksi Kontrak. (%)": [10, 9, 8, 6, 4, 0],
        }), use_container_width=True, hide_index=True)

    with st.expander("Pasal 7 – Diskresi Menteri", expanded=False):
        st.markdown("""
**Ayat (1):** Jika keekonomian lapangan *tidak tercapai*, Menteri dapat menambah persentase
bagi hasil kepada Kontraktor.

**Ayat (2):** Jika keekonomian lapangan *melebihi* batas tertentu, Menteri dapat menambah
persentase bagi hasil untuk Negara.

**Ayat (3-5):** Penetapan berlaku untuk POD I dan/atau POD selanjutnya, dengan mempertimbangkan
hasil evaluasi SKK Migas.
        """)

    with st.expander("Pasal 9 – Penyesuaian Progresif Bulanan", expanded=False):
        st.markdown("""
Penyesuaian akibat komponen progresif harga dilaksanakan **setiap bulan** berdasarkan
evaluasi SKK Migas menggunakan rata-rata ICP seluruh lapangan dalam POD yang telah disetujui.
        """)

    with st.expander("Pasal 14 – Biaya Operasi sebagai Pengurang Pajak", expanded=False):
        st.markdown("""
Biaya operasi Kontraktor menjadi **unsur pengurang penghasilan** dalam perhitungan
Pajak Penghasilan sesuai peraturan perpajakan hulu Migas yang berlaku.
        """)


# ══════════════════════════════════════════════
#  TAB 3 – TENTANG
# ══════════════════════════════════════════════
with tab_about:
    st.markdown("###Tentang Aplikasi")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="sl-card">
          <div class="sl-section-tag">Aplikasi</div>
          <p style="margin-top:12px;line-height:1.8;">
            <strong>SplitLogic</strong> adalah aplikasi kalkulator interaktif untuk menghitung
            bagi hasil produksi minyak dan gas bumi menggunakan skema
            <strong>Gross Split</strong> sesuai
            <em>Peraturan Menteri ESDM No. 8 Tahun 2017</em>.
          </p>
          <p style="line-height:1.8;">
            Aplikasi ini memungkinkan pengguna memasukkan seluruh 10 komponen tetap
            (fixed) dan 3 komponen variabel (progressive) secara interaktif,
            serta melihat visualisasi rincian koreksi split secara langsung.
          </p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="sl-card">
          <div class="sl-section-tag">Informasi Akademik</div>
          <table style="width:100%;margin-top:12px;border-collapse:collapse;">
            <tr style="border-bottom:1px solid rgba(255,255,255,0.06);">
              <td style="padding:8px 0;color:#8BA3BC;font-size:0.85rem;">Mata Kuliah</td>
              <td style="padding:8px 0;font-weight:600;">TM3203 – Manajemen & Keekonomian Proyek</td>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.06);">
              <td style="padding:8px 0;color:#8BA3BC;font-size:0.85rem;">Program Studi</td>
              <td style="padding:8px 0;">Teknik Perminyakan</td>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.06);">
              <td style="padding:8px 0;color:#8BA3BC;font-size:0.85rem;">Fakultas</td>
              <td style="padding:8px 0;">Teknik Pertambangan dan Perminyakan</td>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.06);">
              <td style="padding:8px 0;color:#8BA3BC;font-size:0.85rem;">Institusi</td>
              <td style="padding:8px 0;">Institut Teknologi Bandung (ITB)</td>
            </tr>
            <tr>
              <td style="padding:8px 0;color:#8BA3BC;font-size:0.85rem;">Dosen Pengampu</td>
              <td style="padding:8px 0;">
                Dr. Adityawarman, S.T., M.T.<br>
                Rafael J.S. Purba, S.T., M.T.
            </tr>
            <tr>
              <td style="padding:8px 0;color:#8BA3BC;font-size:0.85rem;">Tim Pengembang</td>
              <td style="padding:8px 0;">
                Ibra Rabbani Dahlan (12223010)<br>
                Abraham Gwen Bramanti (12223027)<br>
                Daniel Syahputra Barus (12223074)<br>
                Iqlima Ayarikka (12223083)               
              </td>
            </tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sl-card" style="margin-top:8px;">
      <div class="sl-section-tag">Dasar Hukum & Metodologi</div>
      <ul style="margin-top:12px;line-height:2;color:#C8D8E8;">
        <li><strong>Peraturan Menteri ESDM No. 8 Tahun 2017</strong> – Kontrak Bagi Hasil Gross Split</li>
        <li>Komponen Fixed (10): Field Status, Lokasi, Kedalaman Reservoir, Infrastruktur,
            Jenis Reservoir, CO₂, H₂S, SG/API, TKDN, Tahapan Produksi</li>
        <li>Komponen Progressive (3): Harga Minyak/Gas, Kumulatif Produksi, Diskresi Menteri</li>
        <li>Base Split Minyak: <strong>57% Pemerintah / 43% Kontraktor</strong></li>
        <li>Base Split Gas: <strong>52% Pemerintah / 48% Kontraktor</strong></li>
        <li>Seluruh koreksi bersifat <em>aditif</em> terhadap base split kontraktor</li>
      </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sl-card" style="margin-top:8px;">
      <div class="sl-section-tag">Stack Teknologi</div>
      <div style="margin-top:12px;display:flex;flex-wrap:wrap;gap:8px;">
        <span class="badge">Python 3.13</span>
        <span class="badge">Streamlit</span>
        <span class="badge">Plotly</span>
        <span class="badge">Pandas</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sl-card" style="margin-top:8px;">
      <div class="sl-section-tag">Feedback & Report</div>
      <ul style="margin-top:12px;line-height:2;color:#C8D8E8;">
        Untuk masukan atau pelaporan bug, silakan hubungi contact person melalui email: abraham.bramanti@outlook.com atau melalui LinkedIn: linkedin.com/in/abraham-bramanti
      </ul>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="footer-text">
  <strong style="color:#E8963C;">SplitLogic</strong> &nbsp;·&nbsp;
  TM3203 Manajemen & Keekonomian Proyek &nbsp;·&nbsp;
  Teknik Perminyakan ITB &nbsp;·&nbsp; 2026<br>
  <span style="font-size:0.7rem;">
    Copyright © 2026 Kelompok 16 &nbsp;|&nbsp; SplitLogic v.1.0
  </span>
</div>
""", unsafe_allow_html=True)
