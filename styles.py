import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
    :root { --bg:#0c0e14; --panel:rgba(25,29,41,.72); --border:rgba(255,255,255,.09); --text:#f1f2f7; --muted:#9aa2b5; --accent:#9a8cff; }
    html, body, [class*="css"] { font-family:'DM Sans', sans-serif; }
    .stApp { background: radial-gradient(ellipse at 15% 0%, rgba(112,91,255,.12), transparent 35%), radial-gradient(ellipse at 90% 25%, rgba(49,170,178,.07), transparent 30%), #0c0e14; color:var(--text); }
    [data-testid="stHeader"] { background:transparent; }
    [data-testid="stSidebar"] { background:rgba(17,19,28,.92); border-right:1px solid rgba(255,255,255,.07); }
    [data-testid="stSidebar"] > div { padding-top:1.3rem; }
    .brand { display:flex; align-items:center; gap:12px; padding:5px 6px 20px; }
    .brand-mark { width:42px;height:42px;border-radius:14px;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#a89cff,#6b5ce7);color:white;font-family:Manrope;font-weight:800;font-size:23px;box-shadow:0 8px 24px rgba(124,105,255,.25); }
    .brand-name { font-family:Manrope;font-weight:800;font-size:22px;letter-spacing:-.8px;color:#f5f4ff; }
    .brand-tag { font-size:10px;color:#9098ac;letter-spacing:.2px;margin-top:-2px; }
    .sidebar-bottom { font-size:11px;color:#8992a7;padding:22px 7px 5px; }
    .status-dot { display:inline-block;width:7px;height:7px;background:#61d6a4;border-radius:50%;margin-right:7px; }
    .eyebrow { font-size:10px;letter-spacing:2px;color:#8f97aa;font-weight:700;padding:8px 0 18px; }
    .page-heading { display:flex;justify-content:space-between;align-items:center;margin:0 0 20px; }
    .page-heading h1 { font-family:Manrope,sans-serif;font-size:30px;font-weight:800;letter-spacing:-1.1px;margin:0;color:#f2f2f9; }
    .page-heading p { color:#9ca4b7;margin:5px 0 0;font-size:13px; }
    .metric-card { background:linear-gradient(145deg,rgba(36,40,55,.78),rgba(23,26,37,.74));border:1px solid rgba(255,255,255,.09);border-radius:18px;padding:20px 20px 17px;box-shadow:0 12px 36px rgba(0,0,0,.12);backdrop-filter:blur(18px);min-height:126px; }
    .metric-label { font-size:10px;letter-spacing:1.1px;font-weight:700;color:#929bb0;margin-bottom:13px; }
    .metric-value { font-family:Manrope;font-size:27px;font-weight:800;letter-spacing:-.8px;color:#f4f3fc; }
    .metric-foot { font-size:11px;color:#8f98ab;margin-top:7px; }
    .section-title { font-family:Manrope;font-size:16px;font-weight:750;color:#ececf6;margin:23px 0 13px; }
    .section-title span { font-family:'DM Sans';font-size:11px;color:#8d96aa;font-weight:400;margin-left:8px; }
    .insight { padding:12px 14px;margin:8px 0;background:rgba(143,128,255,.08);border:1px solid rgba(143,128,255,.17);border-radius:12px;color:#cbd0e0;font-size:12px;line-height:1.55; }
    .muted { float:right;color:#8d96aa;font-size:12px;font-weight:400; }
    div[data-testid="stVerticalBlockBorderWrapper"] { border-color:rgba(255,255,255,.1)!important;background:rgba(255,255,255,.025);border-radius:16px; }
    .stButton button { border-radius:10px;border:1px solid rgba(255,255,255,.12);font-weight:600;transition:all .2s ease; }
    .stButton button[kind="primary"], .stFormSubmitButton button[kind="primary"] { background:linear-gradient(135deg,#9586ff,#7563ed);border:0;color:white; }
    .stTextInput input, .stNumberInput input, .stDateInput input, .stSelectbox div[data-baseweb="select"] > div, .stTextArea textarea { border-radius:10px!important; }
    div[data-testid="stDataFrame"] { border:1px solid rgba(255,255,255,.08);border-radius:12px;overflow:hidden; }
    [data-testid="stMetric"] { background:rgba(255,255,255,.035);border:1px solid rgba(255,255,255,.07);padding:14px;border-radius:13px; }
    [data-testid="stMetricLabel"] { color:#9ba3b5; }
    hr { border-color:rgba(255,255,255,.08); }
    .stProgress > div > div > div > div { background:linear-gradient(90deg,#9586ff,#5fc7c2); }
    footer { visibility:hidden; }
    @media (max-width: 800px) { .page-heading h1 {font-size:24px}.metric-value{font-size:22px}.metric-card{padding:14px;min-height:112px} }
    </style>
    """, unsafe_allow_html=True)
