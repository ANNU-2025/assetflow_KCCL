import streamlit as st
import pandas as pd
from supabase import create_client, Client
import os
from datetime import datetime

# ==========================================
# SUPABASE
# ==========================================
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://emdjnndnsdebhbzebrsg.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVtZGpubmRuc2RlYmhiemVicnNnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODExNzU4NDYsImV4cCI6MjA5Njc1MTg0Nn0.ypy3k30Nbp2caJaNXpwxbrnUzrOLrhwTJ1FZwW5L8Fc")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="AssetFlow KCCL", page_icon="📦", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# SESSION & INITIAL STATE
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.markdown("<style>section[data-testid='stSidebar']{display:none}header[data-testid='stHeader']{display:none}</style>", unsafe_allow_html=True)

# ==========================================
# ULTRA-PREMIUM CORPORATE THEME (CSS)
# ==========================================
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* global typography override */
.stApp, .stApp *, div[data-testid="stMarkdownContainer"] p {
    font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
    color: #1E293B;
}

.stApp { background-color: #F8FAFC; }
.block-container { padding: 1.5rem 2.5rem !important; max-width: 1440px; margin: 0 auto; }

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] { background-color: #0F172A !important; border-right: 1px solid #1E293B !important; width: 250px !important; }
section[data-testid="stSidebar"] > div:first-child { width: 250px !important; }
#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; display: none !important; }

.sb-logo { padding: 30px 20px; text-align: center; border-bottom: 1px solid #1E293B; display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; }
.sb-logo-icon { width: 52px; height: 52px; margin-bottom: 12px; background: linear-gradient(135deg, #3B82F6, #2563EB); border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 24px; color: #fff; box-shadow: 0 4px 20px rgba(59,130,246,0.25); }
.sb-logo-name { font-size: 18px; font-weight: 700; color: #F8FAFC; letter-spacing: -0.4px; }
.sb-logo-sub { font-size: 10px; color: #64748B; text-transform: uppercase; letter-spacing: 1.5px; margin-top: 4px; font-weight: 600; }
.sb-logo img { border-radius: 10px; max-width: 110px; height: auto; object-fit: contain; margin-bottom: 10px; display: block; }

.sb-nav-label { font-size: 10px; color: #475569; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700; padding: 24px 20px 10px; }
section[data-testid="stSidebar"] div[data-testid="stRadio"] > label { margin-bottom: 4px !important; }
section[data-testid="stSidebar"] div[data-testid="stRadio"] > label > div { padding: 12px 20px !important; font-size: 14px !important; font-weight: 500 !important; color: #94A3B8 !important; border-left: 4px solid transparent !important; transition: all 0.2s ease !important; background: transparent !important; }
section[data-testid="stSidebar"] div[data-testid="stRadio"] > label > div:hover { background: #1E293B !important; color: #F8FAFC !important; }
section[data-testid="stSidebar"] div[data-testid="stRadio"] > label[aria-checked="true"] > div { background: #1E293B !important; color: #3B82F6 !important; border-left: 4px solid #3B82F6 !important; font-weight: 600 !important; }

.sb-spacer { min-height: 35vh; }
.sb-logout { padding: 16px; }
.sb-logout button { width: 100%; background: transparent !important; border: 1px solid #334155 !important; color: #94A3B8 !important; border-radius: 8px; padding: 10px 0 !important; font-size: 13px !important; font-weight: 600 !important; transition: all 0.2s; }
.sb-logout button:hover { border-color: #EF4444 !important; color: #EF4444 !important; background: rgba(239,68,68,0.1) !important; }

/* ===== METRICS & STATUS CARDS ===== */
.stat-box { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 20px; position: relative; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.02); }
.stat-box::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px; }
.sg::before { background: #3B82F6; } .sb2::before { background: #10B981; } .so::before { background: #F59E0B; } .sy::before { background: #8B5CF6; }
.stat-lbl { font-size: 11px; color: #64748B; text-transform: uppercase; letter-spacing: 0.8px; font-weight: 700; }
.stat-val { font-size: 26px; font-weight: 800; color: #0F172A; margin-top: 6px; }

.p-card { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 18px; height: 120px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 1px 3px rgba(0,0,0,0.01); transition: all 0.2s ease; }
.p-card:hover { border-color: #3B82F6; transform: translateY(-2px); box-shadow: 0 6px 20px rgba(59,130,246,0.06); }
.p-name { font-size: 14px; font-weight: 700; color: #0F172A; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.p-stock { font-size: 24px; font-weight: 800; color: #10B981; line-height: 1.2; margin-top: 4px; }
.p-div { height: 1px; background: #F1F5F9; margin: 8px 0; }
.p-total { font-size: 11px; color: #64748B; font-weight: 500; }
.p-total b { color: #334155; font-weight: 600; }
.dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 6px; }
.dot-g { background: #10B981; } .dot-y { background: #F59E0B; } .dot-r { background: #EF4444; }

.sec-h { font-size: 15px; font-weight: 700; color: #0F172A; margin: 28px 0 14px; padding-bottom: 8px; border-bottom: 1px solid #E2E8F0; letter-spacing: -0.2px; }

/* ===== INPUTS & VISUAL RECTIFICATION ===== */
.form-sec { font-size: 12px; font-weight: 700; color: #2563EB; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 16px; border-left: 3px solid #2563EB; padding-left: 8px; }
.hint { font-size: 11px; color: #64748B; margin-top: 4px; font-weight: 400; }

label p { font-size: 13px !important; font-weight: 600 !important; color: #344054 !important; }
.stTextInput>div>div>input, .stSelectbox>div>div, .stNumberInput>div>div>input, .stTextArea>div>div>textarea {
    background-color: #FFFFFF !important; border: 1px solid #D0D5DD !important; border-radius: 8px !important; color: #101828 !important; font-size: 14px !important; padding: 2px 4px; }

/* BUTTONS CRITICAL FIX: Static text visible clearly always */
.stDownloadButton > button {
    background: #FFFFFF !important; color: #344054 !important; border: 1px solid #D0D5DD !important; border-radius: 8px !important; font-weight: 600 !important; font-size: 13px !important; padding: 10px 16px !important; width: 100% !important; box-shadow: 0 1px 2px rgba(16,24,40,0.05) !important; transition: all 0.15s ease; opacity: 1 !important; visibility: visible !important; display: inline-flex !important; align-items: center; justify-content: center; }
.stDownloadButton > button:hover {
    background: #F9FAFB !important; border-color: #C6C9F4 !important; color: #1D2939 !important; }
.stButton > button[kind="primary"] {
    background: #2563EB !important; color: #FFFFFF !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important; font-size: 14px !important; padding: 12px 24px !important; box-shadow: 0 1px 2px rgba(16,24,40,0.05) !important; width: 100%; transition: all 0.2s; }
.stButton > button[kind="primary"]:hover { background: #1D4ED8 !important; box-shadow: 0 4px 12px rgba(37,99,235,0.2) !important; }

/* ===== LOGIN CLEANUP ===== */
.login-wrapper { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 60px 0; }
.login-card { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 40px; width: 100%; max-width: 380px; box-shadow: 0 12px 32px rgba(0,0,0,0.04); text-align: center; }
.login-icon { width: 60px; height: 60px; margin: 0 auto 16px; background: linear-gradient(135deg, #3B82F6, #2563EB); border-radius: 16px; display: flex; align-items: center; justify-content: center; font-size: 26px; color: #fff; box-shadow: 0 6px 16px rgba(59,130,246,0.2); }
</style>""", unsafe_allow_html=True)

# ==========================================
# UNITS
# ==========================================
UNITS = ["PCS","LTR","ML","MTR","DRUM","BOX","KG","GM","SET","PAIR","ROLL","CAN","BOTTLE","PACK","SHEET","BUNDLE","TUBE","GAL","NOS","KIT"]

# ==========================================
# HELPERS
# ==========================================
COLS_P = ["id","product_name","item_code","default_unit","total_added_to_system"]
COLS_T = ["id","product_id","item_code","serial_number","quantity","unit","issued_to","invoice_no","action_type","created_at"]

@st.cache_data(ttl=60)
def load_data():
    try:
        r = supabase.table("tpl_inv_products").select(",".join(COLS_P)).order("product_name").execute()
        dp = pd.DataFrame(r.data) if r.data else pd.DataFrame(columns=COLS_P)
    except:
        dp = pd.DataFrame(columns=COLS_P)
    try:
        r = supabase.table("tpl_inv_transactions").select(",".join(COLS_T)).execute()
        dt = pd.DataFrame(r.data) if r.data else pd.DataFrame(columns=COLS_T)
    except:
        dt = pd.DataFrame(columns=COLS_T)
    return dp, dt

def get_stock(dt, pid):
    if dt.empty: return 0.0
    m = dt[dt["product_id"] == pid]
    up = pd.to_numeric(m[m["action_type"]=="UPLOAD"]["quantity"], errors="coerce").fillna(0).sum()
    rt = pd.to_numeric(m[m["action_type"]=="RETURN"]["quantity"], errors="coerce").fillna(0).sum()
    is_ = pd.to_numeric(m[m["action_type"]=="ISSUE"]["quantity"], errors="coerce").fillna(0).sum()
    return float((up + rt) - is_)

def dot_cls(s, t):
    if t <= 0: return "dot-r"
    r = s / t
    return "dot-g" if r > .5 else "dot-y" if r > .15 else "dot-r"

def ind_dt(v):
    try: return pd.to_datetime(v).strftime("%d-%b-%Y %H:%M")
    except: return str(v)

def to_csv(df):
    return df.to_csv(index=False).encode("utf-8")

def safe_num(v, d=0.0):
    try: return float(v)
    except: return d

def explode_serials(df):
    if df.empty: return df
    rows = []
    for _, r in df.iterrows():
        s = str(r.get("serial_number","")).strip()
        if s:
            parts = [x.strip() for x in s.split(",") if x.strip()]
            if len(parts) > 1:
                for p in parts:
                    nr = r.copy()
                    nr["serial_number"] = p
                    rows.append(nr)
                continue
        rows.append(r)
    return pd.DataFrame(rows)

# ==========================================
# LOGIN SCREEN
# ==========================================
if not st.session_state["logged_in"]:
    _, mid, _ = st.columns([1.3, 1.4, 1.3])
    with mid:
        st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
        st.markdown('''<div class="login-card">
        <div class="login-icon">📦</div>
        <div style="font-size:22px;font-weight:700;color:#0F172A;letter-spacing:-0.5px">AssetFlow KCCL</div>
        <div style="font-size:13px;color:#64748B;margin-top:4px;margin-bottom:24px">Inventory Management System</div>''', unsafe_allow_html=True)
        
        with st.form("lf", clear_on_submit=False):
            u = st.text_input("Username", placeholder="Enter username", label_visibility="collapsed")
            p = st.text_input("Password", type="password", placeholder="Enter password", label_visibility="collapsed")
            st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
            if st.form_submit_button("Sign In Securely", use_container_width=True, type="primary"):
                if u == "admin" and p == "kccl@2026":
                    st.session_state["logged_in"] = True
                    st.rerun()
                else:
                    st.error("Invalid credentials!")
                    
        st.markdown('<div style="text-align:center;margin-top:16px"><code style="font-size:11px;color:#64748B;background:#F1F5F9;padding:4px 12px;border-radius:6px;border:1px solid #E2E8F0">admin / kccl@2026</code></div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
st.sidebar.markdown('<div class="sb-logo">', unsafe_allow_html=True)

# Validated Logo Asset Alignment
_logo_shown = False
if os.path.exists("assets/logo.png"):
    try:
        st.sidebar.image("assets/logo.png", use_container_width=True)
        _logo_shown = True
    except:
        pass

if not _logo_shown:
    st.sidebar.markdown('<div class="sb-logo-icon">📦</div>', unsafe_allow_html=True)

st.sidebar.markdown('<div class="sb-logo-name">AssetFlow</div><div class="sb-logo-sub">KCCL Operations</div></div>', unsafe_allow_html=True)

st.sidebar.markdown('<div class="sb-nav-label">Navigation Menu</div>', unsafe_allow_html=True)
page = st.sidebar.radio("", ["Dashboard", "Transaction", "Reports"], label_visibility="collapsed")

st.sidebar.markdown('<div class="sb-spacer"></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sb-logout">', unsafe_allow_html=True)
if st.sidebar.button("Logout System", key="sb_logout", use_container_width=True):
    st.session_state["logged_in"] = False
    st.rerun()
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# DATA RESOLUTION
# ==========================================
NOW = datetime.now()
DT_STR = NOW.strftime("%d%b%Y")
df_p, df_t = load_data()

# ==========================================
# CORE PAGES: DASHBOARD
# ==========================================
if page == "Dashboard":
    if df_p.empty:
        st.info("No active assets found. Configure items inside database backend.")
        st.stop()

    ts = sum(get_stock(df_t, r["id"]) for _, r in df_p.iterrows())
    im = rm = 0.0
    if not df_t.empty:
        dft = df_t.copy()
        dft["created_at"] = pd.to_datetime(dft["created_at"], errors="coerce")
        m = dft.dropna(subset=["created_at"])
        mk = (m["created_at"].dt.month == NOW.month) & (m["created_at"].dt.year == NOW.year)
        im = safe_num(m[mk & (m["action_type"]=="ISSUE")]["quantity"].sum())
        rm = safe_num(m[mk & (m["action_type"]=="RETURN")]["quantity"].sum())

    s1, s2, s3, s4 = st.columns(4)
    with s1: st.markdown(f'<div class="stat-box sg"><div class="stat-lbl">Registered Assets</div><div class="stat-val">{len(df_p)}</div></div>', unsafe_allow_html=True)
    with s2: st.markdown(f'<div class="stat-box sb2"><div class="stat-lbl">Total Stock Balance</div><div class="stat-val">{ts:,.1f}</div></div>', unsafe_allow_html=True)
    with s3: st.markdown(f'<div class="stat-box so"><div class="stat-lbl">Issued This Month</div><div class="stat-val">{im:,.1f}</div></div>', unsafe_allow_html=True)
    with s4: st.markdown(f'<div class="stat-box sy"><div class="stat-lbl">Returned This Month</div><div class="stat-val">{rm:,.1f}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-h">Live Inventory Status</div>', unsafe_allow_html=True)
    cards = st.columns(5)
    sum_rows = []
    
    for idx, (_, r) in enumerate(df_p.iterrows()):
        pid, nm, code, unit = r["id"], r["product_name"], r["item_code"], r["default_unit"]
        total = safe_num(r.get("total_added_to_system", 0), 0)
        stk = get_stock(df_t, pid)
        dc = dot_cls(stk, total)
        sum_rows.append({"Product Name": nm, "Item Code": code, "In Stock": round(stk, 3), "Unit": unit, "Total Added": int(total)})
        
        # Item Code successfully stripped from layout card
        with cards[idx % 5]:
            st.markdown(f'<div class="p-card"><div><div style="display:flex;align-items:center;gap:3px"><span class="dot {dc}"></span><div class="p-name">{nm}</div></div></div><div><div class="p-stock">{stk:.2f}</div><div class="p-div"></div><div class="p-total">Capacity: <b>{int(total)} {unit}</b></div></div></div>', unsafe_allow_html=True)

    df_sum = pd.DataFrame(sum_rows)
    st.markdown('<div class="sec-h">Export Hub</div>', unsafe_allow_html=True)
    d1, d2, d3 = st.columns(3)
    with d1:
        st.markdown("<p style='font-size:13px;font-weight:600;color:#344054;margin-bottom:6px;'>Full Logs Dump</p>", unsafe_allow_html=True)
        if not df_t.empty:
            df_d = df_t.copy()
            df_d["created_at"] = df_d["created_at"].apply(ind_dt)
            df_d = explode_serials(df_d)
            st.download_button("Download Full Dump CSV", data=to_csv(df_d), file_name=f"AssetFlow_FullDump_{DT_STR}.csv", mime="text/csv", key="d1")
    with d2:
        st.markdown("<p style='font-size:13px;font-weight:600;color:#344054;margin-bottom:6px;'>Current Summary Balance</p>", unsafe_allow_html=True)
        if not df_sum.empty:
            st.download_button("Download Summary CSV", data=to_csv(df_sum), file_name=f"AssetFlow_Summary_{DT_STR}.csv", mime="text/csv", key="d2")
    with d3:
        st.markdown("<p style='font-size:13px;font-weight:600;color:#344054;margin-bottom:6px;'>Product-wise Issue Statements</p>", unsafe_allow_html=True)
        sel = st.selectbox("Select Target Product", df_p["product_name"].tolist(), key="cs", label_visibility="collapsed")
        if sel:
            tid = df_p[df_p["product_name"]==sel]["id"].values[0]
            df_is = df_t[(df_t["product_id"]==tid) & (df_t["action_type"]=="ISSUE")].copy()
            if not df_is.empty:
                df_is["created_at"] = df_is["created_at"].apply(ind_dt)
                df_is["Product"] = sel
                df_is = explode_serials(df_is)
                ec = [c for c in ["created_at","Product","item_code","serial_number","quantity","unit","issued_to","invoice_no"] if c in df_is.columns]
                st.markdown("<div style='margin-top:5px;'></div>", unsafe_allow_html=True)
                st.download_button(f"Download {sel} Logs", data=to_csv(df_is[ec]), file_name=f"AssetFlow_{sel.lower().replace(' ','_')}_Issued_{DT_STR}.csv", mime="text/csv", key="d3")
            else:
                st.markdown('<div class="hint">No ISSUE logs available for this item.</div>', unsafe_allow_html=True)

# ==========================================
# CORE PAGES: TRANSACTION (CLEAN GRIDS)
# ==========================================
elif page == "Transaction":
    if df_p.empty:
        st.warning("Please configure products inside database first.")
        st.stop()

    cl, cr = st.columns(2, gap="large")
    with cl:
        st.markdown('<div class="form-sec">Product Specification</div>', unsafe_allow_html=True)
        sel_prod = st.selectbox("Selected Asset Type *", df_p["product_name"].tolist(), key="tp")
        item_code = st.text_input("Item Tracking Code *", placeholder="e.g. IC-7890 (Comma-separated for multiple uploads)", key="tc")
        serial = st.text_area("Hardware Serial Numbers *", placeholder="Split with comma: SN-012, SN-013, SN-014", height=80, key="ts")
        st.markdown('<div class="hint">Notice: UPLOAD entries register fresh hardware batch. ISSUE/RETURN validates sequence.</div>', unsafe_allow_html=True)
        
        st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
        unit = st.selectbox("System Unit Metric *", UNITS, key="tu")
        qty = st.number_input("Transactional Quantity *", min_value=0.001, step=0.001, format="%.3f", key="tq")
    with cr:
        st.markdown('<div class="form-sec">Action Authorization</div>', unsafe_allow_html=True)
        action = st.selectbox("Workflow Action *", ["ISSUE","RETURN","UPLOAD"], key="ta")
        issued_to = st.text_input("Target Entity/Assignee" + (" *" if action != "UPLOAD" else ""), placeholder="Person, Site Location or LCO Name", key="ti")
        invoice = st.text_input("Challan / Invoice / DC Reference No *", placeholder="e.g. KCCL/DC/26/1023", key="tn")
        st.text_input("Execution Timestamp", value=NOW.strftime("%d-%b-%Y  %H:%M:%S"), disabled=True, key="td")
        
        st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)
        submitted = st.button("Commit Ledger Transaction", use_container_width=True, type="primary")

    if submitted:
        errs = []
        if not item_code.strip(): errs.append("Item Code tracking reference field is missing.")
        if not serial.strip(): errs.append("Serial ID configuration input data cannot be empty.")
        if qty <= 0: errs.append("Asset quantity matrix metric must exceed 0.000.")
        if action != "UPLOAD" and not issued_to.strip(): errs.append("Target Assignee name parameters required for execution.")
        if not invoice.strip(): errs.append("Valid Invoice reference link is mandatory.")
        if errs:
            for e in errs: st.error(e)
            st.stop()
            
        pid = int(df_p[df_p["product_name"]==sel_prod]["id"].values[0])
        if action == "UPLOAD":
            codes = [c.strip() for c in item_code.split(",") if c.strip()]
            serials = [s.strip() for s in serial.split(",") if s.strip()]
            if not codes:
                st.error("Operation halted. Provide tracking codes.")
                st.stop()
            ok = 0
            for i, code in enumerate(codes):
                sn = serials[i] if i < len(serials) else ""
                payload = {"product_id": pid, "item_code": code, "serial_number": sn, "quantity": qty, "unit": unit, "issued_to": "", "invoice_no": invoice.strip(), "action_type": "UPLOAD", "created_at": datetime.now().isoformat()}
                try:
                    res = supabase.table("tpl_inv_transactions").insert(payload).execute()
                    if res.data: ok += 1
                except Exception as ex:
                    st.error(f"Process skipped for code {code}: {ex}")
            if ok > 0:
                st.success(f"Batch registered successfully. Processed {ok} item nodes.")
                load_data.clear()
                st.rerun()
        else:
            ic, sn = item_code.strip(), serial.strip()
            if not df_t.empty:
                uploads = df_t[df_t["action_type"]=="UPLOAD"]
                if ic not in uploads["item_code"].values:
                    st.error(f"Tracking error. Item code '{ic}' not identified inside UPLOAD logs.")
                    st.stop()
                if sn:
                    match = uploads[(uploads["item_code"]==ic) & (uploads["serial_number"]==sn)]
                    if match.empty:
                        st.error(f"Hardware sequence mismatch. Serial '{sn}' doesn't match Code reference '{ic}'.")
                        st.stop()
            if action == "ISSUE":
                cs = get_stock(df_t, pid)
                if qty > cs:
                    st.error(f"Warehouse stock shortfall. Balance available: {cs:.3f} {unit}")
                    st.stop()
            payload = {"product_id": pid, "item_code": ic, "serial_number": sn, "quantity": qty, "unit": unit, "issued_to": issued_to.strip(), "invoice_no": invoice.strip(), "action_type": action, "created_at": datetime.now().isoformat()}
            try:
                res = supabase.table("tpl_inv_transactions").insert(payload).execute()
                if res.data:
                    st.success(f"Verified & Written: {action} transaction verified for {qty:.3f} {unit}")
                    load_data.clear()
                    st.rerun()
                else:
                    st.error("Internal storage rejected execution statement. Re-check permissions.")
            except Exception as ex:
                st.error(f"Engine connection exception: {ex}")

# ==========================================
# CORE PAGES: REPORTS (CLEAN DESIGN)
# ==========================================
elif page == "Reports":
    if df_t.empty:
        st.info("No active logs database available to parse ledger reports.")
        st.stop()

    df_r = df_t.copy()
    if not df_p.empty:
        pmap = df_p.set_index("id")["product_name"].to_dict()
        df_r["product_name"] = df_r["product_id"].map(pmap).fillna("Unknown")
    df_r["created_at"] = pd.to_datetime(df_r["created_at"], errors="coerce")
    df_r["_d"] = df_r["created_at"].dt.date
    mn = df_r["_d"].min() if df_r["_d"].notna().any() else NOW.date()
    mx = df_r["_d"].max() if df_r["_d"].notna().any() else NOW.date()

    st.markdown('<div class="form-sec">Query & Filtering Parameters</div>', unsafe_allow_html=True)
    f1, f2, f3, f4, f5 = st.columns(5)
    with f1: df_ = st.date_input("Start Date", value=mn, key="rf")
    with f2: dt_ = st.date_input("End Date", value=mx, key="rt")
    with f3: it_ = st.multiselect("Filter Assignee", sorted(df_r["issued_to"].dropna().unique()), key="ri")
    with f4: im_ = st.multiselect("Filter Asset Type", sorted(df_p["product_name"].tolist()), key="rm")
    with f5: st_ = st.multiselect("Filter Workflow", ["ISSUE","RETURN","UPLOAD"], key="rs")
    
    st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
    iv_ = st.multiselect("Search Reference/Invoice ID", sorted(df_r["invoice_no"].dropna().unique()), key="rv")

    active = df_ != mn or dt_ != mx or it_ or im_ or st_ or iv_
    if not active:
        st.info("Specify filtration query variables to generate standard accounting ledger records.")
        st.stop()

    df_f = df_r.copy()
    if df_ != mn: df_f = df_f[df_f["_d"] >= df_]
    if dt_ != mx: df_f = df_f[df_f["_d"] <= dt_]
    if it_: df_f = df_f[df_f["issued_to"].isin(it_)]
    if im_: df_f = df_f[df_f["product_name"].isin(im_)]
    if st_: df_f = df_f[df_f["action_type"].isin(st_)]
    if iv_: df_f = df_f[df_f["invoice_no"].isin(iv_)]

    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
    r1, r2 = st.columns([2, 1])
    with r1:
        st.markdown(f'<p style="font-size:14px;color:#475569;margin-top:10px;font-weight:500">Query returned <span style="font-weight:700;color:#2563EB">{len(df_f)}</span> synchronized logs</p>', unsafe_allow_html=True)
    with r2:
        if not df_f.empty:
            df_ex = df_f.copy()
            df_ex["created_at"] = df_ex["created_at"].apply(ind_dt)
            df_ex = explode_serials(df_ex)
            ec = [c for c in ["created_at","product_name","item_code","serial_number","quantity","unit","issued_to","invoice_no","action_type"] if c in df_ex.columns]
            st.download_button("Export Compiled Ledger to CSV", data=to_csv(df_ex[ec]), file_name=f"AssetFlow_Report_{DT_STR}.csv", mime="text/csv", key="dr")

    if not df_f.empty:
        df_s = df_f.copy()
        df_s["created_at"] = df_s["created_at"].apply(ind_dt)
        df_s = explode_serials(df_s)
        ec = [c for c in ["created_at","product_name","item_code","serial_number","quantity","unit","issued_to","invoice_no","action_type"] if c in df_s.columns]
        df_s = df_s[ec].rename(columns={"created_at":"Date","product_name":"Product","item_code":"Code","serial_number":"Serial","quantity":"Qty","unit":"Unit","issued_to":"Issued To","invoice_no":"Invoice","action_type":"Action"})
        st.dataframe(df_s, use_container_width=True, hide_index=True, height=450)
    else:
        st.warning("No logs database rows match selected parameter rules.")
