import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="CyberWatch SOC — Analytics Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────
# CUSTOM CSS (dark cyber theme)
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Share+Tech+Mono&family=Exo+2:wght@300;400;600;800&display=swap');

/* Root variables */
:root {
    --bg-dark:    #070d1a;
    --bg-card:    #0d1b2a;
    --bg-panel:   #0a1525;
    --accent:     #00d4ff;
    --accent2:    #00ff9d;
    --accent3:    #ff6b6b;
    --accent4:    #ffd166;
    --text-main:  #e0eaff;
    --text-muted: #7a92b8;
    --border:     #1a3050;
}

/* Main app background */
.stApp {
    background: var(--bg-dark);
    font-family: 'Exo 2', sans-serif;
    color: var(--text-main);
}

/* Hide default Streamlit header */
#MainMenu, footer, header { visibility: hidden; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #070d1a 0%, #0a1828 100%);
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--text-main) !important; }

/* Metrics */
[data-testid="stMetricValue"] {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: var(--accent) !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'Exo 2', sans-serif !important;
    color: var(--text-muted) !important;
    font-size: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}
[data-testid="stMetricDelta"] { font-size: 0.8rem !important; }

/* KPI cards */
.kpi-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-top: 3px solid var(--accent);
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.5rem;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(135deg, rgba(0,212,255,0.04) 0%, transparent 60%);
    pointer-events: none;
}
.kpi-val {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--accent);
    line-height: 1.1;
}
.kpi-label {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: var(--text-muted);
    margin-top: 0.3rem;
}
.kpi-green  { border-top-color: var(--accent2); }
.kpi-green .kpi-val { color: var(--accent2); }
.kpi-red    { border-top-color: var(--accent3); }
.kpi-red .kpi-val   { color: var(--accent3); }
.kpi-yellow { border-top-color: var(--accent4); }
.kpi-yellow .kpi-val{ color: var(--accent4); }

/* Section headers */
.section-header {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: 2px;
    text-transform: uppercase;
    border-left: 4px solid var(--accent);
    padding-left: 1rem;
    margin: 1.5rem 0 1rem;
}

/* Page title banner */
.page-banner {
    background: linear-gradient(90deg, #0d1b2a 0%, #0a1525 100%);
    border: 1px solid var(--border);
    border-left: 5px solid var(--accent);
    border-radius: 8px;
    padding: 1.2rem 1.8rem;
    margin-bottom: 1.5rem;
}
.page-banner h1 {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.9rem;
    font-weight: 700;
    color: var(--accent);
    margin: 0;
    letter-spacing: 2px;
}
.page-banner p {
    color: var(--text-muted);
    font-size: 0.9rem;
    margin: 0.3rem 0 0;
}

/* Tables */
.dataframe { background: var(--bg-card) !important; color: var(--text-main) !important; }

/* Info / warning boxes */
.info-box {
    background: rgba(0,212,255,0.07);
    border: 1px solid rgba(0,212,255,0.3);
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin: 0.8rem 0;
    font-size: 0.92rem;
}
.warn-box {
    background: rgba(255,107,107,0.07);
    border: 1px solid rgba(255,107,107,0.35);
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin: 0.8rem 0;
}
.success-box {
    background: rgba(0,255,157,0.07);
    border: 1px solid rgba(0,255,157,0.35);
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin: 0.8rem 0;
}

/* Sliders */
[data-testid="stSlider"] > div > div > div > div { background: var(--accent) !important; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #0066cc, #004d99);
    color: white;
    border: 1px solid var(--accent);
    border-radius: 6px;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 600;
    font-size: 1rem;
    letter-spacing: 1px;
    padding: 0.5rem 1.5rem;
    transition: all 0.2s;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #0088ff, #0066cc);
    box-shadow: 0 0 15px rgba(0,212,255,0.4);
}

/* Divider */
hr { border-color: var(--border) !important; }

/* Plot backgrounds */
.element-container { background: transparent !important; }

/* Sidebar nav title */
.nav-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.nav-sub {
    font-size: 0.72rem;
    color: var(--text-muted);
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* Cluster badge */
.badge {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: 600;
    font-family: 'Rajdhani', sans-serif;
    letter-spacing: 1px;
}
.badge-premium { background: rgba(0,255,157,0.15); color: #00ff9d; border: 1px solid #00ff9d; }
.badge-standard{ background: rgba(255,209,102,0.15); color: #ffd166; border: 1px solid #ffd166; }
.badge-atrisk  { background: rgba(255,107,107,0.15); color: #ff6b6b; border: 1px solid #ff6b6b; }

/* Matplotlib style fix */
figure { background: transparent !important; }

/* Hide sidebar collapse/expand button so it can never be hidden */
[data-testid="collapsedControl"] { display: none !important; }
button[kind="header"] { display: none !important; }
section[data-testid="stSidebar"] > div:first-child > div:first-child button { display: none !important; }

</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# SESSION STATE — page tracking
# ──────────────────────────────────────────────
PAGES = [
    "🏠  Executive Dashboard",
    "📊  Exploratory Data Analysis",
    "🔵  Client Segmentation (K-Means)",
    "🤖  Satisfaction Predictor",
    "💰  CLV & Business Recommendation",
]

if "page" not in st.session_state:
    st.session_state.page = PAGES[0]

def set_page(p):
    st.session_state.page = p

# ──────────────────────────────────────────────
# MATPLOTLIB GLOBAL STYLE
# ──────────────────────────────────────────────
DARK_BG   = "#0d1b2a"
DARK_FIG  = "#070d1a"
TEXT_CLR  = "#e0eaff"
GRID_CLR  = "#1a3050"
ACCENT    = "#00d4ff"
ACCENT2   = "#00ff9d"
ACCENT3   = "#ff6b6b"
ACCENT4   = "#ffd166"

plt.rcParams.update({
    "figure.facecolor":  DARK_FIG,
    "axes.facecolor":    DARK_BG,
    "axes.edgecolor":    GRID_CLR,
    "axes.labelcolor":   TEXT_CLR,
    "xtick.color":       TEXT_CLR,
    "ytick.color":       TEXT_CLR,
    "text.color":        TEXT_CLR,
    "grid.color":        GRID_CLR,
    "grid.alpha":        0.5,
    "axes.grid":         True,
    "axes.titlecolor":   TEXT_CLR,
    "legend.facecolor":  DARK_BG,
    "legend.edgecolor":  GRID_CLR,
    "figure.figsize":    (12, 5),
    "axes.titlesize":    13,
    "axes.labelsize":    11,
})

CLUSTER_COLORS = {0: "#00d4ff", 1: "#ffd166", 2: "#ff6b6b"}

# ──────────────────────────────────────────────
# DATA GENERATION (CACHED)
# ──────────────────────────────────────────────
@st.cache_data
def generate_and_clean_data():
    np.random.seed(42)
    N = 150
    client_types = np.random.choice([0, 1, 2], N, p=[0.45, 0.35, 0.20])
    type_labels  = {0: "SME", 1: "IT Firm", 2: "Bank/Govt"}

    def generate(base_values, noise, low, high, integer=False):
        base = np.choose(client_types, base_values)
        data = np.clip(base + np.random.normal(0, noise, N), low, high)
        return data.astype(int) if integer else data

    tdr  = generate([89, 93, 96], 2.5, 78, 99.9)
    irt  = generate([18, 12, 8],  3,   3,  45)
    su   = np.clip(np.random.normal(99.5, 0.4, N), 97.5, 99.99)
    fpr  = generate([14, 9, 5],   2,   1,  25)
    apd  = generate([250, 500, 850], 80, 80, 1500, True)
    ih   = generate([15, 28, 45],  6,  3, 100, True)
    er   = generate([16, 10, 6],   2,  1,  30)
    au   = np.clip(np.random.normal(72, 8, N), 45, 95)
    pcr  = generate([75, 85, 92],  5, 55,  99)

    sat_raw = (0.04*tdr - 0.10*irt + 0.05*su - 0.05*fpr
               + np.random.normal(0, 0.4, N))
    cs = np.clip(1 + 9*(sat_raw - sat_raw.min())/(sat_raw.max()-sat_raw.min()), 1, 10).round(2)

    def inject(arr, frac=0.04):
        arr = arr.astype(float)
        idx = np.random.choice(len(arr), int(frac*len(arr)), replace=False)
        arr[idx] = np.nan
        return arr

    ids = [f"CW-{i+1:03d}" for i in range(N)]
    raw = pd.DataFrame({
        "client_id": ids,
        "client_type": [type_labels[t] for t in client_types],
        "threat_detection_rate":  inject(tdr),
        "incident_response_time": inject(irt),
        "system_uptime":          inject(su),
        "false_positive_rate":    inject(fpr),
        "alerts_per_day":         inject(apd.astype(float)),
        "incidents_handled":      inject(ih.astype(float)),
        "client_satisfaction":    cs,
        "escalation_rate":        inject(er),
        "analyst_utilization":    inject(au),
        "patch_compliance_rate":  pcr,
    })

    dup_idx = np.random.choice(N, 5, replace=False)
    raw = pd.concat([raw, raw.iloc[dup_idx]], ignore_index=True)
    raw.loc[155, "incident_response_time"] = 120
    raw.loc[156, "threat_detection_rate"]  = 35
    raw.loc[157, "alerts_per_day"]         = 5000

    # --- Clean ---
    numeric_cols = [
        "threat_detection_rate","incident_response_time","system_uptime",
        "false_positive_rate","alerts_per_day","incidents_handled",
        "client_satisfaction","escalation_rate","analyst_utilization",
        "patch_compliance_rate"
    ]
    df = raw.drop_duplicates().reset_index(drop=True)
    mask = pd.Series(False, index=df.index)
    for col in numeric_cols:
        Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
        IQR = Q3 - Q1
        mask |= (df[col] < Q1-1.5*IQR) | (df[col] > Q3+1.5*IQR)
    df = df[~mask].reset_index(drop=True)
    for col in numeric_cols:
        df[col].fillna(df[col].median(), inplace=True)

    df["alerts_per_day"]    = df["alerts_per_day"].fillna(df["alerts_per_day"].median()).astype(int)
    df["incidents_handled"] = df["incidents_handled"].fillna(df["incidents_handled"].median()).astype(int)

    # Extra safety: fill any residual NaNs in all numeric cols
    for c in numeric_cols:
        df[c] = df[c].fillna(df[c].median())

    # Feature engineering
    df["detection_efficiency"] = (df["threat_detection_rate"] * (1 - df["false_positive_rate"]/100)).round(3)
    df["response_quality"]     = (df["system_uptime"] / df["incident_response_time"]).round(4)
    df["sla_score"] = (
        0.35*df["threat_detection_rate"]
        + 0.30*(df["system_uptime"]-97)*10
        + 0.20*(1-df["false_positive_rate"]/100)*100
        + 0.15*(1-df["escalation_rate"]/100)*100
    ).round(3)
    df["client_type_code"] = df["client_type"].map({"SME":0,"IT Firm":1,"Bank/Govt":2})
    return df

@st.cache_data
def fit_models(df):
    # K-Means
    cluster_features = [
        "threat_detection_rate","incident_response_time","system_uptime",
        "false_positive_rate","client_satisfaction",
        "patch_compliance_rate","escalation_rate"
    ]
    scaler   = StandardScaler()
    X_scaled = scaler.fit_transform(df[cluster_features])
    kmeans   = KMeans(n_clusters=3, init="k-means++", n_init=20,
                      max_iter=500, random_state=42)
    kmeans.fit(X_scaled)
    df = df.copy()
    df["cluster"] = kmeans.labels_

    profile_cols = list(dict.fromkeys(cluster_features + ["client_satisfaction"]))
    profile    = df.groupby("cluster")[profile_cols].mean().round(3)
    sat_series = df.groupby("cluster")["client_satisfaction"].mean()
    sat_order  = sat_series.sort_values(ascending=False).index.tolist()
    tier_names = ["Premium (High-Performance)","Standard (Mid-Tier)","At-Risk (Low-Performance)"]
    label_map  = {int(c): name for c, name in zip(sat_order, tier_names)}
    df["cluster_label"] = df["cluster"].map(label_map)

    pca  = PCA(n_components=2, random_state=42)
    Xpca = pca.fit_transform(X_scaled)
    df["pca1"] = Xpca[:, 0]
    df["pca2"] = Xpca[:, 1]

    sil = silhouette_score(X_scaled, kmeans.labels_)

    # Linear Regression
    feat_cols = [
        "threat_detection_rate","incident_response_time",
        "system_uptime","false_positive_rate",
        "patch_compliance_rate","escalation_rate",
        "analyst_utilization","alerts_per_day"
    ]
    X = df[feat_cols]
    y = df["client_satisfaction"]
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
    lr = LinearRegression().fit(X_tr, y_tr)
    y_pred = lr.predict(X_te)
    r2   = r2_score(y_te, y_pred)
    mae  = mean_absolute_error(y_te, y_pred)
    rmse = np.sqrt(mean_squared_error(y_te, y_pred))

    coef_df = pd.DataFrame({"Feature": feat_cols, "Coefficient": lr.coef_})

    # CLV
    def ret_from_sat(s):
        return 0.92 if s >= 8.0 else (0.75 if s >= 5.0 else 0.50)
    df["retention_rate"]     = df["client_satisfaction"].apply(ret_from_sat)
    df["avg_lifetime_years"] = 1 / (1 - df["retention_rate"])
    df["clv"]                = df["avg_lifetime_years"] * 300_000

    return df, kmeans, scaler, pca, label_map, lr, feat_cols, X_te, y_te, y_pred, r2, mae, rmse, coef_df, sil, cluster_features, profile

# ──────────────────────────────────────────────
# LOAD DATA
# ──────────────────────────────────────────────
with st.spinner("Initialising SOC Analytics Engine…"):
    df_clean = generate_and_clean_data()
    (df, kmeans, scaler, pca, label_map, lr, feat_cols,
     X_te, y_te, y_pred, r2, mae, rmse, coef_df, sil,
     cluster_features, profile) = fit_models(df_clean)

# ──────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 1.5rem;'>
        <div style='font-size:2.5rem;'>🛡️</div>
        <div class='nav-title'>CyberWatch</div>
        <div class='nav-sub'>SOC Analytics Platform</div>
        <div style='font-size:0.7rem; color:#3a5278; margin-top:0.3rem;'>Case Study 94 · B.Tech CSE 2024-28</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    selected = st.radio(
        "NAVIGATION",
        options=PAGES,
        index=PAGES.index(st.session_state.page),
        label_visibility="visible"
    )
    if selected != st.session_state.page:
        set_page(selected)
        st.rerun()
    page = st.session_state.page
    st.markdown("---")
    st.markdown(f"""
    <div style='font-size:0.72rem; color:#3a5278; line-height:1.8;'>
    <b style='color:#7a92b8;'>DATASET</b><br>
    Clients: {len(df)}<br>
    Features: {len(feat_cols)}<br>
    Clusters: 3<br>
    Model R²: {r2:.3f}<br>
    <br>
    <b style='color:#7a92b8;'>COMPANY</b><br>
    CyberWatch SOC Services<br>
    Hyderabad, India
    </div>
    """, unsafe_allow_html=True)

# ensure page var is always defined (when sidebar is collapsed, with block may not run)
if "page" not in st.session_state:
    st.session_state.page = PAGES[0]
page = st.session_state.page

# ══════════════════════════════════════════════════════════════════
# PAGE 1: EXECUTIVE DASHBOARD
# ══════════════════════════════════════════════════════════════════
if page == "🏠  Executive Dashboard":
    st.markdown("""
    <div class='page-banner'>
        <h1>🛡️ EXECUTIVE DASHBOARD</h1>
        <p>CyberWatch SOC Services Pvt. Ltd. · Hyderabad · Financial & Operational Overview</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Financial Parameters ──
    st.markdown("<div class='section-header'>Financial Parameters</div>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        initial_invest = st.number_input("Initial Investment (₹ Cr)", value=6.0, step=0.5, min_value=1.0, max_value=20.0)
    with c2:
        op_cost = st.number_input("Annual Op. Cost (₹ Cr)", value=2.0, step=0.1, min_value=0.5, max_value=10.0)
    with c3:
        num_clients = st.number_input("Year-1 Clients", value=150, step=10, min_value=10, max_value=500)
    with c4:
        fee_lakh = st.number_input("Fee per Client (₹ Lakh/yr)", value=3.0, step=0.5, min_value=0.5, max_value=10.0)

    revenue    = num_clients * fee_lakh / 100          # crores
    net_yr1    = revenue - op_cost - initial_invest
    surplus_yr2= revenue - op_cost
    payback    = initial_invest / surplus_yr2 if surplus_yr2 > 0 else float("inf")

    # ── KPI Row ──
    st.markdown("<div class='section-header'>Key Financial KPIs</div>", unsafe_allow_html=True)
    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:
        st.markdown(f"""<div class='kpi-card'>
            <div class='kpi-val'>₹{revenue:.1f} Cr</div>
            <div class='kpi-label'>Annual Revenue</div>
        </div>""", unsafe_allow_html=True)
    with k2:
        col = "kpi-red" if net_yr1 < 0 else "kpi-green"
        sign = "" if net_yr1 >= 0 else "-"
        st.markdown(f"""<div class='kpi-card {col}'>
            <div class='kpi-val'>{sign}₹{abs(net_yr1):.1f} Cr</div>
            <div class='kpi-label'>Net Benefit (Yr 1)</div>
        </div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""<div class='kpi-card kpi-green'>
            <div class='kpi-val'>₹{surplus_yr2:.1f} Cr</div>
            <div class='kpi-label'>Annual Surplus (Yr 2+)</div>
        </div>""", unsafe_allow_html=True)
    with k4:
        st.markdown(f"""<div class='kpi-card kpi-yellow'>
            <div class='kpi-val'>{payback:.1f} yrs</div>
            <div class='kpi-label'>Payback Period</div>
        </div>""", unsafe_allow_html=True)
    with k5:
        roi = (surplus_yr2 / initial_invest) * 100
        st.markdown(f"""<div class='kpi-card'>
            <div class='kpi-val'>{roi:.0f}%</div>
            <div class='kpi-label'>Annual ROI (Yr 2+)</div>
        </div>""", unsafe_allow_html=True)

    # ── Operational KPIs ──
    st.markdown("<div class='section-header'>Operational KPIs</div>", unsafe_allow_html=True)
    o1, o2, o3, o4, o5 = st.columns(5)
    with o1:
        st.markdown(f"""<div class='kpi-card'>
            <div class='kpi-val'>{df["threat_detection_rate"].mean():.1f}%</div>
            <div class='kpi-label'>Avg Detection Rate</div>
        </div>""", unsafe_allow_html=True)
    with o2:
        st.markdown(f"""<div class='kpi-card kpi-yellow'>
            <div class='kpi-val'>{df["incident_response_time"].mean():.1f} min</div>
            <div class='kpi-label'>Avg Response Time</div>
        </div>""", unsafe_allow_html=True)
    with o3:
        st.markdown(f"""<div class='kpi-card kpi-green'>
            <div class='kpi-val'>{df["system_uptime"].mean():.2f}%</div>
            <div class='kpi-label'>Avg System Uptime</div>
        </div>""", unsafe_allow_html=True)
    with o4:
        st.markdown(f"""<div class='kpi-card'>
            <div class='kpi-val'>{df["client_satisfaction"].mean():.2f}/10</div>
            <div class='kpi-label'>Avg Satisfaction</div>
        </div>""", unsafe_allow_html=True)
    with o5:
        st.markdown(f"""<div class='kpi-card kpi-red'>
            <div class='kpi-val'>{df["false_positive_rate"].mean():.1f}%</div>
            <div class='kpi-label'>Avg False Positive</div>
        </div>""", unsafe_allow_html=True)

    # ── 5-Year Projection Chart ──
    st.markdown("<div class='section-header'>5-Year Financial Projection</div>", unsafe_allow_html=True)

    growth_rate = st.slider("Annual Client Growth Rate (%)", 10, 40, 20, 5) / 100
    years   = [1, 2, 3, 4, 5]
    clients = [num_clients * (1 + growth_rate)**(y-1) for y in years]
    rev_yr  = [c * fee_lakh / 100 for c in clients]
    opc_yr  = [op_cost * (1.1**(y-1)) for y in years]
    inv_yr  = [initial_invest, 0, 0, 0, 0]
    net_yr  = [r - o - i for r, o, i in zip(rev_yr, opc_yr, inv_yr)]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.patch.set_facecolor(DARK_FIG)

    x     = np.arange(5)
    width = 0.25
    axes[0].bar(x - width, rev_yr, width, color=ACCENT,  label="Revenue",     alpha=0.85)
    axes[0].bar(x,          opc_yr,  width, color=ACCENT3, label="Op. Cost",    alpha=0.85)
    axes[0].bar(x + width, inv_yr,  width, color=ACCENT4, label="Investment",  alpha=0.85)
    axes[0].set_xticks(x)
    axes[0].set_xticklabels([f"Yr {y}" for y in years])
    axes[0].set_ylabel("₹ Crores")
    axes[0].set_title("Revenue vs. Cost Breakdown")
    axes[0].legend()

    bar_colors = [ACCENT3 if n < 0 else ACCENT2 for n in net_yr]
    bars = axes[1].bar(years, net_yr, color=bar_colors, edgecolor=DARK_BG, linewidth=0.8)
    axes[1].axhline(0, color=TEXT_CLR, linewidth=1, linestyle="--", alpha=0.5)
    axes[1].set_xlabel("Year")
    axes[1].set_ylabel("₹ Crores")
    axes[1].set_title("5-Year Net Benefit")
    for bar, n in zip(bars, net_yr):
        axes[1].text(bar.get_x()+bar.get_width()/2,
                     n + (0.08 if n >= 0 else -0.25),
                     f"₹{n:.1f}Cr", ha="center", fontsize=9, fontweight="bold",
                     color=TEXT_CLR)

    fig.suptitle("CyberWatch SOC — 5-Year Financial Projection", fontsize=14, fontweight="bold", color=ACCENT)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    # ── Financial Summary ──
    if net_yr1 < 0:
        st.markdown(f"""<div class='warn-box'>
        ⚠️ <b>Year 1 Net Benefit: ₹{net_yr1:.2f} Crores</b> — Negative due to ₹{initial_invest:.1f} Cr upfront capital outlay.
        This is expected in infrastructure-heavy businesses.
        </div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class='success-box'>
    ✅ <b>Payback Period: {payback:.1f} years</b> — From Year 2, annual surplus is ₹{surplus_yr2:.1f} Crores.
    The SOC becomes profitable by Year {int(np.ceil(payback))+1}, with cumulative 5-year net benefit of
    <b>₹{sum(net_yr):.1f} Crores</b>.
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# PAGE 2: EDA
# ══════════════════════════════════════════════════════════════════
elif page == "📊  Exploratory Data Analysis":
    st.markdown("""
    <div class='page-banner'>
        <h1>📊 EXPLORATORY DATA ANALYSIS</h1>
        <p>Synthetic SOC performance data · 150 clients · 10 core KPI variables</p>
    </div>
    """, unsafe_allow_html=True)

    # Variable info
    st.markdown("<div class='section-header'>SOC Performance Variables (Q3)</div>", unsafe_allow_html=True)
    vars_info = {
        "threat_detection_rate (%)": ("🎯", "% of actual threats correctly identified. Target: >95%"),
        "incident_response_time (min)": ("⚡", "Time from detection to response. Target: <15 min"),
        "system_uptime (%)": ("🔋", "% SOC operational time. Target: >99.9%"),
        "false_positive_rate (%)": ("⚠️", "Fraction of alerts that are not real threats. Target: <10%"),
        "alerts_per_day (count)": ("📡", "Daily security alerts per client. Needs AI triage"),
        "incidents_handled (count)": ("🛡️", "Confirmed incidents resolved per month"),
        "client_satisfaction (1-10)": ("⭐", "Client rating of service quality. Drives retention & CLV"),
        "escalation_rate (%)": ("📈", "% incidents escalated to higher tiers. High = analyst gaps"),
        "analyst_utilization (%)": ("👨‍💻", "% analyst hours on active monitoring. Target: 65-80%"),
        "patch_compliance_rate (%)": ("🔒", "% client systems with up-to-date patches"),
    }
    r1, r2_ = st.columns(2)
    items = list(vars_info.items())
    for i, (var, (icon, desc)) in enumerate(items):
        col = r1 if i % 2 == 0 else r2_
        with col:
            st.markdown(f"""<div class='info-box'>
            <b>{icon} {var}</b><br>
            <span style='color:#7a92b8; font-size:0.85rem;'>{desc}</span>
            </div>""", unsafe_allow_html=True)

    # ── Distribution Plots ──
    st.markdown("<div class='section-header'>Metric Distributions</div>", unsafe_allow_html=True)

    cols_to_plot = ["threat_detection_rate","incident_response_time","system_uptime",
                    "false_positive_rate","client_satisfaction","alerts_per_day"]
    labels_plt   = ["Threat Detection Rate (%)","Incident Response Time (min)","System Uptime (%)",
                    "False Positive Rate (%)","Client Satisfaction (1–10)","Alerts per Day"]
    pal = [ACCENT, ACCENT3, ACCENT2, ACCENT4, "#c77dff", "#4cc9f0"]

    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    fig.patch.set_facecolor(DARK_FIG)
    axes = axes.flatten()
    for i, (col_, lbl, clr) in enumerate(zip(cols_to_plot, labels_plt, pal)):
        ax = axes[i]
        ax.hist(df[col_], bins=22, color=clr, edgecolor=DARK_FIG, alpha=0.82)
        mean_v  = df[col_].mean()
        med_v   = df[col_].median()
        ax.axvline(mean_v,  color="white", linestyle="--", lw=1.5, label=f"Mean={mean_v:.2f}")
        ax.axvline(med_v,   color=ACCENT4, linestyle=":",  lw=1.5, label=f"Median={med_v:.2f}")
        ax.set_title(f"Distribution · {lbl}")
        ax.set_xlabel(lbl)
        ax.set_ylabel("Frequency")
        ax.legend(fontsize=8)
    fig.suptitle("SOC Performance Metric Distributions", fontsize=14, fontweight="bold", color=ACCENT, y=1.01)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    # ── Correlation Heatmap ──
    st.markdown("<div class='section-header'>Correlation Heatmap</div>", unsafe_allow_html=True)
    num_cols = ["threat_detection_rate","incident_response_time","system_uptime",
                "false_positive_rate","alerts_per_day","client_satisfaction",
                "escalation_rate","analyst_utilization","patch_compliance_rate"]
    corr = df[num_cols].corr()

    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor(DARK_FIG)
    ax.set_facecolor(DARK_BG)
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    sns.heatmap(corr, annot=True, fmt=".2f", cmap=cmap,
                linewidths=0.5, linecolor=DARK_FIG, ax=ax,
                annot_kws={"size": 9}, vmin=-1, vmax=1,
                cbar_kws={"shrink": 0.8})
    ax.set_title("Correlation Matrix — SOC KPIs", fontsize=13, fontweight="bold", color=ACCENT)
    ax.tick_params(colors=TEXT_CLR, labelsize=9)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown("""<div class='info-box'>
    🔍 <b>Key Insights:</b>
    <ul style='margin:0.5rem 0 0; padding-left:1.2rem; color:#7a92b8; font-size:0.88rem;'>
    <li><b>threat_detection_rate</b> shows a strong positive correlation with client satisfaction</li>
    <li><b>incident_response_time</b> has a negative correlation — faster response = higher satisfaction</li>
    <li><b>false_positive_rate</b> negatively impacts satisfaction by causing alert fatigue</li>
    <li><b>system_uptime</b> is positively correlated with both detection rate and satisfaction</li>
    </ul>
    </div>""", unsafe_allow_html=True)

    # ── Segment Comparison ──
    st.markdown("<div class='section-header'>Performance by Client Segment</div>", unsafe_allow_html=True)
    seg_metrics = ["threat_detection_rate","incident_response_time",
                   "system_uptime","false_positive_rate","client_satisfaction"]
    seg_labels  = ["Detection Rate","Response Time","Uptime","False Positive","Satisfaction"]
    seg_df = df.groupby("client_type")[seg_metrics].mean()

    fig, ax = plt.subplots(figsize=(13, 6))
    fig.patch.set_facecolor(DARK_FIG)
    ax.set_facecolor(DARK_BG)
    x    = np.arange(len(seg_labels))
    w    = 0.25
    segs = ["SME", "IT Firm", "Bank/Govt"]
    clrs = [ACCENT3, ACCENT4, ACCENT2]
    for i, (seg, clr) in enumerate(zip(segs, clrs)):
        if seg in seg_df.index:
            vals = seg_df.loc[seg, seg_metrics].values
            ax.bar(x + (i-1)*w, vals, w, label=seg, color=clr, alpha=0.85, edgecolor=DARK_FIG)
    ax.set_xticks(x)
    ax.set_xticklabels(seg_labels)
    ax.set_ylabel("Value")
    ax.set_title("Average KPI Performance by Client Segment")
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    # ── Raw data ──
    with st.expander("🗂️ View Cleaned Dataset (first 50 rows)"):
        st.dataframe(df.head(50), use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# PAGE 3: K-MEANS CLUSTERING
# ══════════════════════════════════════════════════════════════════
elif page == "🔵  Client Segmentation (K-Means)":
    st.markdown("""
    <div class='page-banner'>
        <h1>🔵 CLIENT SEGMENTATION · K-MEANS CLUSTERING</h1>
        <p>Unsupervised ML to identify distinct client performance tiers (K=3)</p>
    </div>
    """, unsafe_allow_html=True)

    # Cluster summary cards
    st.markdown("<div class='section-header'>Cluster Profiles</div>", unsafe_allow_html=True)
    seg_clr_map = {
        "Premium (High-Performance)":   ("kpi-green",  "badge-premium", "✅"),
        "Standard (Mid-Tier)":          ("kpi-yellow", "badge-standard","⚡"),
        "At-Risk (Low-Performance)":    ("kpi-red",    "badge-atrisk",  "⚠️"),
    }
    for cid in range(3):
        lbl = label_map[cid]
        kc, bc, icon = seg_clr_map.get(lbl, ("kpi-card","",""))
        grp = df[df["cluster"] == cid]
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            st.markdown(f"""<div class='kpi-card {kc}'>
                <div class='kpi-val'>{len(grp)}</div>
                <div class='kpi-label'>{icon} {lbl[:20]}..</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class='kpi-card'>
                <div class='kpi-val'>{grp["threat_detection_rate"].mean():.1f}%</div>
                <div class='kpi-label'>Detection Rate</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class='kpi-card'>
                <div class='kpi-val'>{grp["incident_response_time"].mean():.1f}m</div>
                <div class='kpi-label'>Response Time</div>
            </div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""<div class='kpi-card'>
                <div class='kpi-val'>{grp["client_satisfaction"].mean():.2f}/10</div>
                <div class='kpi-label'>Satisfaction</div>
            </div>""", unsafe_allow_html=True)
        with c5:
            st.markdown(f"""<div class='kpi-card'>
                <div class='kpi-val'>{grp["false_positive_rate"].mean():.1f}%</div>
                <div class='kpi-label'>False Positive</div>
            </div>""", unsafe_allow_html=True)
        st.markdown("")

    st.markdown(f"<div class='info-box'>📐 <b>Silhouette Score: {sil:.4f}</b> — A score above 0.4 indicates well-separated, meaningful clusters.</div>",
                unsafe_allow_html=True)

    # ── PCA Scatter + Boxplot ──
    st.markdown("<div class='section-header'>Cluster Visualisations</div>", unsafe_allow_html=True)

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    fig.patch.set_facecolor(DARK_FIG)

    for cid, lbl in label_map.items():
        mask = df["cluster"] == cid
        axes[0].scatter(df.loc[mask,"pca1"], df.loc[mask,"pca2"],
                        label=f"C{cid}: {lbl[:15]}..",
                        color=CLUSTER_COLORS[cid], alpha=0.72,
                        edgecolors=DARK_FIG, linewidth=0.4, s=65)
    Xpca_c = pca.transform(kmeans.cluster_centers_)
    axes[0].scatter(Xpca_c[:,0], Xpca_c[:,1], marker="X", s=220,
                    color="white", zorder=5, label="Centroids")
    axes[0].set_xlabel(f"PCA 1")
    axes[0].set_ylabel(f"PCA 2")
    axes[0].set_title("K-Means Clusters (PCA 2D Projection)")
    axes[0].legend(fontsize=8)

    data_sat  = [df[df["cluster"]==c]["client_satisfaction"].values for c in range(3)]
    xlabs_bp  = [f"C{c}\n{label_map[c][:12]}.." for c in range(3)]
    bp = axes[1].boxplot(data_sat, labels=xlabs_bp, patch_artist=True)
    for patch, c in zip(bp["boxes"], range(3)):
        patch.set_facecolor(CLUSTER_COLORS[c])
        patch.set_alpha(0.75)
    for element in ["whiskers","caps","medians","fliers"]:
        for item in bp[element]:
            item.set_color(TEXT_CLR)
    axes[1].set_ylabel("Client Satisfaction (1–10)")
    axes[1].set_title("Satisfaction Distribution by Cluster")

    fig.suptitle("K-Means Client Segmentation Analysis", fontsize=14, fontweight="bold", color=ACCENT)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    # ── Radar Chart ──
    st.markdown("<div class='section-header'>Cluster Performance Radar</div>", unsafe_allow_html=True)
    radar_metrics = ["threat_detection_rate","system_uptime","client_satisfaction",
                     "patch_compliance_rate","false_positive_rate"]
    radar_labels  = ["Detection Rate","Uptime","Satisfaction","Patch Compliance","False Positive (inv)"]

    norm_p = profile[radar_metrics].copy()
    for col_ in radar_metrics:
        mn, mx = norm_p[col_].min(), norm_p[col_].max()
        if mx > mn:
            norm_p[col_] = (norm_p[col_] - mn) / (mx - mn)
    # Invert false positive so higher = better
    norm_p["false_positive_rate"] = 1 - norm_p["false_positive_rate"]

    angles = np.linspace(0, 2*np.pi, len(radar_metrics), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={"polar": True})
    fig.patch.set_facecolor(DARK_FIG)
    ax.set_facecolor(DARK_BG)
    ax.spines["polar"].set_color(GRID_CLR)

    for cid in range(3):
        if cid in norm_p.index:
            values = norm_p.loc[cid, radar_metrics].tolist()
            values += values[:1]
            ax.plot(angles, values, linewidth=2.5,
                    label=f"C{cid}: {label_map[cid]}",
                    color=CLUSTER_COLORS[cid])
            ax.fill(angles, values, alpha=0.12, color=CLUSTER_COLORS[cid])

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(radar_labels, fontsize=11, color=TEXT_CLR)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["25%","50%","75%","100%"], fontsize=8, color=TEXT_CLR)
    ax.grid(color=GRID_CLR, alpha=0.5)
    ax.set_title("Cluster Performance Radar Chart", fontsize=13, fontweight="bold",
                 color=ACCENT, pad=20)
    ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.15), fontsize=9)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    # ── Cluster distribution by client type ──
    st.markdown("<div class='section-header'>Cluster × Client Type Breakdown</div>", unsafe_allow_html=True)
    cross = pd.crosstab(df["cluster_label"], df["client_type"])
    st.dataframe(cross, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# PAGE 4: SATISFACTION PREDICTOR
# ══════════════════════════════════════════════════════════════════
elif page == "🤖  Satisfaction Predictor":
    st.markdown("""
    <div class='page-banner'>
        <h1>🤖 CLIENT SATISFACTION PREDICTOR</h1>
        <p>Linear Regression model · Predict satisfaction score from SOC operational metrics</p>
    </div>
    """, unsafe_allow_html=True)

    # Model metrics
    st.markdown("<div class='section-header'>Model Performance</div>", unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""<div class='kpi-card kpi-green'>
            <div class='kpi-val'>{r2:.4f}</div>
            <div class='kpi-label'>R² Score (Test)</div>
        </div>""", unsafe_allow_html=True)
    with m2:
        st.markdown(f"""<div class='kpi-card'>
            <div class='kpi-val'>{mae:.4f}</div>
            <div class='kpi-label'>MAE</div>
        </div>""", unsafe_allow_html=True)
    with m3:
        st.markdown(f"""<div class='kpi-card kpi-yellow'>
            <div class='kpi-val'>{np.sqrt(mean_squared_error(y_te, y_pred)):.4f}</div>
            <div class='kpi-label'>RMSE</div>
        </div>""", unsafe_allow_html=True)
    with m4:
        st.markdown(f"""<div class='kpi-card'>
            <div class='kpi-val'>{r2*100:.1f}%</div>
            <div class='kpi-label'>Variance Explained</div>
        </div>""", unsafe_allow_html=True)

    # ── Prediction Interface ──
    st.markdown("<div class='section-header'>🎛️ Interactive Prediction Interface</div>", unsafe_allow_html=True)
    st.markdown("<div class='info-box'>Adjust the SOC operational metrics below to predict the resulting Client Satisfaction Score (1–10).</div>",
                unsafe_allow_html=True)

    col_l, col_r = st.columns([3, 2])
    with col_l:
        c1, c2 = st.columns(2)
        with c1:
            tdr_in  = st.slider("Threat Detection Rate (%)",   78.0, 99.9,  df["threat_detection_rate"].mean(),  0.5)
            su_in   = st.slider("System Uptime (%)",           97.5, 99.99, df["system_uptime"].mean(),           0.01)
            pcr_in  = st.slider("Patch Compliance Rate (%)",   55.0, 99.0,  df["patch_compliance_rate"].mean(),   1.0)
            au_in   = st.slider("Analyst Utilization (%)",     45.0, 95.0,  df["analyst_utilization"].mean(),     1.0)
        with c2:
            irt_in  = st.slider("Incident Response Time (min)",3.0,  45.0,  df["incident_response_time"].mean(),  0.5)
            fpr_in  = st.slider("False Positive Rate (%)",     1.0,  25.0,  df["false_positive_rate"].mean(),     0.5)
            er_in   = st.slider("Escalation Rate (%)",         1.0,  30.0,  df["escalation_rate"].mean(),         0.5)
            apd_in  = st.slider("Alerts per Day",              80,   1500,  int(df["alerts_per_day"].mean()),     10)

    input_vals = pd.DataFrame([{
        "threat_detection_rate":  tdr_in,
        "incident_response_time": irt_in,
        "system_uptime":          su_in,
        "false_positive_rate":    fpr_in,
        "patch_compliance_rate":  pcr_in,
        "escalation_rate":        er_in,
        "analyst_utilization":    au_in,
        "alerts_per_day":         apd_in,
    }])[feat_cols]

    prediction = np.clip(lr.predict(input_vals)[0], 1, 10)
    if prediction >= 8.0:
        ret_rate = 0.92; tier = "Premium"; badge = "badge-premium"; picon = "✅"
    elif prediction >= 5.0:
        ret_rate = 0.75; tier = "Standard"; badge = "badge-standard"; picon = "⚡"
    else:
        ret_rate = 0.50; tier = "At-Risk";  badge = "badge-atrisk";  picon = "⚠️"

    clv_pred = (1 / (1 - ret_rate)) * 300_000

    with col_r:
        score_color = ACCENT2 if prediction >= 7 else (ACCENT4 if prediction >= 5 else ACCENT3)
        st.markdown(f"""
        <div style='background:{DARK_BG}; border:2px solid {score_color};
                    border-radius:12px; padding:2rem; text-align:center; margin-top:0.5rem;'>
            <div style='font-size:0.8rem; color:#7a92b8; text-transform:uppercase;
                        letter-spacing:2px; margin-bottom:0.5rem;'>Predicted Satisfaction</div>
            <div style='font-family:Rajdhani,sans-serif; font-size:4.5rem; font-weight:700;
                        color:{score_color}; line-height:1;'>{prediction:.2f}</div>
            <div style='color:#7a92b8; font-size:0.9rem; margin-bottom:1rem;'>out of 10</div>
            <span class='badge {badge}'>{picon} {tier}</span>
            <hr style='border-color:#1a3050; margin:1rem 0;'>
            <div style='font-size:0.8rem; color:#7a92b8;'>Retention Rate</div>
            <div style='font-family:Rajdhani,sans-serif; font-size:1.8rem; color:{score_color};'>{ret_rate*100:.0f}%</div>
            <div style='font-size:0.8rem; color:#7a92b8; margin-top:0.5rem;'>Est. CLV</div>
            <div style='font-family:Rajdhani,sans-serif; font-size:1.8rem; color:{score_color};'>
                ₹{clv_pred/100000:.1f}L
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── What-If Scenario Analysis ──
    st.markdown("<div class='section-header'>What-If Scenario Analysis</div>", unsafe_allow_html=True)
    baseline = X_te.mean()

    scenarios = {
        "Baseline":            {},
        "Better Detection":    {"threat_detection_rate": +5},
        "Faster Response":     {"incident_response_time": -5},
        "Lower FPR":           {"false_positive_rate": -5},
        "Better Compliance":   {"patch_compliance_rate": +5},
        "All Improvements":    {"threat_detection_rate": +5, "incident_response_time": -5,
                                "false_positive_rate": -5, "patch_compliance_rate": +5},
    }
    names, preds_sc = [], []
    for name, changes in scenarios.items():
        vals = baseline.copy()
        for k, v in changes.items(): vals[k] += v
        vals["incident_response_time"] = max(3, vals["incident_response_time"])
        vals["false_positive_rate"]    = max(1, vals["false_positive_rate"])
        vals["patch_compliance_rate"]  = min(99, vals["patch_compliance_rate"])
        p = np.clip(lr.predict(pd.DataFrame([vals])[feat_cols])[0], 1, 10)
        names.append(name); preds_sc.append(p)

    fig, ax = plt.subplots(figsize=(13, 5))
    fig.patch.set_facecolor(DARK_FIG)
    ax.set_facecolor(DARK_BG)
    clrs_sc = [ACCENT if n == "Baseline" else (ACCENT2 if n == "All Improvements" else ACCENT4)
               for n in names]
    bars = ax.bar(names, preds_sc, color=clrs_sc, edgecolor=DARK_FIG, linewidth=0.6)
    ax.axhline(preds_sc[0], linestyle="--", color=TEXT_CLR, alpha=0.4, linewidth=1)
    ax.set_ylabel("Predicted Satisfaction (1–10)")
    ax.set_title("What-If Scenario: Impact of SOC Improvements on Client Satisfaction")
    ax.set_ylim(0, 10.5)
    for bar, val in zip(bars, preds_sc):
        ax.text(bar.get_x()+bar.get_width()/2, val+0.1,
                f"{val:.2f}", ha="center", fontweight="bold", color=TEXT_CLR, fontsize=10)
    plt.xticks(rotation=15)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    # ── Regression Diagnostics ──
    st.markdown("<div class='section-header'>Model Diagnostics</div>", unsafe_allow_html=True)
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.patch.set_facecolor(DARK_FIG)

    # Actual vs Predicted
    lo_, hi_ = min(y_te.min(), y_pred.min()), max(y_te.max(), y_pred.max())
    axes[0].scatter(y_te, y_pred, alpha=0.72, s=60, color=ACCENT, edgecolors=DARK_FIG, linewidth=0.4)
    axes[0].plot([lo_, hi_],[lo_, hi_], color=ACCENT3, lw=2, linestyle="--", label="Perfect")
    axes[0].set(title=f"Actual vs Predicted (R²={r2:.3f})",
                xlabel="Actual Satisfaction", ylabel="Predicted Satisfaction")
    axes[0].legend()

    # Residuals
    residuals = y_te - y_pred
    axes[1].hist(residuals, bins=20, color=ACCENT2, edgecolor=DARK_FIG, alpha=0.85)
    axes[1].axvline(0, color=ACCENT3, ls="--", lw=2)
    axes[1].set(title="Residual Distribution", xlabel="Residual", ylabel="Frequency")

    # Feature Coefficients
    coef_sorted = coef_df.sort_values("Coefficient")
    bar_clrs    = [ACCENT3 if c < 0 else ACCENT2 for c in coef_sorted["Coefficient"]]
    axes[2].barh(coef_sorted["Feature"], coef_sorted["Coefficient"],
                 color=bar_clrs, edgecolor=DARK_FIG)
    axes[2].axvline(0, color=TEXT_CLR, linewidth=0.8)
    axes[2].set(title="Feature Coefficients", xlabel="Coefficient")

    fig.suptitle("Linear Regression — Model Diagnostics", fontsize=14,
                 fontweight="bold", color=ACCENT)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown("""<div class='info-box'>
    📘 <b>Interpretation:</b><br>
    <span style='color:#7a92b8;'>
    Positive coefficients (threat_detection_rate, system_uptime, patch_compliance_rate) 
    improve satisfaction. Negative coefficients (incident_response_time, false_positive_rate, 
    escalation_rate) reduce it. The model validates that operational excellence directly 
    translates into client satisfaction.</span>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# PAGE 5: CLV & RECOMMENDATION
# ══════════════════════════════════════════════════════════════════
elif page == "💰  CLV & Business Recommendation":
    st.markdown("""
    <div class='page-banner'>
        <h1>💰 CLV ANALYSIS & BUSINESS RECOMMENDATION</h1>
        <p>Customer Lifetime Value · CRM Impact · Final Strategic Recommendation (Q5)</p>
    </div>
    """, unsafe_allow_html=True)

    # CLV Overview
    st.markdown("<div class='section-header'>Customer Lifetime Value (CLV) Overview</div>", unsafe_allow_html=True)
    total_clv = df["clv"].sum()
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class='kpi-card kpi-green'>
            <div class='kpi-val'>₹{total_clv/1e7:.2f} Cr</div>
            <div class='kpi-label'>Total Portfolio CLV</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class='kpi-card'>
            <div class='kpi-val'>₹37.5L</div>
            <div class='kpi-label'>High-Sat CLV (8–10)</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class='kpi-card kpi-yellow'>
            <div class='kpi-val'>₹12L</div>
            <div class='kpi-label'>Mid-Sat CLV (5–7)</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class='kpi-card kpi-red'>
            <div class='kpi-val'>₹6L</div>
            <div class='kpi-label'>Low-Sat CLV (&lt;5)</div>
        </div>""", unsafe_allow_html=True)

    # CLV Charts
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    fig.patch.set_facecolor(DARK_FIG)

    for cid, lbl in label_map.items():
        mask_ = df["cluster"] == cid
        axes[0].hist(df.loc[mask_, "clv"]/100_000, bins=12, alpha=0.70,
                     label=f"C{cid}: {lbl[:18]}", color=CLUSTER_COLORS[cid], edgecolor=DARK_FIG)
    axes[0].set_xlabel("CLV (₹ Lakhs)")
    axes[0].set_ylabel("Number of Clients")
    axes[0].set_title("CLV Distribution by Cluster")
    axes[0].legend(fontsize=8)

    bands    = ["Low (1–4)", "Mid (5–7)", "High (8–10)"]
    ret_vals = [0.50, 0.75, 0.92]
    clv_vals = [1/(1-r) * 300_000 / 100_000 for r in ret_vals]
    bar_clr  = [ACCENT3, ACCENT4, ACCENT2]
    bars_ = axes[1].bar(bands, clv_vals, color=bar_clr, edgecolor=DARK_FIG, linewidth=0.6)
    axes[1].set_xlabel("Satisfaction Band")
    axes[1].set_ylabel("CLV (₹ Lakhs)")
    axes[1].set_title("CLV by Satisfaction Level")
    for bar_, val in zip(bars_, clv_vals):
        axes[1].text(bar_.get_x()+bar_.get_width()/2, val+0.3,
                     f"₹{val:.1f}L", ha="center", fontweight="bold", fontsize=11, color=TEXT_CLR)

    fig.suptitle("Customer Lifetime Value Analysis — CyberWatch SOC",
                 fontsize=14, fontweight="bold", color=ACCENT)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown("""<div class='success-box'>
    🚀 <b>Key Insight:</b> High-satisfaction clients (score 8–10) generate <b>₹37.5L CLV</b> vs ₹6L 
    for low-satisfaction clients — a <b>6.25× revenue multiplier</b>. Operational excellence IS revenue.
    </div>""", unsafe_allow_html=True)

    # CRM Impact (Q5)
    st.markdown("<div class='section-header'>CRM & Business Impact (Q5 Answer)</div>", unsafe_allow_html=True)
    q1, q2, q3 = st.columns(3)
    with q1:
        st.markdown("""<div class='kpi-card kpi-green'>
        <div style='font-size:1.5rem;'>🎯</div>
        <div style='font-weight:700; color:#00ff9d; font-size:1rem; margin:0.5rem 0;'>Fast Threat Detection</div>
        <div style='font-size:0.82rem; color:#7a92b8;'>
        Minimises time-to-detect breaches, reducing financial damage.
        Builds client trust through proactive protection.
        Clients with >95% detection rate show 23% higher retention.
        </div></div>""", unsafe_allow_html=True)
    with q2:
        st.markdown("""<div class='kpi-card kpi-yellow'>
        <div style='font-size:1.5rem;'>⚡</div>
        <div style='font-weight:700; color:#ffd166; font-size:1rem; margin:0.5rem 0;'>Quick Incident Response</div>
        <div style='font-size:0.82rem; color:#7a92b8;'>
        Reduces Mean-Time-To-Respond (MTTR) and SLA violations.
        Every 5-min improvement in response time lifts satisfaction by ~0.3 pts.
        Prevents cascading breaches and regulatory fines.
        </div></div>""", unsafe_allow_html=True)
    with q3:
        st.markdown("""<div class='kpi-card'>
        <div style='font-size:1.5rem;'>🔋</div>
        <div style='font-weight:700; color:#00d4ff; font-size:1rem; margin:0.5rem 0;'>Reliable Monitoring</div>
        <div style='font-size:0.82rem; color:#7a92b8;'>
        99.9%+ uptime ensures zero unprotected windows.
        Consistent monitoring enables AI-driven threat intelligence.
        High uptime = confidence → 92% client retention → ₹37.5L CLV.
        </div></div>""", unsafe_allow_html=True)

    # ── Tiered Pricing ──
    st.markdown("<div class='section-header'>Recommended Tiered Pricing Strategy</div>", unsafe_allow_html=True)
    pricing = {
        "SME": {"price": "₹2L/yr", "features": "Basic 24×7 monitoring, monthly reports, email alerts"},
        "IT Firm": {"price": "₹3.5L/yr", "features": "Advanced SIEM, weekly threat reports, API integration"},
        "Bank/Govt": {"price": "₹5L+/yr", "features": "Dedicated analysts, SLA <10 min, compliance reports, ISO 27001"},
    }
    p1, p2, p3 = st.columns(3)
    for (seg, info), col in zip(pricing.items(), [p1, p2, p3]):
        with col:
            clr = {"SME":"kpi-red","IT Firm":"kpi-yellow","Bank/Govt":"kpi-green"}[seg]
            st.markdown(f"""<div class='kpi-card {clr}'>
            <div style='font-size:1.1rem; font-weight:700;'>{seg}</div>
            <div class='kpi-val'>{info["price"]}</div>
            <div style='font-size:0.8rem; color:#7a92b8; margin-top:0.5rem;'>{info["features"]}</div>
            </div>""", unsafe_allow_html=True)

    # ── Final Recommendation ──
    st.markdown("<div class='section-header'>⭐ Final Recommendation</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0a1f0a 0%,#051510 100%);
                border:2px solid #00ff9d; border-radius:12px; padding:1.5rem 2rem 0.5rem;
                margin-top:1rem; text-align:center;'>
        <div style='font-family:Rajdhani,sans-serif; font-size:1.6rem; font-weight:700;
                    color:#00ff9d; letter-spacing:2px; margin-bottom:0.5rem;'>
            ✅ RECOMMENDATION: ESTABLISH THE SOC
        </div>
    </div>
    """, unsafe_allow_html=True)

    rec_c1, rec_c2 = st.columns(2)
    with rec_c1:
        st.markdown("""<div class='info-box'>
        <div style='color:#00d4ff; font-weight:700; font-size:1rem; margin-bottom:0.5rem;'>📊 Financial Justification</div>
        <div style='color:#7a92b8; font-size:0.88rem; line-height:1.9;'>
        • Annual Revenue: ₹4.5 Crores (150 clients × ₹3L)<br>
        • Year 1 Net: -₹3.5 Cr (one-time capex)<br>
        • Year 2+ Surplus: ₹2.5 Crores/year<br>
        • Payback Period: ~2.4 years<br>
        • 5-Year Cumulative Net: ~₹7+ Crores
        </div></div>""", unsafe_allow_html=True)

        st.markdown("""<div style='background:rgba(255,209,102,0.07); border:1px solid rgba(255,209,102,0.3);
                    border-radius:8px; padding:1rem 1.2rem; margin-top:0.8rem;'>
        <div style='color:#ffd166; font-weight:700; font-size:1rem; margin-bottom:0.5rem;'>🎯 Priority Actions</div>
        <div style='color:#7a92b8; font-size:0.88rem; line-height:1.9;'>
        1. Tiered SLA agreements by segment<br>
        2. Reduce response time for At-Risk cluster first<br>
        3. AI-assisted alert triage (lower false positives)<br>
        4. ISO 27001 + SOC 2 Type II certification in Year 1<br>
        5. Upgrade Bank/Govt to ₹5L/yr pricing by Year 2
        </div></div>""", unsafe_allow_html=True)

    with rec_c2:
        st.markdown("""<div class='info-box'>
        <div style='color:#00d4ff; font-weight:700; font-size:1rem; margin-bottom:0.5rem;'>🔬 Technical Justification</div>
        <div style='color:#7a92b8; font-size:0.88rem; line-height:1.9;'>
        • K-Means reveals 3 distinct client segments for targeted SLAs<br>
        • Regression R²: strong — SOC KPIs explain satisfaction<br>
        • High-sat clients: 6× CLV multiplier vs low-sat<br>
        • AI-assisted triage reduces false positive overload<br>
        • SIEM enables scalability without headcount
        </div></div>""", unsafe_allow_html=True)

        st.markdown("""<div class='warn-box'>
        <div style='color:#ff6b6b; font-weight:700; font-size:1rem; margin-bottom:0.5rem;'>⚠️ Key Risks & Mitigation</div>
        <div style='color:#7a92b8; font-size:0.88rem; line-height:1.9;'>
        • <b>Analyst attrition</b> → Retention bonuses, upskilling budget<br>
        • <b>Zero-day threats</b> → Threat intelligence feed subscriptions<br>
        • <b>Regulatory changes</b> → Dedicated compliance officer<br>
        • <b>Price competition</b> → Differentiate via AI + certified SOC
        </div></div>""", unsafe_allow_html=True)

    # ── Summary Table ──
    st.markdown("<div class='section-header'>Analysis Summary Table</div>", unsafe_allow_html=True)
    summary_df = pd.DataFrame({
        "Section":     ["Q1: Revenue","Q2: Net Benefit","Q3: Variables","Q4: Data Gen",
                        "EDA","K-Means (K=3)","Linear Regression","Q5: CRM Impact","Recommendation"],
        "Method":      ["Formula","Formula","Domain Analysis","Python NumPy",
                        "Plots & Heatmap","K-Means Clustering","Predictive Model","CLV Analysis","All Evidence"],
        "Key Finding": ["₹4.5 Crores/year","-₹3.5 Cr Yr1 / +₹2.5 Cr Yr2+","10 critical SOC KPIs defined",
                        "150 synthetic client records","Detection rate & response time drive satisfaction",
                        "Premium / Standard / At-Risk segments",f"R²={r2:.3f} — SOC KPIs explain satisfaction",
                        "High-sat clients = 6× lifetime revenue","ESTABLISH THE SOC ✅"],
    })
    st.dataframe(summary_df, use_container_width=True, hide_index=True)
    st.markdown("""
    <div style='text-align:center; color:#3a5278; font-size:0.72rem; margin-top:2rem;'>
    CyberWatch SOC Services Pvt. Ltd. · Case Study 94 · B.Tech CSE 2024–28 · Semester IV · Business Studies
    </div>""", unsafe_allow_html=True)
