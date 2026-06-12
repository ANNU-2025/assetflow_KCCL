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

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.markdown("<style>section[data-testid='stSidebar']{display:none}header[data-testid='stHeader']{display:none}</style>", unsafe_allow_html=True)

# ==========================================
# PREMIUM TRIPLE-ACCENT HIGH CONTRAST THEME
# ==========================================
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* Reset and Global Typography - Ultra High Contrast */
.stApp, .stApp *, div[data-testid="stMarkdownContainer"] p {
    font-family: 'Inter', system-ui, sans-serif !important;
    color: #0A0F1D !important; /* Absolute Deep Black for maximum contrast on light bg */
}

.stApp { background-color: #F1F5F9 !important; }
.block-container { padding: 1rem 2rem !important; max-width: 1600px; margin: 0 auto; }

/* ===== SIDEBAR (NON-SCROLLABLE & PERFECTLY CENTERED) ===== */
section[data-testid="stSidebar"] { 
    background-color: #0B0F19 !important; /* Pitch Dark Premium Blue/Black */
    border-right: 2px solid #1E293B !important; 
    width: 260px !important; 
    overflow: hidden !important; /* Force Disable Scroll */
}
section[data-testid="stSidebar"] > div:first-child { width: 260px !important; overflow: hidden !important; }
#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; display: none !important; }

/* Centered Logo Container */
.sb-logo { 
    padding: 24px 10px; 
    text-align: center !important; 
    border-bottom: 1px solid #1E293B; 
    display: flex !important;
    flex-direction: column !important; 
    align-items: center !important; 
    justify-content: center !important; 
    width: 100%; 
}
.sb-logo-icon { 
    width: 56px; height: 56px; 
    margin: 0 auto 10px auto !important;
    background: linear-gradient(135deg, #2563EB, #1D4ED8); 
    border-radius: 12px; 
    display: flex !important; align-items: center !important; justify-content: center !important; 
    font-size: 26px; color: #FFFFFF !important; 
    box-shadow: 0 4px 12px rgba(37,99,235,0.3); 
}
.sb-logo-name { font-size: 19px; font-weight: 800; color: #FFFFFF !important; letter-spacing: -0.5px; text-align: center; }
.sb-logo-sub { font-size: 11px; color: #38BDF8 !important; text-transform: uppercase; letter-spacing: 1.5px; margin-top: 4px; font-weight: 700; text-align: center; }
.sb-logo img { border-radius: 8px; max-width: 140px !important; height: auto; margin: 0 auto 10px auto !important; display: block !important; }

/* Sidebar Navigation Items */
.sb-nav-label { font-size: 11px; color: #64748B !important; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700; padding: 20px 20px 8px; text-align: left; }
section[data-testid="stSidebar"] div[data-testid="stRadio"] > label { margin-bottom: 2px !important; }
section[data-testid="stSidebar"] div[data-testid="stRadio"] > label > div { 
    padding: 12px 24px !important; font-size: 14px !important; font-weight: 600 !important; 
    color: #94A3B8 !important; border-left: 4px solid transparent !important; transition: all 0.15s ease !important; 
}
section[data-testid="stSidebar"] div[data-testid="stRadio"] > label > div:hover { background: #1E293B !important; color: #FFFFFF !important; }
section[data-testid="stSidebar"] div[data-testid="stRadio"] > label[aria-checked="true"] > div { 
    background: #111827 !important; color: #38BDF8 !important; /* High contrast cyan accent text */
    border-left: 4px solid #38BDF8 !important; font-weight: 700 !important; 
}

/* Sidebar Absolute Bottom Sticky Elements */
.sb-logout { padding: 16px; margin-top: 20px; }
.sb-logout button { 
    width: 100%; background: #1E293B !important; border: 1px solid #475569 !important; 
    color: #F8FAFC !important; border-radius: 8px; padding: 8px 0 !important; font-size: 13px !important; font-weight: 700 !important; 
}
.sb-logout button:hover { border-color: #EF4444 !important; color: #FFFFFF !important; background: #991B1B !important; }

/* ===== DASHBOARD ULTRA COMPACT CARDS ===== */
.stat-box { background: #FFFFFF; border: 2px solid #0A0F1D; border-radius: 10px; padding: 14px 18px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
.stat-lbl { font-size: 11px; color: #475569 !important; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; }
.stat-val { font-size: 28px; font-weight: 800; color: #0A0F1D !important; margin-top: 2px; }

/* One Page Grid Slim Cards */
.p-card { 
    background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 8px; 
    padding: 8px 12px; height: 56px; /* Ultra-low height to fit on one screen */
    display: flex; align-items: center; justify-content: space-between; 
    box-shadow: 0 1px 2px rgba(0,0,0,0.02); transition: all 0.15s ease; 
}
.p-card:hover { border-color: #2563EB; background: #F8FAFF; transform: translateY(-1px); }
.p-name { font-size: 13px; font-weight: 700; color: #0A0F1D !important; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 160px; }
.p-stock { font-size: 18px; font-weight: 800; color: #16A34A !important; text-align: right; }
.p-total { font-size: 11px; color: #475569 !important; font-weight: 600; text-align: right; }

.dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 6px; }
.dot-g { background: #16A34A; } .dot-y { background: #D97706; } .dot-r { background: #DC2626; }
.sec-h { font-size: 16px; font-weight: 800; color: #0A0F1D !important; margin: 20px 0 10px; padding-bottom: 6px; border-bottom: 2px solid #0A0F1D; }

/* ===== FIXED VISIBILITY DOWNLOAD BUTTONS ===== */
.stDownloadButton > button {
    background: #0A0F1D !important; /* Solid Black Background */
    color: #FFFFFF !important; /* Bold White Text always visible */
    border: none !important; border-radius: 8px !important; 
    font-weight: 700 !important; font-size: 13px !important; 
    padding: 10px 16px !important; width: 100% !important; 
    display: inline-flex !important; align-items: center; justify-content: center;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important; opacity: 1 !important; visibility: visible !important;
}
.stDownloadButton > button:hover { background: #2563EB !important; color: #FFFFFF !important; }

.stButton > button[kind="primary"] {
    background: #2563EB !important; color: #FFFFFF !important; border: none !important; border-radius: 8px !important; 
    font-weight: 700 !important; font-size: 14px !important; padding: 12px 24px !important; width: 100%;
}
.stButton > button[kind="primary"]:hover { background: #1D4ED8 !important; }

/* Forms & Text Fields Contrast Override */
label p { font-size: 13px !important; font-weight: 700 !important; color: #0A0F1D !important; }
.stTextInput>div>div>input, .stSelectbox>div>div, .stNumberInput>div>div>input, .stTextArea>div>div>textarea {
    background-color: #FFFFFF !important; border: 2px solid #94A3B8 !important; border-radius: 6px !important; color: #0A0F1D !important; font-weight: 600 !important; }

/* ===== LOGIN WINDOW STYLING ===== */
.login-wrapper { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 100px 0; }
.login-card { background: #FFFFFF; border: 2px solid #0A0F1D; border-radius: 12px; padding: 40px; width: 100%; max-width: 380px; text-align: center; }
</style>""", unsafe_allow_html=True)

# ==========================================
# UNITS & CONFIG
# ==========================================
UNITS = ["PCS","LTR","ML","MTR","DRUM","BOX","KG","GM","SET","PAIR","ROLL","CAN","BOTTLE","PACK","SHEET","BUNDLE","TUBE","GAL","NOS","KIT"]
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
# CENTRALLY CONTROLLED SECURITY GATE
# ==========================================
if not st.session_state["logged_in"]:
    _, mid, _ = st.columns([1.3, 1.4, 1.3])
    with mid:
        st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
        st.markdown('''<div class="login-card">
        <div class="sb-logo-icon">📦</div>
        <div style="font-size:22px;font-weight:800;color:#0A0F1D;letter-spacing:-0.5px">AssetFlow KCCL</div>
        <div style="font-size:13px;color:#475569;margin-top:4px;margin-bottom:24px">Inventory Control Portal</div>''', unsafe_allow_html=True)
        
        with st.form("lf", clear_on_submit=False):
            u = st.text_input("Username", placeholder="Enter admin username", label_visibility="collapsed")
            p = st.text_input("Password", type="password", placeholder="Enter security passphrase", label_visibility="collapsed")
            if st.form_submit_button("Authenticate Sign In", use_container_width=True, type="primary"):
                if u == "admin" and p == "kccl@2026":
                    st.session_state["logged_in"] = True
                    st.rerun()
                else:
                    st.error("Invalid credentials!")
                    
        st.markdown('<div style="text-align:center;margin-top:16px"><code style="font-size:11px;color:#0A0F1D;background:#E2E8F0;padding:4px 12px;border-radius:4px;font-weight:700">admin / kccl@2026</code></div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ==========================================
# SIDEBAR (NON-SCROLLABLE LOCK)
# ==========================================
st.sidebar.markdown('<div class="sb-logo">', unsafe_allow_html=True)

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

st.sidebar.markdown('<div class="sb-nav-label">Navigation</div>', unsafe_allow_html=True)
page = st.sidebar.radio("", ["Dashboard", "Transaction", "Reports"], label_visibility="collapsed")

# Absolute short margin to eliminate scroll bars
st.sidebar.markdown('<div class="sb-logout">', unsafe_allow_html=True)
if st.sidebar.button("Logout Session", key="sb_logout", use_container_width=True):
    st.session_state["logged_in"] = False
    st.rerun()
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# APP EXECUTION PIPELINE
# ==========================================
NOW = datetime.now()
DT_STR = NOW.strftime("%d%b%Y")
df_p, df_t = load_data()

# ==========================================
# PAGE: DASHBOARD
# ==========================================
if page == "Dashboard":
    if df_p.empty:
        st.info("No master entries tracked. Populate tpl_inv_products inside backend.")
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
    with s1: st.markdown(f'<div class="stat-box"><div class="stat-lbl">Active Item Types</div><div class="stat-val">{len(df_p)}</div></div>', unsafe_allow_html=True)
    with s2: st.markdown(f'<div class="stat-box"><div class="stat-lbl">Total Stock Count</div><div class="stat-val">{ts:,.1f}</div></div>', unsafe_allow_html=True)
    with s3: st.markdown(f'<div class="stat-box"><div class="stat-lbl">Issued (Current Month)</div><div class="stat-val">{im:,.1f}</div></div>', unsafe_allow_html=True)
    with s4: st.markdown(f'<div class="stat-box"><div class="stat-lbl">Returned (Current Month)</div><div class="stat-val">{rm:,.1f}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-h">Live Inventory Distribution</div>', unsafe_allow_html=True)
    
    # Grid Distribution for Cards
    cards = st.columns(5)
    sum_rows = []
    for idx, (_, r) in enumerate(df_p.iterrows()):
        pid, nm, code, unit = r["id"], r["product_name"], r["item_code"], r["default_unit"]
        total = safe_num(r.get("total_added_to_system", 0), 0)
        stk = get_stock(df_t, pid)
        dc = dot_cls(stk, total)
        sum_rows.append({"Product Name": nm, "Item Code": code, "In Stock": round(stk, 3), "Unit": unit, "Total Added": int(total)})
        
        # Ultra-Compact 56px Rows (Perfect fit, item code stripped)
        with cards[idx % 5]:
            st.markdown(f'''<div class="p-card">
                <div style="display:flex;align-items:center;gap:4px;overflow:hidden;">
                    <span class="dot {dc}"></span>
                    <span class="p-name">{nm}</span>
                </div>
                <div>
                    <div class="p-stock">{stk:.0f}</div>
                    <div class="p-total">Max: {int(total)}</div>
                </div>
            </div>''', unsafe_allow_html=True)

    df_sum = pd.DataFrame(sum_rows)
    st.markdown('<div class="sec-h">Data Extraction Hub</div>', unsafe_allow_html=True)
    d1, d2, d3 = st.columns(3)
    with d1:
        st.markdown("<p style='font-size:13px;font-weight:700;color:#0A0F1D;margin-bottom:6px;'>Full Ledger Audit Log</p>", unsafe_allow_html=True)
        if not df_t.empty:
            df_d = df_t.copy()
            df_d["created_at"] = df_d["created_at"].apply(ind_dt)
            df_d = explode_serials(df_d)
            st.download_button("Download Full Dump CSV", data=to_csv(df_d), file_name=f"AssetFlow_FullDump_{DT_STR}.csv", mime="text/csv", key="d1")
    with d2:
        st.markdown("<p style='font-size:13px;font-weight:700;color:#0A0F1D;margin-bottom:6px;'>System Balance Summary</p>", unsafe_allow_html=True)
        if not df_sum.empty:
            st.download_button("Download Summary CSV", data=to_csv(df_sum), file_name=f"AssetFlow_Summary_{DT_STR}.csv", mime="text/csv", key="d2")
    with d3:
        st.markdown("<p style='font-size:13px;font-weight:700;color:#0A0F1D;margin-bottom:6px;'>Targeted Asset Log Extraction</p>", unsafe_allow_html=True)
        sel = st.selectbox("Select Target Product", df_p["product_name"].tolist(), key="cs", label_visibility="collapsed")
        if sel:
            tid = df_p[df_p["product_name"]==sel]["id"].values[0]
            df_is = df_t[(df_t["product_id"]==tid) & (df_t["action_type"]=="ISSUE")].copy()
            if not df_is.empty:
                df_is["created_at"] = df_is["created_at"].apply(ind_dt)
                df_is["Product"] = sel
                df_is = explode_serials(df_is)
                ec = [c for c in ["created_at","Product","item_code","serial_number","quantity","unit","issued_to","invoice_no"] if c in df_is.columns]
                st.markdown("<div style='margin-top:4px;'></div>", unsafe_allow_html=True)
                st.download_button(f"Download {sel} Distribution Logs", data=to_csv(df_is[ec]), file_name=f"AssetFlow_{sel.lower().replace(' ','_')}_Issued_{DT_STR}.csv", mime="text/csv", key="d3")
            else:
                st.markdown('<p style="font-size:11px;font-weight:600;color:#DC2626;margin-top:6px;">No transaction history for selected item.</p>', unsafe_allow_html=True)

# ==========================================
# PAGE: TRANSACTION
# ==========================================
elif page == "Transaction":
    if df_p.empty:
        st.warning("Please configure products inside master catalog first.")
        st.stop()

    cl, cr = st.columns(2, gap="large")
    with cl:
        st.markdown('<div class="form-sec">Asset Parameters</div>', unsafe_allow_html=True)
        sel_prod = st.selectbox("Target Catalog Product *", df_p["product_name"].tolist(), key="tp")
        item_code = st.text_input("Item Tracking Reference Code *", placeholder="e.g. IC-4500 (Split with commas for bulk)", key="tc")
        serial = st.text_area("Hardware Unique Serials *", placeholder="e.g. SN-KCCL-01, SN-KCCL-02", height=85, key="ts")
        st.markdown('<div class="hint">Workflow Note: UPLOAD instantiates new batch logic. ISSUE/RETURN performs integrity matches.</div>', unsafe_allow_html=True)
        
        st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)
        unit = st.selectbox("Standard Measurement Unit *", UNITS, key="tu")
        qty = st.number_input("Transaction Unit Quantity *", min_value=0.001, step=0.001, format="%.3f", key="tq")
    with cr:
        st.markdown('<div class="form-sec">Workflow Mapping</div>', unsafe_allow_html=True)
        action = st.selectbox("Ledger Action Trigger *", ["ISSUE","RETURN","UPLOAD"], key="ta")
        issued_to = st.text_input("Recipient Node / Operator Assignee" + (" *" if action != "UPLOAD" else ""), placeholder="Enter operator or site location reference", key="ti")
        invoice = st.text_input("Challan / Invoice Reference ID *", placeholder="e.g. KCCL/2026/CH-8801", key="tn")
        st.text_input("System Logging Datetime", value=NOW.strftime("%d-%b-%Y  %H:%M:%S"), disabled=True, key="td")
        
        st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)
        submitted = st.button("Commit Action Statement to Ledger", use_container_width=True, type="primary")

    if submitted:
        errs = []
        if not item_code.strip(): errs.append("Item code tracking link is required.")
        if not serial.strip(): errs.append("Hardware unique identification array strings are missing.")
        if qty <= 0: errs.append("Quantity cannot read zero.")
        if action != "UPLOAD" and not issued_to.strip(): errs.append("Recipient tracking target context is required.")
        if not invoice.strip(): errs.append("Invoice/Challan hard reference index is mandatory.")
        if errs:
            for e in errs: st.error(e)
            st.stop()
            
        pid = int(df_p[df_p["product_name"]==sel_prod]["id"].values[0])
        if action == "UPLOAD":
            codes = [c.strip() for c in item_code.split(",") if c.strip()]
            serials = [s.strip() for s in serial.split(",") if s.strip()]
            if not codes:
                st.error("Missing tracking code arguments.")
                st.stop()
            ok = 0
            for i, code in enumerate(codes):
                sn = serials[i] if i < len(serials) else ""
                payload = {"product_id": pid, "item_code": code, "serial_number": sn, "quantity": qty, "unit": unit, "issued_to": "", "invoice_no": invoice.strip(), "action_type": "UPLOAD", "created_at": datetime.now().isoformat()}
                try:
                    res = supabase.table("tpl_inv_transactions").insert(payload).execute()
                    if res.data: ok += 1
                except Exception as ex:
                    st.error(f"Write validation exception on node {code}: {ex}")
            if ok > 0:
                st.success(f"Successfully processed and synced {ok} block assets.")
                load_data.clear()
                st.rerun()
        else:
            ic, sn = item_code.strip(), serial.strip()
            if not df_t.empty:
                uploads = df_t[df_t["action_type"]=="UPLOAD"]
                if ic not in uploads["item_code"].values:
                    st.error(f"Validation Error: Code '{ic}' does not map to an existing UPLOAD trace.")
                    st.stop()
                if sn:
                    match = uploads[(uploads["item_code"]==ic) & (uploads["serial_number"]==sn)]
                    if match.empty:
                        st.error(f"Hardware Sequence Alert: Serial sequence '{sn}' mismatch with reference frame '{ic}'.")
                        st.stop()
            if action == "ISSUE":
                cs = get_stock(df_t, pid)
                if qty > cs:
                    st.error(f"Shortfall Exception: Safe stock limit violated. Available balance: {cs:.3f} {unit}")
                    st.stop()
            payload = {"product_id": pid, "item_code": ic, "serial_number": sn, "quantity": qty, "unit": unit, "issued_to": issued_to.strip(), "invoice_no": invoice.strip(), "action_type": action, "created_at": datetime.now().isoformat()}
            try:
                res = supabase.table("tpl_inv_transactions").insert(payload).execute()
                if res.data:
                    st.success(f"Committed Statement: {action} written safely for {qty:.3f} {unit}")
                    load_data.clear()
                    st.rerun()
            except Exception as ex:
                st.error(f"DB Thread Sync Failure: {ex}")

# ==========================================
# PAGE: REPORTS
# ==========================================
elif page == "Reports":
    if df_t.empty:
        st.info("System storage engine is empty. No query logs found.")
        st.stop()

    df_r = df_t.copy()
    if not df_p.empty:
        pmap = df_p.set_index("id")["product_name"].to_dict()
        df_r["product_name"] = df_r["product_id"].map(pmap).fillna("Unknown")
    df_r["created_at"] = pd.to_datetime(df_r["created_at"], errors="coerce")
    df_r["_d"] = df_r["created_at"].dt.date
    mn = df_r["_d"].min() if df_r["_d"].notna().any() else NOW.date()
    mx = df_r["_d"].max() if df_r["_d"].notna().any() else NOW.date()

    st.markdown('<div class="form-sec">Ledger Query Engine</div>', unsafe_allow_html=True)
    f1, f2, f3, f4, f5 = st.columns(5)
    with f1: df_ = st.date_input("Query Start Date", value=mn, key="rf")
    with f2: dt_ = st.date_input("Query End Date", value=mx, key="rt")
    with f3: it_ = st.multiselect("Query Assignee Entity", sorted(df_r["issued_to"].dropna().unique()), key="ri")
    with f4: im_ = st.multiselect("Query Asset Class", sorted(df_p["product_name"].tolist()), key="rm")
    with f5: st_ = st.multiselect("Query Flow State", ["ISSUE","RETURN","UPLOAD"], key="rs")
    
    st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
    iv_ = st.multiselect("Search Reference / Challan ID Array", sorted(df_r["invoice_no"].dropna().unique()), key="rv")

    active = df_ != mn or dt_ != mx or it_ or im_ or st_ or iv_
    if not active:
        st.info("Specify filtration constraints above to process historical log balances.")
        st.stop()

    df_f = df_r.copy()
    if df_ != mn: df_f = df_f[df_f["_d"] >= df_]
    if dt_ != mx: df_f = df_f[df_f["_d"] <= dt_]
    if it_: df_f = df_f[df_f["issued_to"].isin(it_)]
    if im_: df_f = df_f[df_f["product_name"].isin(im_)]
    if st_: df_f = df_f[df_f["action_type"].isin(st_)]
    if iv_: df_f = df_f[df_f["invoice_no"].isin(iv_)]

    st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)
    r1, r2 = st.columns([2, 1])
    with r1:
        st.markdown(f'<p style="font-size:14px;color:#0A0F1D;margin-top:12px;font-weight:700;">Query matched <span style="color:#2563EB;">{len(df_f)}</span> synchronized log lines</p>', unsafe_allow_html=True)
    with r2:
        if not df_f.empty:
            df_ex = df_f.copy()
            df_ex["created_at"] = df_ex["created_at"].apply(ind_dt)
            df_ex = explode_serials(df_ex)
            ec = [c for c in ["created_at","product_name","item_code","serial_number","quantity","unit","issued_to","invoice_no","action_type"] if c in df_ex.columns]
            st.download_button("Export Compiled Data Sheet", data=to_csv(df_ex[ec]), file_name=f"AssetFlow_Report_{DT_STR}.csv", mime="text/csv", key="dr")

    if not df_f.empty:
        df_s = df_f.copy()
        df_s["created_at"] = df_s["created_at"].apply(ind_dt)
        df_s = explode_serials(df_s)
        ec = [c for c in ["created_at","product_name","item_code","serial_number","quantity","unit","issued_to","invoice_no","action_type"] if c in df_s.columns]
        df_s = df_s[ec].rename(columns={"created_at":"Date","product_name":"Product","item_code":"Code","serial_number":"Serial","quantity":"Qty","unit":"Unit","issued_to":"Issued To","invoice_no":"Invoice","action_type":"Action"})
        st.dataframe(df_s, use_container_width=True, hide_index=True, height=450)
    else:
        st.warning("No records matched the execution rules.")
