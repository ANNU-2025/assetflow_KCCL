import streamlit as st
import pandas as pd
from supabase import create_client, Client
import os
from datetime import datetime

# ==========================================
# SUPABASE
# ==========================================
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://emdjnndnsdebhbzebrsg.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZi6ImVtZGpubmRuc2RlYmhiemVicnNnNnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODExNzU4NDYsImV4cCI6MjA5Njc1MTg0Nn0.ypy3k30Nbp2caJaNXpwxbrnUzrOLrhwTJ1FZwW5L8Fc")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="AssetFlow KCCL", page_icon="📦", layout="wide", initial_sidebar_state="expanded")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.markdown("<style>section[data-testid='stSidebar']{display:none}header[data-testid='stHeader']{display:none}</style>", unsafe_allow_html=True)

# ==========================================
# THEME
# ==========================================
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css=URL(...)Inter:wght@400;500;600;700;800&display=swap');
.stApp{background:#F1F5F9!important;color:#0A0F1D!important;font-family:'Inter',system-ui,sans-serif!important}
.block-container{padding:.8rem 2rem!important;max-width:1560px;margin:0 auto;position:relative;z-index:1}
header[data-testid="stHeader"]{height:0!important;min-height:0!important;padding:0!important;overflow:hidden!important;border:none!important;box-shadow:none!important;visibility:hidden!important}
section[data-testid="stSidebar"]{background:#0B0F19!important;border-right:2px solid #1E293B!important;width:250px!important;min-width:250px!important;overflow:hidden!important;overflow-y:hidden!important}
section[data-testid="stSidebar"]>div:first-child{width:250px!important;overflow:hidden!important}
#MainMenu,footer{visibility:hidden}
.sb-logo{text-align:left!important;align-items:flex-start!important;padding:18px 14px 14px!important}
.sb-logo img{border-radius:8px;max-width:130px;height:48px}
.sb-logo-name{font-size:18px;font-weight:800;color:#FFFFFF!important;letter-spacing:-.4px}
.sb-logo-sub{font-size:10px;color:#38BDF8!important;text-transform:uppercase;letter-spacing:1.5px;font-weight:700}
.sb-fallback-icon{width:48px;height:48px;background:linear-gradient(135deg,#0A0F1D,#1E293B);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:22px;color:#fff;box-shadow:0 4px 12px rgba(0,0,0,.3)}
.sb-nav-label{font-size:10px;color:#94A3B8!important;text-transform:uppercase;letter-spacing:1.5px;font-weight:700;padding:14px 20px 8px;text-align:center!important}
/* FIX: Radio button expanded - no collapse */
section[data-testid="stRadio"]>label{margin-bottom:2px!important;display:block!important}
section[data-testid="stRadio"]>div{white-space:normal!important;overflow:visible!important;text-overflow:visible!important;height:auto!important;min-height:44px!important;justify-content:center!important}
section[data-testid="stVerticalBlock"]>label>div{white-space:normal!important;overflow:visible!important;text-overflow:visible!important;height:auto!important;min-height:44px!important;justify-content:center!important}
.stat-box{background:#FFFFFF;border:2px solid #0A0F1D;border-radius:10px;padding:16px 18px;min-height:90px;display:flex;flex-direction:column;justify-content:center;box-shadow:0 1px 3px rgba(0,0,0,.06)}
.stat-lbl{font-size:10px;color:#475569!important;text-transform:uppercase;letter-spacing:1px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.stat-val{font-size:26px;font-weight:800;color:#0A0F1D!important;margin-top:4px;line-height:1}
.p-card{background:#FFFFFF;border:1px solid #CBD5E1;border-radius:8px;padding:10px 14px;display:flex;flex-direction:column;justify-content:space-between;height:72px;box-shadow:0 1px 2px rgba(0,0,0,.03);transition:all .15s}
.p-card:hover{border-color:#2563EB;background:#F8FAFF;transform:translateY(-1px);box-shadow:0 4px 12px rgba(37,99,235,.1)}
.p-top{display:flex;align-items:center;gap:5px;overflow:hidden}
.p-bottom{display:flex;align-items:flex-end;justify-content:space-between}
.p-name{font-size:13px;font-weight:700;color:#0A0F1D!important;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.p-stock{font-size:20px;font-weight:800;color:#16A34A!important;line-height:1;text-align:right}
.p-total{font-size:10px;color:#475569!important;font-weight:600}
.dot{display:inline-block;width:7px;height:7px;border-radius:50%;flex-shrink:0}
.dot-g{background:#16A34A}.dot-y{background:#D97706}.dot-r{background:#DC2626}
.sec-h{font-size:14px;font-weight:800;color:#0A0F1D!important;margin:18px 0 10px;padding-bottom:6px;border-bottom:2px solid #0A0F1D}
.stDownloadButton>button{background:#0EA5E9!important;color:#FFFFFF!important;border:none!important;border-radius:8px!important;font-weight:700!important;font-size:13px!important;padding:10px 16px!important;width:100%;box-shadow:0 2px 8px rgba(14,165,233,.25)!important;transition:all .15s!important}
.stDownloadButton>button:hover{background:#0284C7!important;box-shadow:0 4px 14px rgba(14,165,233,.35)!important}
.stButton>button[kind="primary"]{background:#0A0F1D!important;color:#FFFFFF!important;border:none!important;border-radius:8px!important;font-weight:700!important;font-size:14px!important;padding:11px 24px!important;width:100%;transition:all .15s!important}
.stButton>button[kind="primary"]:hover{background:#1E293B!important;box-shadow:0 4px 14px rgba(0,0,0,.2)!important}
label p,.stDateInput>label{font-size:12px!important;font-weight:700!important;color:#0A0F1D!important}
.stTextInput>div>div>input,.stSelectbox>div>div>select,.stNumberInput>div>div>input,.stTextArea>div>div>textarea{background:#FFFFFF!important;border:2px solid #94A3B8!important;border-radius:6px!important;color:#0A0F1D!important;font-weight:600!important;transition:all .15s}
.stTextInput>div>div>input:focus,.stSelectbox>div>div>select:focus,.stNumberInput>div>div>input:focus{border-color:#2563EB!important;box-shadow:0 0 0 3px rgba(37,99,235,.1)!important}
.stTextInput>div>div>input:disabled,.stNumberInput>div>div>input:disabled{background:#F1F5F9!important;color:#64748B!important;border-color:#CBD5E1!important}
.stTextArea>div>div>textarea{font-family:Courier New,monospace!important;font-size:12px!important}
input[type="date"]{background:#FFFFFF!important;color:#0A0F1D!important;border:2px solid #94A3B8!important;border-radius:6px!important}
[data-baseweb="select"]>div>ul{max-height:260px!important;overflow-y:auto!important;border-radius:6px!important;border:2px solid #94A3B8!important;box-shadow:0 10px 30px rgba(0,0,0,.12)!important;background:#FFFFFF!important}
[data-baseweb="select"]>div>ul>li{font-size:13px!important;color:#0A0F1D!important;padding:8px 12px!important}
[data-baseweb="select"]>div>ul>li:hover{background:#F1F5F9!important}
[data-baseweb="select"]>div>ul>li[aria-selected="true"]{background:#EFF6FF!important;color:#2563EB!important}
[data-baseweb="tag"]{background:#DBEAFE!important;border-radius:4px!important;color:#2563EB!important}
.form-sec{font-size:11px;font-weight:700;color:#2563EB!important;text-transform:uppercase;letter-spacing:.8px;margin-bottom:10px}
.hint{font-size:11px;color:#64748B!important;margin-top:-2px;margin-bottom:8px;font-weight:500}
.dataframe{border:1px solid #CBD5E1!important;border-radius:8px!important;overflow:hidden;background:#FFFFFF!important}
.dataframe th{background:#F8FAFC!important;color:#475569!important;font-size:10px!important;text-transform:uppercase;letter-spacing:.5px;font-weight:700!important;border-bottom:2px solid #0A0F1D!important;padding:10px 14px!important}
.dataframe td{color:#0A0F1D!important;font-size:12.5px!important;border-bottom:1px solid #F1F5F9!important;padding:9px 14px!important}
.dataframe tr:last-child td{border-bottom:none!important}
.dataframe tr:hover td{background:#F8FAFF!important}
.stInfo{background:#EFF6FF!important;border:1px solid #BFDBFE!important;color:#1E40AF!important;border-radius:8px!important}
.stWarning{background:#FFFBEB!important;border:1px solid #FDE68A!important;color:#92400E!important;border-radius:8px!important}
.stSuccess{background:#ECFDF5!important;border:1px solid #A7F3D0!important;color:#065F46!important;border-radius:8px!important}
.stError{background:#FEF2F2!important;border:1px solid #FECACA!important;color:#991B1B!important;border-radius:8px!important}
.login-card{background:#FFFFFF;border:2px solid #0A0F1D;border-radius:14px;padding:40px 36px;box-shadow:0 8px 40px rgba(0,0,0,.08)}
.login-icon{width:64px;height:64px;margin:0 auto 16px;background:linear-gradient(135deg,#0A0F1D,#1E293B);border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:28px;color:#FFFFFF;box-shadow:0 8px 24px rgba(0,0,0,.2)}
.login-logo-wrap{display:flex;justify-content:flex-start;margin-bottom:20px;flex-direction:row;align-items:center;gap:10px}
.login-logo-wrap img{border-radius:8px;max-width:140px;height:48px}
.login-header{text-align:center;margin-bottom:28px}
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
    except Exception:
        dp = pd.DataFrame(columns=COLS_P)
    try:
        r = supabase.table("tpl_inv_transactions").select(",".join(COLS_T)).execute()
        dt = pd.DataFrame(r.data) if r.data else pd.DataFrame(columns=COLS_T)
    except Exception:
        dt = pd.DataFrame(columns=COLS_T)
    return dp, dt

def get_stock(dt, pid):
    if dt.empty:
        return 0.0
    m = dt[dt["product_id"].eq(pid)
    up = pd.to_numeric(m[m["action_type"].eq("UPLOAD")]["quantity"], errors="coerce").fillna(0).sum()
    rt = pd.to_numeric(m[m["action_type"].eq("RETURN")]["quantity"], errors="coerce").fillna(0).sum()
    is_ = pd.to_numeric(m[m["action_type"].eq("ISSUE")]["quantity"], errors="coerce").fillna(0).sum()
    return float((up + rt) - is_)

def dot_cls(s, t):
    if t <= 0:
        return "dot-r"
    r = s / t
    if r > 0.5:
        return "dot-g"
    if r > 0.15:
        return "dot-y"
    return "dot-r"

def ind_dt(v):
    try:
        return pd.to_datetime(v).strftime("%d-%b-%Y %H:%M")
    except Exception:
        return str(v)

def to_csv(df):
    return df.to_csv(index=False).encode("utf-8")

def safe_num(v, d=0.0):
    try:
        return float(v)
    except Exception:
        return d

def explode_serials(df):
    if df.empty:
        return df
    rows = []
    for _, r in df.iterrows():
        s = str(r.get("serial_number", "")).strip()
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
# LOGIN — Logo left-aligned, NO credential code
# ==========================================
if not st.session_state["logged_in"]:
    _, mid, _ = st.columns([1.3, 1.4, 1.3])
    with mid:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<div class="login-logo-wrap">', unsafe_allow_html=True)
        if os.path.exists("assets/logo.png"):
            st.image("assets/logo.png", width=140)
        else:
            st.markdown('<div class="login-icon">📦</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="login-header">'
            '<div style="font-size:24px;font-weight:800;color:#0A0F1D;letter-spacing:-.5px">AssetFlow KCCL</div>'
            '<div style="font-size:13px;color:#475569;margin-top:4px">Inventory Control Portal</div>'
            '</div>',
            unsafe_allow_html=True
        )
        with st.form("lf", clear_on_submit=False):
            u = st.text_input("Username", placeholder="Enter username", label_visibility="collapsed")
            p = st.text_input("Password", type="password", placeholder="Enter password", label_visibility="collapsed")
            if st.form_submit_button("Authenticate Sign In", use_container_width=True, type="primary"):
                if u == "admin" and p == "kccl@2026":
                    st.session_state["logged_in"] = True
                    st.rerun()
                else:
                    st.error("Invalid credentials!")
        st.markdown('</div></div></div>', unsafe_allow_html=True)
    st.stop()

# ==========================================
# SIDEBAR — Logo left-aligned, Nav centered, Logout at bottom
# ==========================================
st.sidebar.markdown('<div class="sb-logo">', unsafe_allow_html=True)
if os.path.exists("assets/logo.png"):
    try:
        st.sidebar.image("assets/logo.png", width=110)
    else:
        st.sidebar.markdown('<div class="sb-fallback-icon">📦</div>', unsafe_allow_html=True)
st.sidebar.markdown(
    '<div class="sb-logo-name">AssetFlow</div>'
    '<div class="sb-logo-sub">KCCL Operations</div></div>',
    unsafe_allow_html=True
)

st.sidebar.markdown('<div class="sb-nav-label">Navigation</div>', unsafe_allow_html=True)
page = st.sidebar.radio("", ["Dashboard", "Transaction", "Reports"], label_visibility="collapsed")

# Logout at the very bottom — spacer + hr + button
st.sidebar.markdown('<div style="min-height:42vh"></div><hr style="border-color:#1E293B;margin:0">', unsafe_allow_html=True)
st.sidebar.markdown('<div style="padding:0 14px 16px">', unsafe_allow_html=True)
if st.sidebar.button("Logout Session", key="sb_logout", use_container_width=True):
    st.session_state["logged_in"] = False
    st.rerun()
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# LOAD DATA
# ==========================================
NOW = datetime.now()
DT_STR = NOW.strftime("%d%b%Y")
df_p, df_t = load_data()

# Product name map for exports
p_name_map = {}
if not df_p.empty:
    p_name_map = dict(zip(df_p["id"].tolist(), df_p["product_name"].tolist()))

# ==========================================
# DASHBOARD
# ==========================================
if page == "Dashboard":
    if df_p.empty:
        st.info("No master entries. Populate tpl_inv_products in backend.")
        st.stop()

    ts = 0.0
    for _, row in df_p.iterrows():
        ts += get_stock(df_t, row["id"])

    im = 0.0
    rm = 0.0
    if not df_t.empty:
        dft = df_t.copy()
        dft["created_at"] = pd.to_datetime(dft["created_at"], errors="coerce")
        m = dft.dropna(subset=["created_at"])
        mk = (m["created_at"].dt.month == NOW.month) & (m["created_at"].dt.year == NOW.year)
        im = safe_num(m[mk & (m["action_type"] == "ISSUE")]["quantity"].sum())
        rm = safe_num(m[mk & (m["action_type"] == "RETURN")]["quantity"].sum())

    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown(
            '<div class="stat-box"><div class="stat-lbl">Active Items</div>'
            '<div class="stat-val">' + str(len(df_p)) + '</div></div>',
            unsafe_allow_html=True
        )
    with s2:
        st.markdown(
            '<div class="stat-box"><div class="stat-lbl">Total Stock</div>'
            '<div class="stat-val">' + "{:,.1f}".format(ts) + '</div></div>',
            unsafe_allow_html=True
        )
    with s3:
        st.markdown(
            '<div class="stat-box"><div class="stat-lbl">Issued (Month)</div>'
            '<div class="stat-val">' + "{:,.1f}".format(im) + '</div></div>',
            unsafe_allow_html=True
        )
    with s4:
        st.markdown(
            '<div class="stat-box"><div class="stat-lbl">Returned (Month)</div>'
            '<div class="stat-val">' + "{:,.1f}".format(rm) + '</div></div>',
            unsafe_allow_html=True
        )

    st.markdown('<div class="sec-h">Live Inventory Distribution</div>', unsafe_allow_html=True)
    cards = st.columns(5)
    sum_rows = []

    idx = 0
    for _, row in df_p.iterrows():
        pid = row["id"]
        nm = row["product_name"]
        unit = row["default_unit"]

        # FIX: Calculate TOTAL UPLOAD COUNT instead of total_added_to_system
        total_uploads = 0.0
        if not df_t.empty:
            total_uploads = pd.to_numeric(
                df_t[(df_t["product_id"].eq(pid)) & (df_t["action_type"].eq("UPLOAD"))]["quantity"], 
                errors="coerce"
            ).fillna(0).sum()

        stk = get_stock(df_t, pid)
        dc = dot_cls(stk, total_uploads)
        stk_str = "{:.0f}".format(stk)
        total_int = str(int(total_uploads))

        sum_rows.append({
            "Product Name": nm,
            "In Stock": round(stk, 3),
            "Unit": unit,
            "Total Added": int(total_uploads)
        })

        card_html = (
            '<div class="p-card">'
            '<div class="p-top">'
            '<span class="dot ' + dc + '"></span>'
            '<div class="p-name">' + nm + '</div>'
            '</div>'
            '<div class="p-bottom">'
            '<div class="p-total">Total: ' + total_int + ' ' + unit + '</div>'
            '<div class="p-stock">' + stk_str + '</div>'
            '</div></div>'
        )

        with cards[idx % 5]:
            st.markdown(card_html, unsafe_allow_html=True)
        idx += 1

    df_sum = pd.DataFrame(sum_rows)

    st.markdown('<div class="sec-h">Data Extraction Hub</div>', unsafe_allow_html=True)
    d1, d2, d3 = st.columns(3)

    with d1:
        st.markdown('<p style="font-size:12px;font-weight:700;color:#0A0F1D;margin-bottom:6px">Full Ledger Audit Log</p>', unsafe_allow_html=True)
        if not df_t.empty:
            df_d = df_t.copy()
            df_d["product_name"] = df_d["product_id"].map(p_name_map).fillna("Unknown")
            df_d["created_at"] = df_d["created_at"].apply(ind_dt)
            df_d = explode_serials(df_d)
            ec = ["created_at", "product_name", "item_code", "serial_number", "quantity", "unit", "issued_to", "invoice_no", "action_type"]
            ec = [c for c in df_d.columns]
            st.download_button(
                "Download Full Dump CSV",
                data=to_csv(df_d[ec]),
                file_name="AssetFlow_FullDump_" + DT_STR + ".csv",
                mime="text/csv",
                key="d1"
            )

    with d2:
        st.markdown('<p style="font-size:12px;font-weight:700;color:#0A0F1D;margin-bottom:6px">System Balance Summary</p>', unsafe_allow_html=True)
        if not df_sum.empty:
            st.download_button(
                "Download Summary CSV",
                data=to_csv(df_sum),
                file_name="AssetFlow_Summary_" + DT_STR + ".csv",
                mime="text/csv",
                key="d2"
            )

    with d3:
        st.markdown('<p style="font-size:12px;font-weight:700;color:#0A0F1D;margin-bottom:6px">Targeted Asset Extraction</p>', unsafe_allow_html=True)
        sel = st.selectbox("Select Product", df_p["product_name"].tolist(), key="cs", label_visibility="collapsed")
        if sel:
            tid = df_p[df_p["product_name"].eq(sel)]["id"].values[0]
            df_is = df_t[(df_t["product_id"].eq(tid)) & (df_t["action_type"].eq("ISSUE"))].copy()
            if not df_is.empty:
                df_is["created_at"] = df_is["created_at"].apply(ind_dt)
                df_is["Product"] = sel
                df_is = explode_serials(df_is)
                ec = ["created_at", "Product", "item_code", "serial_number", "quantity", "unit", "issued_to", "invoice_no"]
                ec = [c for c in df_is.columns]
                safe_name = sel.lower().replace(" ", "_")
                st.download_button(
                    "Download " + sel + " Logs",
                    data=to_csv(df_is[ec]),
                    file_name="AssetFlow_" + safe_name + "_Issued_" + DT_STR + ".csv",
                    mime="text/csv",
                    key="d3"
                )
            else:
                st.markdown(
                    '<p style="font-size:11px;color:#DC2626;margin-top:4px;font-weight:600">No issue records.</p>',
                    unsafe_allow_html=True
                )

# ==========================================
# TRANSACTION
# ==========================================
elif page == "Transaction":
    if df_p.empty:
        st.warning("Add products to master catalog first.")
        st.stop()

    cl, cr = st.columns(2)

    with cl:
        st.markdown('<div class="form-sec">Asset Parameters</div>', unsafe_allow_html=True)
        sel_prod = st.selectbox("Product *", df_p["product_name"].tolist(), key="tp")
        item_code = st.text_input("Item Code *", placeholder="Comma-separated for bulk: IC-001, IC-002", key="tc")
        serial = st.text_area("Serial Number(s) *", placeholder="Comma-separated: SN-001, SN-002", height=60, key="ts")
        st.markdown(
            '<div class="hint">UPLOAD: comma = separate entries. ISSUE/RETURN: must match uploads.</div>',
            unsafe_allow_html=True
        )
        unit = st.selectbox("Unit *", UNITS, key="tu")
        qty = st.number_input("Quantity *", min_value=0.001, step=0.001, format="%.3f", key="tq")

    with cr:
        st.markdown('<div class="form-sec">Workflow Action</div>', unsafe_allow_html=True)
        action = st.selectbox("Action *", ["ISSUE", "RETURN", "UPLOAD"], key="ta")
        issued_to_label = "Issued To *" if action != "UPLOAD" else "Issued To"
        issued_to = st.text_input(issued_to_label, placeholder="Person or site name", key="ti")
        invoice = st.text_input("Invoice / DC No *", placeholder="e.g. INV-2025-042", key="tn")
        st.text_input("DateTime (Auto)", value=NOW.strftime("%d-%b-%Y  %H:%M:%S"), disabled=True, key="td")
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.button("Commit Transaction", use_container_width=True, type="primary")

    if submitted:
        errs = []
        if not item_code.strip():
            errs.append("Item Code is required.")
        if not serial.strip():
            errs.append("Serial Number is required.")
        if qty <= 0:
            errs.append("Quantity must be greater than zero.")
        if action != "UPLOAD" and not issued_to.strip():
            errs.append("Issued To is required for ISSUE/RETURN.")
        if not invoice.strip():
            errs.append("Invoice / DC No is required.")
        if errs:
            for e in errs:
                st.error(e)
            st.stop()

        pid = int(df_p[df_p["product_name"].eq(sel_prod)]["id"].values[0]

        if action == "UPLOAD":
            codes = [c.strip() for c in item_code.split(",") if c.strip()]
            serials = [s.strip() for s in serial.split(",") if s.strip()]
            if not codes:
                st.error("No valid Item Code.")
                st.stop()
            ok = 0
            for i, code in enumerate(codes):
                sn = serials[i] if i < len(serials) else ""
                payload = {
                    "product_id": pid,
                    "item_code": code,
                    "serial_number": sn,
                    "quantity": qty,
                    "unit": unit,
                    "issued_to": "",
                    "invoice_no": invoice.strip(),
                    "action_type": "UPLOAD",
                    "created_at": datetime.now().isoformat()
                }
                try:
                    res = supabase.table("tpl_inv_transactions").insert(payload).execute()
                    if res.data:
                        ok += 1
                except Exception as ex:
                    st.error("Failed for " + code + ": " + str(ex))
            if ok > 0:
                st.success("Uploaded " + str(ok) + " item(s) successfully!")
                load_data.clear()
                st.rerun()
        else:
            ic = item_code.strip()
            sn = serial.strip()
            if not df_t.empty:
                uploads = df_t[df_t["action_type"].eq("UPLOAD")]
                if ic not in uploads["item_code"].values:
                    st.error("Item Code '" + ic + "' not found in uploads!")
                    st.stop()
                if sn:
                    match = uploads[(uploads["item_code"].eq(ic)) & (uploads["serial_number"].eq(sn))]
                    if match.empty:
                        st.error("Serial '" + sn + "' not found for '" + ic + "'!")
                        st.stop()
            if action == "ISSUE":
                cs = get_stock(df_t, pid)
                if qty > cs:
                    st.error("Insufficient stock! Available: " + "{:.3f}".format(cs) + " " + unit)
                    st.stop()
            payload = {
                "product_id": pid,
                "item_code": ic,
                "serial_number": sn,
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
                    st.success("Committed: " + action + " " + "{:.3f}".format(qty) + " " + unit + " - " + ic)
                    load_data.clear()
                    st.rerun()
                else:
                    st.error("Insert failed. Check RLS.")
            except Exception as ex:
                st.error("DB Error: " + str(ex))

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

    st.markdown(
        '<div class="form-sec" style="margin-bottom:14px">Filter Criteria</div>',
        unsafe_allow_html=True
    )
    f1, f2, f3, f4, f5 = st.columns(5)
    with f1:
        df_ = st.date_input("From", value=mn, key="rf")
    with f2:
        dt_ = st.date_input("To", value=mx, key="rt")
    with f3:
        it_ = st.multiselect("Issued To", sorted(df_r["issued_to"].dropna().unique()), key="ri")
    with f4:
        im_ = st.multiselect("Item", sorted(df_p["product_name"].tolist()), key="rm")
    with f5:
        st_ = st.multiselect("Type", ["ISSUE", "RETURN", "UPLOAD"], key="rs")
    iv_ = st.multiselect("Invoice No", sorted(df_r["invoice_no"].dropna().unique()), key="rv")

    active = df_ != mn or dt_ != mx or it_ or im_ or st_ or iv_
    if not active:
        st.info("Select at least one filter to view data.")
        st.stop()

    df_f = df_r.copy()
    if df_ != mn:
        df_f = df_f[df_f["_d"] >= df_]
    if dt_ != mx:
        df_f = df_f[df_f["_d"] <= dt_]
    if it_:
        df_f = df_f[df_f["issued_to"].isin(it_)]
    if im_:
        df_f = df_f[df_f["product_name"].isin(im_)]
    if st_:
        df_f = df_f[df_f["action_type"].isin(st_)]
    if iv_:
        df_f = df_f[df_f["invoice_no"].isin(iv_)]

    r1, r2 = st.columns([2, 1])
    with r1:
        st.markdown(
            '<p style="font-size:13px;color:#0A0F1D;margin-top:10px;font-weight:700">'
            'Showing <span style="color:#2563EB">' + str(len(df_f)) + '</span> records</p>',
            unsafe_allow_html=True
        )
    with r2:
        if not df_f.empty:
            df_ex = df_f.copy()
            df_ex["created_at"] = df_ex["created_at"].apply(ind_dt)
            df_ex = explode_serials(df_ex)
            ec = ["created_at", "product_name", "item_code", "serial_number", "quantity", "unit", "issued_to", "invoice_no", "action_type"]
            ec = [c for c in df_ex.columns]
            st.download_button(
                "Export CSV",
                data=to_csv(df_ex[ec]),
                file_name="AssetFlow_Report_" + DT_STR + ".csv",
                mime="text/csv",
                key="dr"
            )

    if not df_f.empty:
        df_s = df_f.copy()
        df_s["created_at"] = df_s["created_at"].apply(ind_dt)
        df_s = explode_serials(df_s)
        ec = ["created_at", "product_name", "item_code", "serial_number", "quantity", "unit", "issued_to", "invoice_no", "action_type"]
        ec = [c for c in df_s.columns]
        df_s = df_s[ec].rename(columns={
            "created_at": "Date",
            "product_name": "Product",
            "item_code": "Code",
            "serial_number": "Serial",
            "quantity": "Qty",
            "unit": "Unit",
            "issued_to": "Issued To",
            "invoice_no": "Invoice",
            "action_type": "Action"
        })
        st.dataframe(df_s, use_container_width=True, hide_index=True, height=440)
    else:
        st.warning("No records match this filter.")

# ==========================================
# LOGOUT (TOP-RIGHT CORNER — KEEP FOR VISIBILITY
# ==========================================
# (NO sidebar logout — top-right corner)
st.markdown("""
<style>
.top-logout{
    position:fixed;top:16px;right:20px;z-index:200;
}
.top-logout button{background:#0A0F1D!important;border:1px solid #1E293B!important;color:#CBD5E1!important;border-radius:6px;padding:6px 16px!important;
font-size:12px;font-weight:600;cursor:pointer;transition:all .15s!important;display:inline-flex!important;gap:6px;align-items:center!important;
}
.top-logout:hover{border-color:#EF4444!important;color:#FFFFFF!important;background:#3B18181!important;box-shadow:0 4px 12px rgba(239,68,68,.15)!important}
</style>""", unsafe_allow_html=True)

# ==========================================
# REMOVE THE SIDEBAR LOGOUT (from sidebar) — so only top-right logout remains
# ==========================================
# The sidebar no longer has logout. Removed from sidebar code above.
# The sidebar only has nav + logo now.
</style>""", unsafe_allow_html=True)
