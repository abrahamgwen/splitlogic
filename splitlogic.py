# ==========================================
# PSCore \u2013 PSC Modelling Suite
# Combines: PSChii (Cost Recovery) + SplitLogic (Gross Split)
# Theme: SplitLogic dark navy/amber aesthetic
# ==========================================

# \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
# 0. LIBRARY
# \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy_financial as npf
import os
from PIL import Image

try:
    import yfinance as yf
    YFINANCE_OK = True
except ImportError:
    YFINANCE_OK = False

# \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
# 1. PAGE CONFIG
# \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
logo_path = os.path.join("assets", "splitlogic.png")
try:
    logo = Image.open(logo_path)
    st.set_page_config(layout="wide", page_title="PSCore v1.0", page_icon=logo)
except FileNotFoundError:
    st.set_page_config(layout="wide", page_title="PSCore v1.0", page_icon="\u26a1")
    logo = None

# \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
# 2. GLOBAL CSS  (SplitLogic theme)
# \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

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

  .stApp {
    background:
      linear-gradient(rgba(232,150,60,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(232,150,60,0.03) 1px, transparent 1px),
      linear-gradient(160deg, #0D1B2A 0%, #12243A 50%, #0D1B2A 100%);
    background-size: 48px 48px, 48px 48px, 100% 100%;
  }

  [data-testid="stSidebar"] {
    background: var(--navy-2) !important;
    border-right: 1px solid var(--border) !important;
  }
  [data-testid="stSidebar"] .stSelectbox label,
  [data-testid="stSidebar"] .stNumberInput label,
  [data-testid="stSidebar"] .stRadio label,
  [data-testid="stSidebar"] p,
  [data-testid="stSidebar"] span { color: var(--text) !important; }

  h1, h2, h3, h4 {
    font-family: 'Syne', sans-serif !important;
    color: var(--text) !important;
  }

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

  [data-testid="stDataFrame"] {
    border-radius: var(--radius);
    border: 1px solid var(--border);
  }

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

  hr { border-color: var(--border) !important; }

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

  .stAlert { border-radius: var(--radius) !important; }

  .stRadio label { color: var(--text) !important; }
  .stRadio [data-baseweb="radio"] div { border-color: var(--amber) !important; }

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
  .mode-pill {
    display: inline-block;
    background: rgba(232,150,60,0.20);
    border: 1px solid rgba(232,150,60,0.5);
    color: var(--amber);
    font-family: 'Syne', sans-serif;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 4px 14px;
    border-radius: 20px;
    margin-left: 12px;
    vertical-align: middle;
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

# \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
# 3. PLOTLY HELPERS (shared)
# \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
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

# \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
# 4. SIDEBAR \u2013 MODE SELECTOR + HEADER
# \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
with st.sidebar:
    if logo:
        st.image(logo, use_container_width=True)
    else:
        st.markdown("""
        <div style="text-align:center;padding:20px 0 8px;">
          <span style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;
                       color:#E8963C;letter-spacing:-0.02em;">\u26a1 PSCore</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;margin-bottom:18px;">
      <span class="badge">PSCore</span>
      <span class="badge">v1.0</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown('<div class="sl-section-tag">Pilih Modul</div>', unsafe_allow_html=True)
    app_mode = st.radio(
        "Skema PSC",
        ["\ud83d\udcb0 Cost Recovery (PSChii)", "\u26a1 Gross Split (SplitLogic)"],
        index=0,
    )
    st.markdown("---")

# \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
# \u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588  MODULE A \u2013 COST RECOVERY (PSChii)  \u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588
# \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
if app_mode == "\ud83d\udcb0 Cost Recovery (PSChii)":

    # \u2500\u2500 Sidebar inputs \u2500\u2500
    with st.sidebar:
        st.markdown("### \u2699\ufe0f Input Parameter")

        with st.sidebar.expander("\ud83d\udcc8 Production Profile", expanded=True):
            q_initial     = st.number_input("Initial Rate (BOPD)", value=0, step=1000)
            q_peak        = st.number_input("Peak Rate (BOPD)", value=0, step=1000)
            plateau_years = st.number_input("Plateau Duration (Years)", value=0, step=1)
            decline_rate  = st.number_input("Decline Rate (%)", value=0.0, step=1.0) / 100
            prod_years    = st.number_input("Production Duration (Years)", value=0, step=1)

        with st.sidebar.expander("\ud83c\udfd7\ufe0f CAPEX (Exploration & Dev)", expanded=False):
            exp_years = st.number_input("Exploration Duration (Years)", value=0, step=1)
            st.markdown("**Exploration Cost (MUS$)**")
            df_exp = pd.DataFrame({"Tahun": range(1, int(exp_years)+1),
                                   "Biaya": [0]*int(exp_years)})
            edit_exp = st.data_editor(df_exp, hide_index=True, use_container_width=True, key="editor_exp")
            exp_costs_input = ",".join(edit_exp["Biaya"].astype(str))

            dev_years = st.number_input("Development Duration (Years)", value=0, step=1)
            st.markdown("**Development Cost (MUS$)**")
            df_dev = pd.DataFrame({"Tahun": range(1, int(dev_years)+1),
                                   "Biaya": [0]*int(dev_years)})
            edit_dev = st.data_editor(df_dev, hide_index=True, use_container_width=True, key="editor_dev")
            dev_costs_input = ",".join(edit_dev["Biaya"].astype(str))

            tangible_pct  = st.number_input("Tangible Split (%)", value=0.0, step=1.0) / 100
            intangible_pct = 1.0 - tangible_pct
            st.caption(f"\u21b3 *Implied Intangible Split:* **{intangible_pct*100:.1f}%**")

        with st.sidebar.expander("\ud83d\udcb0 Economic & PSC Terms", expanded=False):
            oil_price           = st.number_input("Oil Price ($/bbl)", value=0.0, step=1.0)
            opex_per_bbl        = st.number_input("Opex ($/bbl)", value=0.0, step=1.0)
            ftp_rate            = st.number_input("FTP (%)", value=0.0, step=1.0) / 100
            tax_rate            = st.number_input("Corporate Tax (%)", value=0.0, step=1.0) / 100
            gov_split_after_tax = st.number_input("Gov After-Tax Split (%)", value=0.0, step=1.0) / 100
            st.markdown("**Domestic Market Obligation (DMO)**")
            dmo_volume_rate     = st.number_input("DMO Volume Obligation (%)", value=0.0, step=1.0) / 100
            dmo_fee_rate        = st.number_input("DMO Fee Rate (%)", value=0.0, step=1.0) / 100
            dmo_holiday_years   = st.number_input("DMO Holiday Duration (Years)", value=0, step=1)
            discount_rate       = st.number_input("Discount Rate for NPV (%)", value=0.0, step=1.0) / 100

            ctr_split_after_tax  = 1 - gov_split_after_tax
            ctr_split_before_tax = ctr_split_after_tax / (1 - tax_rate) if tax_rate != 1 else 0
            gov_split_before_tax = 1 - ctr_split_before_tax
            st.info(f"""
            **\ud83d\udcca Implied Split Breakdown:**
            - Ctr After-Tax: **{ctr_split_after_tax*100:.2f}%**
            - Gov Before-Tax: **{gov_split_before_tax*100:.2f}%**
            - Ctr Before-Tax: **{ctr_split_before_tax*100:.2f}%**
            """)

        with st.sidebar.expander("\ud83d\udcc9 Depreciation Rules", expanded=False):
            dep_group = st.selectbox("Tangible Depreciation Group",
                                     ["Group 1 (50%)", "Group 2 (25%)", "Group 3 (12.5%)"])
            dep_years = st.number_input("Target Depreciation (Years)", value=1, min_value=1, step=1)

    # \u2500\u2500 Live Oil Price \u2500\u2500
    @st.cache_data(ttl=3600)
    def fetch_live_oil_prices():
        if not YFINANCE_OK:
            return {"status": "failed"}
        try:
            brent = yf.Ticker("BZ=F").history(period="2d")
            wti   = yf.Ticker("CL=F").history(period="2d")
            bp    = brent['Close'].iloc[-1]; bprev = brent['Close'].iloc[-2]
            wp    = wti['Close'].iloc[-1];   wprev = wti['Close'].iloc[-2]
            return {
                "brent": {"price": bp, "change": (bp-bprev)/bprev*100},
                "wti":   {"price": wp, "change": (wp-wprev)/wprev*100},
                "status": "success"
            }
        except Exception:
            return {"status": "failed"}

    live_prices = fetch_live_oil_prices()

    # \u2500\u2500 Core Model \u2500\u2500
    def run_psc_model(override_oil_price=None, capex_mult=1.0):
        current_oil_price = override_oil_price if override_oil_price is not None else oil_price

        try:
            exploration_costs_list = [(float(x.strip()) * capex_mult) for x in exp_costs_input.split(',')]
        except ValueError:
            exploration_costs_list = [0]
        try:
            development_costs_list = [(float(x.strip()) * capex_mult) for x in dev_costs_input.split(',')]
        except ValueError:
            development_costs_list = [0]

        exploration_costs_list = (exploration_costs_list + [0]*int(exp_years))[:int(exp_years)]
        development_costs_list = (development_costs_list + [0]*int(dev_years))[:int(dev_years)]

        actual_prod_years = int(prod_years) + 1
        prod_start_year   = int(exp_years) + int(dev_years)
        total_years       = prod_start_year + actual_prod_years
        years_array       = np.arange(1, total_years + 1)

        exp_costs  = np.zeros(total_years)
        exp_costs[0:int(exp_years)] = exploration_costs_list
        dev_costs  = np.zeros(total_years)
        dev_costs[int(exp_years):prod_start_year] = development_costs_list
        dev_tangible   = dev_costs * tangible_pct
        dev_intangible = dev_costs * intangible_pct

        prod_bopd = np.zeros(total_years)
        if actual_prod_years > 0:
            prod_bopd[prod_start_year] = q_initial
            for i in range(1, min(int(plateau_years)+1, actual_prod_years)):
                if prod_start_year + i < total_years:
                    prod_bopd[prod_start_year + i] = q_peak
            for i in range(int(plateau_years)+1, actual_prod_years):
                if prod_start_year + i < total_years:
                    prod_bopd[prod_start_year+i] = prod_bopd[prod_start_year+i-1] * (1-decline_rate)

        prod_mstb = (prod_bopd * 365) / 1000

        rate_map = {"Group 1 (50%)": 0.50, "Group 2 (25%)": 0.25, "Group 3 (12.5%)": 0.125}
        depreciation_rate = rate_map[dep_group]
        dep_sched = []
        bal = 1.0
        for i in range(int(dep_years)):
            if i == int(dep_years) - 1:
                dep_sched.append(bal)
            else:
                chg = bal * depreciation_rate
                dep_sched.append(chg)
                bal -= chg

        total_tangible_pool = np.sum(dev_tangible)
        depreciation = np.zeros(total_years)
        for i, pct in enumerate(dep_sched):
            ty = prod_start_year + i
            if ty < total_years:
                depreciation[ty] = total_tangible_pool * pct

        finding_amort   = np.zeros(total_years)
        intangible_amort = np.zeros(total_years)
        if prod_start_year < total_years:
            finding_amort[prod_start_year]    = np.sum(exp_costs)
            intangible_amort[prod_start_year] = np.sum(dev_intangible)

        gross_revenue = prod_mstb * current_oil_price
        opex          = prod_mstb * opex_per_bbl
        ftp           = gross_revenue * ftp_rate
        gov_ftp       = ftp * gov_split_before_tax
        ctr_ftp       = ftp * ctr_split_before_tax
        gr_minus_ftp  = gross_revenue - ftp
        total_costs_amort = finding_amort + intangible_amort + depreciation + opex

        recovered = np.zeros(total_years)
        unrecovered = np.zeros(total_years)
        ets = np.zeros(total_years)
        cur_unrk = 0

        for i in range(total_years):
            if prod_mstb[i] > 0:
                pool = cur_unrk + total_costs_amort[i]
                recovered[i] = min(gr_minus_ftp[i], pool)
                cur_unrk = pool - recovered[i]
                unrecovered[i] = cur_unrk
                ets[i] = gr_minus_ftp[i] - recovered[i]

        gov_equity = ets * gov_split_before_tax
        ctr_equity = ets * ctr_split_before_tax

        dmo_gross = np.zeros(total_years)
        dmo_fee   = np.zeros(total_years)
        for i in range(total_years):
            if prod_mstb[i] > 0:
                prod_year = i - prod_start_year + 1
                if prod_year == 1:
                    pass
                elif prod_year <= int(dmo_holiday_years):
                    dmo_gross[i] = gross_revenue[i] * ctr_split_before_tax * dmo_volume_rate
                    dmo_fee[i]   = dmo_gross[i]
                else:
                    dmo_gross[i] = gross_revenue[i] * ctr_split_before_tax * dmo_volume_rate
                    dmo_fee[i]   = dmo_gross[i] * dmo_fee_rate

        dmo_penalty    = dmo_gross - dmo_fee
        net_ctr_share  = np.where(prod_mstb > 0, ctr_ftp + ctr_equity - dmo_penalty, 0)
        taxable_income = np.maximum(0, net_ctr_share)
        tax_paid       = taxable_income * tax_rate

        cash_in  = np.where(prod_mstb > 0, recovered + net_ctr_share, 0)
        cash_out = np.where(prod_mstb > 0, opex + tax_paid, exp_costs + dev_tangible + dev_intangible)
        net_cf   = np.where(prod_mstb > 0, cash_in - cash_out, -cash_out)
        gov_take = gov_ftp + gov_equity + dmo_penalty + tax_paid

        return dict(
            years=years_array, prod_bopd=prod_bopd, prod_mstb=prod_mstb,
            gross_revenue=gross_revenue, recovered=recovered, unrecovered=unrecovered,
            net_cf=net_cf, gov_take=gov_take, tax_paid=tax_paid,
            total_costs_amort=total_costs_amort, cash_in=cash_in, cash_out=cash_out,
            exp_costs=exp_costs, dev_tangible=dev_tangible, dev_intangible=dev_intangible,
            ftp=ftp, gov_ftp=gov_ftp, ctr_ftp=ctr_ftp,
            gov_equity=gov_equity, ctr_equity=ctr_equity,
            dmo_penalty=dmo_penalty, finding_amort=finding_amort,
            depreciation=depreciation, intangible_amort=intangible_amort,
            opex=opex, gr_minus_ftp=gr_minus_ftp, ets=ets,
            net_ctr_share=net_ctr_share, dmo_gross=dmo_gross, dmo_fee=dmo_fee,
            prod_start_year=prod_start_year, total_years=total_years,
        )

    results = run_psc_model()

    # \u2500\u2500 KPIs \u2500\u2500
    total_gross_revenue = np.sum(results['gross_revenue'])
    total_gov_take      = np.sum(results['gov_take'])
    gov_take_pct        = total_gov_take / total_gross_revenue if total_gross_revenue > 0 else 0
    total_ctr_take_at   = np.sum(results['net_ctr_share']) - np.sum(results['tax_paid'])

    npv_base = npf.npv(discount_rate, results['net_cf']) / (1 + discount_rate)
    try:
        irr_base = npf.irr(results['net_cf'])
    except Exception:
        irr_base = float('nan')

    cumulative_cf = np.cumsum(results['net_cf'])
    payback_year  = "-"
    for y, val in enumerate(cumulative_cf):
        if val >= 0 and y >= results['prod_start_year']:
            payback_year = f"Year {y+1}"
            break

    bep_price = 0
    for test_p in range(10, 200):
        tr = run_psc_model(override_oil_price=test_p)
        if (npf.npv(discount_rate, tr['net_cf']) / (1 + discount_rate)) > 0:
            bep_price = test_p
            break

    # \u2500\u2500 HEADER \u2500\u2500
    col_logo, col_title = st.columns([1, 10])
    with col_logo:
        if logo:
            st.image(logo, use_container_width=True)
    with col_title:
        st.markdown("""
        <h1 style="margin-bottom:0;">
          PSCore
          <span class="mode-pill">Cost Recovery</span>
        </h1>
        <p style="color:var(--muted);margin-top:4px;font-size:0.9rem;">
          PSC Cost Recovery Financial Modeller \u2014 formerly <em>PSChii</em>
        </p>
        """, unsafe_allow_html=True)
    st.markdown("---")

    # \u2500\u2500 Tabs \u2500\u2500
    tab1, tab2, tab3, tab_about = st.tabs(["\ud83d\udcca Dashboard", "\ud83d\udcd1 Economic Tables", "\ud83d\udcc8 Sensitivity", "\u2139\ufe0f About"])

    # \u2500\u2500 TAB 1: Dashboard \u2500\u2500
    with tab1:
        if live_prices.get("status") == "success":
            st.markdown("##### \ud83c\udf0d Live Global Oil Market (Reference Only)")
            p1, p2, _, _ = st.columns(4)
            p1.metric("Brent Crude (BZ=F)",
                      f"${live_prices['brent']['price']:.2f}/bbl",
                      f"{live_prices['brent']['change']:.2f}%")
            p2.metric("WTI Crude (CL=F)",
                      f"${live_prices['wti']['price']:.2f}/bbl",
                      f"{live_prices['wti']['change']:.2f}%")
            st.markdown("---")

        st.markdown("### \ud83c\udfc6 Key Economic Indicators")
        c1,c2,c3,c4,c5,c6 = st.columns(6)
        c1.metric("Reserve (MMBO)",              f"{np.sum(results['prod_mstb'])/1000:.2f}")
        c2.metric(f"NPV @{discount_rate*100:.0f}% (MUS$)", f"{npv_base:,.0f}")
        c3.metric("IRR Full Cycle",              f"{irr_base:.2%}" if not np.isnan(irr_base) else "-")
        c4.metric("Gov Take (%)",                f"{gov_take_pct:.2%}")
        c5.metric("Payback Period",              payback_year)
        c6.metric("Break-Even Price",            f"${bep_price}/bbl")
        st.markdown("---")

        # Gantt
        st.markdown("### \ud83d\udcc5 Project Phase Timeline")
        df_tl = pd.DataFrame([
            dict(Task="Exploration Phase", Start=1,                       Finish=int(exp_years),                    Color="#E18D11"),
            dict(Task="Development Phase", Start=int(exp_years)+1,        Finish=int(exp_years)+int(dev_years),     Color="#17BECF"),
            dict(Task="Production Phase",  Start=int(exp_years)+int(dev_years)+1, Finish=results['total_years'],   Color="#2CA02C"),
        ])
        fig_gantt = go.Figure()
        for _, row in df_tl.iterrows():
            if row['Finish'] >= row['Start']:
                fig_gantt.add_trace(go.Bar(
                    x=[row['Finish']-row['Start']+1], y=[row['Task']],
                    base=[row['Start']-1], orientation='h',
                    marker_color=row['Color'], name=row['Task'],
                    text=f"Year {row['Start']} to {row['Finish']}",
                    textposition="inside",
                ))
        fig_gantt.update_layout(barmode='stack', height=200, xaxis_title="Project Year",
                                showlegend=False, **plotly_layout())
        st.plotly_chart(fig_gantt, use_container_width=True)
        st.markdown("---")

        cc1, cc2 = st.columns(2)
        with cc1:
            fig_prod = make_subplots(specs=[[{"secondary_y": True}]])
            fig_prod.add_trace(go.Bar(x=results['years'], y=results['prod_bopd'],
                                     name="BOPD", marker_color=SLATE), secondary_y=False)
            fig_prod.add_trace(go.Scatter(x=results['years'], y=np.cumsum(results['prod_mstb']),
                                          name="Cum. Prod (MSTB)",
                                          line=dict(color=AMBER, width=3)), secondary_y=True)
            fig_prod.update_layout(**plotly_layout("\ud83d\udcc8 Production Profile & Cumulative"))
            fig_prod.update_yaxes(title_text="BOPD", secondary_y=False)
            fig_prod.update_yaxes(title_text="MSTB (Cumulative)", secondary_y=True)
            st.plotly_chart(fig_prod, use_container_width=True)

        with cc2:
            fig_cf = go.Figure()
            bar_colors = [AMBER if v >= 0 else "#C05050" for v in results['net_cf']]
            fig_cf.add_trace(go.Bar(x=results['years'], y=results['net_cf'],
                                    name="Yearly CF", marker_color=bar_colors))
            fig_cf.add_trace(go.Scatter(x=results['years'], y=cumulative_cf,
                                         name="Cumulative CF",
                                         line=dict(color="#F5B96B", width=3)))
            fig_cf.update_layout(**plotly_layout("\ud83d\udcb5 Contractor Net Cash Flow"),
                                 yaxis_title="MUS$")
            st.plotly_chart(fig_cf, use_container_width=True)

        st.markdown("---")
        cc3, cc4 = st.columns(2)

        with cc3:
            st.markdown("### \ud83c\udf0a PSC Distribution Waterfall")
            fig_wf = go.Figure(go.Waterfall(
                orientation="v",
                measure=["relative","relative","relative","relative","relative","relative","total"],
                x=["Gross Revenue","Cost Recovery","Gov FTP","Gov Equity","DMO Penalty","Corp Tax","Contractor Take"],
                y=[total_gross_revenue, -np.sum(results['recovered']),
                   -np.sum(results['gov_ftp']), -np.sum(results['gov_equity']),
                   -np.sum(results['dmo_penalty']), -np.sum(results['tax_paid']),
                   total_ctr_take_at],
                decreasing=dict(marker=dict(color="#C05050")),
                increasing=dict(marker=dict(color=SLATE)),
                totals=dict(marker=dict(color=AMBER)),
            ))
            fig_wf.update_layout(**plotly_layout("Revenue Distribution Waterfall"))
            st.plotly_chart(fig_wf, use_container_width=True)

        with cc4:
            st.markdown("### \ud83e\udd67 Gross Revenue Allocation")
            fig_pie = go.Figure(data=[go.Pie(
                labels=['Cost Recovery', 'Government Take', 'Contractor Take (After Tax)'],
                values=[np.sum(results['recovered']), total_gov_take, total_ctr_take_at],
                hole=.4,
                marker_colors=[SLATE, MUTED, AMBER],
                textinfo='label+percent',
            )])
            fig_pie.update_layout(**plotly_layout("Proporsi Pembagian Total Pendapatan"))
            st.plotly_chart(fig_pie, use_container_width=True)

    # \u2500\u2500 TAB 2: Tables \u2500\u2500
    with tab2:
        st.subheader("\ud83d\udccb Annual Economic Summary")
        total_yrs = results['total_years']
        df_out = pd.DataFrame({
            "Year":            results['years'],
            "Prod (BOPD)":     np.round(results['prod_bopd'], 0),
            "Prod (MSTB)":     np.round(results['prod_mstb'], 2),
            "Gross Rev (MUS$)":np.round(results['gross_revenue'], 2),
            "FTP (MUS$)":      np.round(results['ftp'], 2),
            "Cost Rec (MUS$)": np.round(results['recovered'], 2),
            "Unrecov (MUS$)":  np.round(results['unrecovered'], 2),
            "ETS (MUS$)":      np.round(results['ets'], 2),
            "Gov Equity":      np.round(results['gov_equity'], 2),
            "Ctr Equity":      np.round(results['ctr
