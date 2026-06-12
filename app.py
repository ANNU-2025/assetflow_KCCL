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
# MINIMAL CSS
# ==========================================
st.markdown("""<style>
.block-container{padding-top:1.5rem;padding-bottom:2rem}
.stApp{background:#0A0F16;color:#E6EDF3}
section[data-testid="stSidebar"]{background:#111921;border-right:1px solid #1B2636}
#MainMenu{visibility:hidden}footer{visibility:hidden}
header[data-testid="stHeader"]{background:#0A0F16}
.inv-card{background:#141D28;border:1px solid #1B2636;border-radius:12px;padding:16px;transition:all .2s}
.inv-card:hover{border-color:rgba(0,229,160,.3);transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,229,160,.06)}
.stat-box{background:#141D28;border:1px solid #1B2636;border-radius:12px;padding:18px}
.dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:6px}
.dot-g{background:#00E5A0;box-shadow:0 0 6px #00E5A0}
.dot-y{background:#F59E0B;box-shadow:0 0 6px #F59E0B}
.dot-r{background:#EF4444;box-shadow:0 0 6px #EF4444}
.badge{display:inline-block;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:600}
.b-i{background:rgba(255,107,53,.12);color:#FF6B35}
.b-r{background:rgba(0,229,160,.1);color:#00E5A0}
.b-u{background:rgba(56,189,248,.1);color:#38BDF8}
.dataframe th{background:#111921!important;color:#8B949E!important;font-size:11px!important;text-transform:uppercase;letter-spacing:.5px;border-bottom:1px solid #1B2636!important}
.dataframe td{color:#E6EDF3!important;font-size:13px!important;border-bottom:1px solid #1B2636!important}
.dataframe tr:hover td{background:rgba(0,229,160,.03)!important}
.stDownloadButton>button{background:#141D28;border:1px solid #1B2636;color:#E6EDF3;border-radius:8px}
.stDownloadButton>button:hover{border-color:#00E5A0;color:#00E5A0}
.stTextInput>div>div>input,.stSelectbox>div>div>select,.stNumberInput>div>div>input,.stTextArea>div>div>textarea{background:#0E151E!important;color:#E6EDF3!important;border-color:#1B2636!important;border-radius:8px!important}
.stTextInput>div>div>input:focus,.stSelectbox>div>div>select:focus{border-color:#00E5A0!important;box-shadow:0 0 0 3px rgba(0,229,160,.08)!important}
.stButton>button[kind="primary"]{background:linear-gradient(135deg,#00E5A0,#00C98A);color:#060A10;border:none;border-radius:8px;font-weight:700}
.stButton>button[kind="primary"]:hover{transform:translateY(-1px);box-shadow:0 6px 20px rgba(0,229,160,.3)}
[data-baseweb="select"]>div>ul{max-height:260px!important;overflow-y:auto!important}
.sec-h{font-size:14px;font-weight:700;color:#E6EDF3;margin-bottom:12px;padding-bottom:6px;border-bottom:1px solid #1B2636}
</style>""", unsafe_allow_html=True)

# ==========================================
# LOGO
# ==========================================
if os.path.exists("assets/logo.png"):
    st.sidebar.image("assets/logo.png", width=130)
else:
    st.sidebar.markdown('<div style="text-align:center;margin-bottom:6px"><div style="width:44px;height:44px;margin:0 auto 6px;background:rgba(0,229,160,.08);border:1.5px solid rgba(0,229,160,.25);border-radius:11px;display:flex;align-items:center;justify-content:center;font-size:20px">📦</div><span style="font-size:17px;font-weight:800;color:#E6EDF3">AssetFlow</span><br><span style="font-size:10px;color:#484F58">KCCL Inventory</span></div>', unsafe_allow_html=True)
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

def indian_dt(v):
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

# ==========================================
# LOGIN
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.subheader("🔑 System Login")
    with st.form("lf"):
        c1, c2 = st.columns(2)
        u = c1.text_input("Username")
        p = c2.text_input("Password", type="password")
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
page = st.sidebar.radio("📌 Menu", ["Dashboard", "Transaction", "Reports"], label_visibility="collapsed")

# ==========================================
# LOAD DATA
# ==========================================
df_p, df_t = load_data()

# ==========================================
# DASHBOARD
# ==========================================
if page == "Dashboard":
    st.header("📈 Dashboard")

    if df_p.empty:
        st.info("No products in `tpl_inv_products`. Add via Supabase first.")
        st.stop()

    # Stats
    ts = sum(get_stock(df_t, r["id"]) for _, r in df_p.iterrows())
    now = datetime.now()
    im = rm = 0.0
    if not df_t.empty:
        df_t["created_at"] = pd.to_datetime(df_t["created_at"], errors="coerce")
        m = df_t.dropna(subset=["created_at"])
        mk = (m["created_at"].dt.month == now.month) & (m["created_at"].dt.year == now.year)
        im = safe_num(m[mk & (m["action_type"]=="ISSUE")]["quantity"].sum())
        rm = safe_num(m[mk & (m["action_type"]=="RETURN")]["quantity"].sum())

    c1, c2, c3, c4 = st.columns(4)
    for col, lbl, val, cls in [
        (c1,"Products",len(df_p),"#00E5A0"),
        (c2,"In Stock",f"{ts:,.1f}","#38BDF8"),
        (c3,"Issued (Month)",f"{im:,.1f}","#FF6B35"),
        (c4,"Returned (Month)",f"{rm:,.1f}","#F59E0B")
    ]:
        with col:
            st.markdown(f'<div class="stat-box"><div style="font-size:11px;color:#8B949E;text-transform:uppercase;letter-spacing:.5px;font-weight:600">{lbl}</div><div style="font-size:26px;font-weight:800;margin-top:4px;color:{cls}">{val}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Product Cards
    st.markdown('<div class="sec-h">📦 Product Cards</div>', unsafe_allow_html=True)
    cards = st.columns(4)
    sum_rows = []

    for idx, (_, r) in enumerate(df_p.iterrows()):
        pid, nm, code, unit = r["id"], r["product_name"], r["item_code"], r["default_unit"]
        total = safe_num(r.get("total_added_to_system", 0), 0)
        stk = get_stock(df_t, pid)
        dc = dot_cls(stk, total)
        sum_rows.append({"Product Name": nm, "Item Code": code, "In Stock": round(stk, 3), "Unit": unit, "Total Added": int(total)})

        with cards[idx % 4]:
            st.markdown(f'<div class="inv-card"><div style="display:flex;align-items:center;gap:6px;margin-bottom:2px"><span class="dot {dc}"></span><span style="font-size:13px;font-weight:600;color:#E6EDF3;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{nm}</span></div><div style="font-size:11px;color:#484F58;font-family:monospace;margin-bottom:10px">{code}</div><div style="font-size:22px;font-weight:800;color:#E6EDF3;font-family:monospace">{stk:.3f}</div><div style="font-size:11px;color:#8B949E;margin-top:2px">Unit: {unit}</div><div style="height:1px;background:#1B2636;margin:8px 0"></div><div style="font-size:11px;color:#484F58">Total Added: <b style="color:#8B949E">{int(total)}</b></div></div>', unsafe_allow_html=True)

    df_sum = pd.DataFrame(sum_rows)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-h">📥 Downloads</div>', unsafe_allow_html=True)

    d1, d2, d3 = st.columns(3)

    # 1. Full Dump
    with d1:
        st.markdown("##### Full Dump")
        if not df_t.empty:
            df_dump = df_t.copy()
            df_dump["created_at"] = df_dump["created_at"].apply(indian_dt)
            st.download_button("📥 Download", data=to_csv(df_dump), file_name=f"full_dump_{now.strftime('%d%b%Y')}.csv", mime="text/csv", key="d1")

    # 2. Product Summary
    with d2:
        st.markdown("##### Product Summary")
        if not df_sum.empty:
            st.download_button("📥 Download", data=to_csv(df_sum), file_name="product_summary.csv", mime="text/csv", key="d2")

    # 3. Card Issued
    with d3:
        st.markdown("##### Issued Details")
        sel = st.selectbox("Product", df_p["product_name"].tolist(), key="cs", label_visibility="collapsed")
        if sel:
            tid = df_p[df_p["product_name"]==sel]["id"].values[0]
            df_is = df_t[(df_t["product_id"]==tid) & (df_t["action_type"]=="ISSUE")].copy()
            if not df_is.empty:
                df_is["created_at"] = df_is["created_at"].apply(indian_dt)
                df_is["Product"] = sel
                ec = [c for c in ["created_at","Product","item_code","serial_number","quantity","unit","issued_to","invoice_no"] if c in df_is.columns]
                st.download_button("📥 Download", data=to_csv(df_is[ec]), file_name=f"{sel.lower().replace(' ','_')}_issued.csv", mime="text/csv", key="d3")
            else:
                st.caption("No ISSUE records.")

# ==========================================
# TRANSACTION
# ==========================================
elif page == "Transaction":
    st.header("🔄 Transaction")

    if df_p.empty:
        st.warning("Add products to `tpl_inv_products` first.")
        st.stop()

    cl, cr = st.columns(2)

    with cl:
        st.markdown('<div class="sec-h">Product & Quantity</div>', unsafe_allow_html=True)
        sel_prod = st.selectbox("Product *", df_p["product_name"].tolist(), key="tp")
        item_code = st.text_input("Item Code *", placeholder="e.g. EDF-2401", key="tc")
        serial = st.text_area("Serial Number(s)", placeholder="Comma-separated", height=60, key="ts")
        unit = st.selectbox("Unit *", UNITS, key="tu")
        qty = st.number_input("Quantity *", min_value=0.001, step=0.001, format="%.3f", key="tq")

    with cr:
        st.markdown('<div class="sec-h">Action & Destination</div>', unsafe_allow_html=True)
        issued_to = st.text_input("Issued To *", placeholder="Person or site name", key="ti")
        invoice = st.text_input("Invoice / DC No *", placeholder="e.g. INV-2025-042", key="tn")
        action = st.selectbox("Action *", ["ISSUE","RETURN","UPLOAD"], key="ta")
        st.text_input("DateTime (Auto)", value=now.strftime("%d-%b-%Y  %H:%M:%S"), disabled=True, key="td")
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.button("⚡ Commit Transaction", use_container_width=True, type="primary")

    if submitted:
        errs = []
        if not item_code.strip(): errs.append("Item Code required.")
        if qty <= 0: errs.append("Quantity must be > 0.")
        if action != "UPLOAD" and not issued_to.strip(): errs.append("Issued To required.")
        if not invoice.strip(): errs.append("Invoice required.")

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
                    st.success(f"{action} {qty:.3f} {unit} — {item_code} committed!")
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
    st.header("📊 Reports")

    if df_t.empty:
        st.info("No transaction data.")
        st.stop()

    df_r = df_t.copy()
    if not df_p.empty:
        pmap = df_p.set_index("id")["product_name"].to_dict()
        df_r["product_name"] = df_r["product_id"].map(pmap).fillna("Unknown")
    df_r["created_at"] = pd.to_datetime(df_r["created_at"], errors="coerce")
    df_r["_d"] = df_r["created_at"].dt.date

    mn = df_r["_d"].min() if df_r["_d"].notna().any() else now.date()
    mx = df_r["_d"].max() if df_r["_d"].notna().any() else now.date()

    st.markdown('<div class="sec-h">🔍 Filters</div>', unsafe_allow_html=True)
    f1,f2,f3,f4,f5 = st.columns(5)

    with f1: df_ = st.date_input("From", value=mn, key="rf")
    with f2: dt_ = st.date_input("To", value=mx, key="rt")
    with f3: it_ = st.multiselect("Issued To", sorted(df_r["issued_to"].dropna().unique()), key="ri")
    with f4: im_ = st.multiselect("Item", sorted(df_p["product_name"].tolist()), key="rm")
    with f5: st_ = st.multiselect("Type", ["ISSUE","RETURN","UPLOAD"], key="rs")

    iv_ = st.multiselect("Invoice", sorted(df_r["invoice_no"].dropna().unique()), key="rv")

    # Only show when at least one filter is active
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

    r1, r2 = st.columns([1,1])
    with r1:
        st.markdown(f'Records: **<span style="color:#00E5A0">{len(df_f)}</span>**', unsafe_allow_html=True)
    with r2:
        if not df_f.empty:
            df_ex = df_f.copy()
            df_ex["created_at"] = df_ex["created_at"].apply(indian_dt)
            ec = [c for c in ["created_at","product_name","item_code","serial_number","quantity","unit","issued_to","invoice_no","action_type"] if c in df_ex.columns]
            st.download_button("📥 Export CSV", data=to_csv(df_ex[ec]), file_name=f"report_{now.strftime('%d%b%Y')}.csv", mime="text/csv", key="dr")

    st.markdown("<br>", unsafe_allow_html=True)

    if not df_f.empty:
        df_s = df_f.copy()
        df_s["created_at"] = df_s["created_at"].apply(indian_dt)
        ec = [c for c in ["created_at","product_name","item_code","serial_number","quantity","unit","issued_to","invoice_no","action_type"] if c in df_s.columns]
        df_s = df_s[ec].rename(columns={"created_at":"Date","product_name":"Product","item_code":"Code","serial_number":"Serial","quantity":"Qty","unit":"Unit","issued_to":"Issued To","invoice_no":"Invoice","action_type":"Action"})
        st.dataframe(df_s, use_container_width=True, hide_index=True, height=420)
    else:
        st.warning("No records match this filter.")
