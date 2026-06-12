import streamlit as st
import pandas as pd
from supabase import create_client, Client
import os
from datetime import datetime

# ==========================================
# SUPABASE CONFIG
# ==========================================
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://emdjnndnsdebhbzebrsg.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVtZGpubmRuc2RlYmhiemVicnNnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODExNzU4NDYsImV4cCI6MjA5Njc1MTg0Nn0.ypy3k30Nbp2caJaNXpwxbrnUzrOLrhwTJ1FZwW5L8Fc")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="AssetFlow KCCL", page_icon="📦", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# PROFESSIONAL DARK THEME (Screenshot Inspired)
# ==========================================
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.block-container{padding-top:1.5rem;padding-bottom:2rem;max-width:1400px}
.stApp{background:#0B0F19;color:#E8ECF4;font-family:'Inter',system-ui,sans-serif}
section[data-testid="stSidebar"]{background:#0D1120;border-right:1px solid #1B2236}
section[data-testid="stSidebar"] .stMarkdown{color:#E8ECF4}
#MainMenu{visibility:hidden}footer{visibility:hidden}
header[data-testid="stHeader"]{background:#0D1120;border-bottom:1px solid #1B2236}

.stat-box{background:linear-gradient(135deg,#151C2E 0%,#18223A 100%);border:1px solid #1E2A45;border-radius:12px;padding:18px 20px;position:relative;overflow:hidden}
.stat-box::before{content:'';position:absolute;top:0;left:0;right:0;height:2px}
.sg::before{background:linear-gradient(90deg,#00D68F,#00B377)}
.sb::before{background:linear-gradient(90deg,#4C9AFF,#2D7AE0)}
.so::before{background:linear-gradient(90deg,#FFB020,#E09800)}
.sy::before{background:linear-gradient(90deg,#A78BFA,#7C5CE0)}
.stat-lbl{font-size:11px;color:#5A6478;text-transform:uppercase;letter-spacing:.8px;font-weight:600;margin-bottom:6px}
.stat-val{font-size:26px;font-weight:800;color:#E8ECF4;line-height:1}

.p-card{background:#151C2E;border:1px solid #1E2A45;border-radius:10px;padding:14px 16px;transition:all .2s ease}
.p-card:hover{border-color:#2A3E5F;background:#18223A;transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,.3)}
.p-name{font-size:12.5px;font-weight:700;color:#E8ECF4;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.p-code{font-size:10px;color:#5A6478;font-family:'Courier New',monospace;margin:3px 0 10px;letter-spacing:.3px}
.p-stock{font-size:20px;font-weight:800;color:#00D68F;line-height:1}
.p-div{height:1px;background:#1E2A45;margin:8px 0}
.p-total{font-size:10px;color:#5A6478}
.p-total b{color:#8892A6}
.dot{display:inline-block;width:6px;height:6px;border-radius:50%;margin-right:4px;vertical-align:middle}
.dot-g{background:#00D68F;box-shadow:0 0 6px rgba(0,214,143,.4)}
.dot-y{background:#FFB020;box-shadow:0 0 6px rgba(255,176,32,.4)}
.dot-r{background:#FF4757;box-shadow:0 0 6px rgba(255,71,87,.4)}

.sec-h{font-size:12px;font-weight:700;color:#8892A6;text-transform:uppercase;letter-spacing:1px;margin-bottom:12px;padding-bottom:8px;border-bottom:1px solid #1E2A45}

.dataframe{border:1px solid #1E2A45!important;border-radius:10px!important;overflow:hidden;background:#111827!important}
.dataframe th{background:#0D1120!important;color:#5A6478!important;font-size:10px!important;text-transform:uppercase;letter-spacing:.6px;font-weight:700!important;border-bottom:1px solid #1E2A45!important;padding:10px 14px!important}
.dataframe td{color:#C8D0E0!important;font-size:12px!important;border-bottom:1px solid #151C2E!important;padding:9px 14px!important}
.dataframe tr:last-child td{border-bottom:none!important}
.dataframe tr:hover td{background:#151C2E!important}

.badge{display:inline-block;padding:2px 10px;border-radius:12px;font-size:10px;font-weight:700;letter-spacing:.3px}
.b-i{background:rgba(255,176,32,.1);color:#FFB020}
.b-r{background:rgba(0,214,143,.1);color:#00D68F}
.b-u{background:rgba(76,154,255,.1);color:#4C9AFF}

.stTextInput>div>div>input,.stSelectbox>div>div>select,.stNumberInput>div>div>input,.stTextArea>div>div>textarea{background:#0D1120!important;color:#E8ECF4!important;border:1px solid #1E2A45!important;border-radius:8px!important;font-size:13px!important}
.stTextInput>div>div>input:focus,.stSelectbox>div>div>select:focus,.stNumberInput>div>div>input:focus{border-color:#00D68F!important;box-shadow:0 0 0 3px rgba(0,214,143,.1)!important}
.stTextArea>div>div>textarea{font-family:'Courier New',monospace!important;font-size:12px!important}
input[type="date"]{background:#0D1120!important;color:#E8ECF4!important;border:1px solid #1E2A45!important;border-radius:8px!important}

.stDownloadButton>button{background:#151C2E!important;border:1px solid #1E2A45!important;color:#8892A6!important;border-radius:8px!important;font-weight:600!important;font-size:12px!important;transition:all .2s}
.stDownloadButton>button:hover{border-color:#00D68F!important;color:#00D68F!important;background:#18223A!important}
.stButton>button[kind="primary"]{background:linear-gradient(135deg,#00D68F,#00B377)!important;color:#0B0F19!important;border:none!important;border-radius:8px!important;font-weight:700!important;font-size:13px!important;transition:all .2s}
.stButton>button[kind="primary"]:hover{box-shadow:0 6px 20px rgba(0,214,143,.3)!important;transform:translateY(-1px)}
.stButton>button[kind="secondary"]{background:#151C2E!important;border:1px solid #1E2A45!important;color:#8892A6!important;border-radius:8px!important}

[data-baseweb="select"]>div>ul{max-height:260px!important;overflow-y:auto!important;border-radius:8px!important;border:1px solid #1E2A45!important;box-shadow:0 12px 32px rgba(0,0,0,.5)!important;background:#151C2E!important}
[data-baseweb="select"]>div>ul>li{font-size:13px!important;color:#C8D0E0!important;padding:8px 14px!important}
[data-baseweb="select"]>div>ul>li:hover{background:#1E2A45!important}
[data-baseweb="select"]>div>ul>li[aria-selected="true"]{background:#18223A!important;color:#00D68F!important}
[data-baseweb="tag"]{background:#1E2A45!important;border-radius:6px!important}

.form-sec{font-size:11px;font-weight:700;color:#00D68F;text-transform:uppercase;letter-spacing:.8px;margin-bottom:12px}
.login-card{background:linear-gradient(145deg,#151C2E 0%,#111827 100%);border:1px solid #1E2A45;border-radius:16px;padding:36px 32px;box-shadow:0 24px 64px rgba(0,0,0,.5)}
.nav-lbl{font-size:9px;color:#3A4660;text-transform:uppercase;letter-spacing:1.5px;font-weight:700;margin-bottom:8px}
.form-wrap{background:#111827;border:1px solid #1E2A45;border-radius:12px;padding:24px;box-shadow:0 2px 8px rgba(0,0,0,.2)}
.hint{font-size:11px;color:#5A6478;margin-top:-6px;margin-bottom:10px}
.stInfo{background:rgba(76,154,255,.08)!important;border:1px solid rgba(76,154,255,.2)!important;color:#4C9AFF!important;border-radius:10px!important}
.stWarning{background:rgba(255,176,32,.08)!important;border:1px solid rgba(255,176,32,.2)!important;color:#FFB020!important;border-radius:10px!important}
.stSuccess{background:rgba(0,214,143,.08)!important;border:1px solid rgba(0,214,143,.2)!important;color:#00D68F!important;border-radius:10px!important}
.stError{background:rgba(255,71,87,.08)!important;border:1px solid rgba(255,71,87,.2)!important;color:#FF4757!important;border-radius:10px!important}
</style>""", unsafe_allow_html=True)

# ==========================================
# LOGO (CENTERED IN SIDEBAR)
# ==========================================
if os.path.exists("assets/logo.png"):
    st.sidebar.markdown('<div style="text-align:center;padding:12px 0 4px"><img src="data:image/png;base64,' + open("assets/logo.png","rb").read().hex() + '" style="width:110px;border-radius:10px"></div>', unsafe_allow_html=True)
else:
    st.sidebar.markdown('''<div style="text-align:center;padding:12px 0 4px">
    <div style="width:46px;height:46px;margin:0 auto 10px;background:linear-gradient(135deg,#00D68F,#00B377);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:22px;box-shadow:0 6px 18px rgba(0,214,143,.2)">📦</div>
    <div style="font-size:17px;font-weight:800;color:#E8ECF4;letter-spacing:-.3px">AssetFlow</div>
    <div style="font-size:9px;color:#3A4660;letter-spacing:1.5px;text-transform:uppercase;margin-top:2px">KCCL Inventory</div>
    </div>''', unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown('<div class="nav-lbl">Navigation</div>', unsafe_allow_html=True)

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
        if s and s != "":
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
# LOGIN
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    _, box, _ = st.columns([1.3, 1, 1.3])
    with box:
        st.markdown('''<div class="login-card" style="text-align:center;margin-bottom:20px">
        <div style="width:54px;height:54px;margin:0 auto 14px;background:linear-gradient(135deg,#00D68F,#00B377);
        border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:24px;
        box-shadow:0 8px 24px rgba(0,214,143,.25)">📦</div>
        <div style="font-size:21px;font-weight:800;color:#E8ECF4;letter-spacing:-.3px">AssetFlow KCCL</div>
        <div style="font-size:11px;color:#5A6478;margin-top:4px">Inventory Management System</div>
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
        st.markdown('<div style="text-align:center;margin-top:14px"><span style="font-size:11px;color:#3A4660">Template: </span><code style="font-size:11px;color:#5A6478;background:#0D1120;padding:2px 8px;border-radius:4px;font-family:monospace">admin / kccl@2026</code></div>', unsafe_allow_html=True)
    st.stop()

# ==========================================
# SIDEBAR: NAV + LOGOUT AT BOTTOM
# ==========================================
page = st.sidebar.radio("", ["Dashboard", "Transaction", "Reports"], label_visibility="collapsed")
st.sidebar.markdown('<div style="min-height:42vh"></div>', unsafe_allow_html=True)
st.sidebar.markdown("---")
if st.sidebar.button("🔓  Logout", use_container_width=True, key="logout_btn"):
    st.session_state["logged_in"] = False
    st.rerun()

# ==========================================
# LOAD DATA
# ==========================================
df_p, df_t = load_data()
NOW = datetime.now()
DT_STR = NOW.strftime("%d%b%Y")

# ==========================================
# DASHBOARD
# ==========================================
if page == "Dashboard":
    st.header("Dashboard")
    st.markdown('<div style="font-size:12px;color:#5A6478;margin-top:-8px;margin-bottom:20px">Real-time inventory overview</div>', unsafe_allow_html=True)

    if df_p.empty:
        st.info("No products found. Add via Supabase SQL Editor.")
        st.stop()

    ts = sum(get_stock(df_t, r["id"]) for _, r in df_p.iterrows())
    im = rm = 0.0
    if not df_t.empty:
        df_t["created_at"] = pd.to_datetime(df_t["created_at"], errors="coerce")
        m = df_t.dropna(subset=["created_at"])
        mk = (m["created_at"].dt.month == NOW.month) & (m["created_at"].dt.year == NOW.year)
        im = safe_num(m[mk & (m["action_type"]=="ISSUE")]["quantity"].sum())
        rm = safe_num(m[mk & (m["action_type"]=="RETURN")]["quantity"].sum())

    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown(f'<div class="stat-box sg"><div class="stat-lbl">Products</div><div class="stat-val">{len(df_p)}</div></div>', unsafe_allow_html=True)
    with s2:
        st.markdown(f'<div class="stat-box sb"><div class="stat-lbl">In Stock</div><div class="stat-val">{ts:,.1f}</div></div>', unsafe_allow_html=True)
    with s3:
        st.markdown(f'<div class="stat-box so"><div class="stat-lbl">Issued (Month)</div><div class="stat-val">{im:,.1f}</div></div>', unsafe_allow_html=True)
    with s4:
        st.markdown(f'<div class="stat-box sy"><div class="stat-lbl">Returned (Month)</div><div class="stat-val">{rm:,.1f}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
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
            st.markdown(f'<div class="p-card"><div style="display:flex;align-items:center;gap:4px"><span class="dot {dc}"></span><div class="p-name">{nm}</div></div><div class="p-code">{code}</div><div class="p-stock">{stk:.2f}</div><div class="p-div"></div><div class="p-total">Total: <b>{int(total)} {unit}</b></div></div>', unsafe_allow_html=True)

    df_sum = pd.DataFrame(sum_rows)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-h">Export Data</div>', unsafe_allow_html=True)

    d1, d2, d3 = st.columns(3)
    with d1:
        st.markdown("**Full Dump**")
        if not df_t.empty:
            df_d = df_t.copy()
            df_d["created_at"] = df_d["created_at"].apply(ind_dt)
            df_d = explode_serials(df_d)
            st.download_button("📥 Download CSV", data=to_csv(df_d), file_name=f"AssetFlow_FullDump_{DT_STR}.csv", mime="text/csv", key="d1")
    with d2:
        st.markdown("**Product Summary**")
        if not df_sum.empty:
            st.download_button("📥 Download CSV", data=to_csv(df_sum), file_name=f"AssetFlow_Summary_{DT_STR}.csv", mime="text/csv", key="d2")
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
                st.download_button("📥 Download CSV", data=to_csv(df_is[ec]), file_name=f"AssetFlow_{sel.lower().replace(' ','_')}_Issued_{DT_STR}.csv", mime="text/csv", key="d3")
            else:
                st.markdown('<div class="hint">No ISSUE records.</div>', unsafe_allow_html=True)

# ==========================================
# TRANSACTION
# ==========================================
elif page == "Transaction":
    st.header("New Transaction")
    st.markdown('<div style="font-size:12px;color:#5A6478;margin-top:-8px;margin-bottom:20px">Issue, return or upload inventory items</div>', unsafe_allow_html=True)

    if df_p.empty:
        st.warning("Add products first.")
        st.stop()

    st.markdown('<div class="form-wrap">', unsafe_allow_html=True)
    cl, cr = st.columns(2)

    with cl:
        st.markdown('<div class="form-sec">Product Details</div>', unsafe_allow_html=True)
        sel_prod = st.selectbox("Product *", df_p["product_name"].tolist(), key="tp")
        item_code = st.text_input("Item Code *", placeholder="e.g. RJ-001", key="tc")
        serial = st.text_area("Serial Number(s)", placeholder="Comma-separated: SN-001, SN-002, SN-003", height=55, key="ts")
        st.markdown('<div class="hint">ℹ️  Each serial will appear as a separate row in reports.</div>', unsafe_allow_html=True)
        unit = st.selectbox("Unit *", UNITS, key="tu")
        qty = st.number_input("Quantity *", min_value=0.001, step=0.001, format="%.3f", key="tq")

    with cr:
        st.markdown('<div class="form-sec">Action Details</div>', unsafe_allow_html=True)
        issued_to = st.text_input("Issued To *", placeholder="Person or site name", key="ti")
        invoice = st.text_input("Invoice / DC No *", placeholder="e.g. INV-2025-042", key="tn")
        action = st.selectbox("Action *", ["ISSUE","RETURN","UPLOAD"], key="ta")
        st.text_input("DateTime", value=NOW.strftime("%d-%b-%Y  %H:%M:%S"), disabled=True, key="td")
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.button("⚡ Commit Transaction", use_container_width=True, type="primary")

    st.markdown('</div>', unsafe_allow_html=True)

    if submitted:
        errs = []
        if not item_code.strip(): errs.append("Item Code is required.")
        if qty <= 0: errs.append("Quantity must be greater than zero.")
        if action != "UPLOAD" and not issued_to.strip(): errs.append("Issued To is required for ISSUE/RETURN.")
        if not invoice.strip(): errs.append("Invoice / DC No is required.")
        if errs:
            for e in errs: st.error(e)
        else:
            if action == "ISSUE":
                pid = df_p[df_p["product_name"]==sel_prod]["id"].values[0]
                cs = get_stock(df_t, pid)
                if qty > cs:
                    st.error(f"Insufficient stock! Available: {cs:.3f} {unit}")
                    st.stop()
            payload = {
                "product_id": int(df_p[df_p["product_name"]==sel_prod]["id"].values[0]),
                "item_code": item_code.strip(),
                "serial_number": serial.strip(),
                "quantity": qty,
                "unit": unit,
                "issued_to": issued_to.strip(),
                "invoice_no": invoice.strip(),
                "action_type": action,
                "created_at": datetime.now().isoformat()
            }
            try:
                res = supabase.table("tpl_inv_transactions").insert(payload).execute()
                if res.data:
                    st.success(f"Committed: {action} {qty:.3f} {unit} — {item_code}")
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
    st.header("Reports")
    st.markdown('<div style="font-size:12px;color:#5A6478;margin-top:-8px;margin-bottom:20px">Filter and export transaction data</div>', unsafe_allow_html=True)

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
    st.markdown('<div class="form-sec">Filters</div>', unsafe_allow_html=True)
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
        st.markdown(f'<span style="font-size:13px;color:#5A6478">Showing </span><span style="font-size:13px;font-weight:700;color:#00D68F">{len(df_f)}</span><span style="font-size:13px;color:#5A6478"> records</span>', unsafe_allow_html=True)
    with r2:
        if not df_f.empty:
            df_ex = df_f.copy()
            df_ex["created_at"] = df_ex["created_at"].apply(ind_dt)
            df_ex = explode_serials(df_ex)
            ec = [c for c in ["created_at","product_name","item_code","serial_number","quantity","unit","issued_to","invoice_no","action_type"] if c in df_ex.columns]
            st.download_button("📥 Export CSV", data=to_csv(df_ex[ec]), file_name=f"AssetFlow_Report_{DT_STR}.csv", mime="text/csv", key="dr")

    st.markdown("<br>", unsafe_allow_html=True)
    if not df_f.empty:
        df_s = df_f.copy()
        df_s["created_at"] = df_s["created_at"].apply(ind_dt)
        df_s = explode_serials(df_s)
        ec = [c for c in ["created_at","product_name","item_code","serial_number","quantity","unit","issued_to","invoice_no","action_type"] if c in df_s.columns]
        df_s = df_s[ec].rename(columns={"created_at":"Date","product_name":"Product","item_code":"Code","serial_number":"Serial","quantity":"Qty","unit":"Unit","issued_to":"Issued To","invoice_no":"Invoice","action_type":"Action"})
        st.dataframe(df_s, use_container_width=True, hide_index=True, height=440)
    else:
        st.warning("No records match this filter.")
