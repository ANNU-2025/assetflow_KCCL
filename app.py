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
# SESSION
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# ==========================================
# HIDE SIDEBAR ON LOGIN
# ==========================================
if not st.session_state["logged_in"]:
    st.markdown("<style>section[data-testid='stSidebar']{display:none}header[data-testid='stHeader']{display:none}</style>", unsafe_allow_html=True)

# ==========================================
# CORPORATE ADMIN PANEL THEME
# ==========================================
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.stApp{background:#F0F2F5;color:#1F2937;font-family:'Inter',system-ui,sans-serif}
.block-container{padding-top:.5rem;padding-bottom:1.5rem;max-width:1440px;position:relative;z-index:1}

/* ===== KILL TOP PANEL COMPLETELY ===== */
header[data-testid="stHeader"]{height:0!important;min-height:0!important;padding:0!important;margin:0!important;overflow:hidden!important;border:none!important;box-shadow:none!important;visibility:hidden!important}

/* ===== SIDEBAR — STATIC, NO SCROLL ===== */
section[data-testid="stSidebar"]{background:#1A2332!important;border-right:1px solid #263245!important;width:220px!important;min-width:220px!important;overflow-y:hidden!important;overflow-x:hidden!important}
section[data-testid="stSidebar"]>div:first-child{width:220px!important;overflow-y:hidden!important}
#MainMenu{visibility:hidden}footer{visibility:hidden}

/* Sidebar logo — centered, not squeezed */
.sb-logo{padding:22px 10px 16px;text-align:center;border-bottom:1px solid #263245}
.sb-logo-icon{width:48px;height:48px;margin:0 auto 12px;background:linear-gradient(135deg,#3B82F6,#2563EB);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:20px;color:#fff;box-shadow:0 4px 12px rgba(59,130,246,.3)}
.sb-logo-name{font-size:16px;font-weight:700;color:#E5E7EB;letter-spacing:-.2px}
.sb-logo-sub{font-size:9px;color:#64748B;text-transform:uppercase;letter-spacing:1.5px;margin-top:3px}

/* Sidebar nav — more spacing */
.sb-nav-label{font-size:9px;color:#475569;text-transform:uppercase;letter-spacing:1.5px;font-weight:700;padding:18px 18px 8px}
section[data-testid="stSidebar"] div[data-testid="stRadio"]>label{margin-bottom:4px!important;display:block!important}
section[data-testid="stSidebar"] div[data-testid="stRadio"]>label>div{padding:12px 18px!important;font-size:13px!important;font-weight:500!important;color:#94A3B8!important;border-radius:0!important;border-left:3px solid transparent!important;transition:all .15s!important;margin:0!important}
section[data-testid="stSidebar"] div[data-testid="stRadio"]>label>div:hover{background:#1E293B!important;color:#E2E8F0!important}
section[data-testid="stSidebar"] div[data-testid="stRadio"]>label[aria-checked="true"]>div{background:#1E293B!important;color:#3B82F6!important;border-left:3px solid #3B82F6!important;font-weight:600!important}

/* Sidebar logout at bottom */
.sb-spacer{min-height:48vh}
.sb-logout{padding:0 14px 20px}
.sb-logout button{width:100%;background:#1E293B!important;border:1px solid #263245!important;color:#94A3B8!important;border-radius:6px;padding:9px 0!important;font-size:12px!important;font-weight:500!important;transition:all .15s!important}
.sb-logout button:hover{border-color:#EF4444!important;color:#EF4444!important;background:#2A1A1A!important}

/* ===== CONTENT CARDS ===== */
.content-card{background:#FFFFFF;border:1px solid #E5E7EB;border-radius:8px;padding:20px 24px;box-shadow:0 1px 2px rgba(0,0,0,.04)}

/* Stat cards */
.stat-box{background:#FFFFFF;border:1px solid #E5E7EB;border-radius:8px;padding:14px 16px;position:relative;overflow:hidden;box-shadow:0 1px 2px rgba(0,0,0,.04)}
.stat-box::before{content:'';position:absolute;top:0;left:0;right:0;height:3px}
.sg::before{background:#3B82F6}
.sb2::before{background:#10B981}
.so::before{background:#F59E0B}
.sy::before{background:#8B5CF6}
.stat-lbl{font-size:10px;color:#6B7280;text-transform:uppercase;letter-spacing:.8px;font-weight:600;margin-bottom:3px}
.stat-val{font-size:22px;font-weight:800;color:#1F2937;line-height:1}

/* Product cards — 16:9 ratio */
.p-card{background:#FFFFFF;border:1px solid #E5E7EB;border-radius:8px;padding:14px 16px;aspect-ratio:16/9;display:flex;flex-direction:column;justify-content:space-between;transition:all .15s;box-shadow:0 1px 2px rgba(0,0,0,.03)}
.p-card:hover{border-color:#93C5FD;background:#F8FAFF;box-shadow:0 4px 12px rgba(59,130,246,.08)}
.p-name{font-size:12px;font-weight:600;color:#1F2937;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.p-code{font-size:9.5px;color:#9CA3AF;font-family:'Courier New',monospace;margin:1px 0 0}
.p-mid{flex:1;display:flex;align-items:center}
.p-stock{font-size:18px;font-weight:800;color:#10B981;line-height:1}
.p-div{height:1px;background:#F3F4F6}
.p-total{font-size:10px;color:#9CA3AF}
.p-total b{color:#6B7280}
.dot{display:inline-block;width:6px;height:6px;border-radius:50%;margin-right:4px;vertical-align:middle}
.dot-g{background:#10B981}
.dot-y{background:#F59E0B}
.dot-r{background:#EF4444}

/* Section headers */
.sec-h{font-size:13px;font-weight:600;color:#374151;margin-bottom:12px;padding-bottom:8px;border-bottom:1px solid #E5E7EB}

/* Tables */
.dataframe{border:1px solid #E5E7EB!important;border-radius:8px!important;overflow:hidden;background:#FFFFFF!important}
.dataframe th{background:#F9FAFB!important;color:#6B7280!important;font-size:11px!important;text-transform:uppercase;letter-spacing:.5px;font-weight:600!important;border-bottom:1px solid #E5E7EB!important;padding:10px 14px!important}
.dataframe td{color:#374151!important;font-size:12.5px!important;border-bottom:1px solid #F3F4F6!important;padding:9px 14px!important}
.dataframe tr:last-child td{border-bottom:none!important}
.dataframe tr:hover td{background:#F8FAFF!important}

/* Badges */
.badge{display:inline-block;padding:2px 10px;border-radius:4px;font-size:10px;font-weight:600;letter-spacing:.3px}
.b-i{background:#FEF3C7;color:#D97706}
.b-r{background:#D1FAE5;color:#059669}
.b-u{background:#DBEAFE;color:#2563EB}

/* ===== FORM INPUTS — ALL SAME WHITE ===== */
.stTextInput>div>div>input,.stSelectbox>div>div>select,.stNumberInput>div>div>input,.stTextArea>div>div>textarea{background:#FFFFFF!important;color:#1F2937!important;border:1px solid #D1D5DB!important;border-radius:6px!important;font-size:13px!important;transition:all .15s}
.stTextInput>div>div>input:focus,.stSelectbox>div>div>select:focus,.stNumberInput>div>div>input:focus{border-color:#3B82F6!important;box-shadow:0 0 0 3px rgba(59,130,246,.1)!important;outline:none!important}
.stTextInput>div>div>input:disabled,.stNumberInput>div>div>input:disabled{background:#F9FAFB!important;color:#9CA3AF!important;border-color:#E5E7EB!important}
.stTextArea>div>div>textarea{font-family:'Courier New',monospace!important;font-size:12px!important}
input[type="date"]{background:#FFFFFF!important;color:#1F2937!important;border:1px solid #D1D5DB!important;border-radius:6px!important}
.stTextInput>label,.stSelectbox>label,.stNumberInput>label,.stTextArea>label,.stDateInput>label{font-size:12px!important;font-weight:600!important;color:#374151!important}

/* Buttons */
.stDownloadButton>button{background:#FFFFFF!important;border:1px solid #D1D5DB!important;color:#374151!important;border-radius:6px!important;font-weight:500!important;font-size:12px!important;transition:all .15s}
.stDownloadButton>button:hover{border-color:#3B82F6!important;color:#3B82F6!important;background:#EFF6FF!important}
.stButton>button[kind="primary"]{background:#3B82F6!important;color:#FFFFFF!important;border:none!important;border-radius:6px!important;font-weight:600!important;font-size:13px!important;transition:all .15s}
.stButton>button[kind="primary"]:hover{background:#2563EB!important;box-shadow:0 4px 12px rgba(59,130,246,.25)!important}

/* Dropdown scroll */
[data-baseweb="select"]>div>ul{max-height:260px!important;overflow-y:auto!important;border-radius:6px!important;border:1px solid #D1D5DB!important;box-shadow:0 10px 30px rgba(0,0,0,.12)!important;background:#FFFFFF!important}
[data-baseweb="select"]>div>ul>li{font-size:13px!important;color:#374151!important;padding:8px 12px!important}
[data-baseweb="select"]>div>ul>li:hover{background:#F3F4F6!important}
[data-baseweb="select"]>div>ul>li[aria-selected="true"]{background:#EFF6FF!important;color:#2563EB!important}
[data-baseweb="tag"]{background:#DBEAFE!important;border-radius:4px!important;color:#2563EB!important}

/* Form section label */
.form-sec{font-size:11px;font-weight:700;color:#3B82F6;text-transform:uppercase;letter-spacing:.8px;margin-bottom:10px}
.form-wrap{background:#FFFFFF;border:1px solid #E5E7EB;border-radius:8px;padding:22px 24px;box-shadow:0 1px 2px rgba(0,0,0,.04)}
.hint{font-size:11px;color:#9CA3AF;margin-top:-2px;margin-bottom:8px}

/* Login */
.login-card{background:#FFFFFF;border:1px solid #E5E7EB;border-radius:12px;padding:44px 40px;box-shadow:0 8px 40px rgba(0,0,0,.08)}
.login-icon{width:64px;height:64px;margin:0 auto 18px;background:linear-gradient(135deg,#3B82F6,#2563EB);border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:28px;color:#fff;box-shadow:0 8px 24px rgba(59,130,246,.25)}

/* Alerts */
.stInfo{background:#EFF6FF!important;border:1px solid #BFDBFE!important;color:#1D4ED8!important;border-radius:8px!important}
.stWarning{background:#FFFBEB!important;border:1px solid #FDE68A!important;color:#B45309!important;border-radius:8px!important}
.stSuccess{background:#ECFDF5!important;border:1px solid #A7F3D0!important;color:#047857!important;border-radius:8px!important}
.stError{background:#FEF2F2!important;border:1px solid #FECACA!important;color:#B91C1C!important;border-radius:8px!important}
</style>""", unsafe_allow_html=True)

# ==========================================
# UNITS (20)
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
# LOGIN (NO SIDEBAR)
# ==========================================
if not st.session_state["logged_in"]:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, box, _ = st.columns([1.3, 1.2, 1.3])
    with box:
        st.markdown('''<div class="login-card" style="text-align:center;margin-bottom:24px">
        <div class="login-icon">📦</div>
        <div style="font-size:22px;font-weight:800;color:#1F2937;letter-spacing:-.3px">AssetFlow KCCL</div>
        <div style="font-size:12px;color:#6B7280;margin-top:4px">Inventory Management System</div>
        </div>''', unsafe_allow_html=True)
        with st.form("lf"):
            u = st.text_input("Username", placeholder="Enter username")
            p = st.text_input("Password", type="password", placeholder="Enter password")
            if st.form_submit_button("Sign In", use_container_width=True):
                if u == "admin" and p == "kccl@2026":
                    st.session_state["logged_in"] = True
                    st.rerun()
                else:
                    st.error("Invalid credentials!")
        st.markdown('<div style="text-align:center;margin-top:16px"><code style="font-size:11px;color:#6B7280;background:#F3F4F6;padding:3px 10px;border-radius:4px;border:1px solid #E5E7EB;font-family:monospace">admin / kccl@2026</code></div>', unsafe_allow_html=True)
    st.stop()

# ==========================================
# SIDEBAR — LOGO + NAV + LOGOUT AT BOTTOM
# ==========================================
st.sidebar.markdown('<div class="sb-logo">', unsafe_allow_html=True)

_logo_shown = False
try:
    if os.path.exists("assets/logo.png"):
        st.sidebar.image("assets/logo.png", width=100, use_container_width=False)
        _logo_shown = True
except:
    pass

if not _logo_shown:
    st.sidebar.markdown('<div class="sb-logo-icon" style="margin:0 auto 12px">📦</div>', unsafe_allow_html=True)

st.sidebar.markdown('<div class="sb-logo-name">AssetFlow</div><div class="sb-logo-sub">KCCL Inventory</div></div>', unsafe_allow_html=True)

st.sidebar.markdown('<div class="sb-nav-label">Main Menu</div>', unsafe_allow_html=True)
page = st.sidebar.radio("", ["Dashboard", "Transaction", "Reports"], label_visibility="collapsed")

st.sidebar.markdown('<div class="sb-spacer"></div>', unsafe_allow_html=True)
st.sidebar.markdown("---", unsafe_allow_html=True)
st.sidebar.markdown('<div class="sb-logout">', unsafe_allow_html=True)
if st.sidebar.button("Logout", key="sb_logout", use_container_width=True):
    st.session_state["logged_in"] = False
    st.rerun()
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# LOAD DATA
# ==========================================
NOW = datetime.now()
DT_STR = NOW.strftime("%d%b%Y")
df_p, df_t = load_data()

# ==========================================
# DASHBOARD
# ==========================================
if page == "Dashboard":
    if df_p.empty:
        st.info("No products found. Add via Supabase SQL Editor.")
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
    with s1: st.markdown(f'<div class="stat-box sg"><div class="stat-lbl">Products</div><div class="stat-val">{len(df_p)}</div></div>', unsafe_allow_html=True)
    with s2: st.markdown(f'<div class="stat-box sb2"><div class="stat-lbl">In Stock</div><div class="stat-val">{ts:,.1f}</div></div>', unsafe_allow_html=True)
    with s3: st.markdown(f'<div class="stat-box so"><div class="stat-lbl">Issued (Month)</div><div class="stat-val">{im:,.1f}</div></div>', unsafe_allow_html=True)
    with s4: st.markdown(f'<div class="stat-box sy"><div class="stat-lbl">Returned (Month)</div><div class="stat-val">{rm:,.1f}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-h">Product Stock</div>', unsafe_allow_html=True)
    cards = st.columns(5)
    sum_rows = []
    for idx, (_, r) in enumerate(df_p.iterrows()):
        pid, nm, code, unit = r["id"], r["product_name"], r["item_code"], r["default_unit"]
        total = safe_num(r.get("total_added_to_system", 0), 0)
        stk = get_stock(df_t, pid)
        dc = dot_cls(stk, total)
        sum_rows.append({"Product Name": nm, "Item Code": code, "In Stock": round(stk, 3), "Unit": unit, "Total Added": int(total)})
        with cards[idx % 5]:
            st.markdown(f'<div class="p-card"><div><div style="display:flex;align-items:center;gap:4px"><span class="dot {dc}"></span><div class="p-name">{nm}</div></div><div class="p-code">{code}</div></div><div class="p-mid"><div class="p-stock">{stk:.2f}</div></div><div><div class="p-div"></div><div class="p-total">Total: <b>{int(total)} {unit}</b></div></div></div>', unsafe_allow_html=True)

    df_sum = pd.DataFrame(sum_rows)
    st.markdown('<div class="sec-h">Export Data</div>', unsafe_allow_html=True)
    d1, d2, d3 = st.columns(3)
    with d1:
        st.markdown("**Full Dump**")
        if not df_t.empty:
            df_d = df_t.copy()
            df_d["created_at"] = df_d["created_at"].apply(ind_dt)
            df_d = explode_serials(df_d)
            st.download_button("Download CSV", data=to_csv(df_d), file_name=f"AssetFlow_FullDump_{DT_STR}.csv", mime="text/csv", key="d1")
    with d2:
        st.markdown("**Product Summary**")
        if not df_sum.empty:
            st.download_button("Download CSV", data=to_csv(df_sum), file_name=f"AssetFlow_Summary_{DT_STR}.csv", mime="text/csv", key="d2")
    with d3:
        st.markdown("**Issued Details**")
        sel = st.selectbox("Select", df_p["product_name"].tolist(), key="cs", label_visibility="collapsed")
        if sel:
            tid = df_p[df_p["product_name"]==sel]["id"].values[0]
            df_is = df_t[(df_t["product_id"]==tid) & (df_t["action_type"]=="ISSUE")].copy()
            if not df_is.empty:
                df_is["created_at"] = df_is["created_at"].apply(ind_dt)
                df_is["Product"] = sel
                df_is = explode_serials(df_is)
                ec = [c for c in ["created_at","Product","item_code","serial_number","quantity","unit","issued_to","invoice_no"] if c in df_is.columns]
                st.download_button("Download CSV", data=to_csv(df_is[ec]), file_name=f"AssetFlow_{sel.lower().replace(' ','_')}_Issued_{DT_STR}.csv", mime="text/csv", key="d3")
            else:
                st.markdown('<div class="hint">No ISSUE records.</div>', unsafe_allow_html=True)

# ==========================================
# TRANSACTION
# ==========================================
elif page == "Transaction":
    if df_p.empty:
        st.warning("Add products first.")
        st.stop()

    st.markdown('<div class="form-wrap">', unsafe_allow_html=True)
    cl, cr = st.columns(2)
    with cl:
        st.markdown('<div class="form-sec">Product Details</div>', unsafe_allow_html=True)
        sel_prod = st.selectbox("Product *", df_p["product_name"].tolist(), key="tp")
        item_code = st.text_input("Item Code *", placeholder="Comma-separated for bulk: IC-001, IC-002", key="tc")
        serial = st.text_area("Serial Number(s) *", placeholder="Comma-separated: SN-001, SN-002, SN-003", height=52, key="ts")
        st.markdown('<div class="hint">UPLOAD: comma = separate entries. ISSUE/RETURN: must match uploaded records.</div>', unsafe_allow_html=True)
        unit = st.selectbox("Unit *", UNITS, key="tu")
        qty = st.number_input("Quantity *", min_value=0.001, step=0.001, format="%.3f", key="tq")
    with cr:
        st.markdown('<div class="form-sec">Action Details</div>', unsafe_allow_html=True)
        action = st.selectbox("Action *", ["ISSUE","RETURN","UPLOAD"], key="ta")
        issued_to = st.text_input("Issued To" + (" *" if action != "UPLOAD" else ""), placeholder="Person or site name", key="ti")
        invoice = st.text_input("Invoice / DC No *", placeholder="e.g. INV-2025-042", key="tn")
        st.text_input("DateTime", value=NOW.strftime("%d-%b-%Y  %H:%M:%S"), disabled=True, key="td")
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.button("Commit Transaction", use_container_width=True, type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

    if submitted:
        errs = []
        if not item_code.strip(): errs.append("Item Code is required.")
        if not serial.strip(): errs.append("Serial Number is required.")
        if qty <= 0: errs.append("Quantity must be greater than zero.")
        if action != "UPLOAD" and not issued_to.strip(): errs.append("Issued To is required for ISSUE/RETURN.")
        if not invoice.strip(): errs.append("Invoice / DC No is required.")
        if errs:
            for e in errs: st.error(e)
            st.stop()
        pid = int(df_p[df_p["product_name"]==sel_prod]["id"].values[0])
        if action == "UPLOAD":
            codes = [c.strip() for c in item_code.split(",") if c.strip()]
            serials = [s.strip() for s in serial.split(",") if s.strip()]
            if not codes:
                st.error("No valid Item Code provided.")
                st.stop()
            ok = 0
            for i, code in enumerate(codes):
                sn = serials[i] if i < len(serials) else ""
                payload = {"product_id": pid, "item_code": code, "serial_number": sn, "quantity": qty, "unit": unit, "issued_to": "", "invoice_no": invoice.strip(), "action_type": "UPLOAD", "created_at": datetime.now().isoformat()}
                try:
                    res = supabase.table("tpl_inv_transactions").insert(payload).execute()
                    if res.data: ok += 1
                except Exception as ex:
                    st.error(f"Failed for {code}: {ex}")
            if ok > 0:
                st.success(f"Uploaded {ok} item(s) successfully!")
                load_data.clear()
                st.rerun()
        else:
            ic, sn = item_code.strip(), serial.strip()
            if not df_t.empty:
                uploads = df_t[df_t["action_type"]=="UPLOAD"]
                if ic not in uploads["item_code"].values:
                    st.error(f"Item Code '{ic}' has not been uploaded! Cannot {action.lower()}.")
                    st.stop()
                if sn:
                    match = uploads[(uploads["item_code"]==ic) & (uploads["serial_number"]==sn)]
                    if match.empty:
                        st.error(f"Serial '{sn}' not found for Item Code '{ic}' in uploads!")
                        st.stop()
            if action == "ISSUE":
                cs = get_stock(df_t, pid)
                if qty > cs:
                    st.error(f"Insufficient stock! Available: {cs:.3f} {unit}")
                    st.stop()
            payload = {"product_id": pid, "item_code": ic, "serial_number": sn, "quantity": qty, "unit": unit, "issued_to": issued_to.strip(), "invoice_no": invoice.strip(), "action_type": action, "created_at": datetime.now().isoformat()}
            try:
                res = supabase.table("tpl_inv_transactions").insert(payload).execute()
                if res.data:
                    st.success(f"Committed: {action} {qty:.3f} {unit} — {ic}")
                    load_data.clear()
                    st.rerun()
                else:
                    st.error("Insert failed. Check RLS policies.")
            except Exception as ex:
                st.error(f"DB Error: {ex}")

# ==========================================
# REPORTS
# ==========================================
elif page == "Reports":
    if df_t.empty:
        st.info("No transaction data available.")
        st.stop()

    df_r = df_t.copy()
    if not df_p.empty:
        pmap = df_p.set_index("id")["product_name"].to_dict()
        df_r["product_name"] = df_r["product_id"].map(pmap).fillna("Unknown")
    df_r["created_at"] = pd.to_datetime(df_r["created_at"], errors="coerce")
    df_r["_d"] = df_r["created_at"].dt.date
    mn = df_r["_d"].min() if df_r["_d"].notna().any() else NOW.date()
    mx = df_r["_d"].max() if df_r["_d"].notna().any() else NOW.date()

    st.markdown('<div class="form-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="form-sec">Filter Criteria</div>', unsafe_allow_html=True)
    f1, f2, f3, f4, f5 = st.columns(5)
    with f1: df_ = st.date_input("From", value=mn, key="rf")
    with f2: dt_ = st.date_input("To", value=mx, key="rt")
    with f3: it_ = st.multiselect("Issued To", sorted(df_r["issued_to"].dropna().unique()), key="ri")
    with f4: im_ = st.multiselect("Item", sorted(df_p["product_name"].tolist()), key="rm")
    with f5: st_ = st.multiselect("Type", ["ISSUE","RETURN","UPLOAD"], key="rs")
    iv_ = st.multiselect("Invoice No", sorted(df_r["invoice_no"].dropna().unique()), key="rv")
    st.markdown('</div>', unsafe_allow_html=True)

    active = df_ != mn or dt_ != mx or it_ or im_ or st_ or iv_
    if not active:
        st.info("Select at least one filter to view data.")
        st.stop()

    df_f = df_r.copy()
    if df_ != mn: df_f = df_f[df_f["_d"] >= df_]
    if dt_ != mx: df_f = df_f[df_f["_d"] <= dt_]
    if it_: df_f = df_f[df_f["issued_to"].isin(it_)]
    if im_: df_f = df_f[df_f["product_name"].isin(im_)]
    if st_: df_f = df_f[df_f["action_type"].isin(st_)]
    if iv_: df_f = df_f[df_f["invoice_no"].isin(iv_)]

    r1, r2 = st.columns([1, 1])
    with r1:
        st.markdown(f'<span style="font-size:13px;color:#6B7280">Showing </span><span style="font-size:13px;font-weight:700;color:#2563EB">{len(df_f)}</span><span style="font-size:13px;color:#6B7280"> records</span>', unsafe_allow_html=True)
    with r2:
        if not df_f.empty:
            df_ex = df_f.copy()
            df_ex["created_at"] = df_ex["created_at"].apply(ind_dt)
            df_ex = explode_serials(df_ex)
            ec = [c for c in ["created_at","product_name","item_code","serial_number","quantity","unit","issued_to","invoice_no","action_type"] if c in df_ex.columns]
            st.download_button("Export CSV", data=to_csv(df_ex[ec]), file_name=f"AssetFlow_Report_{DT_STR}.csv", mime="text/csv", key="dr")

    if not df_f.empty:
        df_s = df_f.copy()
        df_s["created_at"] = df_s["created_at"].apply(ind_dt)
        df_s = explode_serials(df_s)
        ec = [c for c in ["created_at","product_name","item_code","serial_number","quantity","unit","issued_to","invoice_no","action_type"] if c in df_s.columns]
        df_s = df_s[ec].rename(columns={"created_at":"Date","product_name":"Product","item_code":"Code","serial_number":"Serial","quantity":"Qty","unit":"Unit","issued_to":"Issued To","invoice_no":"Invoice","action_type":"Action"})
        st.dataframe(df_s, use_container_width=True, hide_index=True, height=440)
    else:
        st.warning("No records match this filter.")
