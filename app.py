import streamlit as st
import pandas as pd
from supabase import create_client, Client
import os
from datetime import datetime
import urllib.parse
import html
import uuid

# ==========================================
# SUPABASE CONFIGURATION
# ==========================================
SUPABASE_URL = "https://emdjnndnsdebhbzebrsg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVtZGpubmRuc2RlYmhiemVicnNnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODExNzU4NDYsImV4cCI6MjA5Njc1MTg0Nn0.ypy3k30Nbp2caJaNXpwxbrnUzrOLrhwTJ1FZwW5L8Fc"
ADMIN_USER = "admin"
ADMIN_PASS = "kccl@2026"

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error(f"Failed to connect to database: {e}")
    st.stop()

# ==========================================
# SECURE AUTHENTICATION (NO URL BYPASS)
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "auth" in st.query_params:
    st.query_params.clear()

def logout():
    st.session_state["logged_in"] = False
    st.query_params.clear()
    st.rerun()

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(page_title="AssetFlow KCCL", page_icon="📦", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# LOGIN PAGE
# ==========================================
if not st.session_state["logged_in"]:
    st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    section[data-testid='stSidebar']{display:none!important}
    header[data-testid='stHeader']{display:none!important}
    footer{visibility:hidden!important}
    #MainMenu{visibility:hidden!important}
    .stApp{background:#F8FAFC!important}
    .block-container{display:flex!important;flex-direction:column!important;justify-content:center!important;align-items:center!important;min-height:100vh!important;max-width:100%!important;padding:20px!important}
    .block-container > div[data-testid="stVerticalBlock"]{width:100%!important;max-width:440px!important}
    .login-card{background:#FFFFFF!important;border:1px solid #E2E8F0!important;border-radius:16px!important;padding:40px 35px!important;width:100%!important;box-shadow:0 20px 40px rgba(0,0,0,0.04)!important;text-align:center!important}
    .login-brand{font-size:32px!important;font-weight:800!important;color:#0F172A!important;margin-bottom:30px!important;font-family:'Inter',sans-serif!important;letter-spacing:-1px!important}
    .login-card label p{color:#475569!important;font-size:13px!important;font-weight:600!important;text-align:left!important;margin-bottom:4px!important}
    .login-card input{background:#F8FAFC!important;border:2px solid #E2E8F0!important;border-radius:10px!important;color:#0F172A!important;padding:12px 14px!important}
    .login-card input:focus{border-color:#3B82F6!important;box-shadow:0 0 0 3px rgba(59,130,246,0.1)!important}
    .login-card button{background:#0F172A!important;color:#FFFFFF!important;border:none!important;border-radius:10px!important;font-weight:600!important;padding:12px!important;margin-top:15px!important;transition:background .2s!important}
    .login-card button:hover{background:#1E293B!important}
    </style>""", unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 1.2, 1])
    with mid:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<div class="login-brand">KCCL Bangla</div>', unsafe_allow_html=True)
        with st.form("lf", clear_on_submit=False):
            u = st.text_input("Username", placeholder="Enter username")
            p = st.text_input("Password", type="password", placeholder="Enter password")
            if st.form_submit_button("Sign In", use_container_width=True):
                if u == ADMIN_USER and p == ADMIN_PASS:
                    st.session_state["logged_in"] = True
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please try again.")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ==========================================
# MAIN APP CSS (PROFESSIONAL UI)
# ==========================================
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.stApp{background:#F8FAFC!important;color:#0F172A!important;font-family:'Inter',system-ui,sans-serif!important}
.block-container{padding:1.5rem 2rem!important;max-width:1600px;margin:0 auto;position:relative;z-index:1}
header[data-testid="stHeader"]{visibility:hidden!important;height:0!important}
#MainMenu, footer{visibility:hidden!important}

/* SIDEBAR */
section[data-testid="stSidebar"]{background:#0F172A!important;border-right:1px solid #1E293B!important}
section[data-testid="stSidebar"] > div:first-child{display:flex!important;flex-direction:column!important;height:100vh!important;padding-top:20px!important}
.sb-header-title{font-size:18px!important;font-weight:700!important;color:#FFFFFF!important;text-align:center!important;padding:10px 10px 20px 10px!important;letter-spacing:-.5px!important;border-bottom:1px solid #1E293B!important;margin:0 15px 15px 15px!important}
section[data-testid="stSidebar"] section[data-testid="stRadio"] div[role="radiogroup"] > div{padding:12px 20px!important;border-left:4px solid transparent!important;margin:2px 0!important;border-radius:0 8px 8px 0!important}
section[data-testid="stSidebar"] section[data-testid="stRadio"] label p{color:#94A3B8!important;font-size:14px!important;font-weight:500!important}
section[data-testid="stSidebar"] section[data-testid="stRadio"] div[role="radiogroup"] > div:hover{background:#1E293B!important}
section[data-testid="stSidebar"] section[data-testid="stRadio"] div[role="radiogroup"] > div[aria-checked="true"]{background:#1E293B!important;border-left:4px solid #3B82F6!important}
section[data-testid="stSidebar"] section[data-testid="stRadio"] div[role="radiogroup"] > div[aria-checked="true"] label p{color:#FFFFFF!important;font-weight:700!important}
.sb-logout-box{margin-top:auto!important;padding:20px 20px 5px 20px!important}
.sb-logout-box button{background:transparent!important;color:#F87171!important;border:1px solid #B91C1C!important;border-radius:8px!important;padding:8px!important;font-weight:600!important;font-size:13px!important}
.sb-logout-box button:hover{background:#B91C1C!important;color:#FFFFFF!important}
.sb-watermark{text-align:center!important;color:#475569!important;font-size:11px!important;padding:10px 0 20px 0!important}

/* MAIN CONTENT */
.p-card{background:#FFFFFF!important;border:1px solid #E2E8F0!important;border-radius:12px!important;padding:18px 20px!important;display:flex!important;flex-direction:column!important;justify-content:space-between!important;height:110px!important;box-shadow:0 1px 3px rgba(0,0,0,0.05)!important;transition:all .2s ease!important}
.p-card:hover{border-color:#3B82F6!important;box-shadow:0 4px 12px rgba(59,130,246,0.1)!important;transform:translateY(-2px)!important}
.p-top{display:flex!important;align-items:center!important;gap:8px!important}
.p-name{font-size:13px;font-weight:600;color:#334155!important;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.p-bottom{display:flex!important;flex-direction:column!important;gap:2px!important;margin-top:8px!important}
.p-stock{font-size:26px;font-weight:800;color:#0F172A!important;line-height:1.1;text-decoration:none!important}
.p-total{font-size:11px;color:#94A3B8!important;font-weight:500}
.dot{display:inline-block;width:8px;height:8px;border-radius:50%;flex-shrink:0}
.dot-g{background:#10B981}.dot-y{background:#F59E0B}.dot-r{background:#EF4444}

.sec-h{font-size:18px!important;font-weight:700!important;color:#0F172A!important;margin:25px 0 15px!important;padding-bottom:10px!important;border-bottom:1px solid #E2E8F0!important}
label p,.stDateInput>label,.stTextArea>label,.stSelectbox>label,.stNumberInput>label{font-size:13px!important;font-weight:600!important;color:#475569!important;margin-bottom:5px!important}
.form-sec{font-size:12px!important;font-weight:700!important;color:#3B82F6!important;text-transform:uppercase!important;letter-spacing:.5px!important;margin-bottom:15px!important;display:block!important}
.hint{font-size:11px!important;color:#94A3B8!important;margin-top:-5px!important;margin-bottom:10px!important}
.stTextInput>div>div>input,.stSelectbox>div>div>select,.stTextArea>div>div>textarea,.stNumberInput>div>div>input,.stDateInput>div>div>input{background:#FFFFFF!important;border:1px solid #CBD5E1!important;border-radius:8px!important;color:#0F172A!important;font-size:14px!important;padding:8px 10px!important}
.stTextInput>div>div>input:focus,.stSelectbox>div>div>select:focus,.stTextArea>div>div>textarea:focus,.stNumberInput>div>div>input:focus{border-color:#3B82F6!important;box-shadow:0 0 0 2px rgba(59,130,246,0.1)!important}
.stButton>button[kind="primary"]{background:#3B82F6!important;color:#FFFFFF!important;border-radius:8px!important;font-weight:600!important;padding:10px 24px!important;border:none!important}
.stButton>button[kind="primary"]:hover{background:#2563EB!important}
.stDownloadButton>button{background:#F1F5F9!important;color:#334155!important;border:1px solid #CBD5E1!important;border-radius:8px!important;font-weight:600!important;width:100%!important}
.stDownloadButton>button:hover{background:#E2E8F0!important;color:#0F172A!important}
</style>""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================
st.sidebar.markdown('<div class="sb-header-title">KCCL Bangla</div>', unsafe_allow_html=True)
page = st.sidebar.radio("", ["Dashboard", "Transaction", "Reports"], label_visibility="collapsed")
with st.sidebar:
    st.markdown('<div class="sb-logout-box">', unsafe_allow_html=True)
    if st.button("Logout Session", key="sb_logout_btn", use_container_width=True):
        logout()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-watermark">Created by Anurag</div>', unsafe_allow_html=True)

# ==========================================
# CONFIG & DATA
# ==========================================
UNITS = ["PCS", "LTR", "ML", "MTR", "DRUM", "BOX", "KG", "GM", "SET", "PAIR", "ROLL", "CAN", "BOTTLE", "PACK", "SHEET", "BUNDLE", "TUBE", "GAL", "NOS", "KIT"]
COLS_P = ["id", "product_name", "item_code", "default_unit", "total_added_to_system"]
COLS_T = ["id", "product_id", "item_code", "serial_number", "quantity", "unit", "issued_to", "invoice_no", "action_type", "created_at"]

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
    if dt.empty: return 0.0
    m = dt[dt["product_id"].eq(pid)]
    up = pd.to_numeric(m[m["action_type"].eq("UPLOAD")]["quantity"], errors="coerce").fillna(0).sum()
    rt = pd.to_numeric(m[m["action_type"].eq("RETURN")]["quantity"], errors="coerce").fillna(0).sum()
    is_ = pd.to_numeric(m[m["action_type"].eq("ISSUE")]["quantity"], errors="coerce").fillna(0).sum()
    return float((up + rt) - is_)

def get_item_code_net_stock(dt, item_code, pid=None):
    if dt.empty or not item_code: return 0.0
    m = dt[dt["item_code"].eq(item_code)]
    if pid: m = m[m["product_id"].eq(pid)]
    up = pd.to_numeric(m[m["action_type"].eq("UPLOAD")]["quantity"], errors="coerce").fillna(0).sum()
    rt = pd.to_numeric(m[m["action_type"].eq("RETURN")]["quantity"], errors="coerce").fillna(0).sum()
    is_ = pd.to_numeric(m[m["action_type"].eq("ISSUE")]["quantity"], errors="coerce").fillna(0).sum()
    return float((up + rt) - is_)

def get_serial_net_issue(dt, item_code, serial):
    if dt.empty or not item_code or not serial: return 0.0
    m = dt[dt["item_code"].eq(item_code) & dt["serial_number"].eq(serial)]
    issues = pd.to_numeric(m[m["action_type"].eq("ISSUE")]["quantity"], errors="coerce").fillna(0).sum()
    returns = pd.to_numeric(m[m["action_type"].eq("RETURN")]["quantity"], errors="coerce").fillna(0).sum()
    return float(issues - returns)

def explode_serials(df):
    if df.empty: return df
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

def build_exact_stock_dump(dt, pid, unit):
    cols = ["Item Code", "Serial Number", "Available Balance", "Unit"]
    if dt.empty: return pd.DataFrame(columns=cols)
    m = dt[dt["product_id"].eq(pid)].copy()
    if m.empty: return pd.DataFrame(columns=cols)
    
    m["item_code"] = m["item_code"].fillna("").astype(str).str.strip()
    m["serial_number"] = m["serial_number"].fillna("").astype(str).str.strip()
    m["quantity"] = pd.to_numeric(m["quantity"], errors="coerce").fillna(0.0)
    m = explode_serials(m)
    
    m["_signed"] = (
        m["quantity"].where(m["action_type"].eq("UPLOAD"), 0.0) +
        m["quantity"].where(m["action_type"].eq("RETURN"), 0.0) -
        m["quantity"].where(m["action_type"].eq("ISSUE"), 0.0)
    )
    stock = m.groupby(["item_code", "serial_number"], dropna=False, as_index=False)["_signed"].sum().rename(columns={"_signed": "Available Balance"})
    stock = stock[stock["Available Balance"] > 0].copy()
    
    stock["Item Code"] = stock["item_code"].apply(lambda x: html.escape(str(x)) if x else "N/A")
    stock["Serial Number"] = stock["serial_number"].apply(lambda x: html.escape(str(x)) if x else "N/A")
    stock["Available Balance"] = stock["Available Balance"].round(3)
    stock["Unit"] = unit
    return stock[cols]

def dot_cls(s, t):
    if t <= 0: return "dot-r"
    r = s / t
    if r > 0.5: return "dot-g"
    if r > 0.15: return "dot-y"
    return "dot-r"

def ind_dt(v):
    try: return pd.to_datetime(v).strftime("%d-%b-%Y %H:%M")
    except Exception: return str(v)

def to_csv(df):
    return df.to_csv(index=False).encode("utf-8")

# ==========================================
# ROUTER & DATA FETCH
# ==========================================
NOW = datetime.now()
DT_STR = NOW.strftime("%d%b%Y")
df_p, df_t = load_data()

p_name_map = {}
if not df_p.empty:
    p_name_map = dict(zip(df_p["id"].tolist(), df_p["product_name"].tolist()))

if not df_p.empty:
    df_p["display_name"] = df_p["product_name"] + " [" + df_p["item_code"].fillna("N/A") + "]"

# ==========================================
# DASHBOARD
# ==========================================
if page == "Dashboard":
    if df_p.empty:
        st.info("No master entries found.")
        st.stop()

    st.markdown('<div class="sec-h">Live Inventory Distribution</div>', unsafe_allow_html=True)
    cards = st.columns(5)
    sum_rows = []

    for idx, row in df_p.iterrows():
        pid = row["id"]
        nm = html.escape(str(row["product_name"]))
        unit = row["default_unit"]

        total_uploads = 0.0
        if not df_t.empty:
            total_uploads = pd.to_numeric(
                df_t[(df_t["product_id"].eq(pid)) & (df_t["action_type"].eq("UPLOAD"))]["quantity"],
                errors="coerce"
            ).fillna(0).sum()

        df_stock_dump = build_exact_stock_dump(df_t, pid, unit)
        stk = float(df_stock_dump["Available Balance"].sum()) if not df_stock_dump.empty else 0.0

        dc = dot_cls(stk, total_uploads)
        stk_str = "{:.0f}".format(stk)
        total_int = str(int(total_uploads))

        sum_rows.append({"Product Name": nm, "In Stock": round(stk, 3), "Unit": unit, "Total Added": int(total_uploads)})

        csv_payload = df_stock_dump.to_csv(index=False)
        b64_csv = urllib.parse.quote(csv_payload)
        dl_href = f"data:text/csv;charset=utf-8,{b64_csv}"
        filename = f"StockDump_{nm.lower().replace(' ', '_')}_{DT_STR}.csv"

        card_html = (
            f'<div class="p-card"><div class="p-top">'
            f'<span class="dot {dc}"></span>'
            f'<div class="p-name">{nm}</div></div>'
            f'<div class="p-bottom">'
            f'<div style="display:flex; align-items:baseline; gap:5px;">'
            f'<a class="p-stock" href="{dl_href}" download="{filename}" title="Click to download exact In Stock details">{stk_str}</a>'
            f'<span style="font-size:13px;font-weight:500;color:#94A3B8;">In Stock</span>'
            f'</div>'
            f'<div class="p-total">Added: {total_int} {unit}</div>'
            f'</div></div>'
        )
        with cards[idx % 5]:
            st.markdown(card_html, unsafe_allow_html=True)

    st.markdown('<div class="sec-h">Data Extraction Hub</div>', unsafe_allow_html=True)
    d1, d2, d3 = st.columns(3)

    with d1:
        st.markdown('<p style="font-size:13px;font-weight:600;color:#475569;margin-bottom:8px">Full Ledger Audit Log</p>', unsafe_allow_html=True)
        if not df_t.empty:
            df_d = df_t.copy()
            df_d["product_name"] = df_d["product_id"].map(p_name_map).fillna("Unknown")
            df_d["created_at"] = df_d["created_at"].apply(ind_dt)
            df_d = explode_serials(df_d)
            ec = [c for c in ["created_at", "product_name", "item_code", "serial_number", "quantity", "unit", "issued_to", "invoice_no", "action_type"] if c in df_d.columns]
            st.download_button("Download Full Dump CSV", data=to_csv(df_d[ec]), file_name="AssetFlow_FullDump_" + DT_STR + ".csv", mime="text/csv", key="d1")

    with d2:
        st.markdown('<p style="font-size:13px;font-weight:600;color:#475569;margin-bottom:8px">System Balance Summary</p>', unsafe_allow_html=True)
        if sum_rows:
            st.download_button("Download Summary CSV", data=to_csv(pd.DataFrame(sum_rows)), file_name="AssetFlow_Summary_" + DT_STR + ".csv", mime="text/csv", key="d2")

    with d3:
        st.markdown('<p style="font-size:13px;font-weight:600;color:#475569;margin-bottom:8px">Targeted Asset Extraction</p>', unsafe_allow_html=True)
        sel = st.selectbox("Select Product", df_p["display_name"].tolist(), key="cs", label_visibility="collapsed")
        if sel:
            actual_nm = sel.split(" [")[0]
            tid = df_p[df_p["product_name"].eq(actual_nm)]["id"].values[0]
            df_is = df_t[(df_t["product_id"].eq(tid)) & (df_t["action_type"].eq("ISSUE"))].copy()
            if not df_is.empty:
                df_is["created_at"] = df_is["created_at"].apply(ind_dt)
                df_is["Product"] = actual_nm
                df_is = explode_serials(df_is)
                ec = [c for c in ["created_at", "Product", "item_code", "serial_number", "quantity", "unit", "issued_to", "invoice_no"] if c in df_is.columns]
                st.download_button("Download " + actual_nm + " Logs", data=to_csv(df_is[ec]), file_name="AssetFlow_" + actual_nm.lower().replace(" ", "_") + "_Issued_" + DT_STR + ".csv", mime="text/csv", key="d3")
            else:
                st.markdown('<p style="font-size:12px;color:#EF4444;margin-top:4px;font-weight:500">No issue records found.</p>', unsafe_allow_html=True)


# ==========================================
# TRANSACTION
# ==========================================
elif page == "Transaction":
    if df_p.empty:
        st.warning("Add products to master catalog first.")
        st.stop()

    if "txn_processing" not in st.session_state:
        st.session_state.txn_processing = False

    cl, cr = st.columns(2)
    with cl:
        st.markdown('<div class="form-sec">Asset Parameters</div>', unsafe_allow_html=True)
        sel_prod_disp = st.selectbox("Product *", df_p["display_name"].tolist(), key="tp")
        sel_prod = sel_prod_disp.split(" [")[0]
        
        item_code = st.text_input("Item Code *", placeholder="Single item code (e.g., IC-001)", key="tc")
        serial = st.text_area("Serial Number(s)", placeholder="Mandatory for ISSUE/RETURN. Comma-separated for bulk UPLOAD.", height=60, key="ts")
        st.markdown('<div class="hint">UPLOAD: comma-separated serials = each gets its own row. Quantity is auto-divided equally.</div>', unsafe_allow_html=True)
        
        unit = st.selectbox("Unit *", UNITS, key="tu")
        qty = st.number_input("Total Quantity *", min_value=0.001, step=0.001, format="%.3f", key="tq")

    with cr:
        st.markdown('<div class="form-sec">Workflow Action</div>', unsafe_allow_html=True)
        action = st.selectbox("Action *", ["ISSUE", "RETURN", "UPLOAD"], key="ta")
        issued_to_label = "Issued To *" if action != "UPLOAD" else "Issued To"
        issued_to = st.text_input(issued_to_label, placeholder="Person or site name", key="ti")
        invoice = st.text_input("Invoice / DC No *", placeholder="e.g. DC-42", key="tn")
        st.text_input("DateTime (Auto)", value=NOW.strftime("%d-%b-%Y  %H:%M:%S"), disabled=True, key="td")
        st.markdown("<br>", unsafe_allow_html=True)
        
        button_label = "Processing..." if st.session_state.txn_processing else "Commit Transaction"
        submitted = st.button(button_label, use_container_width=True, type="primary", disabled=st.session_state.txn_processing)

    if submitted:
        errs = []
        ic_clean = item_code.strip()
        sn_clean = serial.strip()
        
        if not ic_clean: errs.append("Item Code is required.")
        if qty <= 0: errs.append("Quantity must be greater than zero.")
        if action != "UPLOAD" and not issued_to.strip(): errs.append("Issued To is required for ISSUE / RETURN.")
        if not invoice.strip(): errs.append("Invoice / DC No is required.")
        if action in ["ISSUE", "RETURN"] and not sn_clean:
            errs.append("Serial Number is mandatory for ISSUE and RETURN actions.")
            
        if errs:
            for e in errs: st.error(e)
            st.stop()

        prod_row = df_p[df_p["product_name"].eq(sel_prod)].iloc[0]
        pid = int(prod_row["id"])
        st.session_state.txn_processing = True

        if action == "UPLOAD":
            codes = [c.strip() for c in ic_clean.split(",") if c.strip()]
            serials = [s.strip() for s in sn_clean.split(",") if s.strip()] if sn_clean else []
            
            if serials and len(codes) != len(serials):
                st.error(f"Mismatch error: You provided {len(codes)} Item Code(s) but {len(serials)} Serial Number(s). They must match exactly.")
                st.session_state.txn_processing = False
                st.stop()
            
            num_entries = max(len(codes), len(serials)) if serials else len(codes)
            per_qty = round(qty / num_entries, 3)
            distributed = per_qty * (num_entries - 1)
            last_qty = round(qty - distributed, 3)

            ok = 0
            txn_ref = str(uuid.uuid4())
            for i in range(num_entries):
                code = codes[i] if i < len(codes) else codes[-1]
                sn = serials[i] if i < len(serials) else ""
                entry_qty = last_qty if i == num_entries - 1 else per_qty
                
                payload = {
                    "product_id": pid, "item_code": code, "serial_number": sn,
                    "quantity": entry_qty, "unit": unit, "issued_to": "",
                    "invoice_no": invoice.strip(), "action_type": "UPLOAD",
                    "created_at": datetime.now().isoformat(),
                    "transaction_ref": txn_ref
                }
                try:
                    res = supabase.table("tpl_inv_transactions").insert(payload).execute()
                    if res.data: ok += 1
                except Exception as ex:
                    st.error("Failed for " + code + ": " + str(ex))
            
            if ok > 0:
                st.toast("Batch Upload Committed Successfully!", icon="📥")
                st.success(f"Uploaded {ok} item(s) — {per_qty:.3f} {unit} each (total {qty:.3f})")
                st.session_state.txn_processing = False
                st.rerun()

        elif action == "ISSUE":
            _, df_t_latest = load_data()
            
            valid_match = df_t_latest[(df_t_latest["item_code"].eq(ic_clean)) & (df_t_latest["product_id"].eq(pid))]
            if valid_match.empty:
                st.error(f"Item Code '{ic_clean}' does not belong to '{sel_prod}'. Cross-check failed.")
                st.session_state.txn_processing = False
                st.stop()
                
            match = valid_match[valid_match["serial_number"].eq(sn_clean)]
            if match.empty:
                st.error(f"Serial '{sn_clean}' not found in uploads for '{ic_clean}'!")
                st.session_state.txn_processing = False
                st.stop()
                
            sn_uploaded_qty = pd.to_numeric(match["quantity"], errors="coerce").fillna(0).sum()
            m_history = df_t_latest[df_t_latest["item_code"].eq(ic_clean) & df_t_latest["serial_number"].eq(sn_clean)]
            sn_issued_qty = pd.to_numeric(m_history[m_history["action_type"].eq("ISSUE")]["quantity"], errors="coerce").fillna(0).sum()
            sn_returned_qty = pd.to_numeric(m_history[m_history["action_type"].eq("RETURN")]["quantity"], errors="coerce").fillna(0).sum()
            sn_available_balance = (sn_uploaded_qty + sn_returned_qty) - sn_issued_qty
            
            if qty > sn_available_balance:
                st.error(f"Insufficient stock for Serial '{sn_clean}'! Available Balance: {sn_available_balance:.3f} {unit}")
                st.session_state.txn_processing = False
                st.stop()

            payload = {
                "product_id": pid, "item_code": ic_clean, "serial_number": sn_clean,
                "quantity": qty, "unit": unit, "issued_to": issued_to.strip(),
                "invoice_no": invoice.strip(), "action_type": "ISSUE",
                "created_at": datetime.now().isoformat(),
                "transaction_ref": str(uuid.uuid4())
            }
            try:
                res = supabase.table("tpl_inv_transactions").insert(payload).execute()
                if res.data:
                    st.toast("Asset Issued Successfully!", icon="📤")
                    st.success(f"Issued: {qty:.3f} {unit} — {ic_clean} / {sn_clean}")
                    st.session_state.txn_processing = False
                    st.rerun()
            except Exception as ex:
                st.error("DB Error: " + str(ex))
                st.session_state.txn_processing = False

        elif action == "RETURN":
            _, df_t_latest = load_data()
            
            net_issued = get_serial_net_issue(df_t_latest, ic_clean, sn_clean)
            if net_issued <= 0:
                st.error(f"Serial '{sn_clean}' has NOT been issued or already returned! Cannot return.")
                st.session_state.txn_processing = False
                st.stop()
                
            if qty > net_issued:
                st.error(f"Cannot return {qty} {unit}. Only {net_issued:.3f} {unit} are currently issued for this serial.")
                st.session_state.txn_processing = False
                st.stop()

            payload = {
                "product_id": pid, "item_code": ic_clean, "serial_number": sn_clean,
                "quantity": qty, "unit": unit, "issued_to": issued_to.strip(),
                "invoice_no": invoice.strip(), "action_type": "RETURN",
                "created_at": datetime.now().isoformat(),
                "transaction_ref": str(uuid.uuid4())
            }
            try:
                res = supabase.table("tpl_inv_transactions").insert(payload).execute()
                if res.data:
                    st.toast("Asset Return Logged!", icon="📥")
                    st.success(f"Returned: {qty:.3f} {unit} — {ic_clean} / {sn_clean}")
                    st.session_state.txn_processing = False
                    st.rerun()
            except Exception as ex:
                st.error("DB Error: " + str(ex))
                st.session_state.txn_processing = False


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

    st.markdown('<div class="form-sec" style="margin-bottom:15px">Filter Criteria</div>', unsafe_allow_html=True)
    f1, f2, f3, f4, f5 = st.columns(5)
    with f1: df_ = st.date_input("From", value=mn, key="rf")
    with f2: dt_ = st.date_input("To", value=mx, key="rt")
    with f3: it_ = st.multiselect("Issued To", sorted(df_r["issued_to"].dropna().unique()), key="ri")
    with f4: im_ = st.multiselect("Item", sorted(df_p["display_name"].unique()), key="rm")
    with f5: st_ = st.multiselect("Type", ["ISSUE", "RETURN", "UPLOAD"], key="rs")
    iv_ = st.multiselect("Invoice No", sorted(df_r["invoice_no"].dropna().unique()), key="rv")

    df_f = df_r.copy()
    if df_ != mn: df_f = df_f[df_f["_d"] >= df_]
    if dt_ != mx: df_f = df_f[df_f["_d"] <= dt_]
    if it_: df_f = df_f[df_f["issued_to"].isin(it_)]
    if im_:
        actual_names = [x.split(" [")[0] for x in im_]
        df_f = df_f[df_f["product_name"].isin(actual_names)]
    if st_: df_f = df_f[df_f["action_type"].isin(st_)]
    if iv_: df_f = df_f[df_f["invoice_no"].isin(iv_)]

    r1, r2 = st.columns([2, 1])
    with r1:
        st.markdown(f'<p style="font-size:14px;margin-top:10px;font-weight:500;color:#475569">Showing <span style="color:#3B82F6;font-weight:700">{len(df_f)}</span> records</p>', unsafe_allow_html=True)
    with r2:
        if not df_f.empty:
            df_ex = df_f.copy()
            df_ex["created_at"] = df_ex["created_at"].apply(ind_dt)
            df_ex = explode_serials(df_ex)
            ec = [c for c in ["created_at", "product_name", "item_code", "serial_number", "quantity", "unit", "issued_to", "invoice_no", "action_type"] if c in df_ex.columns]
            st.download_button("Export Filtered Logs", data=to_csv(df_ex[ec]), file_name="AssetFlow_Report_" + DT_STR + ".csv", mime="text/csv", key="dr")

    if not df_f.empty:
        df_s = df_f.copy()
        df_s["created_at"] = df_s["created_at"].apply(ind_dt)
        df_s = explode_serials(df_s)
        ec = [c for c in ["created_at", "product_name", "item_code", "serial_number", "quantity", "unit", "issued_to", "invoice_no", "action_type"] if c in df_s.columns]
        df_s = df_s[ec].rename(columns={
            "created_at": "Date", "product_name": "Product", "item_code": "Code",
            "serial_number": "Serial", "quantity": "Qty", "unit": "Unit",
            "issued_to": "Issued To", "invoice_no": "Invoice", "action_type": "Action"
        })
        st.dataframe(df_s, use_container_width=True, hide_index=True, height=450)
    else:
        st.warning("No records match this filter.")
