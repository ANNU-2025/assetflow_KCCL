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
# SOBER PROFESSIONAL CSS
# Colors: #F2F0EF bg, #4B6E48 primary, #B2AC88 accent, #898989 gray
# ==========================================
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.block-container{padding-top:1.5rem;padding-bottom:2rem;max-width:1360px}
.stApp{background:#F2F0EF;color:#2D2D2D;font-family:'Inter',sans-serif}
section[data-testid="stSidebar"]{background:#FFFFFF;border-right:1px solid #E0DDD9}
section[data-testid="stSidebar"] .stMarkdown{color:#2D2D2D}
#MainMenu{visibility:hidden}footer{visibility:hidden}
header[data-testid="stHeader"]{background:#FFFFFF;border-bottom:1px solid #E0DDD9}

/* Stat Cards */
.stat-box{background:#FFFFFF;border:1px solid #E0DDD9;border-radius:10px;padding:16px 18px;box-shadow:0 1px 3px rgba(0,0,0,.04)}
.stat-lbl{font-size:11px;color:#898989;text-transform:uppercase;letter-spacing:.8px;font-weight:600;margin-bottom:4px}
.stat-val{font-size:24px;font-weight:800;color:#2D2D2D;line-height:1.1}

/* Product Cards — Compact */
.p-card{background:#FFFFFF;border:1px solid #E0DDD9;border-radius:10px;padding:14px 16px;transition:all .2s;box-shadow:0 1px 3px rgba(0,0,0,.03)}
.p-card:hover{border-color:#B2AC88;box-shadow:0 4px 12px rgba(178,172,136,.15);transform:translateY(-1px)}
.p-name{font-size:13px;font-weight:700;color:#2D2D2D;margin-bottom:1px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.p-code{font-size:10px;color:#898989;font-family:'Courier New',monospace;margin-bottom:8px;letter-spacing:.3px}
.p-stock{font-size:20px;font-weight:800;color:#4B6E48;font-family:'Inter',sans-serif;line-height:1}
.p-div{height:1px;background:#E0DDD9;margin:8px 0}
.p-total{font-size:10px;color:#898989}
.p-total b{color:#5A5A5A}
.dot{display:inline-block;width:6px;height:6px;border-radius:50%;margin-right:5px;vertical-align:middle}
.dot-g{background:#4B6E48}
.dot-y{background:#B2AC88}
.dot-r{background:#C0392B}

/* Section Head */
.sec-h{font-size:13px;font-weight:700;color:#4B6E48;text-transform:uppercase;letter-spacing:.8px;margin-bottom:10px;padding-bottom:6px;border-bottom:2px solid #B2AC88}

/* Tables */
.dataframe{border:1px solid #E0DDD9!important;border-radius:8px!important;overflow:hidden}
.dataframe th{background:#FFFFFF!important;color:#898989!important;font-size:10px!important;text-transform:uppercase;letter-spacing:.6px;font-weight:700!important;border-bottom:2px solid #E0DDD9!important;padding:10px 12px!important}
.dataframe td{color:#2D2D2D!important;font-size:12px!important;border-bottom:1px solid #F2F0EF!important;padding:9px 12px!important}
.dataframe tr:last-child td{border-bottom:none!important}
.dataframe tr:hover td{background:#FAF9F8!important}

/* Badges */
.badge{display:inline-block;padding:2px 10px;border-radius:12px;font-size:10px;font-weight:700;letter-spacing:.3px}
.b-i{background:#FDF2E9;color:#B2AC88}
.b-r{background:#EAF4EA;color:#4B6E48}
.b-u{background:#EBF0EB;color:#6B8E6B}

/* Form Inputs */
.stTextInput>div>div>input,.stSelectbox>div>div>select,.stNumberInput>div>div>input,.stTextArea>div>div>textarea{background:#FFFFFF!important;color:#2D2D2D!important;border:1px solid #D5D2CD!important;border-radius:8px!important;font-size:13px!important}
.stTextInput>div>div>input:focus,.stSelectbox>div>div>select:focus,.stNumberInput>div>div>input:focus{border-color:#4B6E48!important;box-shadow:0 0 0 3px rgba(75,110,72,.08)!important}
.stTextArea>div>div>textarea{font-family:'Courier New',monospace!important;font-size:12px!important}

/* Buttons */
.stDownloadButton>button{background:#FFFFFF!important;border:1px solid #D5D2CD!important;color:#4B6E48!important;border-radius:8px!important;font-weight:600!important;font-size:12px!important}
.stDownloadButton>button:hover{border-color:#4B6E48!important;background:#F7F6F4!important}
.stButton>button[kind="primary"]{background:#4B6E48!important;color:#FFFFFF!important;border:none!important;border-radius:8px!important;font-weight:700!important;font-size:13px!important}
.stButton>button[kind="primary"]:hover{background:#3D5C3A!important;box-shadow:0 4px 12px rgba(75,110,72,.2)!important}
.stButton>button[kind="secondary"]{background:#FFFFFF!important;border:1px solid #D5D2CD!important;color:#2D2D2D!important;border-radius:8px!important}
.stButton>button[kind="secondary"]:hover{border-color:#B2AC88!important}

/* Scrollable Dropdown */
[data-baseweb="select"]>div>ul{max-height:260px!important;overflow-y:auto!important;border-radius:8px!important;border:1px solid #E0DDD9!important;box-shadow:0 8px 24px rgba(0,0,0,.08)!important}
[data-baseweb="select"]>div>ul>li{font-size:13px!important;padding:8px 12px!important}
[data-baseweb="select"]>div>ul>li:hover{background:#F2F0EF!important}

/* Form Section Labels */
.form-sec{font-size:11px;font-weight:700;color:#4B6E48;text-transform:uppercase;letter-spacing:.6px;margin-bottom:10px}

/* Sidebar Nav */
.nav-label{font-size:10px;color:#898989;text-transform:uppercase;letter-spacing:1px;font-weight:700;margin-bottom:6px}
</style>""", unsafe_allow_html=True)

# ==========================================
# LOGO
# ==========================================
if os.path.exists("assets/logo.png"):
    st.sidebar.image("assets/logo.png", width=120)
else:
    st.sidebar.markdown('<div style="text-align:center;margin-bottom:4px"><div style="width:40px;height:40px;margin:0 auto 6px;background:#F2F0EF;border:1.5px solid #B2AC88;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:18px">📦</div><span style="font-size:16px;font-weight:800;color:#2D2D2D;letter-spacing:-.3px">AssetFlow</span><br><span style="font-size:9px;color:#898989;letter-spacing:.5px">KCCL INVENTORY</span></div>', unsafe_allow_html=True)
st.sidebar.markdown("---")

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

def dot_cls(stock, total):
    if total <= 0: return "dot-r"
    r = stock / total
    return "dot-g" if r > .5 else "dot-y" if r > .15 else "dot-r"

def ind_dt(v):
    try: return pd.to_datetime(v).strftime("%d-%b-%Y %H:%M")
    except: return str(v)

def ind_date(v):
    try: return pd.to_datetime(v).strftime("%d-%b-%Y")
    except: return str(v)

def badge(a):
    c = {"ISSUE":"b-i","RETURN":"b-r","UPLOAD":"b-u"}.get(a,"b-i")
    return f'<span class="badge {c}">{a}</span>'

def to_csv(df):
    return df.to_csv(index=False).encode("utf-8")

def safe_num(v, d=0.0):
    try: return float(v)
    except: return d

def explode_serials(df):
    """Comma-separated serial numbers কে আলাদা row-তে ভাঙা"""
    if df.empty: return df
    rows = []
    for _, r in df.iterrows():
        serials = str(r.get("serial_number", "")).strip()
        if serials and serials != "":
            parts = [s.strip() for s in serials.split(",") if s.strip()]
            if len(parts) > 1:
                for s in parts:
                    nr = r.copy()
                    nr["serial_number"] = s
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
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, login_box, _ = st.columns([1, 1.2, 1])
    with login_box:
        st.markdown('<div style="background:#FFFFFF;border:1px solid #E0DDD9;border-radius:14px;padding:32px 28px;box-shadow:0 4px 20px rgba(0,0,0,.06)"><div style="text-align:center;margin-bottom:20px"><div style="width:48px;height:48px;margin:0 auto 10px;background:#F2F0EF;border:1.5px solid #B2AC88;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:20px">📦</div><span style="font-size:20px;font-weight:800;color:#2D2D2D">AssetFlow KCCL</span><br><span style="font-size:11px;color:#898989">Inventory Management System</span></div></div>', unsafe_allow_html=True)
        with st.form("lf"):
            u = st.text_input("Username", placeholder="Enter username")
            p = st.text_input("Password", type="password", placeholder="Enter password")
            if st.form_submit_button("Sign In", use_container_width=True):
                if u == "admin" and p == "kccl@2026":
                    st.session_state["logged_in"] = True
                    st.rerun()
                else:
                    st.error("Invalid credentials!")
        st.caption("Template: `admin` / `kccl@2026`")
    st.stop()

if st.sidebar.button("🔓 Logout", use_container_width=True):
    st.session_state["logged_in"] = False
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown('<div class="nav-label">Navigation</div>', unsafe_allow_html=True)
page = st.sidebar.radio("", ["Dashboard", "Transaction", "Reports"], label_visibility="collapsed")

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
    st.caption("Inventory overview at a glance")

    if df_p.empty:
        st.info("No products found. Add via Supabase SQL Editor.")
        st.stop()

    # Stats Row
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
        st.markdown(f'<div class="stat-box"><div class="stat-lbl">Products</div><div class="stat-val">{len(df_p)}</div></div>', unsafe_allow_html=True)
    with s2:
        st.markdown(f'<div class="stat-box"><div class="stat-lbl">In Stock</div><div class="stat-val">{ts:,.1f}</div></div>', unsafe_allow_html=True)
    with s3:
        st.markdown(f'<div class="stat-box"><div class="stat-lbl">Issued (Month)</div><div class="stat-val">{im:,.1f}</div></div>', unsafe_allow_html=True)
    with s4:
        st.markdown(f'<div class="stat-box"><div class="stat-lbl">Returned (Month)</div><div class="stat-val">{rm:,.1f}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Product Cards — Compact
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
            st.markdown(
                f'<div class="p-card">'
                f'<div style="display:flex;align-items:center;gap:4px;margin-bottom:1px">'
                f'<span class="dot {dc}"></span>'
                f'<div class="p-name">{nm}</div>'
                f'</div>'
                f'<div class="p-code">{code}</div>'
                f'<div class="p-stock">{stk:.2f}</div>'
                f'<div class="p-div"></div>'
                f'<div class="p-total">Total: <b>{int(total)} {unit}</b></div>'
                f'</div>',
                unsafe_allow_html=True
            )

    df_sum = pd.DataFrame(sum_rows)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-h">Export Data</div>', unsafe_allow_html=True)

    d1, d2, d3 = st.columns(3)

    with d1:
        st.markdown("**Full Dump**")
        st.caption("All transactions")
        if not df_t.empty:
            df_dump = df_t.copy()
            df_dump["created_at"] = df_dump["created_at"].apply(ind_dt)
            df_dump = explode_serials(df_dump)
            st.download_button("📥 Download CSV", data=to_csv(df_dump), file_name=f"AssetFlow_FullDump_{DT_STR}.csv", mime="text/csv", key="d1")

    with d2:
        st.markdown("**Product Summary**")
        st.caption("Stock + total count")
        if not df_sum.empty:
            st.download_button("📥 Download CSV", data=to_csv(df_sum), file_name=f"AssetFlow_Summary_{DT_STR}.csv", mime="text/csv", key="d2")

    with d3:
        st.markdown("**Issued Details**")
        st.caption("Per-product issue log")
        sel = st.selectbox("Select", df_p["product_name"].tolist(), key="cs", label_visibility="collapsed")
        if sel:
            tid = df_p[df_p["product_name"]==sel]["id"].values[0]
            df_is = df_t[(df_t["product_id"]==tid) & (df_t["action_type"]=="ISSUE")].copy()
            if not df_is.empty:
                df_is["created_at"] = df_is["created_at"].apply(ind_dt)
                df_is["Product"] = sel
                df_is = explode_serials(df_is)
                ec = [c for c in ["created_at","Product","item_code","serial_number","quantity","unit","issued_to","invoice_no"] if c in df_is.columns]
                safe_name = sel.lower().replace(" ","_")
                st.download_button("📥 Download CSV", data=to_csv(df_is[ec]), file_name=f"AssetFlow_{safe_name}_Issued_{DT_STR}.csv", mime="text/csv", key="d3")
            else:
                st.caption("No records.")

# ==========================================
# TRANSACTION
# ==========================================
elif page == "Transaction":
    st.header("New Transaction")
    st.caption("Issue, return or upload inventory items")

    if df_p.empty:
        st.warning("Add products first.")
        st.stop()

    # Form container
    st.markdown('<div style="background:#FFFFFF;border:1px solid #E0DDD9;border-radius:12px;padding:24px;box-shadow:0 1px 4px rgba(0,0,0,.04)">', unsafe_allow_html=True)

    cl, cr = st.columns(2)

    with cl:
        st.markdown('<div class="form-sec">Product Details</div>', unsafe_allow_html=True)
        sel_prod = st.selectbox("Product *", df_p["product_name"].tolist(), key="tp")
        item_code = st.text_input("Item Code *", placeholder="e.g. RJ-001", key="tc")
        serial = st.text_area("Serial Number(s)", placeholder="Comma-separated: SN-001, SN-002, SN-003", height=55, key="ts")
        st.caption("Each serial will appear as a separate row in reports.", icon="ℹ️")
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
    st.caption("Filter and export transaction data")

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

    # Filter bar — clean white card
    st.markdown('<div style="background:#FFFFFF;border:1px solid #E0DDD9;border-radius:12px;padding:20px;box-shadow:0 1px 4px rgba(0,0,0,.04)">', unsafe_allow_html=True)
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

    # Results bar
    r1, r2 = st.columns([1, 1])
    with r1:
        st.markdown(f'<span style="font-size:13px;color:#898989">Showing </span><span style="font-size:13px;font-weight:700;color:#4B6E48">{len(df_f)}</span><span style="font-size:13px;color:#898989"> records</span>', unsafe_allow_html=True)
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
        df_s = df_s[ec].rename(columns={
            "created_at":"Date","product_name":"Product","item_code":"Code",
            "serial_number":"Serial","quantity":"Qty","unit":"Unit",
            "issued_to":"Issued To","invoice_no":"Invoice","action_type":"Action"
        })
        st.dataframe(df_s, use_container_width=True, hide_index=True, height=440)
    else:
        st.warning("No records match this filter.")
