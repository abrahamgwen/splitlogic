#region Judul
# ──────────────────────────────────────────
# SplitLogic v1.0 – PSC Modelling
# Created by Abraham Gwen Bramanti
# Last edited: 4/28/2026
# ──────────────────────────────────────────
#endregion

#region Library
# ──────────────────────────────────────────
# 0. LIBRARY
# ──────────────────────────────────────────
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
#endregion

#region Page Config
# ──────────────────────────────────────────
# 1. PAGE CONFIG
# ──────────────────────────────────────────
logo_path = os.path.join("assets", "splitlogic.png")
try:
    logo = Image.open(logo_path)
    st.set_page_config(layout="wide", page_title="SplitLogic v1.0", page_icon=logo)
except FileNotFoundError:
    st.set_page_config(layout="wide", page_title="SplitLogic v1.0", page_icon="⚡")
    logo = None
#endregion

#region CSS setting
# ──────────────────────────────────────────
# 2. GLOBAL CSS
# ──────────────────────────────────────────
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
#endregion

#region Plotly
# ──────────────────────────────────────────
# 3. PLOTLY HELPERS
# ──────────────────────────────────────────
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
#endregion

#region Sidebar
# ──────────────────────────────────────────
# 4. SIDEBAR
# ──────────────────────────────────────────
with st.sidebar:
    if logo:
        st.image(logo, use_container_width=True)
    else:
        st.markdown("""
        <div style="text-align:center;padding:20px 0 8px;">
          <span style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;
                       color:#E8963C;letter-spacing:-0.02em;">⚡ SplitLogic</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;margin-bottom:18px;">
      <span class="badge">SplitLogic</span>
      <span class="badge">v1.0</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown('<div class="sl-section-tag">Pilih Modul</div>', unsafe_allow_html=True)
    app_mode = st.radio(
        "Available Schemes:",
        ["Cost Recovery", "Gross Split"],
        index=0,
    )
    st.markdown("---")
#endregion

#region Cost Recovery
# ──────────────────────────────────────────
# 5. COST RECOVERY MODULE
# ───────────────────────────────────────────
if app_mode == "Cost Recovery":

    # ── Sidebar inputs ──
    with st.sidebar:
        st.markdown("### ⚙️ Input Parameter")

        with st.sidebar.expander("📈 Production Profile", expanded=True):
            col_sy, col_ey = st.columns(2)
            start_year = col_sy.number_input("Start Year", value=2022, step=1)
            end_year   = col_ey.number_input("End Year",   value=2039, step=1)

            num_years = max(1, end_year - start_year + 1)
            default_lifting = [0.0000, 28.4700, 215.8682, 192.2671, 172.3361, 155.3515,
                               140.7600, 128.1322, 117.1307, 107.4878, 98.9887, 91.4593,
                               84.7575, 78.7663, 73.3887, 60.1345, 56.2766, 52.7784]

            if num_years > len(default_lifting):
                default_lifting += [0.0] * (num_years - len(default_lifting))
            else:
                default_lifting = default_lifting[:num_years]

            default_prices = [70.0] * num_years

            df_prod_init = pd.DataFrame({
                "Year":             range(start_year, end_year + 1),
                "Lifting (MSTB)":   default_lifting,
                "Price (USD/bbl)":  default_prices,
            })
            edit_prod = st.data_editor(df_prod_init, hide_index=True,
                                       use_container_width=True, key="editor_prod")

        # ── VAT Rate table ──
        with st.sidebar.expander("🧾 VAT Rate", expanded=False):
            df_vat_init = pd.DataFrame({
                "Year":     range(start_year, end_year + 1),
                "VAT Rate": [0.00] * num_years,          # decimal, e.g. 0.11 = 11 %
            })
            edit_vat = st.data_editor(df_vat_init, hide_index=True,
                                      use_container_width=True, key="editor_vat")

        with st.sidebar.expander("📈 Escalation Factor (%/year)", expanded=False):
            df_esc_init = pd.DataFrame({
                "Year":           range(start_year, end_year + 1),
                "Esc. Factor (%)": [0.00] * num_years,   # e.g. 3 means 3 % p.a.
            })
            edit_esc = st.data_editor(df_esc_init, hide_index=True,
                                      use_container_width=True, key="editor_esc")

        def after_vat_col(base_vals, vat_flags, vat_rates):
            """Return list of values after applying VAT where flag is True."""
            result = []
            for v, flag, r in zip(base_vals, vat_flags, vat_rates):
                result.append(v * (1 + r) if flag else v)
            return result

        # ── CAPEX I ──
        with st.sidebar.expander("🏗️ CAPEX I (Drilling & Workover)", expanded=False):
            default_tangible_1 = [0.0, 569.43, 261.96]
            if num_years > len(default_tangible_1):
                default_tangible_1 += [0.0] * (num_years - len(default_tangible_1))
            else:
                default_tangible_1 = default_tangible_1[:num_years]

            vat_rates_now = edit_vat["VAT Rate"].tolist()

            df_capex1_init = pd.DataFrame({
                "Year":             list(range(start_year, end_year + 1)),
                "Tangible (MU)":    default_tangible_1,
                "Association":      ["Oil"] * num_years,
                "PIS Year":         [2023] * num_years,
                "Useful Life (y)":  [5]    * num_years,
                "Depreciation":     ["25%"] * num_years,
                "VAT":              [True]  * num_years,
                "Tangible After":   after_vat_col(default_tangible_1,
                                                  [True]*num_years, vat_rates_now),
            })
            edit_capex_1 = st.data_editor(
                df_capex1_init, hide_index=True, use_container_width=True,
                key="editor_capex_1",
                column_config={
                    "VAT": st.column_config.CheckboxColumn("VAT"),
                    "Tangible After": st.column_config.NumberColumn(
                        "Tangible After (MU)", disabled=True),
                },
            )
            # Recompute "Tangible After" live from current VAT toggles + rates
            c1_after = after_vat_col(
                edit_capex_1["Tangible (MU)"].tolist(),
                edit_capex_1["VAT"].tolist(),
                vat_rates_now,
            )

        # ── CAPEX II ──
        with st.sidebar.expander("🏗️ CAPEX II (Production Facilities)", expanded=False):
            default_tangible_2 = [0.0, 584.9824, 4196.1153, 2204.392]
            if num_years > len(default_tangible_2):
                default_tangible_2 += [0.0] * (num_years - len(default_tangible_2))
            else:
                default_tangible_2 = default_tangible_2[:num_years]

            df_capex2_init = pd.DataFrame({
                "Year":             list(range(start_year, end_year + 1)),
                "Tangible (MU)":    default_tangible_2,
                "Association":      ["Oil"] * num_years,
                "PIS Year":         [2023] * num_years,
                "Useful Life (y)":  [5]    * num_years,
                "Depreciation":     ["25%"] * num_years,
                "VAT":              [True]  * num_years,
                "Tangible After":   after_vat_col(default_tangible_2,
                                                  [True]*num_years, vat_rates_now),
            })
            edit_capex_2 = st.data_editor(
                df_capex2_init, hide_index=True, use_container_width=True,
                key="editor_capex_2",
                column_config={
                    "VAT": st.column_config.CheckboxColumn("VAT"),
                    "Tangible After": st.column_config.NumberColumn(
                        "Tangible After (MU)", disabled=True),
                },
            )
            c2_after = after_vat_col(
                edit_capex_2["Tangible (MU)"].tolist(),
                edit_capex_2["VAT"].tolist(),
                vat_rates_now,
            )

        # ── CAPEX III ──
        with st.sidebar.expander("🏗️ CAPEX III (Intangible)", expanded=False):
            default_intangible = [0.0, 2322.12, 1064.49]
            if num_years > len(default_intangible):
                default_intangible += [0.0] * (num_years - len(default_intangible))
            else:
                default_intangible = default_intangible[:num_years]

            df_capex3_init = pd.DataFrame({
                "Year":           list(range(start_year, end_year + 1)),
                "Intangible (MU)": default_intangible,
                "VAT":             [True] * num_years,
                "Intangible After": after_vat_col(default_intangible,
                                                  [True]*num_years, vat_rates_now),
            })
            edit_capex_3 = st.data_editor(
                df_capex3_init, hide_index=True, use_container_width=True,
                key="editor_capex_3",
                column_config={
                    "VAT": st.column_config.CheckboxColumn("VAT"),
                    "Intangible After": st.column_config.NumberColumn(
                        "Intangible After (MU)", disabled=True),
                },
            )
            c3_after = after_vat_col(
                edit_capex_3["Intangible (MU)"].tolist(),
                edit_capex_3["VAT"].tolist(),
                vat_rates_now,
            )

        # ── OPEX helper ──
        def make_opex_df(default_vals, key_suffix):
            df = pd.DataFrame({
                "Year":         list(range(start_year, end_year + 1)),
                "Opex (MUSD)":  default_vals,
                "VAT":          [True] * num_years,
                "Opex After":   after_vat_col(default_vals, [True]*num_years, vat_rates_now),
            })
            return st.data_editor(
                df, hide_index=True, use_container_width=True,
                key=f"editor_opex_{key_suffix}",
                column_config={
                    "VAT": st.column_config.CheckboxColumn("VAT"),
                    "Opex After": st.column_config.NumberColumn(
                        "Opex After (MUSD)", disabled=True),
                },
            )

        with st.sidebar.expander("🛠️ OPEX I (WIWS)", expanded=False):
            edit_opex_1 = make_opex_df([0.0] * num_years, "1")
        with st.sidebar.expander("🛠️ OPEX II (Operation & Maintenance)", expanded=False):
            edit_opex_2 = make_opex_df([0.0] * num_years, "2")

        with st.sidebar.expander("🛠️ OPEX III (Electricity)", expanded=False):
            default_opex_3 = [0.0, 2037.7363, 8625.7219, 6863.8197, 4119.1711,
                              4024.5949, 3943.3438, 3873.027, 3811.7665, 3758.0713,
                              3710.7449, 3668.8183, 3631.5001, 3598.1389, 2982.3002,
                              2908.4958, 2887.0137, 2867.5344]
            if num_years > len(default_opex_3):
                default_opex_3 += [0.0] * (num_years - len(default_opex_3))
            else:
                default_opex_3 = default_opex_3[:num_years]
            edit_opex_3 = make_opex_df(default_opex_3, "3")

        with st.sidebar.expander("🛠️ OPEX IV (ASR)", expanded=False):
            default_opex_4 = [0.0, 0.0] + [21.9516] * max(0, num_years - 2)
            edit_opex_4 = make_opex_df(default_opex_4[:num_years], "4")

        with st.sidebar.expander("🛠️ OPEX V (LBT)", expanded=False):
            edit_opex_5 = make_opex_df([0.0] * num_years, "5")

        with st.sidebar.expander("🛠️ OPEX VI (Carbon Tax)", expanded=False):
            edit_opex_6 = make_opex_df([0.0] * num_years, "6")

        with st.sidebar.expander("💰 Fiscal & Split Terms", expanded=True):
            tax_rate             = st.number_input("Cont. Eff. Tax Rate (%)",      value=37.60, step=1.0) / 100
            dmo_volume_rate      = st.number_input("DMO Volume (%)",               value=25.00, step=1.0) / 100
            dmo_fee_rate         = st.number_input("DMO Fee (%)",                  value=100.00, step=1.0) / 100
            dmo_holiday_years    = st.number_input("DMO Holiday Duration (years)", value=0,     step=1)
            discount_rate        = st.number_input("Discount Factor (%)",          value=10.00, step=1.0) / 100
            discount_factor_year = st.number_input("Discount Factor Year",         value=2023,  step=1)
            ftp_rate             = st.number_input("FTP (%)",                      value=10.00, step=1.0) / 100

            st.markdown("---")
            st.markdown("**Split Breakdown (%)**")
            gov_split_after_tax  = st.number_input("Gov. After Tax Split (%)", value=62.60, step=1.0) / 100
            ctr_split_after_tax  = 1 - gov_split_after_tax
            ctr_split_before_tax = ctr_split_after_tax / (1 - tax_rate) if tax_rate != 1 else 0
            gov_split_before_tax = 1 - ctr_split_before_tax

            st.info(f"""
            **📊 Implied Split Information:**
            - **After Tax Split**: Gov = {gov_split_after_tax*100:.4f}% | Ctr = {ctr_split_after_tax*100:.4f}%
            - **Before Tax Split**: Gov = {gov_split_before_tax*100:.4f}% | Ctr = {ctr_split_before_tax*100:.4f}%
            """)

        with st.sidebar.expander("⚙️ Method Selection", expanded=True):
            ftp_sharing_method  = st.selectbox("FTP Sharing Method",  ["Shared", "Not Shared"])
            depreciation_method = st.selectbox("Depreciation Method",
                ["Straight Line", "Declining Balance", "Double Declining Balance",
                 "Unit of Production", "Sum of the Year"])

    # ── Live Oil Price ──
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
                "brent": {"price": bp, "change": (bp - bprev) / bprev * 100},
                "wti":   {"price": wp, "change": (wp - wprev) / wprev * 100},
                "status": "success",
            }
        except Exception:
            return {"status": "failed"}

    live_prices = fetch_live_oil_prices()

    # ══════════════════════════════════════════════════════════
    # ── Core PSC Model ──
    # ══════════════════════════════════════════════════════════
    def run_psc_model(override_oil_price=None, capex_mult=1.0):

        total_years  = len(edit_prod)
        years_array  = edit_prod["Year"].values
        prod_mstb    = edit_prod["Lifting (MSTB)"].values.astype(float)
        prod_bopd    = (prod_mstb * 1000) / 365

        non_zero_idx  = np.where(prod_mstb > 0)[0]
        prod_start_yr = int(non_zero_idx[0]) if len(non_zero_idx) > 0 else 0

        # Esc. Factor (%) is the *incremental* annual escalation.
        # Multiplier cumulates from the first production year onward.
        esc_pct = edit_esc["Esc. Factor (%)"].values.astype(float) / 100.0
        # Each year's multiplier = product of (1 + esc_i) for all i up to that year
        # relative to prod_start_yr (base = 1.0 at prod_start_yr)
        esc_mult = np.ones(total_years)
        for i in range(1, total_years):
            esc_mult[i] = esc_mult[i - 1] * (1.0 + esc_pct[i])

        # Re-base so that prod_start_yr = 1.0
        base_esc = esc_mult[prod_start_yr] if prod_start_yr < total_years else 1.0
        esc_mult = esc_mult / base_esc if base_esc != 0 else esc_mult

        # ── Arrays ──
        dev_tangible   = np.zeros(total_years)
        dev_intangible = np.zeros(total_years)
        opex           = np.zeros(total_years)
        depreciation   = np.zeros(total_years)
        dep_capex1     = np.zeros(total_years)
        dep_capex2     = np.zeros(total_years)

        def calc_depreciation(asset_value, start_idx, life, method, prod_profile=None):
            arr      = np.zeros(total_years)
            if asset_value <= 0 or start_idx >= total_years:
                return arr
            life     = max(int(life), 1)
            book_val = float(asset_value)

            if method == "Straight Line":
                dep_amount = asset_value / life
                for i in range(life):
                    y = start_idx + i
                    if y >= total_years:
                        break
                    actual = min(dep_amount, book_val)
                    arr[y]    = actual
                    book_val -= actual

            elif method == "Declining Balance":
                rate = 1.0 / life
                for i in range(life):
                    y = start_idx + i
                    if y >= total_years:
                        break
                    if i == life - 1 or book_val <= 0:
                        arr[y]    = book_val
                        book_val  = 0
                        break
                    dep          = book_val * rate
                    arr[y]       = dep
                    book_val    -= dep

            elif method == "Double Declining Balance":
                rate = 2.0 / life
                for i in range(life):
                    y = start_idx + i
                    if y >= total_years:
                        break
                    if i == life - 1 or book_val <= 0:
                        arr[y]   = book_val
                        book_val = 0
                        break
                    dep          = book_val * rate
                    arr[y]       = dep
                    book_val    -= dep

            elif method == "Unit of Production":
                if prod_profile is not None:
                    total_prod = np.sum(prod_profile[start_idx:])
                    if total_prod > 0:
                        for y in range(start_idx, total_years):
                            if book_val <= 0:
                                break
                            dep          = asset_value * (prod_profile[y] / total_prod)
                            actual       = min(dep, book_val)
                            arr[y]       = actual
                            book_val    -= actual

            elif method in ("Sum of the Year", "Sum of The Year"):
                syd = life * (life + 1) / 2.0
                for i in range(life):
                    y = start_idx + i
                    if y >= total_years:
                        break
                    if i == life - 1:
                        arr[y]   = book_val
                        break
                    dep          = asset_value * (life - i) / syd
                    arr[y]       = dep
                    book_val    -= dep

            return arr

        # ── CAPEX / OPEX → build arrays using pre-computed After-VAT values ──
        #             and respect PIS Year from the editor.
        for i in range(total_years):
            # CAPEX I
            t1_after = float(c1_after[i]) * capex_mult
            if t1_after > 0:
                pis_yr  = int(edit_capex_1["PIS Year"].iloc[i])
                idx_pis = np.searchsorted(years_array, pis_yr)
                idx_pis = int(np.clip(idx_pis, prod_start_yr, total_years - 1))
                life_1  = int(edit_capex_1["Useful Life (y)"].iloc[i])
                d1      = calc_depreciation(t1_after, idx_pis, life_1,
                                            depreciation_method, prod_profile=prod_mstb)
                dep_capex1  += d1
                depreciation += d1

            # CAPEX II
            t2_after = float(c2_after[i]) * capex_mult
            if t2_after > 0:
                pis_yr  = int(edit_capex_2["PIS Year"].iloc[i])
                idx_pis = np.searchsorted(years_array, pis_yr)
                idx_pis = int(np.clip(idx_pis, prod_start_yr, total_years - 1))
                life_2  = int(edit_capex_2["Useful Life (y)"].iloc[i])
                d2      = calc_depreciation(t2_after, idx_pis, life_2,
                                            depreciation_method, prod_profile=prod_mstb)
                dep_capex2  += d2
                depreciation += d2

            dev_tangible[i] = t1_after + t2_after

            # CAPEX III (Intangible — fully expensed in year incurred, no depreciation schedule)
            dev_intangible[i] = float(c3_after[i]) * capex_mult

            def _opex_after(df_opex, idx):
                val     = float(df_opex["Opex (MUSD)"].iloc[idx])
                is_vat  = bool(df_opex["VAT"].iloc[idx])
                vat_r   = float(edit_vat["VAT Rate"].iloc[idx])
                after   = val * (1 + vat_r) if is_vat else val
                return after * esc_mult[idx]        # apply escalation

            op1 = _opex_after(edit_opex_1, i)
            op2 = _opex_after(edit_opex_2, i)
            op3 = _opex_after(edit_opex_3, i)
            op4 = _opex_after(edit_opex_4, i)
            op5 = _opex_after(edit_opex_5, i)
            op6 = _opex_after(edit_opex_6, i)
            opex[i] = op1 + op2 + op3 + op4 + op5 + op6

        exp_costs      = np.zeros(total_years)
        intangible_amort = np.copy(dev_intangible)
        finding_amort  = np.zeros(total_years)

        # ── Revenue ──
        if override_oil_price is not None:
            oil_price_arr = np.full(total_years, float(override_oil_price))
        else:
            oil_price_arr = edit_prod["Price (USD/bbl)"].values.astype(float)

        gross_revenue = prod_mstb * oil_price_arr
        ftp           = gross_revenue * ftp_rate

        if ftp_sharing_method == "Shared":
            gov_ftp = ftp * gov_split_before_tax
            ctr_ftp = ftp * ctr_split_before_tax
        else:
            gov_ftp = ftp.copy()
            ctr_ftp = np.zeros(total_years)

        gr_minus_ftp      = gross_revenue - ftp
        total_costs_amort = finding_amort + intangible_amort + depreciation + opex

        # ── Cost Recovery loop ──
        recovered   = np.zeros(total_years)
        unrecovered = np.zeros(total_years)
        ets         = np.zeros(total_years)
        cur_unrk    = 0.0

        for i in range(total_years):
            pool = cur_unrk + total_costs_amort[i]
            if prod_mstb[i] > 0:
                recovered[i] = min(gr_minus_ftp[i], pool)
                cur_unrk     = pool - recovered[i]
                ets[i]       = gr_minus_ftp[i] - recovered[i]
            else:
                cur_unrk     = pool
                ets[i]       = 0
            unrecovered[i]   = cur_unrk

        gov_equity = ets * gov_split_before_tax
        ctr_equity = ets * ctr_split_before_tax

        # ── DMO ──
        dmo_gross = np.zeros(total_years)
        dmo_fee   = np.zeros(total_years)
        for i in range(total_years):
            if prod_mstb[i] > 0:
                prod_year = i - prod_start_yr + 1
                dmo_gross[i] = gross_revenue[i] * ctr_split_before_tax * dmo_volume_rate
                if prod_year <= int(dmo_holiday_years):
                    dmo_fee[i] = dmo_gross[i]          # full fee refund during holiday
                else:
                    dmo_fee[i] = dmo_gross[i] * dmo_fee_rate

        dmo_penalty    = dmo_gross - dmo_fee
        net_ctr_share  = np.where(prod_mstb > 0,
                                  ctr_ftp + ctr_equity - dmo_penalty, 0.0)
        taxable_income = np.maximum(0.0, net_ctr_share)
        tax_paid       = taxable_income * tax_rate

        # ── Cash Flow ──
        cash_in  = recovered + net_ctr_share
        capex_total = exp_costs + dev_tangible + dev_intangible
        cash_out = capex_total + opex + tax_paid
        net_cf   = cash_in - cash_out

        gov_take = gov_ftp + gov_equity + dmo_penalty + tax_paid

        return dict(
            years=years_array, prod_bopd=prod_bopd, prod_mstb=prod_mstb,
            oil_price_arr=oil_price_arr, gross_revenue=gross_revenue,
            recovered=recovered, unrecovered=unrecovered,
            net_cf=net_cf, gov_take=gov_take, tax_paid=tax_paid,
            taxable_income=taxable_income, total_costs_amort=total_costs_amort,
            cash_in=cash_in, cash_out=cash_out,
            exp_costs=exp_costs, dev_tangible=dev_tangible, dev_intangible=dev_intangible,
            ftp=ftp, gov_ftp=gov_ftp, ctr_ftp=ctr_ftp,
            gov_equity=gov_equity, ctr_equity=ctr_equity,
            dmo_penalty=dmo_penalty, finding_amort=finding_amort,
            depreciation=depreciation, dep_capex1=dep_capex1, dep_capex2=dep_capex2,
            intangible_amort=intangible_amort, opex=opex, gr_minus_ftp=gr_minus_ftp,
            ets=ets, net_ctr_share=net_ctr_share,
            dmo_gross=dmo_gross, dmo_fee=dmo_fee,
            prod_start_year=prod_start_yr, total_years=total_years,
        )

    results = run_psc_model()

    # ══════════════════════════════════════════════════════════
    # ── KPIs ──
    # ══════════════════════════════════════════════════════════
    total_gross_revenue = float(np.sum(results['gross_revenue']))
    total_gov_take      = float(np.sum(results['gov_take']))
    gov_take_pct        = total_gov_take / total_gross_revenue if total_gross_revenue > 0 else 0
    total_ctr_take_at   = float(np.sum(results['net_ctr_share']) - np.sum(results['tax_paid']))

    npv_base = 0.0
    for i in range(results['total_years']):
        # t = number of years from discount_factor_year (can be negative for earlier years)
        t = float(results['years'][i]) - float(discount_factor_year)
        df_factor = (1.0 + discount_rate) ** t
        npv_base += results['net_cf'][i] / df_factor

    try:
        cf = results['net_cf']
        # IRR only meaningful when there is at least one negative and one positive CF
        if np.any(cf < 0) and np.any(cf > 0):
            irr_base = npf.irr(cf)
            if np.isnan(irr_base) or np.isinf(irr_base):
                irr_base = float('nan')
        else:
            irr_base = float('nan')
    except Exception:
        irr_base = float('nan')

    cumulative_cf = np.cumsum(results['net_cf'])
    payback_year  = "-"
    for y, val in enumerate(cumulative_cf):
        if val >= 0 and y >= results['prod_start_year']:
            payback_year = str(int(results['years'][y]))
            break

    # ── Break-Even Price ──
    bep_price = None
    for test_p in range(1, 300):
        tr = run_psc_model(override_oil_price=float(test_p))
        test_npv = 0.0
        for i in range(tr['total_years']):
            t = float(tr['years'][i]) - float(discount_factor_year)
            test_npv += tr['net_cf'][i] / ((1.0 + discount_rate) ** t)
        if test_npv >= 0:
            bep_price = test_p
            break
    if bep_price is None:
        bep_price = float('nan')

    # ── Summary aggregates ──
    sum_prod_mstb    = float(np.sum(results['prod_mstb']))
    avg_oil_price    = total_gross_revenue / sum_prod_mstb if sum_prod_mstb > 0 else 0

    sum_ftp_gov      = float(np.sum(results['gov_ftp']))
    sum_ftp_ctr      = float(np.sum(results['ctr_ftp']))
    sum_ftp_total    = float(np.sum(results['ftp']))

    sum_ets_gov      = float(np.sum(results['gov_equity']))
    sum_ets_ctr      = float(np.sum(results['ctr_equity']))
    sum_ets_total    = float(np.sum(results['ets']))

    sum_sunk_cost    = float(np.sum(results['exp_costs']))
    sum_tangible     = float(np.sum(results['dev_tangible']))
    sum_intangible   = float(np.sum(results['dev_intangible']))
    sum_opex         = float(np.sum(results['opex']))

    sum_cost_recovery = float(np.sum(results['recovered']))
    pct_cost_recovery = sum_cost_recovery / total_gross_revenue if total_gross_revenue > 0 else 0

    sum_dmo_penalty  = float(np.sum(results['dmo_penalty']))
    sum_tax          = float(np.sum(results['tax_paid']))

    pct_gov_share    = total_gov_take / total_gross_revenue if total_gross_revenue > 0 else 0
    pct_ctr_share    = total_ctr_take_at / total_gross_revenue if total_gross_revenue > 0 else 0

    # ══════════════════════════════════════════════════════════
    # ── HEADER ──
    # ══════════════════════════════════════════════════════════
    col_logo, col_title = st.columns([1, 10])
    with col_logo:
        if logo:
            st.image(logo, use_container_width=True)
    with col_title:
        st.markdown("""
        <h1 style="margin-bottom:0;">
          SplitLogic
          <span class="mode-pill">Cost Recovery</span>
        </h1>
        <p style="color:var(--muted);margin-top:4px;font-size:0.9rem;">
          PSC Cost Recovery Financial Modeller — <em>SplitLogic</em>
        </p>
        """, unsafe_allow_html=True)
    st.markdown("---")

    # ── Tabs ──
    tab1, tab_summary, tab2, tab_about = st.tabs(
        ["📊 Dashboard", "📑 Executive Summary", "🗂️ Economic Tables", "ℹ️ About"])

    # ══════════════════════════════════════════════════════════
    # ── TAB 1: Dashboard ──
    # ══════════════════════════════════════════════════════════
    with tab1:
        if live_prices.get("status") == "success":
            st.markdown("##### 🌍 Live Global Oil Market (Reference Only)")
            p1, p2, _, _ = st.columns(4)
            p1.metric("Brent Crude (BZ=F)",
                      f"${live_prices['brent']['price']:.2f}/bbl",
                      f"{live_prices['brent']['change']:.2f}%")
            p2.metric("WTI Crude (CL=F)",
                      f"${live_prices['wti']['price']:.2f}/bbl",
                      f"{live_prices['wti']['change']:.2f}%")
            st.markdown("---")

        st.markdown("### 🏆 Key Economic Indicators")
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        c1.metric("Reserve (MMBO)",
                  f"{sum_prod_mstb / 1000:.4f}")
        c2.metric(f"NPV @{discount_rate*100:.0f}% (MUS$)",
                  f"{npv_base:,.2f}")
        c3.metric("IRR Full Cycle",
                  f"{irr_base:.2%}" if not np.isnan(irr_base) else "N/A")
        c4.metric("Gov Take (%)",
                  f"{gov_take_pct:.2%}")
        c5.metric("Payback Year", payback_year)
        c6.metric("Break-Even Price",
                  f"${bep_price:.0f}/bbl" if not np.isnan(float(bep_price)) else "N/A")
        st.markdown("---")

        cc1, cc2 = st.columns(2)
        with cc1:
            fig_prod = make_subplots(specs=[[{"secondary_y": True}]])
            fig_prod.add_trace(go.Bar(x=results['years'], y=results['prod_bopd'],
                                      name="BOPD", marker_color=SLATE), secondary_y=False)
            fig_prod.add_trace(go.Scatter(x=results['years'],
                                           y=np.cumsum(results['prod_mstb']),
                                           name="Cum. Prod (MSTB)",
                                           line=dict(color=AMBER, width=3)),
                               secondary_y=True)
            fig_prod.update_layout(**plotly_layout("📈 Production Profile & Cumulative"))
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
            fig_cf.update_layout(**plotly_layout("💵 Contractor Net Cash Flow"),
                                  yaxis_title="MUS$")
            st.plotly_chart(fig_cf, use_container_width=True)

        st.markdown("---")
        cc3, cc4 = st.columns(2)

        with cc3:
            st.markdown("### 🌊 PSC Distribution Waterfall")
            fig_wf = go.Figure(go.Waterfall(
                orientation="v",
                measure=["relative","relative","relative","relative","relative","relative","total"],
                x=["Gross Revenue","Cost Recovery","Gov FTP","Gov Equity",
                   "DMO Penalty","Corp Tax","Contractor Take"],
                y=[total_gross_revenue,
                   -sum_cost_recovery,
                   -sum_ftp_gov,
                   -sum_ets_gov,
                   -sum_dmo_penalty,
                   -sum_tax,
                   total_ctr_take_at],
                decreasing=dict(marker=dict(color="#C05050")),
                increasing=dict(marker=dict(color=SLATE)),
                totals=dict(marker=dict(color=AMBER)),
            ))
            fig_wf.update_layout(**plotly_layout("Revenue Distribution Waterfall"))
            st.plotly_chart(fig_wf, use_container_width=True)

        with cc4:
            st.markdown("### 🥧 Gross Revenue Allocation")
            fig_pie = go.Figure(data=[go.Pie(
                labels=['Cost Recovery', 'Government Take', 'Contractor Take (After Tax)'],
                values=[sum_cost_recovery, total_gov_take, total_ctr_take_at],
                hole=.4,
                marker_colors=[SLATE, MUTED, AMBER],
                textinfo='label+percent',
            )])
            fig_pie.update_layout(**plotly_layout("Proporsi Pembagian Total Pendapatan"))
            st.plotly_chart(fig_pie, use_container_width=True)

    # ══════════════════════════════════════════════════════════
    # ── TAB Summary ──
    # ══════════════════════════════════════════════════════════
    with tab_summary:
        st.subheader("📑 Executive Summary Report")

        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown("#### 🛢️ Production Profile")
            st.markdown(f"""
| Indicator | Unit | Value |
| :--- | :--- | ---: |
| **Oil Production** | MSTB | {sum_prod_mstb:,.4f} |
| **Average Oil Price** | USD/bbl | {avg_oil_price:,.4f} |
| **Gross Revenue** | MUSD | {total_gross_revenue:,.4f} |
""")
            st.markdown("#### ✂️ Split")
            st.markdown(f"""
| Indicator | Unit | Gov. | Ctr. | Total |
| :--- | :--- | ---: | ---: | ---: |
| **FTP** | MUSD | {sum_ftp_gov:,.4f} | {sum_ftp_ctr:,.4f} | {sum_ftp_total:,.4f} |
| **ETS** | MUSD | {sum_ets_gov:,.4f} | {sum_ets_ctr:,.4f} | {sum_ets_total:,.4f} |
""")

        with col_s2:
            st.markdown("#### 💰 Investment & OPEX")
            st.markdown(f"""
| Indicator | Unit | Value |
| :--- | :--- | ---: |
| **Sunk Cost** | MUSD | {sum_sunk_cost:,.4f} |
| **Tangible** | MUSD | {sum_tangible:,.4f} |
| **Intangible** | MUSD | {sum_intangible:,.4f} |
| **Total OPEX** | MUSD | {sum_opex:,.4f} |
""")
            st.markdown("#### 💵 Cost Recovery")
            st.markdown(f"""
| Indicator | Unit | Value |
| :--- | :--- | ---: |
| **Cost Recovery** | MUSD | {sum_cost_recovery:,.4f} |
| **% Cost Recovery** | % | {pct_cost_recovery:,.4%} |
""")

        st.markdown("---")
        col_s3, col_s4 = st.columns(2)
        with col_s3:
            st.markdown("#### 🏛️ Government Profitability")
            st.markdown(f"""
| Indicator | Unit | Value |
| :--- | :--- | ---: |
| **Gov. FTP** | MUSD | {sum_ftp_gov:,.4f} |
| **Gov. ETS** | MUSD | {sum_ets_gov:,.4f} |
| **Net DMO** | MUSD | {sum_dmo_penalty:,.4f} |
| **Tax** | MUSD | {sum_tax:,.4f} |
| **Gov Share** | MUSD | {total_gov_take:,.4f} |
| **% Gov Share** | % | {pct_gov_share:,.4%} |
""")

        with col_s4:
            st.markdown("#### 👷 Contractor Profitability")
            st.markdown(f"""
| Indicator | Unit | Value |
| :--- | :--- | ---: |
| **Ctr Share (AT)** | MUSD | {total_ctr_take_at:,.4f} |
| **% Ctr Share** | % | {pct_ctr_share:,.4%} |
| **NPV PF** | MUSD | {npv_base:,.4f} |
| **IRR FC** | % | {f"{irr_base:.4%}" if not np.isnan(irr_base) else "N/A"} |
""")

    # ══════════════════════════════════════════════════════════
    # ── TAB 2: Economic Tables ──
    # ══════════════════════════════════════════════════════════
    with tab2:
        st.subheader("📋 Annual Economic Summary")

        st.markdown("##### 🛢️ Group 1: Production & Revenue")
        df_g1 = pd.DataFrame({
            "Year":            results['years'],
            "Lifting (MSTB)":  results['prod_mstb'],
            "Price (USD/bbl)": results['oil_price_arr'],
            "GR (MUSD)":       results['gross_revenue'],
            "FTP (MUSD)":      results['ftp'],
            "GR-FTP (MUSD)":   results['gr_minus_ftp'],
        })
        st.dataframe(df_g1.style.format({c: "{:,.4f}" for c in df_g1.columns if c != "Year"}),
                     use_container_width=True)

        st.markdown("##### 💵 Group 2: Cost Recovery")
        df_g2 = pd.DataFrame({
            "Year":                         results['years'],
            "Dep. CAPEX I (MUSD)":          results['dep_capex1'],
            "Dep. CAPEX II (MUSD)":         results['dep_capex2'],
            "CAPEX III Intangible (MUSD)":  results['intangible_amort'],
            "Total OPEX (MUSD)":            results['opex'],
            "Total Cost (MUSD)":            results['total_costs_amort'],
            "Recovered (MUSD)":             results['recovered'],
            "Unrecovered (MUSD)":           results['unrecovered'],
        })
        st.dataframe(df_g2.style.format({c: "{:,.4f}" for c in df_g2.columns if c != "Year"}),
                     use_container_width=True)

        st.markdown("##### ⚖️ Group 3: Equity Split")
        df_g3 = pd.DataFrame({
            "Year":              results['years'],
            "ETS (MUSD)":        results['ets'],
            "Gov Equity (MUSD)": results['gov_equity'],
            "Ctr Equity (MUSD)": results['ctr_equity'],
        })
        st.dataframe(df_g3.style.format({c: "{:,.4f}" for c in df_g3.columns if c != "Year"}),
                     use_container_width=True)

        st.markdown("##### 🤝 Group 4: First Tranche Petroleum (FTP)")
        df_g4 = pd.DataFrame({
            "Year":           results['years'],
            "FTP (MUSD)":     results['ftp'],
            "Gov FTP (MUSD)": results['gov_ftp'],
            "Ctr FTP (MUSD)": results['ctr_ftp'],
        })
        st.dataframe(df_g4.style.format({c: "{:,.4f}" for c in df_g4.columns if c != "Year"}),
                     use_container_width=True)

        st.markdown("##### 🏛️ Group 5: DMO & Taxes")
        df_g5 = pd.DataFrame({
            "Year":                  results['years'],
            "Ctr FTP (MUSD)":        results['ctr_ftp'],
            "Ctr ETS (MUSD)":        results['ctr_equity'],
            "DMO Gross (MUSD)":      results['dmo_gross'],
            "DMO Fee (MUSD)":        results['dmo_fee'],
            "Taxable Income (MUSD)": results['taxable_income'],
            "Tax Paid (MUSD)":       results['tax_paid'],
        })
        st.dataframe(df_g5.style.format({c: "{:,.4f}" for c in df_g5.columns if c != "Year"}),
                     use_container_width=True)

        st.markdown("##### 💰 Group 6: Cash Flow")
        df_g6 = pd.DataFrame({
            "Year":            results['years'],
            "Cash In (MUSD)":  results['cash_in'],
            "Cash Out (MUSD)": results['cash_out'],
            "Net CF (MUSD)":   results['net_cf'],
            "Cum. CF (MUSD)":  np.cumsum(results['net_cf']),
        })
        st.dataframe(df_g6.style.format({c: "{:,.4f}" for c in df_g6.columns if c != "Year"}),
                     use_container_width=True)

    # ── TAB About ──
    with tab_about:
        st.markdown("""
        <div class="sl-card">
          <div class="sl-section-tag">About SplitLogic – Cost Recovery Module</div>
          <h3>PSC Cost Recovery Financial Modeller</h3>
          <p>
            Modul ini memodelkan skema <strong>Production Sharing Contract (PSC) Cost Recovery</strong>
            yang merupakan mekanisme kontrak antara Pemerintah dan Kontraktor dimana biaya operasional
            dan investasi Kontraktor dapat dikembalikan melalui mekanisme Cost Recovery sebelum bagi hasil dilakukan.
          </p>
          <hr/>
          <h4>Fitur Utama</h4>
          <ul>
            <li>Production profile modeling dengan tabel lifting dan harga interaktif</li>
            <li>CAPEX (Tangible I & II, Intangible) & OPEX (I-VI) interaktif dengan VAT boolean per baris</li>
            <li>Escalation Factor per tahun yang diterapkan ke seluruh komponen OPEX</li>
            <li>Depreciation terintegrasi PIS Year (Straight Line, Declining Balance, Unit of Production, dll)</li>
            <li>FTP (Shared/Not Shared), Cost Recovery, Equity Split, DMO, dan Pajak</li>
            <li>Metrik NPV (discounted dari tahun pilihan), IRR, Payback Year, Break-Even Price</li>
          </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="footer-text">SplitLogic v1.1 · Cost Recovery Module · © 2026</div>',
                unsafe_allow_html=True)
#endregion

#region Gross Split
# ───────────────────────────────────────────
# 6. GROSS SPLIT MODULE
# ───────────────────────────────────────────
else:

    # ══════════════════════════════════════════════════════════
    # ── SPLIT CALCULATION ENGINE
    # ══════════════════════════════════════════════════════════
    BASE_SPLIT = {
        "Minyak Bumi": {"gov": 57.0, "cont": 43.0},
        "Gas Bumi":    {"gov": 52.0, "cont": 48.0},
    }

    def calc_field_status(status):
        return {"POD I": 5.0, "POD II": 3.0, "No POD": 0.0}.get(status, 0.0)

    def calc_field_location(depth_m, is_offshore):
        if not is_offshore: return 0.0
        if depth_m <= 20:   return 8.0
        if depth_m <= 50:   return 10.0
        if depth_m <= 150:  return 12.0
        if depth_m <= 1000: return 14.0
        return 16.0

    def calc_reservoir_depth(depth_m):
        return 1.0 if depth_m > 2500 else 0.0

    def calc_infrastructure(infra):
        return {"Well Developed": 0.0, "New Frontier Offshore": 2.0,
                "New Frontier Onshore": 4.0}.get(infra, 0.0)

    def calc_reservoir_type(rtype):
        return {"Konvensional (Sandstone / Limestone / Carbonate)": 0.0,
                "Non-Konvensional (Shale / CBM)": 15.0}.get(rtype, 0.0)

    def calc_co2(pct):
        if pct < 5:  return 0.0
        if pct < 10: return 0.5
        if pct < 20: return 1.0
        if pct < 40: return 1.5
        if pct < 60: return 2.0
        return 4.0

    def calc_h2s(ppm):
        if ppm < 100:  return 0.0
        if ppm < 1000: return 1.0
        if ppm < 2000: return 2.0
        if ppm < 3000: return 3.0
        if ppm < 4000: return 4.0
        return 5.0

    def calc_sg(api):
        return 1.0 if api < 25 else 0.0

    def calc_tkdn(pct):
        if pct < 30: return 0.0
        if pct < 50: return 2.0
        if pct < 70: return 3.0
        return 4.0

    def calc_prod_stage(stage):
        return {"Primary": 0.0, "Sekunder (Injeksi Air / Gas)": 6.0,
                "Tersier (EOR)": 10.0}.get(stage, 0.0)

    def calc_oil_price(icp):
        if icp >= 85: return 0.0
        return (85 - icp) * 0.25

    def calc_gas_price(price):
        if price < 7:  return (7 - price) * 2.5
        if price < 10: return 0.0
        return (price - 10) * 2.5

    def calc_nett_prod(mmboe):
        if mmboe < 30:  return 10.0
        if mmboe < 60:  return 9.0
        if mmboe < 90:  return 8.0
        if mmboe < 125: return 6.0
        if mmboe < 175: return 4.0
        return 0.0

    def calculate_gross_split(params):
        """Hitung split untuk satu set parameter (digunakan per-tahun & sensitivitas)."""
        commodity = params["commodity"]
        base      = BASE_SPLIT[commodity]
        fc = {
            "Status Lapangan":     calc_field_status(params["field_status"]),
            "Lokasi Lapangan":     calc_field_location(params["water_depth"], params["is_offshore"]),
            "Kedalaman Reservoir": calc_reservoir_depth(params["reservoir_depth"]),
            "Infrastruktur":       calc_infrastructure(params["infrastructure"]),
            "Jenis Reservoir":     calc_reservoir_type(params["reservoir_type"]),
            "Kandungan CO2":       calc_co2(params["co2_pct"]),
            "Kandungan H2S":       calc_h2s(params["h2s_ppm"]),
            "SG (API)":            calc_sg(params["api"]),
            "TKDN":                calc_tkdn(params["tkdn_pct"]),
            "Tahapan Produksi":    calc_prod_stage(params["prod_stage"]),
        }
        pc = {}
        if commodity == "Minyak Bumi":
            pc["Harga Minyak (ICP)"]          = calc_oil_price(params.get("icp_price", 85))
        else:
            pc["Harga Gas Bumi"]              = calc_gas_price(params.get("gas_price", 8))
        pc["Kumulatif Produksi (MMBOE)"]      = calc_nett_prod(params["nett_prod"])

        ministerial = params.get("ministerial_adj", 0.0)
        total_corr  = sum(fc.values()) + sum(pc.values()) + ministerial
        final_cont  = base["cont"] + total_corr
        final_gov   = 100.0 - final_cont

        return dict(commodity=commodity, base_gov=base["gov"], base_cont=base["cont"],
                    fixed_comps=fc, progressive_comps=pc, ministerial_adj=ministerial,
                    total_correction=total_corr, final_cont=final_cont, final_gov=final_gov)

    # ══════════════════════════════════════════════════════════
    # ── CHART HELPERS
    # ══════════════════════════════════════════════════════════
    def donut_chart_gs(gov_pct, cont_pct, label="Final Split"):
        fig = go.Figure(go.Pie(
            labels=["Pemerintah", "Kontraktor"],
            values=[round(gov_pct, 4), round(cont_pct, 4)],
            hole=0.65,
            marker=dict(colors=[SLATE, AMBER],
                        line=dict(color="rgba(13,27,42,1)", width=3)),
            textfont=dict(family="Syne", size=13, color="#E8EEF4"),
            hovertemplate="<b>%{label}</b><br>%{value:.2f}%<extra></extra>",
        ))
        fig.add_annotation(text=f"<b>{label}</b>", x=0.5, y=0.5, showarrow=False,
                           font=dict(family="Syne", size=12, color=MUTED), align="center")
        fig.update_layout(**plotly_layout(height=320))
        return fig

    def waterfall_chart_gs(result):
        labels  = (["Base (Kontraktor)"]
                   + list(result["fixed_comps"].keys())
                   + list(result["progressive_comps"].keys())
                   + (["Diskresi Menteri"] if result["ministerial_adj"] != 0 else [])
                   + ["Final (Kontraktor)"])
        values  = ([result["base_cont"]]
                   + list(result["fixed_comps"].values())
                   + list(result["progressive_comps"].values())
                   + ([result["ministerial_adj"]] if result["ministerial_adj"] != 0 else [])
                   + [result["final_cont"]])
        measure = ["absolute"] + ["relative"] * (len(labels) - 2) + ["total"]
        fig = go.Figure(go.Waterfall(
            orientation="v", measure=measure, x=labels, y=values,
            text=[f"{v:+.2f}%" if m == "relative" else f"{v:.2f}%"
                  for m, v in zip(measure, values)],
            textposition="outside",
            textfont=dict(family="DM Sans", size=10, color="#E8EEF4"),
            connector=dict(line=dict(color=MUTED, width=1, dash="dot")),
            increasing=dict(marker=dict(color="#5DA897")),
            decreasing=dict(marker=dict(color="#C05050")),
            totals=dict(marker=dict(color=AMBER)),
        ))
        fig.update_layout(**plotly_layout("Waterfall - Koreksi Split Kontraktor", height=440),
                          xaxis=dict(tickangle=-35, tickfont=dict(size=10, color=MUTED),
                                     gridcolor="rgba(255,255,255,0.04)"),
                          yaxis=dict(title="Split Kontraktor (%)",
                                     gridcolor="rgba(255,255,255,0.04)"),
                          showlegend=False)
        return fig

    def bar_comparison_gs(result):
        cats = (list(result["fixed_comps"].keys())
                + list(result["progressive_comps"].keys())
                + (["Diskresi Menteri"] if result["ministerial_adj"] != 0 else []))
        vals = (list(result["fixed_comps"].values())
                + list(result["progressive_comps"].values())
                + ([result["ministerial_adj"]] if result["ministerial_adj"] != 0 else []))
        fig = go.Figure(go.Bar(
            x=cats, y=vals,
            marker=dict(color=[AMBER if v > 0 else "#C05050" for v in vals],
                        line=dict(color="rgba(0,0,0,0.3)", width=1)),
            text=[f"{v:+.2f}%" for v in vals],
            textposition="outside",
            textfont=dict(family="DM Sans", size=10, color="#E8EEF4"),
        ))
        fig.update_layout(**plotly_layout("Koreksi per Komponen (% Split Kontraktor)", height=400),
                          xaxis=dict(tickangle=-35, tickfont=dict(size=10, color=MUTED),
                                     gridcolor="rgba(255,255,255,0.04)"),
                          yaxis=dict(title="Koreksi (%)",
                                     gridcolor="rgba(255,255,255,0.04)"),
                          showlegend=False)
        return fig

    # ══════════════════════════════════════════════════════════
    # ── SIDEBAR INPUTS
    # ══════════════════════════════════════════════════════════
    with st.sidebar:
        st.markdown("### Input Parameter")

        # ── Production Profile ──
        with st.sidebar.expander("Production Profile", expanded=True):
            col_sy, col_ey = st.columns(2)
            start_year = col_sy.number_input("Start Year", value=2022, step=1, key="gs_sy")
            end_year   = col_ey.number_input("End Year",   value=2040, step=1, key="gs_ey")

            num_years = max(1, end_year - start_year + 1)

            default_lifting = [
                0.0000, 403.2517, 2180.7837, 3574.9866, 3800.9527,
                3216.8753, 2564.7615, 2023.5689, 1617.4838, 1314.8373,
                1078.2295, 881.4653, 737.0439, 621.7578, 519.4544,
                437.4333, 376.8032, 326.5546, 285.1195
            ]
            if num_years > len(default_lifting):
                default_lifting += [0.0] * (num_years - len(default_lifting))
            else:
                default_lifting = default_lifting[:num_years]

            default_prices = [65.0] * num_years

            df_prod_init = pd.DataFrame({
                "Year":            range(start_year, end_year + 1),
                "Lifting (MSTB)":  default_lifting,
                "Price (USD/bbl)": default_prices,
            })
            edit_prod = st.data_editor(df_prod_init, hide_index=True,
                                       use_container_width=True, key="gs_editor_prod")

        # ── VAT Rate ──
        with st.sidebar.expander("VAT Rate", expanded=False):
            df_vat_init = pd.DataFrame({
                "Year":     range(start_year, end_year + 1),
                "VAT Rate": [0.00] * num_years,
            })
            edit_vat = st.data_editor(df_vat_init, hide_index=True,
                                      use_container_width=True, key="gs_editor_vat")

        # ── Escalation Factor ──
        with st.sidebar.expander("Escalation Factor (%/year)", expanded=False):
            df_esc_init = pd.DataFrame({
                "Year":            range(start_year, end_year + 1),
                "Esc. Factor (%)": [0.00] * num_years,
            })
            edit_esc = st.data_editor(df_esc_init, hide_index=True,
                                      use_container_width=True, key="gs_editor_esc")

        # ── Gas Toll Fee ──
        with st.sidebar.expander("Gas Toll Fee", expanded=False):
            df_gtf_init = pd.DataFrame({
                "Year":                range(start_year, end_year + 1),
                "Gas Toll Fee (MUSD)": [0.00] * num_years,
            })
            edit_gtf = st.data_editor(df_gtf_init, hide_index=True,
                                      use_container_width=True, key="gs_editor_gtf")

        # ── VAT helper ──
        def gs_after_vat(base_vals, vat_flags, vat_rates):
            return [v * (1 + r) if flag else v
                    for v, flag, r in zip(base_vals, vat_flags, vat_rates)]

        vat_rates_gs = edit_vat["VAT Rate"].tolist()

        # ── CAPEX I (Drilling & Workover) ──
        with st.sidebar.expander("CAPEX I (Drilling & Workover)", expanded=False):
            default_c1 = [0.0, 569.43, 261.96]
            if num_years > len(default_c1):
                default_c1 += [0.0] * (num_years - len(default_c1))
            else:
                default_c1 = default_c1[:num_years]

            df_c1_init = pd.DataFrame({
                "Year":            list(range(start_year, end_year + 1)),
                "Tangible (MU)":   default_c1,
                "Association":     ["Oil"] * num_years,
                "PIS Year":        [2023]  * num_years,
                "Useful Life (y)": [5]     * num_years,
                "Depreciation":    ["25%"] * num_years,
                "VAT":             [True]  * num_years,
                "Tangible After":  gs_after_vat(default_c1, [True]*num_years, vat_rates_gs),
            })
            edit_capex_1 = st.data_editor(
                df_c1_init, hide_index=True, use_container_width=True,
                key="gs_editor_capex_1",
                column_config={
                    "VAT": st.column_config.CheckboxColumn("VAT"),
                    "Tangible After": st.column_config.NumberColumn(
                        "Tangible After (MU)", disabled=True),
                },
            )
            c1_after = gs_after_vat(
                edit_capex_1["Tangible (MU)"].tolist(),
                edit_capex_1["VAT"].tolist(),
                vat_rates_gs,
            )

        # ── CAPEX II (Production Facilities) ──
        with st.sidebar.expander("CAPEX II (Production Facilities)", expanded=False):
            default_c2 = [0.0, 584.9824, 4196.1153, 2204.392]
            if num_years > len(default_c2):
                default_c2 += [0.0] * (num_years - len(default_c2))
            else:
                default_c2 = default_c2[:num_years]

            df_c2_init = pd.DataFrame({
                "Year":            list(range(start_year, end_year + 1)),
                "Tangible (MU)":   default_c2,
                "Association":     ["Oil"] * num_years,
                "PIS Year":        [2023]  * num_years,
                "Useful Life (y)": [5]     * num_years,
                "Depreciation":    ["25%"] * num_years,
                "VAT":             [True]  * num_years,
                "Tangible After":  gs_after_vat(default_c2, [True]*num_years, vat_rates_gs),
            })
            edit_capex_2 = st.data_editor(
                df_c2_init, hide_index=True, use_container_width=True,
                key="gs_editor_capex_2",
                column_config={
                    "VAT": st.column_config.CheckboxColumn("VAT"),
                    "Tangible After": st.column_config.NumberColumn(
                        "Tangible After (MU)", disabled=True),
                },
            )
            c2_after = gs_after_vat(
                edit_capex_2["Tangible (MU)"].tolist(),
                edit_capex_2["VAT"].tolist(),
                vat_rates_gs,
            )

        # ── CAPEX III (Intangible) ──
        with st.sidebar.expander("CAPEX III (Intangible)", expanded=False):
            default_c3 = [0.0, 2322.12, 1064.49]
            if num_years > len(default_c3):
                default_c3 += [0.0] * (num_years - len(default_c3))
            else:
                default_c3 = default_c3[:num_years]

            df_c3_init = pd.DataFrame({
                "Year":             list(range(start_year, end_year + 1)),
                "Intangible (MU)":  default_c3,
                "VAT":              [True] * num_years,
                "Intangible After": gs_after_vat(default_c3, [True]*num_years, vat_rates_gs),
            })
            edit_capex_3 = st.data_editor(
                df_c3_init, hide_index=True, use_container_width=True,
                key="gs_editor_capex_3",
                column_config={
                    "VAT": st.column_config.CheckboxColumn("VAT"),
                    "Intangible After": st.column_config.NumberColumn(
                        "Intangible After (MU)", disabled=True),
                },
            )
            c3_after = gs_after_vat(
                edit_capex_3["Intangible (MU)"].tolist(),
                edit_capex_3["VAT"].tolist(),
                vat_rates_gs,
            )

        # ── OPEX helper (sama persis dengan Cost Recovery) ──
        def make_gs_opex_df(default_vals, key_suffix):
            df = pd.DataFrame({
                "Year":        list(range(start_year, end_year + 1)),
                "Opex (MUSD)": default_vals,
                "VAT":         [True] * num_years,
                "Opex After":  gs_after_vat(default_vals, [True]*num_years, vat_rates_gs),
            })
            return st.data_editor(
                df, hide_index=True, use_container_width=True,
                key=f"gs_editor_opex_{key_suffix}",
                column_config={
                    "VAT": st.column_config.CheckboxColumn("VAT"),
                    "Opex After": st.column_config.NumberColumn(
                        "Opex After (MUSD)", disabled=True),
                },
            )

        with st.sidebar.expander("OPEX I (WIWS)", expanded=False):
            edit_opex_1 = make_gs_opex_df([0.0] * num_years, "1")

        with st.sidebar.expander("OPEX II (Operation & Maintenance)", expanded=False):
            edit_opex_2 = make_gs_opex_df([0.0] * num_years, "2")

        with st.sidebar.expander("OPEX III (Electricity)", expanded=False):
            default_o3 = [0.0, 2037.7363, 8625.7219, 6863.8197, 4119.1711,
                          4024.5949, 3943.3438, 3873.027,  3811.7665, 3758.0713,
                          3710.7449, 3668.8183, 3631.5001, 3598.1389, 2982.3002,
                          2908.4958, 2887.0137, 2867.5344, 2849.12]
            if num_years > len(default_o3):
                default_o3 += [0.0] * (num_years - len(default_o3))
            else:
                default_o3 = default_o3[:num_years]
            edit_opex_3 = make_gs_opex_df(default_o3, "3")

        with st.sidebar.expander("OPEX IV (ASR)", expanded=False):
            default_o4 = [0.0, 0.0] + [21.9516] * max(0, num_years - 2)
            edit_opex_4 = make_gs_opex_df(default_o4[:num_years], "4")

        with st.sidebar.expander("OPEX V (LBT)", expanded=False):
            edit_opex_5 = make_gs_opex_df([0.0] * num_years, "5")

        with st.sidebar.expander("OPEX VI (Carbon Tax)", expanded=False):
            edit_opex_6 = make_gs_opex_df([0.0] * num_years, "6")

        # ── Gross Split Field Parameters ──
        st.markdown('<div class="sl-section-tag">Komoditas</div>', unsafe_allow_html=True)
        commodity = st.radio("Jenis Komoditas", ["Minyak Bumi", "Gas Bumi"], horizontal=True)

        st.markdown("---")
        st.markdown('<div class="sl-section-tag">Fixed Components</div>', unsafe_allow_html=True)

        field_status = st.selectbox("1. Status Lapangan", ["No POD", "POD I", "POD II"])
        is_offshore  = st.radio("Lokasi Lapangan", ["Onshore", "Offshore"],
                                horizontal=True) == "Offshore"
        water_depth  = (st.number_input("2. Kedalaman Air (m)", min_value=0.0,
                                        value=0.0, step=1.0)
                        if is_offshore else 0.0)
        if not is_offshore:
            st.markdown("**2. Lokasi:** Onshore Koreksi **0%**")

        reservoir_depth = st.number_input("3. Kedalaman Reservoir (m)",
                                          min_value=0.0, value=0.0, step=50.0)
        infrastructure  = st.selectbox("4. Infrastruktur",
                                       ["Well Developed", "New Frontier Offshore",
                                        "New Frontier Onshore"])
        reservoir_type  = st.selectbox("5. Jenis Reservoir",
                                       ["Konvensional (Sandstone / Limestone / Carbonate)",
                                        "Non-Konvensional (Shale / CBM)"])
        co2_pct   = st.number_input("6. CO2 (%)", min_value=0.0, max_value=100.0,
                                    value=0.0, step=0.5)
        h2s_ppm   = st.number_input("7. H2S (ppm)", min_value=0.0, value=0.0, step=10.0)
        api       = st.number_input("8. API (API)", min_value=0.0, max_value=70.0,
                                    value=0.0, step=0.5)
        tkdn_pct  = st.number_input("9. TKDN (%)", min_value=0.0, max_value=100.0,
                                    value=0.0, step=1.0)
        prod_stage = st.selectbox("10. Tahapan Produksi",
                                  ["Primary", "Sekunder (Injeksi Air / Gas)", "Tersier (EOR)"])

        st.markdown("---")
        st.markdown('<div class="sl-section-tag">Pasal 7 - Diskresi Menteri</div>',
                    unsafe_allow_html=True)
        ministerial_adj = st.number_input(
            "Tambahan / Pengurangan Split Kontraktor (%)", value=0.0, step=0.5)

        # ── Fiscal Terms ──
        with st.sidebar.expander("Fiscal & Split Terms", expanded=True):
            tax_rate             = st.number_input("Cont. Eff. Tax Rate (%)",
                                                   value=37.00, step=1.0, key="gs_tax")      / 100
            dmo_volume_rate      = st.number_input("DMO Volume (%)",
                                                   value=25.00, step=1.0, key="gs_dmo_vol")  / 100
            dmo_fee_rate         = st.number_input("DMO Fee (%)",
                                                   value=25.00, step=1.0, key="gs_dmo_fee")  / 100
            dmo_holiday_years    = st.number_input("DMO Holiday Duration (years)",
                                                   value=5, step=1, key="gs_dmo_hol")
            discount_rate        = st.number_input("Discount Factor (%)",
                                                   value=10.00, step=1.0, key="gs_disc")     / 100
            discount_factor_year = st.number_input("Discount Factor Year",
                                                   value=2023, step=1, key="gs_disc_yr")

        with st.sidebar.expander("Method Selection", expanded=True):
            depreciation_method = st.selectbox(
                "Depreciation Method",
                ["Straight Line", "Declining Balance", "Double Declining Balance",
                 "Unit of Production", "Sum of the Year"],
                key="gs_dep_method",
            )

    # ══════════════════════════════════════════════════════════
    # ── BASE SPLIT (tampilan & sensitivitas)
    # ══════════════════════════════════════════════════════════
    initial_price    = edit_prod["Price (USD/bbl)"].iloc[0] if len(edit_prod) > 0 else 65.0
    initial_cum_prod = edit_prod["Lifting (MSTB)"].sum() / 1000

    base_params = dict(
        commodity=commodity, field_status=field_status, is_offshore=is_offshore,
        water_depth=water_depth, reservoir_depth=reservoir_depth,
        infrastructure=infrastructure, reservoir_type=reservoir_type,
        co2_pct=co2_pct, h2s_ppm=h2s_ppm, api=api, tkdn_pct=tkdn_pct,
        prod_stage=prod_stage,
        icp_price=initial_price if commodity == "Minyak Bumi" else 0.0,
        gas_price=initial_price if commodity == "Gas Bumi" else 0.0,
        nett_prod=initial_cum_prod,
        ministerial_adj=ministerial_adj,
    )
    result_base = calculate_gross_split(base_params)

    # ══════════════════════════════════════════════════════════
    # ── PSC GROSS SPLIT ECONOMIC ENGINE
    # ══════════════════════════════════════════════════════════
    def run_gs_model(override_oil_price=None, capex_mult=1.0):
        """
        Engine ekonomi PSC Gross Split.

        Alur per tahun:
          1.  Escalation multiplier (kumulatif, basis = tahun produksi pertama)
          2.  Split dinamis per tahun (harga tahun-i + cum prod rolling)
          3.  Gross Revenue  = Lifting x Price
          4.  Gas Toll Fee   dikurangkan dari Gross Revenue
          5.  Net Revenue    = Gross Revenue - Gas Toll Fee
          6.  Ctr Revenue    = Net Revenue x final_cont%
          7.  Gov Revenue    = Net Revenue x final_gov%
          8.  DMO            dari Ctr Revenue (volume & fee rate + holiday)
          9.  CAPEX I & II   disusutkan berdasarkan PIS Year & Useful Life
          10. CAPEX III      dibebankan penuh tahun berjalan (intangible)
          11. OPEX           setelah VAT & escalation
          12. Taxable Income = max(0, Ctr Revenue - DMO Penalty - OPEX - CAPEX total)
          13. Tax            = Taxable Income x tax_rate
          14. Net CF         = Ctr Revenue - DMO Penalty - OPEX - CAPEX total - Tax
        """
        total_years   = len(edit_prod)
        years_array   = edit_prod["Year"].values
        prod_mstb     = edit_prod["Lifting (MSTB)"].values.astype(float)
        prod_bopd     = (prod_mstb * 1000) / 365

        non_zero_idx  = np.where(prod_mstb > 0)[0]
        prod_start_yr = int(non_zero_idx[0]) if len(non_zero_idx) > 0 else 0

        # ── Escalation multiplier ──
        esc_pct  = edit_esc["Esc. Factor (%)"].values.astype(float) / 100.0
        esc_mult = np.ones(total_years)
        for i in range(1, total_years):
            esc_mult[i] = esc_mult[i - 1] * (1.0 + esc_pct[i])
        base_esc = esc_mult[prod_start_yr] if prod_start_yr < total_years else 1.0
        esc_mult = esc_mult / base_esc if base_esc != 0 else esc_mult

        # ── Gas Toll Fee ──
        gtf_arr = edit_gtf["Gas Toll Fee (MUSD)"].values.astype(float)

        # ── CAPEX arrays (After-VAT + multiplier) ──
        capex_tangible   = np.zeros(total_years)
        capex_intangible = np.zeros(total_years)
        dep_capex1       = np.zeros(total_years)
        dep_capex2       = np.zeros(total_years)
        depreciation     = np.zeros(total_years)

        def calc_dep(asset_value, start_idx, life, method, prod_profile=None):
            arr      = np.zeros(total_years)
            if asset_value <= 0 or start_idx >= total_years:
                return arr
            life     = max(int(life), 1)
            book_val = float(asset_value)

            if method == "Straight Line":
                dep_amt = asset_value / life
                for k in range(life):
                    y = start_idx + k
                    if y >= total_years: break
                    actual   = min(dep_amt, book_val)
                    arr[y]   = actual
                    book_val -= actual

            elif method == "Declining Balance":
                rate = 1.0 / life
                for k in range(life):
                    y = start_idx + k
                    if y >= total_years: break
                    if k == life - 1 or book_val <= 0:
                        arr[y] = book_val; book_val = 0; break
                    dep = book_val * rate
                    arr[y] = dep; book_val -= dep

            elif method == "Double Declining Balance":
                rate = 2.0 / life
                for k in range(life):
                    y = start_idx + k
                    if y >= total_years: break
                    if k == life - 1 or book_val <= 0:
                        arr[y] = book_val; book_val = 0; break
                    dep = book_val * rate
                    arr[y] = dep; book_val -= dep

            elif method == "Unit of Production":
                if prod_profile is not None:
                    total_prod = np.sum(prod_profile[start_idx:])
                    if total_prod > 0:
                        for y in range(start_idx, total_years):
                            if book_val <= 0: break
                            dep      = asset_value * (prod_profile[y] / total_prod)
                            actual   = min(dep, book_val)
                            arr[y]   = actual; book_val -= actual

            elif method in ("Sum of the Year", "Sum of The Year"):
                syd = life * (life + 1) / 2.0
                for k in range(life):
                    y = start_idx + k
                    if y >= total_years: break
                    if k == life - 1:
                        arr[y] = book_val; break
                    dep = asset_value * (life - k) / syd
                    arr[y] = dep; book_val -= dep

            return arr

        for i in range(total_years):
            # CAPEX I
            t1 = float(c1_after[i]) * capex_mult
            if t1 > 0:
                pis_yr  = int(edit_capex_1["PIS Year"].iloc[i])
                idx_pis = int(np.clip(np.searchsorted(years_array, pis_yr),
                                      prod_start_yr, total_years - 1))
                d1 = calc_dep(t1, idx_pis,
                              int(edit_capex_1["Useful Life (y)"].iloc[i]),
                              depreciation_method, prod_profile=prod_mstb)
                dep_capex1  += d1
                depreciation += d1
            capex_tangible[i] += t1

            # CAPEX II
            t2 = float(c2_after[i]) * capex_mult
            if t2 > 0:
                pis_yr  = int(edit_capex_2["PIS Year"].iloc[i])
                idx_pis = int(np.clip(np.searchsorted(years_array, pis_yr),
                                      prod_start_yr, total_years - 1))
                d2 = calc_dep(t2, idx_pis,
                              int(edit_capex_2["Useful Life (y)"].iloc[i]),
                              depreciation_method, prod_profile=prod_mstb)
                dep_capex2  += d2
                depreciation += d2
            capex_tangible[i] += t2

            # CAPEX III (Intangible)
            capex_intangible[i] = float(c3_after[i]) * capex_mult

        # ── OPEX helper (VAT + escalation) ──
        def _opex_esc(df_opex, idx):
            val    = float(df_opex["Opex (MUSD)"].iloc[idx])
            is_vat = bool(df_opex["VAT"].iloc[idx])
            vat_r  = float(edit_vat["VAT Rate"].iloc[idx])
            after  = val * (1 + vat_r) if is_vat else val
            return after * esc_mult[idx]

        # ── Output arrays ──
        final_cont_arr = np.zeros(total_years)
        final_gov_arr  = np.zeros(total_years)
        gross_revenue  = np.zeros(total_years)
        net_revenue    = np.zeros(total_years)
        ctr_revenue    = np.zeros(total_years)
        gov_revenue    = np.zeros(total_years)
        opex_total     = np.zeros(total_years)
        dmo_gross      = np.zeros(total_years)
        dmo_fee_arr    = np.zeros(total_years)
        dmo_penalty    = np.zeros(total_years)
        taxable_income = np.zeros(total_years)
        tax_paid       = np.zeros(total_years)
        net_cf         = np.zeros(total_years)
        split_details  = []

        cum_prod_mmboe = 0.0

        for i in range(total_years):
            price_i = (float(override_oil_price) if override_oil_price is not None
                       else float(edit_prod["Price (USD/bbl)"].iloc[i]))

            # Split dinamis (cum prod s.d. akhir tahun sebelumnya)
            params_i = dict(
                commodity=commodity, field_status=field_status,
                is_offshore=is_offshore, water_depth=water_depth,
                reservoir_depth=reservoir_depth, infrastructure=infrastructure,
                reservoir_type=reservoir_type, co2_pct=co2_pct,
                h2s_ppm=h2s_ppm, api=api, tkdn_pct=tkdn_pct,
                prod_stage=prod_stage,
                icp_price=price_i if commodity == "Minyak Bumi" else 0.0,
                gas_price=price_i if commodity == "Gas Bumi" else 0.0,
                nett_prod=cum_prod_mmboe,
                ministerial_adj=ministerial_adj,
            )
            res_i = calculate_gross_split(params_i)
            cum_prod_mmboe += prod_mstb[i] / 1000.0

            final_cont_arr[i] = res_i["final_cont"]
            final_gov_arr[i]  = res_i["final_gov"]
            split_details.append(res_i)

            # OPEX
            opex_total[i] = (_opex_esc(edit_opex_1, i) + _opex_esc(edit_opex_2, i)
                             + _opex_esc(edit_opex_3, i) + _opex_esc(edit_opex_4, i)
                             + _opex_esc(edit_opex_5, i) + _opex_esc(edit_opex_6, i))

            # Revenue
            gross_revenue[i] = prod_mstb[i] * price_i
            net_revenue[i]   = gross_revenue[i] - gtf_arr[i]
            ctr_revenue[i]   = net_revenue[i] * (res_i["final_cont"] / 100.0)
            gov_revenue[i]   = net_revenue[i] * (res_i["final_gov"]  / 100.0)

            # DMO
            if prod_mstb[i] > 0:
                prod_year_num    = i - prod_start_yr + 1
                dmo_gross[i]     = ctr_revenue[i] * dmo_volume_rate
                if prod_year_num <= int(dmo_holiday_years):
                    dmo_fee_arr[i] = dmo_gross[i]
                else:
                    dmo_fee_arr[i] = dmo_gross[i] * dmo_fee_rate
                dmo_penalty[i]   = dmo_gross[i] - dmo_fee_arr[i]

            # Tax & Cash Flow
            capex_total_i      = capex_tangible[i] + capex_intangible[i]
            taxable_income[i]  = max(0.0,
                                     ctr_revenue[i] - dmo_penalty[i]
                                     - opex_total[i] - capex_total_i)
            tax_paid[i]        = taxable_income[i] * tax_rate
            net_cf[i]          = (ctr_revenue[i] - dmo_penalty[i]
                                  - opex_total[i] - capex_total_i - tax_paid[i])

        gov_take        = gov_revenue + dmo_penalty + tax_paid
        capex_total_arr = capex_tangible + capex_intangible

        return dict(
            years=years_array, prod_bopd=prod_bopd, prod_mstb=prod_mstb,
            gross_revenue=gross_revenue, gtf_arr=gtf_arr, net_revenue=net_revenue,
            ctr_revenue=ctr_revenue, gov_revenue=gov_revenue,
            final_cont_arr=final_cont_arr, final_gov_arr=final_gov_arr,
            dmo_gross=dmo_gross, dmo_fee_arr=dmo_fee_arr, dmo_penalty=dmo_penalty,
            capex_tangible=capex_tangible, capex_intangible=capex_intangible,
            capex_total_arr=capex_total_arr,
            dep_capex1=dep_capex1, dep_capex2=dep_capex2, depreciation=depreciation,
            opex_total=opex_total,
            taxable_income=taxable_income, tax_paid=tax_paid,
            net_cf=net_cf, gov_take=gov_take,
            prod_start_year=prod_start_yr, total_years=total_years,
            split_details=split_details,
        )

    # ── Run model ──
    eco           = run_gs_model()
    cumulative_cf = np.cumsum(eco["net_cf"])

    # ══════════════════════════════════════════════════════════
    # ── KPIs
    # ══════════════════════════════════════════════════════════
    total_gross_revenue = float(np.sum(eco["gross_revenue"]))
    total_gtf           = float(np.sum(eco["gtf_arr"]))
    total_net_revenue   = float(np.sum(eco["net_revenue"]))
    total_ctr_revenue   = float(np.sum(eco["ctr_revenue"]))
    total_gov_revenue   = float(np.sum(eco["gov_revenue"]))
    total_gov_take      = float(np.sum(eco["gov_take"]))
    total_tax           = float(np.sum(eco["tax_paid"]))
    total_dmo_penalty   = float(np.sum(eco["dmo_penalty"]))
    total_dmo_gross     = float(np.sum(eco["dmo_gross"]))
    total_dmo_fee       = float(np.sum(eco["dmo_fee_arr"]))
    total_capex         = float(np.sum(eco["capex_total_arr"]))
    total_capex_tang    = float(np.sum(eco["capex_tangible"]))
    total_capex_intang  = float(np.sum(eco["capex_intangible"]))
    total_opex          = float(np.sum(eco["opex_total"]))
    # Ctr Take (AT) = Ctr Revenue - DMO Penalty - Tax
    total_ctr_take_at   = total_ctr_revenue - total_dmo_penalty - total_tax

    gov_take_pct   = total_gov_take / total_gross_revenue if total_gross_revenue > 0 else 0
    sum_prod_mstb  = float(np.sum(eco["prod_mstb"]))
    avg_oil_price  = total_gross_revenue / sum_prod_mstb if sum_prod_mstb > 0 else 0
    avg_split_cont = (float(np.mean(eco["final_cont_arr"][eco["prod_mstb"] > 0]))
                      if np.any(eco["prod_mstb"] > 0) else result_base["final_cont"])
    avg_split_gov  = 100.0 - avg_split_cont

    pct_gov_share  = total_gov_take    / total_gross_revenue if total_gross_revenue > 0 else 0
    pct_ctr_share  = total_ctr_take_at / total_gross_revenue if total_gross_revenue > 0 else 0

    # NPV
    npv_base = sum(
        eco["net_cf"][i] / ((1.0 + discount_rate) **
                            (float(eco["years"][i]) - float(discount_factor_year)))
        for i in range(eco["total_years"])
    )

    # IRR
    try:
        cf = eco["net_cf"]
        if np.any(cf < 0) and np.any(cf > 0):
            irr_base = npf.irr(cf)
            irr_base = float("nan") if (np.isnan(irr_base) or np.isinf(irr_base)) else irr_base
        else:
            irr_base = float("nan")
    except Exception:
        irr_base = float("nan")

    # Payback
    payback_year = "-"
    for y, val in enumerate(cumulative_cf):
        if val >= 0 and y >= eco["prod_start_year"]:
            payback_year = str(int(eco["years"][y]))
            break

    # Break-Even Price
    bep_price = None
    for test_p in range(1, 300):
        tr = run_gs_model(override_oil_price=float(test_p))
        test_npv = sum(
            tr["net_cf"][i] / ((1.0 + discount_rate) **
                               (float(tr["years"][i]) - float(discount_factor_year)))
            for i in range(tr["total_years"])
        )
        if test_npv >= 0:
            bep_price = test_p
            break
    if bep_price is None:
        bep_price = float("nan")

    # ══════════════════════════════════════════════════════════
    # ── HEADER
    # ══════════════════════════════════════════════════════════
    col_logo, col_title = st.columns([1, 10])
    with col_logo:
        if logo:
            st.image(logo, use_container_width=True)
        else:
            st.markdown('<div style="font-size:3rem;text-align:center;">&#9889;</div>',
                        unsafe_allow_html=True)
    with col_title:
        st.markdown(f"""
        <h1 style="margin-bottom:0;">
          SplitLogic
          <span class="mode-pill">Gross Split</span>
        </h1>
        <p style="color:var(--muted);margin-top:4px;font-size:0.9rem;">
          PSC Gross Split Financial Modeller &mdash; <em>SplitLogic</em> &nbsp;|&nbsp;
          Komoditas: <strong style="color:var(--amber);">{commodity}</strong>
        </p>
        """, unsafe_allow_html=True)
    st.markdown("---")

    # ── KPI strip ──
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Base Split - Kontraktor",  f"{result_base['base_cont']:.1f}%")
    m2.metric("Total Koreksi",            f"{result_base['total_correction']:+.2f}%")
    m3.metric("Avg Split - Kontraktor",   f"{avg_split_cont:.2f}%")
    m4.metric("Avg Split - Pemerintah",   f"{avg_split_gov:.2f}%")
    m5.metric("Diskresi Menteri",         f"{result_base['ministerial_adj']:+.2f}%")
    st.markdown("---")

    # ══════════════════════════════════════════════════════════
    # ── TABS
    # ══════════════════════════════════════════════════════════
    tab_dash, tab_split, tab_summary, tab_econ, tab_sens, tab_about = st.tabs([
        "Dashboard",
        "Split Analysis",
        "Executive Summary",
        "Economic Tables",
        "Sensitivity",
        "About",
    ])

    # ══════════════════════════════════════════════════════════
    # ── TAB 1: Dashboard
    # ══════════════════════════════════════════════════════════
    with tab_dash:
        st.markdown("### Key Economic Indicators")
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        c1.metric("Reserve (MMBO)",        f"{sum_prod_mstb / 1000:.4f}")
        c2.metric(f"NPV @{discount_rate*100:.0f}% (MUS$)", f"{npv_base:,.2f}")
        c3.metric("IRR Full Cycle",
                  f"{irr_base:.2%}" if not np.isnan(irr_base) else "N/A")
        c4.metric("Gov Take (%)",          f"{gov_take_pct:.2%}")
        c5.metric("Payback Year",          payback_year)
        c6.metric("Break-Even Price",
                  f"${bep_price:.0f}/bbl" if not np.isnan(float(bep_price)) else "N/A")
        st.markdown("---")

        cc1, cc2 = st.columns(2)
        with cc1:
            fig_prod = make_subplots(specs=[[{"secondary_y": True}]])
            fig_prod.add_trace(go.Bar(x=eco["years"], y=eco["prod_bopd"],
                                      name="BOPD", marker_color=SLATE), secondary_y=False)
            fig_prod.add_trace(go.Scatter(x=eco["years"],
                                           y=np.cumsum(eco["prod_mstb"]),
                                           name="Cum. Prod (MSTB)",
                                           line=dict(color=AMBER, width=3)),
                               secondary_y=True)
            fig_prod.update_layout(**plotly_layout("Production Profile & Cumulative"))
            fig_prod.update_yaxes(title_text="BOPD",              secondary_y=False)
            fig_prod.update_yaxes(title_text="MSTB (Cumulative)", secondary_y=True)
            st.plotly_chart(fig_prod, use_container_width=True)

        with cc2:
            fig_cf = go.Figure()
            bar_colors = [AMBER if v >= 0 else "#C05050" for v in eco["net_cf"]]
            fig_cf.add_trace(go.Bar(x=eco["years"], y=eco["net_cf"],
                                    name="Yearly CF", marker_color=bar_colors))
            fig_cf.add_trace(go.Scatter(x=eco["years"], y=cumulative_cf,
                                         name="Cumulative CF",
                                         line=dict(color="#F5B96B", width=3)))
            fig_cf.update_layout(**plotly_layout("Contractor Net Cash Flow"),
                                  yaxis_title="MUS$")
            st.plotly_chart(fig_cf, use_container_width=True)

        st.markdown("---")
        cc3, cc4 = st.columns(2)

        with cc3:
            st.markdown("### Revenue Distribution Waterfall")
            wf_labels  = ["Gross Revenue", "Gas Toll Fee", "Gov Revenue (Split)",
                           "DMO Penalty", "Corp Tax", "Contractor Net (AT)"]
            wf_values  = [total_gross_revenue, -total_gtf,
                          -total_gov_revenue, -total_dmo_penalty,
                          -total_tax, total_ctr_take_at]
            wf_measure = ["relative", "relative", "relative",
                          "relative", "relative", "total"]
            fig_wf = go.Figure(go.Waterfall(
                orientation="v", measure=wf_measure,
                x=wf_labels, y=wf_values,
                decreasing=dict(marker=dict(color="#C05050")),
                increasing=dict(marker=dict(color=SLATE)),
                totals=dict(marker=dict(color=AMBER)),
            ))
            fig_wf.update_layout(**plotly_layout("Revenue Distribution Waterfall"))
            st.plotly_chart(fig_wf, use_container_width=True)

        with cc4:
            st.markdown("### Gross Revenue Allocation")
            pie_labels = ["Gov Revenue (Split)", "DMO Penalty", "Tax", "Contractor Net (AT)"]
            pie_values = [total_gov_revenue, total_dmo_penalty, total_tax, total_ctr_take_at]
            pie_colors = [SLATE, "#8B6F47", "#C05050", AMBER]
            if total_gtf > 0:
                pie_labels.insert(1, "Gas Toll Fee")
                pie_values.insert(1, total_gtf)
                pie_colors.insert(1, MUTED)
            fig_pie = go.Figure(data=[go.Pie(
                labels=pie_labels, values=pie_values, hole=.4,
                marker_colors=pie_colors, textinfo="label+percent",
            )])
            fig_pie.update_layout(**plotly_layout("Alokasi Gross Revenue"))
            st.plotly_chart(fig_pie, use_container_width=True)

    # ══════════════════════════════════════════════════════════
    # ── TAB 2: Split Analysis
    # ══════════════════════════════════════════════════════════
    with tab_split:
        col_d, col_w = st.columns([1, 2])
        with col_d:
            st.plotly_chart(donut_chart_gs(avg_split_gov, avg_split_cont,
                                           "Avg Split\n(Prod. Years)"),
                            use_container_width=True)
        with col_w:
            st.plotly_chart(waterfall_chart_gs(result_base), use_container_width=True)

        st.markdown("---")
        fig_split_yr = go.Figure()
        fig_split_yr.add_trace(go.Scatter(
            x=eco["years"], y=eco["final_cont_arr"],
            name="Contractor Split (%)", line=dict(color=AMBER, width=3),
            fill="tozeroy", fillcolor="rgba(232,150,60,0.12)",
        ))
        fig_split_yr.add_trace(go.Scatter(
            x=eco["years"], y=eco["final_gov_arr"],
            name="Government Split (%)", line=dict(color=SLATE, width=2, dash="dot"),
        ))
        fig_split_yr.update_layout(
            **plotly_layout("Dynamic Split per Year (Progressive)", height=360),
            yaxis_title="Split (%)", xaxis_title="Year",
        )
        st.plotly_chart(fig_split_yr, use_container_width=True)

        st.markdown("---")
        st.markdown("### Ringkasan Komponen Split (Base Params)")
        rows = []
        for k, v in result_base["fixed_comps"].items():
            rows.append({"Komponen": k, "Tipe": "Fixed", "Koreksi (%)": v})
        for k, v in result_base["progressive_comps"].items():
            rows.append({"Komponen": k, "Tipe": "Progressive", "Koreksi (%)": v})
        if result_base["ministerial_adj"] != 0:
            rows.append({"Komponen": "Diskresi Menteri", "Tipe": "Diskresi",
                         "Koreksi (%)": result_base["ministerial_adj"]})
        df_comp = pd.DataFrame(rows)
        df_comp["Arah"] = df_comp["Koreksi (%)"].apply(
            lambda x: "Pro-Kontraktor" if x > 0 else ("Pro-Pemerintah" if x < 0 else "Netral"))
        st.dataframe(df_comp, use_container_width=True)
        st.plotly_chart(bar_comparison_gs(result_base), use_container_width=True)

    # ══════════════════════════════════════════════════════════
    # ── TAB 3: Executive Summary
    # ══════════════════════════════════════════════════════════
    with tab_summary:
        st.subheader("Executive Summary Report")

        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown("#### Production Profile")
            st.markdown(f"""
| Indicator | Unit | Value |
| :--- | :--- | ---: |
| **Oil Production** | MSTB | {sum_prod_mstb:,.4f} |
| **Average Oil Price** | USD/bbl | {avg_oil_price:,.4f} |
| **Gross Revenue** | MUSD | {total_gross_revenue:,.4f} |
| **Gas Toll Fee** | MUSD | {total_gtf:,.4f} |
| **Net Revenue** | MUSD | {total_net_revenue:,.4f} |
""")
            st.markdown("#### Split")
            st.markdown(f"""
| Indicator | Unit | Gov. | Ctr. |
| :--- | :--- | ---: | ---: |
| **Revenue (Split)** | MUSD | {total_gov_revenue:,.4f} | {total_ctr_revenue:,.4f} |
| **Avg Split** | % | {avg_split_gov:.2f}% | {avg_split_cont:.2f}% |
""")

        with col_s2:
            st.markdown("#### Investment & OPEX")
            st.markdown(f"""
| Indicator | Unit | Value |
| :--- | :--- | ---: |
| **CAPEX Tangible (I+II)** | MUSD | {total_capex_tang:,.4f} |
| **CAPEX Intangible (III)** | MUSD | {total_capex_intang:,.4f} |
| **Total CAPEX** | MUSD | {total_capex:,.4f} |
| **Total OPEX** | MUSD | {total_opex:,.4f} |
""")
            st.markdown("#### DMO")
            st.markdown(f"""
| Indicator | Unit | Value |
| :--- | :--- | ---: |
| **DMO Gross** | MUSD | {total_dmo_gross:,.4f} |
| **DMO Fee** | MUSD | {total_dmo_fee:,.4f} |
| **DMO Penalty** | MUSD | {total_dmo_penalty:,.4f} |
""")

        st.markdown("---")
        col_s3, col_s4 = st.columns(2)
        with col_s3:
            st.markdown("#### Government Profitability")
            st.markdown(f"""
| Indicator | Unit | Value |
| :--- | :--- | ---: |
| **Gov. Revenue (Split)** | MUSD | {total_gov_revenue:,.4f} |
| **Gas Toll Fee** | MUSD | {total_gtf:,.4f} |
| **DMO Penalty** | MUSD | {total_dmo_penalty:,.4f} |
| **Tax** | MUSD | {total_tax:,.4f} |
| **Gov Total Take** | MUSD | {total_gov_take:,.4f} |
| **% Gov Take** | % | {pct_gov_share:,.4%} |
""")

        with col_s4:
            st.markdown("#### Contractor Profitability")
            st.markdown(f"""
| Indicator | Unit | Value |
| :--- | :--- | ---: |
| **Ctr Revenue (Split)** | MUSD | {total_ctr_revenue:,.4f} |
| **Ctr Share (AT)** | MUSD | {total_ctr_take_at:,.4f} |
| **% Ctr Share** | % | {pct_ctr_share:,.4%} |
| **NPV PF** | MUSD | {npv_base:,.4f} |
| **IRR FC** | % | {f"{irr_base:.4%}" if not np.isnan(irr_base) else "N/A"} |
| **Payback Year** | -- | {payback_year} |
| **Break-Even Price** | USD/bbl | {f"{bep_price:.0f}" if not np.isnan(float(bep_price)) else "N/A"} |
""")

    # ══════════════════════════════════════════════════════════
    # ── TAB 4: Economic Tables
    # ══════════════════════════════════════════════════════════
    with tab_econ:
        st.subheader("Annual Economic Tables")

        st.markdown("##### Group 1: Production & Revenue")
        df_g1 = pd.DataFrame({
            "Year":                 eco["years"],
            "Lifting (MSTB)":       eco["prod_mstb"],
            "BOPD":                 eco["prod_bopd"],
            "Price (USD/bbl)":      edit_prod["Price (USD/bbl)"].values,
            "Gross Revenue (MUSD)": eco["gross_revenue"],
            "Gas Toll Fee (MUSD)":  eco["gtf_arr"],
            "Net Revenue (MUSD)":   eco["net_revenue"],
        })
        st.dataframe(df_g1.style.format({c: "{:,.4f}" for c in df_g1.columns if c != "Year"}),
                     use_container_width=True)

        st.markdown("##### Group 2: Split & Revenue Allocation")
        df_g2 = pd.DataFrame({
            "Year":                  eco["years"],
            "Cont. Split (%)":       eco["final_cont_arr"],
            "Gov. Split (%)":        eco["final_gov_arr"],
            "Cont. Revenue (MUSD)":  eco["ctr_revenue"],
            "Gov. Revenue (MUSD)":   eco["gov_revenue"],
        })
        st.dataframe(df_g2.style.format({c: "{:,.4f}" for c in df_g2.columns if c != "Year"}),
                     use_container_width=True)

        st.markdown("##### Group 3: CAPEX & Depreciation")
        df_g3 = pd.DataFrame({
            "Year":                      eco["years"],
            "CAPEX Tangible (MUSD)":     eco["capex_tangible"],
            "CAPEX Intangible (MUSD)":   eco["capex_intangible"],
            "Total CAPEX (MUSD)":        eco["capex_total_arr"],
            "Dep. CAPEX I (MUSD)":       eco["dep_capex1"],
            "Dep. CAPEX II (MUSD)":      eco["dep_capex2"],
            "Total Depreciation (MUSD)": eco["depreciation"],
        })
        st.dataframe(df_g3.style.format({c: "{:,.4f}" for c in df_g3.columns if c != "Year"}),
                     use_container_width=True)

        st.markdown("##### Group 4: OPEX")
        df_g4 = pd.DataFrame({
            "Year":              eco["years"],
            "Total OPEX (MUSD)": eco["opex_total"],
        })
        st.dataframe(df_g4.style.format({c: "{:,.4f}" for c in df_g4.columns if c != "Year"}),
                     use_container_width=True)

        st.markdown("##### Group 5: DMO")
        df_g5 = pd.DataFrame({
            "Year":               eco["years"],
            "DMO Gross (MUSD)":   eco["dmo_gross"],
            "DMO Fee (MUSD)":     eco["dmo_fee_arr"],
            "DMO Penalty (MUSD)": eco["dmo_penalty"],
        })
        st.dataframe(df_g5.style.format({c: "{:,.4f}" for c in df_g5.columns if c != "Year"}),
                     use_container_width=True)

        st.markdown("##### Group 6: Tax & Government Take")
        df_g6 = pd.DataFrame({
            "Year":                   eco["years"],
            "Taxable Income (MUSD)":  eco["taxable_income"],
            "Tax Paid (MUSD)":        eco["tax_paid"],
            "Gov. Total Take (MUSD)": eco["gov_take"],
        })
        st.dataframe(df_g6.style.format({c: "{:,.4f}" for c in df_g6.columns if c != "Year"}),
                     use_container_width=True)

        st.markdown("##### Group 7: Contractor Cash Flow")
        df_g7 = pd.DataFrame({
            "Year":               eco["years"],
            "Ctr Revenue (MUSD)": eco["ctr_revenue"],
            "DMO Penalty (MUSD)": eco["dmo_penalty"],
            "CAPEX Total (MUSD)": eco["capex_total_arr"],
            "OPEX Total (MUSD)":  eco["opex_total"],
            "Tax Paid (MUSD)":    eco["tax_paid"],
            "Net CF (MUSD)":      eco["net_cf"],
            "Cum. CF (MUSD)":     np.cumsum(eco["net_cf"]),
        })
        st.dataframe(df_g7.style.format({c: "{:,.4f}" for c in df_g7.columns if c != "Year"}),
                     use_container_width=True)

    # ══════════════════════════════════════════════════════════
    # ── TAB 5: Sensitivity
    # ══════════════════════════════════════════════════════════
    with tab_sens:
        st.subheader("Sensitivitas Split terhadap Harga")
        if commodity == "Minyak Bumi":
            prices = list(range(30, 151, 5))
            splits = [calculate_gross_split({**base_params, "icp_price": p})["final_cont"]
                      for p in prices]
            fig_s = go.Figure()
            fig_s.add_trace(go.Scatter(x=prices, y=splits, name="Ctr Split (%)",
                                        line=dict(color=AMBER, width=3), fill="tozeroy",
                                        fillcolor="rgba(232,150,60,0.1)"))
            fig_s.add_trace(go.Scatter(x=prices, y=[100 - s for s in splits],
                                        name="Gov Split (%)",
                                        line=dict(color=SLATE, width=2, dash="dot")))
            fig_s.update_layout(**plotly_layout("Split Kontraktor vs Harga Minyak ICP", height=420),
                                 xaxis_title="ICP (US$/bbl)", yaxis_title="Split (%)")
            st.plotly_chart(fig_s, use_container_width=True)
        else:
            prices = [round(x * 0.5, 1) for x in range(4, 30)]
            splits = [calculate_gross_split({**base_params, "gas_price": p})["final_cont"]
                      for p in prices]
            fig_s = go.Figure()
            fig_s.add_trace(go.Scatter(x=prices, y=splits, name="Ctr Split (%)",
                                        line=dict(color=AMBER, width=3)))
            fig_s.update_layout(**plotly_layout("Split Kontraktor vs Harga Gas", height=420),
                                 xaxis_title="Harga Gas (US$/MMBTU)", yaxis_title="Split (%)")
            st.plotly_chart(fig_s, use_container_width=True)

        st.subheader("Sensitivitas Kumulatif Produksi terhadap Split")
        prod_vals   = list(range(5, 250, 10))
        prod_splits = [calculate_gross_split({**base_params, "nett_prod": p})["final_cont"]
                       for p in prod_vals]
        fig_p = go.Figure(go.Scatter(x=prod_vals, y=prod_splits,
                                      name="Ctr Split (%)", line=dict(color=AMBER, width=3)))
        fig_p.update_layout(**plotly_layout("Split Kontraktor vs Kumulatif Produksi", height=380),
                             xaxis_title="MMBOE", yaxis_title="Split Kontraktor (%)")
        st.plotly_chart(fig_p, use_container_width=True)

        st.markdown("---")
        st.subheader("Sensitivitas Harga terhadap NPV")
        price_range = list(range(20, 151, 5))
        npv_vals    = []
        for test_p in price_range:
            tr = run_gs_model(override_oil_price=float(test_p))
            test_npv = sum(
                tr["net_cf"][i] / ((1.0 + discount_rate) **
                                   (float(tr["years"][i]) - float(discount_factor_year)))
                for i in range(tr["total_years"])
            )
            npv_vals.append(test_npv)
        fig_npv = go.Figure()
        fig_npv.add_trace(go.Bar(
            x=price_range, y=npv_vals,
            marker_color=[AMBER if v >= 0 else "#C05050" for v in npv_vals],
            name="NPV",
        ))
        fig_npv.add_hline(y=0, line_dash="dash", line_color=MUTED)
        fig_npv.update_layout(**plotly_layout("NPV vs Oil Price (Break-Even Analysis)", height=380),
                               xaxis_title="Oil Price (USD/bbl)", yaxis_title="NPV (MUSD)")
        st.plotly_chart(fig_npv, use_container_width=True)

        st.subheader("Sensitivitas CAPEX terhadap NPV")
        capex_mults = [round(x * 0.1, 1) for x in range(5, 21)]
        npv_capex   = []
        for mult in capex_mults:
            tr = run_gs_model(capex_mult=mult)
            test_npv = sum(
                tr["net_cf"][i] / ((1.0 + discount_rate) **
                                   (float(tr["years"][i]) - float(discount_factor_year)))
                for i in range(tr["total_years"])
            )
            npv_capex.append(test_npv)
        fig_capex = go.Figure(go.Scatter(
            x=capex_mults, y=npv_capex,
            line=dict(color=AMBER, width=3),
            fill="tozeroy", fillcolor="rgba(232,150,60,0.08)",
            name="NPV",
        ))
        fig_capex.add_hline(y=0, line_dash="dash", line_color=MUTED)
        fig_capex.update_layout(**plotly_layout("NPV vs CAPEX Multiplier", height=360),
                                 xaxis_title="CAPEX Multiplier", yaxis_title="NPV (MUSD)")
        st.plotly_chart(fig_capex, use_container_width=True)

    # ══════════════════════════════════════════════════════════
    # ── TAB 6: About
    # ══════════════════════════════════════════════════════════
    with tab_about:
        st.markdown("""
        <div class="sl-card">
          <div class="sl-section-tag">About SplitLogic - Gross Split Module</div>
          <h3>PSC Gross Split Financial Modeller</h3>
          <p>
            Modul ini memodelkan skema <strong>PSC Gross Split</strong> sesuai regulasi Indonesia
            (Permen ESDM No. 20 Tahun 2019 dan perubahannya), dimana bagi hasil ditetapkan
            berdasarkan karakteristik lapangan <em>tanpa mekanisme cost recovery</em>.
            Semua biaya (CAPEX dan OPEX) ditanggung sepenuhnya oleh kontraktor.
          </p>
          <hr/>
          <h4>Alur Perhitungan</h4>
          <ul>
            <li><strong>Split Dinamis per Tahun</strong>: Progressive components (harga dan cum. prod.)
                dihitung ulang setiap tahun dengan cumulative production rolling</li>
            <li><strong>Gross Revenue</strong> = Lifting x Harga</li>
            <li><strong>Net Revenue</strong> = Gross Revenue - Gas Toll Fee (default 0)</li>
            <li><strong>Revenue Split</strong>: Net Revenue dibagi Ctr / Gov sesuai final split per tahun</li>
            <li><strong>DMO</strong>: Diambil dari Contractor Revenue (volume rate x fee rate, dengan holiday period)</li>
            <li><strong>CAPEX I dan II</strong>: Tangible - disusutkan berdasarkan PIS Year, Useful Life, dan metode pilihan</li>
            <li><strong>CAPEX III</strong>: Intangible - dibebankan penuh tahun berjalan</li>
            <li><strong>OPEX I-VI</strong>: Masing-masing dengan toggle VAT per baris dan escalation factor kumulatif</li>
            <li><strong>Taxable Income</strong> = Ctr Revenue - DMO Penalty - OPEX - CAPEX</li>
            <li><strong>Net CF</strong> = Ctr Revenue - DMO Penalty - OPEX - CAPEX - Tax</li>
            <li><strong>Metrik</strong>: NPV (discounted), IRR, Payback Year, Break-Even Price,
                Sensitivitas Harga dan CAPEX</li>
          </ul>
          <h4>Input Sidebar</h4>
          <ul>
            <li><strong>VAT Rate</strong>: Per tahun, diterapkan ke seluruh CAPEX dan OPEX (toggle per baris)</li>
            <li><strong>Escalation Factor</strong>: Kumulatif per tahun, diterapkan ke seluruh OPEX</li>
            <li><strong>Gas Toll Fee</strong>: Dikurangkan dari Gross Revenue sebelum split (default 0)</li>
          </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<div class="footer-text">SplitLogic v1.1 - Gross Split Module - 2026</div>',
        unsafe_allow_html=True,
    )
#endregion
