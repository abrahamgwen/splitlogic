#region Judul
# ──────────────────────────────────────────
# SplitLogic v1.0 – PSC Modelling
# Created by Abraham Gwen Bramanti
# Last edited: 4/19/2026
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
        "Skema PSC",
        ["💰 Cost Recovery", "⚡ Gross Split"],
        index=0,
    )
    st.markdown("---")
#endregion

#region Cost Recovery
# ──────────────────────────────────────────
# 5. COST RECOVERY MODULE
# ───────────────────────────────────────────
if app_mode == "💰 Cost Recovery":

    # ── Sidebar inputs ──
    with st.sidebar:
        st.markdown("### ⚙️ Input Parameter")

        with st.sidebar.expander("📈 Production Profile", expanded=True):
            q_initial     = st.number_input("Initial Rate (BOPD)", value=0, step=1000)
            q_peak        = st.number_input("Peak Rate (BOPD)", value=0, step=1000)
            plateau_years = st.number_input("Plateau Duration (Years)", value=0, step=1)
            decline_rate  = st.number_input("Decline Rate (%)", value=0.0, step=1.0) / 100
            prod_years    = st.number_input("Production Duration (Years)", value=0, step=1)

        with st.sidebar.expander("🏗️ CAPEX (Exploration & Dev)", expanded=False):
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
            st.caption(f"↳ *Implied Intangible Split:* **{intangible_pct*100:.1f}%**")

        with st.sidebar.expander("💰 Economic & PSC Terms", expanded=False):
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
            **📊 Implied Split Breakdown:**
            - Ctr After-Tax: **{ctr_split_after_tax*100:.2f}%**
            - Gov Before-Tax: **{gov_split_before_tax*100:.2f}%**
            - Ctr Before-Tax: **{ctr_split_before_tax*100:.2f}%**
            """)

        with st.sidebar.expander("📉 Depreciation Rules", expanded=False):
            dep_group = st.selectbox("Tangible Depreciation Group",
                                     ["Group 1 (50%)", "Group 2 (25%)", "Group 3 (12.5%)"])
            # dep_years cannot be 0, keeping default at 1
            dep_years = st.number_input("Target Depreciation (Years)", value=1, min_value=1, step=1)

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
                "brent": {"price": bp, "change": (bp-bprev)/bprev*100},
                "wti":   {"price": wp, "change": (wp-wprev)/wprev*100},
                "status": "success"
            }
        except Exception:
            return {"status": "failed"}

    live_prices = fetch_live_oil_prices()

    # ── Core Model ──
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

    # ── KPIs ──
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

    # ── HEADER ──
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
    tab1, tab2, tab3, tab_about = st.tabs(["📊 Dashboard", "📑 Economic Tables", "📈 Sensitivity", "ℹ️ About"])

    # ── TAB 1: Dashboard ──
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
        c1,c2,c3,c4,c5,c6 = st.columns(6)
        c1.metric("Reserve (MMBO)",              f"{np.sum(results['prod_mstb'])/1000:.2f}")
        c2.metric(f"NPV @{discount_rate*100:.0f}% (MUS$)", f"{npv_base:,.0f}")
        c3.metric("IRR Full Cycle",              f"{irr_base:.2%}" if not np.isnan(irr_base) else "-")
        c4.metric("Gov Take (%)",                f"{gov_take_pct:.2%}")
        c5.metric("Payback Period",              payback_year)
        c6.metric("Break-Even Price",            f"${bep_price}/bbl")
        st.markdown("---")

        # Gantt
        st.markdown("### 📅 Project Phase Timeline")
        df_tl = pd.DataFrame([
            dict(Task="Exploration Phase", Start=1,                        Finish=int(exp_years),                    Color="#E18D11"),
            dict(Task="Development Phase", Start=int(exp_years)+1,         Finish=int(exp_years)+int(dev_years),      Color="#17BECF"),
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
        fig_gantt.update_layout(barmode='stack', xaxis_title="Project Year",
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
            st.markdown("### 🥧 Gross Revenue Allocation")
            fig_pie = go.Figure(data=[go.Pie(
                labels=['Cost Recovery', 'Government Take', 'Contractor Take (After Tax)'],
                values=[np.sum(results['recovered']), total_gov_take, total_ctr_take_at],
                hole=.4,
                marker_colors=[SLATE, MUTED, AMBER],
                textinfo='label+percent',
            )])
            fig_pie.update_layout(**plotly_layout("Proporsi Pembagian Total Pendapatan"))
            st.plotly_chart(fig_pie, use_container_width=True)

    # ── TAB 2: Tables ──
    with tab2:
        st.subheader("📋 Annual Economic Summary")
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
            "Ctr Equity":      np.round(results['ctr_equity'], 2),
            "DMO Penalty":     np.round(results['dmo_penalty'], 2),
            "Net Ctr (MUS$)":  np.round(results['net_ctr_share'], 2),
            "Tax (MUS$)":      np.round(results['tax_paid'], 2),
            "Net CF (MUS$)":   np.round(results['net_cf'], 2),
            "Cum CF (MUS$)":   np.round(cumulative_cf, 2),
        })
        st.dataframe(df_out, use_container_width=True)

        st.markdown("---")
        st.subheader("📊 Project Totals")
        totals = {
            "Total Gross Revenue (MUS$)":       f"{total_gross_revenue:,.2f}",
            "Total Cost Recovery (MUS$)":        f"{np.sum(results['recovered']):,.2f}",
            "Total Government Take (MUS$)":      f"{total_gov_take:,.2f}",
            "Total Contractor Take AT (MUS$)":   f"{total_ctr_take_at:,.2f}",
            "Government Take (%)":               f"{gov_take_pct:.2%}",
            f"NPV @{discount_rate*100:.0f}% (MUS$)": f"{npv_base:,.2f}",
            "IRR":                               f"{irr_base:.2%}" if not np.isnan(irr_base) else "-",
        }
        for k, v in totals.items():
            c_k, c_v = st.columns([3, 2])
            c_k.write(k)
            c_v.write(f"**{v}**")

    # ── TAB 3: Sensitivity ──
    with tab3:
        st.subheader("📈 Oil Price Sensitivity")
        price_range = range(20, 151, 5)
        sens_npv  = []
        sens_irr  = []
        for p in price_range:
            r = run_psc_model(override_oil_price=p)
            n = npf.npv(discount_rate, r['net_cf']) / (1 + discount_rate)
            sens_npv.append(n)
            try:
                sens_irr.append(npf.irr(r['net_cf']))
            except Exception:
                sens_irr.append(float('nan'))

        fig_sens = make_subplots(specs=[[{"secondary_y": True}]])
        fig_sens.add_trace(go.Scatter(x=list(price_range), y=sens_npv,
                                      name="NPV (MUS$)", line=dict(color=AMBER, width=3)),
                           secondary_y=False)
        fig_sens.add_trace(go.Scatter(x=list(price_range), y=[v*100 if not np.isnan(v) else None for v in sens_irr],
                                      name="IRR (%)", line=dict(color="#5DA897", width=2, dash="dot")),
                           secondary_y=True)
        fig_sens.add_hline(y=0, line_dash="dash", line_color=MUTED)
        fig_sens.update_layout(**plotly_layout("NPV & IRR vs Oil Price", height=420))
        fig_sens.update_yaxes(title_text="NPV (MUS$)", secondary_y=False)
        fig_sens.update_yaxes(title_text="IRR (%)", secondary_y=True)
        st.plotly_chart(fig_sens, use_container_width=True)

        st.subheader("📉 CAPEX Sensitivity")
        capex_mults = [0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3]
        capex_npvs  = []
        for m in capex_mults:
            r = run_psc_model(capex_mult=m)
            capex_npvs.append(npf.npv(discount_rate, r['net_cf']) / (1 + discount_rate))

        fig_capex = go.Figure(go.Bar(
            x=[f"{int(m*100)}%" for m in capex_mults],
            y=capex_npvs,
            marker_color=[AMBER if v >= 0 else "#C05050" for v in capex_npvs],
            text=[f"{v:,.0f}" for v in capex_npvs],
            textposition="outside",
        ))
        fig_capex.update_layout(**plotly_layout("NPV vs CAPEX Multiplier", height=380),
                                 yaxis_title="NPV (MUS$)")
        st.plotly_chart(fig_capex, use_container_width=True)

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
            <li>Production profile modeling dengan decline curve</li>
            <li>CAPEX exploration &amp; development dengan split tangible/intangible</li>
            <li>FTP, Cost Recovery, Equity Split, DMO, dan Pajak</li>
            <li>Metrik NPV, IRR, Payback Period, Break-Even Price</li>
            <li>Sensitivity analysis terhadap harga minyak dan CAPEX</li>
            <li>Live Brent &amp; WTI oil price feed</li>
          </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="footer-text">SplitLogic v1.0 · Cost Recovery Module · © 2026</div>',
                unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
# ██████████████  MODULE B – GROSS SPLIT  ████████
# ──────────────────────────────────────────────────────────────
else:

    # ── Gross Split Calculation Engine ──
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
        commodity = params["commodity"]
        base      = BASE_SPLIT[commodity]
        fc = {
            "Status Lapangan":     calc_field_status(params["field_status"]),
            "Lokasi Lapangan":     calc_field_location(params["water_depth"], params["is_offshore"]),
            "Kedalaman Reservoir": calc_reservoir_depth(params["reservoir_depth"]),
            "Infrastruktur":       calc_infrastructure(params["infrastructure"]),
            "Jenis Reservoir":     calc_reservoir_type(params["reservoir_type"]),
            "Kandungan CO₂":       calc_co2(params["co2_pct"]),
            "Kandungan H₂S":       calc_h2s(params["h2s_ppm"]),
            "SG (API)":            calc_sg(params["api"]),
            "TKDN":                calc_tkdn(params["tkdn_pct"]),
            "Tahapan Produksi":    calc_prod_stage(params["prod_stage"]),
        }
        pc = {}
        if commodity == "Minyak Bumi":
            pc["Harga Minyak (ICP)"] = calc_oil_price(params.get("icp_price", 85))
        else:
            pc["Harga Gas Bumi"]     = calc_gas_price(params.get("gas_price", 8))
        pc["Kumulatif Produksi (MMBOE)"] = calc_nett_prod(params["nett_prod"])
        ministerial    = params.get("ministerial_adj", 0.0)
        total_corr     = sum(fc.values()) + sum(pc.values()) + ministerial
        final_cont     = base["cont"] + total_corr
        final_gov      = 100.0 - final_cont
        return dict(commodity=commodity, base_gov=base["gov"], base_cont=base["cont"],
                    fixed_comps=fc, progressive_comps=pc, ministerial_adj=ministerial,
                    total_correction=total_corr, final_cont=final_cont, final_gov=final_gov)

    # ── Chart helpers ──
    def donut_chart(gov_pct, cont_pct, label="Final Split"):
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
        labels = (["Base (Kontraktor)"]
                  + list(result["fixed_comps"].keys())
                  + list(result["progressive_comps"].keys())
                  + (["Diskresi Menteri"] if result["ministerial_adj"] != 0 else [])
                  + ["Final (Kontraktor)"])
        values = ([result["base_cont"]]
                  + list(result["fixed_comps"].values())
                  + list(result["progressive_comps"].values())
                  + ([result["ministerial_adj"]] if result["ministerial_adj"] != 0 else [])
                  + [result["final_cont"]])
        measure = (["absolute"] + ["relative"] * (len(labels) - 2) + ["total"])
        fig = go.Figure(go.Waterfall(
            orientation="v", measure=measure, x=labels, y=values,
            text=[f"{v:+.2f}%" if m == "relative" else f"{v:.2f}%" for m, v in zip(measure, values)],
            textposition="outside",
            textfont=dict(family="DM Sans", size=10, color="#E8EEF4"),
            connector=dict(line=dict(color=MUTED, width=1, dash="dot")),
            increasing=dict(marker=dict(color="#5DA897")),
            decreasing=dict(marker=dict(color="#C05050")),
            totals=dict(marker=dict(color=AMBER)),
        ))
        fig.update_layout(**plotly_layout("Waterfall – Koreksi Split Kontraktor", height=440),
                          xaxis=dict(tickangle=-35, tickfont=dict(size=10, color=MUTED),
                                     gridcolor="rgba(255,255,255,0.04)"),
                          yaxis=dict(title="Split Kontraktor (%)", gridcolor="rgba(255,255,255,0.04)"),
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
                          yaxis=dict(title="Koreksi (%)", gridcolor="rgba(255,255,255,0.04)"),
                          showlegend=False)
        return fig

    # ── Sidebar inputs ──
    with st.sidebar:
        st.markdown('<div class="sl-section-tag">Komoditas</div>', unsafe_allow_html=True)
        commodity = st.radio("Jenis Komoditas", ["Minyak Bumi", "Gas Bumi"], horizontal=True)
        st.markdown("---")
        st.markdown('<div class="sl-section-tag">Fixed Components</div>', unsafe_allow_html=True)

        field_status  = st.selectbox("1 · Status Lapangan", ["No POD", "POD I", "POD II"])
        is_offshore   = st.radio("Lokasi Lapangan", ["Onshore", "Offshore"], horizontal=True) == "Offshore"
        water_depth   = st.number_input("2 · Kedalaman Air (m)", min_value=0.0, value=0.0, step=1.0) if is_offshore else 0.0
        if not is_offshore:
            st.markdown("**2 · Lokasi:** Onshore → Koreksi **0%**")

        reservoir_depth = st.number_input("3 · Kedalaman Reservoir (m)", min_value=0.0, value=0.0, step=50.0)
        infrastructure  = st.selectbox("4 · Infrastruktur",
                                       ["Well Developed", "New Frontier Offshore", "New Frontier Onshore"])
        reservoir_type  = st.selectbox("5 · Jenis Reservoir",
                                       ["Konvensional (Sandstone / Limestone / Carbonate)",
                                        "Non-Konvensional (Shale / CBM)"])
        co2_pct  = st.number_input("6 · CO₂ (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.5)
        h2s_ppm  = st.number_input("7 · H₂S (ppm)", min_value=0.0, value=0.0, step=10.0)
        api      = st.number_input("8 · API (°API)", min_value=0.0, max_value=70.0, value=0.0, step=0.5)
        tkdn_pct = st.number_input("9 · TKDN (%)", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
        prod_stage = st.selectbox("10 · Tahapan Produksi",
                                  ["Primary", "Sekunder (Injeksi Air / Gas)", "Tersier (EOR)"])

        st.markdown("---")
        st.markdown('<div class="sl-section-tag">Progressive Components</div>', unsafe_allow_html=True)
        if commodity == "Minyak Bumi":
            icp_price = st.number_input("11 · Harga Minyak ICP (US$/BBL)", min_value=0.0, value=0.0, step=1.0)
            gas_price = 0.0
        else:
            gas_price = st.number_input("11 · Harga Gas (US$/MMBTU)", min_value=0.0, value=0.0, step=0.1)
            icp_price = 0.0
        nett_prod = st.number_input("12 · Kumulatif Produksi (MMBOE)", min_value=0.0, value=0.0, step=1.0)

        st.markdown("---")
        st.markdown('<div class="sl-section-tag">Pasal 7 – Diskresi Menteri</div>', unsafe_allow_html=True)
        ministerial_adj = st.number_input("Tambahan / Pengurangan Split Kontraktor (%)", value=0.0, step=0.5)
        st.markdown("---")
        calc_btn = st.button("⚡ Hitung Gross Split", use_container_width=True)

    # ── Run Calculation ──
    params = dict(
        commodity=commodity, field_status=field_status, is_offshore=is_offshore,
        water_depth=water_depth, reservoir_depth=reservoir_depth,
        infrastructure=infrastructure, reservoir_type=reservoir_type,
        co2_pct=co2_pct, h2s_ppm=h2s_ppm, api=api, tkdn_pct=tkdn_pct,
        prod_stage=prod_stage, icp_price=icp_price, gas_price=gas_price,
        nett_prod=nett_prod, ministerial_adj=ministerial_adj,
    )
    result = calculate_gross_split(params)

    # ── Header ──
    col_logo, col_hero = st.columns([1, 4])
    with col_logo:
        if logo:
            st.image(logo, width=110)
        else:
            st.markdown('<div style="font-size:3rem;text-align:center;">⚡</div>', unsafe_allow_html=True)
    with col_hero:
        st.markdown(f"""
        <h1 style="margin-bottom:0;">
          SplitLogic
          <span class="mode-pill">Gross Split</span>
        </h1>
        <p style="color:var(--muted);margin-top:4px;font-size:0.9rem;">
          PSC Gross Split Calculator — <em>SplitLogic</em> &nbsp;|&nbsp;
          Komoditas: <strong style="color:var(--amber);">{commodity}</strong>
        </p>
        """, unsafe_allow_html=True)
    st.markdown("---")

    # ── KPI Metrics ──
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Base Split – Kontraktor", f"{result['base_cont']:.1f}%")
    m2.metric("Total Koreksi",           f"{result['total_correction']:+.2f}%")
    m3.metric("Final Split – Kontraktor",f"{result['final_cont']:.2f}%")
    m4.metric("Final Split – Pemerintah",f"{result['final_gov']:.2f}%")
    m5.metric("Diskresi Menteri",        f"{result['ministerial_adj']:+.2f}%")
    st.markdown("---")

    # ── Tabs ──
    tab_dash, tab_detail, tab_sens, tab_about = st.tabs(
        ["📊 Dashboard", "🔍 Detail Komponen", "📈 Analisis Sensitivitas", "ℹ️ About"])

    # ── TAB Dashboard ──
    with tab_dash:
        col_d, col_w = st.columns([1, 2])
        with col_d:
            st.plotly_chart(donut_chart(result['final_gov'], result['final_cont'], "Final Split"),
                            use_container_width=True)
        with col_w:
            st.plotly_chart(waterfall_chart_gs(result), use_container_width=True)

        st.markdown("---")
        st.markdown("### 📋 Ringkasan Komponen")

        rows = []
        for k, v in result["fixed_comps"].items():
            rows.append({"Komponen": k, "Tipe": "Fixed", "Koreksi (%)": v})
        for k, v in result["progressive_comps"].items():
            rows.append({"Komponen": k, "Tipe": "Progressive", "Koreksi (%)": v})
        if result["ministerial_adj"] != 0:
            rows.append({"Komponen": "Diskresi Menteri", "Tipe": "Diskresi", "Koreksi (%)": result["ministerial_adj"]})

        df_comp = pd.DataFrame(rows)
        df_comp["Arah"] = df_comp["Koreksi (%)"].apply(lambda x: "▲ Pro-Kontraktor" if x > 0 else ("▼ Pro-Pemerintah" if x < 0 else "— Netral"))
        st.dataframe(df_comp, use_container_width=True)

    # ── TAB Detail ──
    with tab_detail:
        st.plotly_chart(bar_comparison_gs(result), use_container_width=True)
        st.markdown("---")

        c_fix, c_prog = st.columns(2)
        with c_fix:
            st.markdown("#### Fixed Components")
            for k, v in result["fixed_comps"].items():
                arrow = "🟢" if v > 0 else ("🔴" if v < 0 else "⚪")
                st.markdown(f"{arrow} **{k}**: `{v:+.2f}%`")

        with c_prog:
            st.markdown("#### Progressive Components")
            for k, v in result["progressive_comps"].items():
                arrow = "🟢" if v > 0 else ("🔴" if v < 0 else "⚪")
                st.markdown(f"{arrow} **{k}**: `{v:+.2f}%`")

        st.markdown("---")
        st.info(f"""
        **📊 Final Split Summary**
        - Base Contractor Split: **{result['base_cont']:.1f}%**
        - Total Correction: **{result['total_correction']:+.2f}%**
        - **Final Contractor Split: {result['final_cont']:.2f}%**
        - **Final Government Split: {result['final_gov']:.2f}%**
        """)

    # ── TAB Sensitivity ──
    with tab_sens:
        st.subheader("📈 Sensitivitas Harga terhadap Split")
        if commodity == "Minyak Bumi":
            prices  = list(range(30, 151, 5))
            splits  = []
            for p in prices:
                r = calculate_gross_split({**params, "icp_price": p})
                splits.append(r["final_cont"])
            fig_s = go.Figure()
            fig_s.add_trace(go.Scatter(x=prices, y=splits, name="Ctr Split (%)",
                                       line=dict(color=AMBER, width=3), fill='tozeroy',
                                       fillcolor="rgba(232,150,60,0.1)"))
            fig_s.add_trace(go.Scatter(x=prices, y=[100-s for s in splits], name="Gov Split (%)",
                                       line=dict(color=SLATE, width=2, dash="dot")))
            fig_s.update_layout(**plotly_layout("Split Kontraktor vs Harga Minyak ICP", height=420),
                                 xaxis_title="ICP (US$/bbl)", yaxis_title="Split (%)")
            st.plotly_chart(fig_s, use_container_width=True)
        else:
            prices = [round(x * 0.5, 1) for x in range(4, 30)]
            splits = []
            for p in prices:
                r = calculate_gross_split({**params, "gas_price": p})
                splits.append(r["final_cont"])
            fig_s = go.Figure()
            fig_s.add_trace(go.Scatter(x=prices, y=splits, name="Ctr Split (%)",
                                       line=dict(color=AMBER, width=3)))
            fig_s.update_layout(**plotly_layout("Split Kontraktor vs Harga Gas", height=420),
                                 xaxis_title="Harga Gas (US$/MMBTU)", yaxis_title="Split (%)")
            st.plotly_chart(fig_s, use_container_width=True)

        st.subheader("📉 Sensitivitas Kumulatif Produksi")
        prod_vals = list(range(5, 250, 10))
        prod_splits = [calculate_gross_split({**params, "nett_prod": p})["final_cont"] for p in prod_vals]
        fig_p = go.Figure(go.Scatter(x=prod_vals, y=prod_splits,
                                      name="Ctr Split (%)", line=dict(color=AMBER, width=3)))
        fig_p.update_layout(**plotly_layout("Split Kontraktor vs Kumulatif Produksi", height=380),
                             xaxis_title="MMBOE", yaxis_title="Split Kontraktor (%)")
        st.plotly_chart(fig_p, use_container_width=True)

    # ── TAB About ──
    with tab_about:
        st.markdown("""
        <div class="sl-card">
          <div class="sl-section-tag">About SplitLogic – Gross Split Module</div>
          <h3>PSC Gross Split Calculator</h3>
          <p>
            Modul ini menghitung <strong>PSC Gross Split</strong> sesuai dengan regulasi Indonesia
            (Permen ESDM No. 52 Tahun 2017 dan perubahannya), dimana bagi hasil ditetapkan di awal
            berdasarkan karakteristik lapangan dan komoditas tanpa mekanisme cost recovery.
          </p>
          <hr/>
          <h4>Komponen Koreksi</h4>
          <ul>
            <li><strong>Fixed Components (10 komponen)</strong>: Status lapangan, lokasi, kedalaman reservoir, infrastruktur, jenis reservoir, CO₂, H₂S, SG/API, TKDN, tahapan produksi</li>
            <li><strong>Progressive Components</strong>: Harga komoditas dan kumulatif produksi</li>
            <li><strong>Diskresi Menteri (Pasal 7)</strong>: Penyesuaian atas pertimbangan khusus</li>
          </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="footer-text">SplitLogic v1.0 · Gross Split Module · © 2026</div>',
                unsafe_allow_html=True)
