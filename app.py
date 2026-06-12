import streamlit as st
import pandas as pd
from supabase import create_client, Client
import os
from datetime import datetime
import pytz

# ==========================================
# SUPABASE CONFIGURATION
# ==========================================
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://emdjnndnsdebhbzebrsg.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVtZGpubmRuc2RlYmhiemVicnNnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODExNzU4NDYsImV4cCI6MjA5Njc1MTg0Nn0.ypy3k30Nbp2caJaNXpwxbrnUzrOLrhwTJ1FZwW5L8Fc")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="AssetFlow KCCL", page_icon="📦", layout="wide", initial_sidebar_state="expanded")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.markdown("<style>section[data-testid='stSidebar']{display:none!important}header[data-testid='stHeader']{display:none!important}</style>", unsafe_allow_html=True)

# ==========================================
# TIME (IST)
# ==========================================
IST = pytz.timezone('Asia/Kolkata')
NOW_IST = datetime.now(IST)
DT_STR = NOW_IST.strftime("%d%b%Y")
CLOCK_STR = NOW_IST.strftime("%H:%M:%S | %d-%b-%Y")

# ==========================================
# PRO-MODE CSS ENGINE
# ==========================================
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* 1. Eliminate Top Panel Overlay */
header[data-testid="stHeader"] { display: none !important; }
.block-container { padding-top: 0rem !important; margin-top: -10px; }

/* 2. Global Typography & Contrast */
.stApp { background-color: #F8FAFC !important; }
.stApp *, label p, div[data-testid="stMarkdownContainer"] p {
    font-family: 'Inter', sans-serif !important;
    color: #090D1A; 
}

/* 3. Sidebar Lockdown (Dark Background) */
section[data-testid="stSidebar"] { 
    background-color: #090D16 !important; border-right: 3px solid #1E293B !important; width: 260px !important; overflow: hidden !important; 
}
section[data-testid="stSidebar"] * { color: #FFFFFF; } 

/* 4. Yellow Navigation Menu Labels */
section[data-testid="stSidebar"] div[data-testid="stRadio"] label > div { 
    color: #FFD700 !important; 
    font-weight: 700 !important; font-size: 15px !important;
}

/* 5. Sky Blue Logout Button with Black Text */
.sb-logout button { 
    background-color: #0EA5E9 !important; 
    color: #000000 !important; 
    border: none !important; font-weight: 800 !important; border-radius: 8px; width: 100%; height: 45px;
}
.sb-logout button:hover { background-color: #0284C7 !important; color: #FFFFFF !important; }

/* 6. Dropdown (Selectbox) White Font Styling */
.stSelectbox div[data-baseweb="select"] > div {
    color: #FFFFFF !important; 
    background-color: #1E293B !important; 
    font-weight: 600 !important; border-radius: 6px;
}

/* 7. Sidebar Clock & Logo */
.sb-clock-container { padding: 20px 16px; text-align: center; border-bottom: 1px solid #1E293B; background: #111827; }
.sb-clock-val { font-size: 14px; color: #38BDF8 !important; font-weight: 700; font-family: monospace !important; }

.sb-logo { padding: 20px 10px; text-align: center; border-bottom: 1px solid #1E293B; display: flex; flex-direction: column; align-items: center; justify-content: center; }
.sb-logo img { border-radius: 8px; max-width: 150px; height: auto; margin-bottom: 5px; }

/* 8. Dashboard Inventory Card Refactor */
.p-card { 
    background: #FFFFFF; border: 2px solid #090D1A; border-radius: 10px; 
    padding: 10px 14px; height: 65px; display: flex; flex-direction: column; justify-content: space-between;
}
.p-name { font-size: 14px; font-weight: 700; color: #090D1A; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.p-total { font-size: 11px; color: #475569; font-weight: 600; }
.p-stock { font-size: 22px; font-weight: 800; color: #16A34A; }

/* Uniform Stat Boxes */
.stat-box { background: #FFFFFF; border: 2px solid #090D1A; border-radius: 12px; padding: 15px; height: 100px; text-align: left; }

/* SKY BLUE EXPORT BUTTONS OVERRIDE */
div[data-testid="stDownloadButton"] > button, .stDownloadButton > button {
    background-color: #0EA5E9 !important; color: #FFFFFF !important;
    border: none !important; border-radius: 8px !important; font-weight: 700 !important; font-size: 13px !important; 
    padding: 10px 16px !important; width: 100% !important; display: inline-flex !important; align-items: center; justify-content: center;
    box-shadow: 0 2px 4px rgba(14,165,233,0.2) !important; opacity: 1 !important; visibility: visible !important;
}
div[data-testid="stDownloadButton"] > button:hover, .stDownloadButton > button:hover { background-color: #0284C7 !important; color: #FFFFFF !important; }

/* Inputs Border Sync */
.stTextInput>div>div>input, .stNumberInput>div>div>input, .stTextArea>div>div>textarea {
    background-color: #FFFFFF !important; border: 2px solid #64748B !important; border-radius: 6px !important; color: #090D1A !important; font-weight: 600 !important;
}
.form-sec { font-size: 13px; font-weight: 700; color: #2563EB !important; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 14px; border-left: 4px solid #2563EB; padding-left: 8px; }
</style>""", unsafe_allow_html=True)

# ==========================================
# UNITS & CORE LOGIC
# ==========================================
UNITS = ["PCS","LTR","ML","MTR","DRUM","BOX","KG","GM","SET","PAIR","ROLL","CAN","BOTTLE","PACK","SHEET","BUNDLE","TUBE","GAL","NOS","KIT"]
COLS_P = ["id","product_name","item_code","default_unit","total_added_to_system"]
COLS_T = ["id","product_id","item_code","serial_number","quantity","unit","issued_to","invoice_no","action_type","created_at"]

@st.cache_data(ttl=60)
def load_data():
    try:
        r = supabase.table("tpl_inv_products").select(",".join(COLS_P)).order("product_name").execute()
        dp = pd.DataFrame(r.data) if r.data else pd.DataFrame(columns=COLS_P)
    except: dp = pd.DataFrame(columns=COLS_P)
    try:
        r = supabase.table("tpl_inv_transactions").select(",".join(COLS_T)).execute()
        dt = pd.DataFrame(r.data) if r.data else pd.DataFrame(columns=COLS_T)
    except: dt = pd.DataFrame(columns=COLS_T)
    return dp, dt

def get_stock(dt, pid):
    if dt.empty: return 0.0
    m = dt[dt["product_id"] == pid]
    up = pd.to_numeric(m[m["action_type"]=="UPLOAD"]["quantity"], errors="coerce").fillna(0).sum()
    rt = pd.to_numeric(m[m["action_type"]=="RETURN"]["quantity"], errors="coerce").fillna(0).sum()
    is_ = pd.to_numeric(m[m["action_type"]=="ISSUE"]["quantity"], errors="coerce").fillna(0).sum()
    return float((up + rt) - is_)

def to_csv(df): return df.to_csv(index=False).encode("utf-8")

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
# SECURE GATEWAY
# ==========================================
if not st.session_state["logged_in"]:
    _, mid, _ = st.columns([1.3, 1.4, 1.3])
    with mid:
        st.markdown('<div style="height:15vh"></div>', unsafe_allow_html=True)
        st.markdown('<div style="background:#FFF; padding:40px; border:2px solid #090D1A; border-radius:16px; text-align:center;">', unsafe_allow_html=True)
        st.markdown('<h2 style="margin-bottom:5px; color:#090D1A;">AssetFlow KCCL</h2>', unsafe_allow_html=True)
        st.markdown('<p style="color:#64748B; margin-bottom:30px;">Inventory Control Portal</p>', unsafe_allow_html=True)
        with st.form("lf"):
            u = st.text_input("Username", label_visibility="collapsed", placeholder="Username")
            p = st.text_input("Password", type="password", label_visibility="collapsed", placeholder="Passphrase")
            if st.form_submit_button("Sign In Securely", use_container_width=True):
                if u == "admin" and p == "kccl@2026":
                    st.session_state["logged_in"] = True
                    st.rerun()
                else: st.error("Access Denied")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ==========================================
# SIDEBAR
# ==========================================
st.sidebar.markdown(f'<div class="sb-clock-container"><div class="sb-clock-val">{CLOCK_STR}</div></div>', unsafe_allow_html=True)

st.sidebar.markdown('<div class="sb-logo">', unsafe_allow_html=True)
LOGO_PATH = "assets/logo.png"
if os.path.exists(LOGO_PATH): st.sidebar.image(LOGO_PATH, use_container_width=True)
else: st.sidebar.markdown('<div style="font-size:40px;">📦</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sb-logo-name">AssetFlow</div><div class="sb-logo-sub">KCCL Operations</div></div>', unsafe_allow_html=True)

page = st.sidebar.radio("Navigation", ["Dashboard", "Transaction", "Reports"], label_visibility="collapsed")

st.sidebar.markdown('<div style="height:30vh"></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sb-logout">', unsafe_allow_html=True)
if st.sidebar.button("Logout Portal"):
    st.session_state["logged_in"] = False
    st.rerun()
st.sidebar.markdown('</div>', unsafe_allow_html=True)

df_p, df_t = load_data()

# ==========================================
# CORE VIEWPORTS
# ==========================================
if page == "Dashboard":
    if df_p.empty:
        st.info("System storage schema blank.")
        st.stop()

    ts = sum(get_stock(df_t, r["id"]) for _, r in df_p.iterrows())
    im = rm = 0.0
    if not df_t.empty:
        dft = df_t.copy()
        dft["created_at"] = pd.to_datetime(dft["created_at"], errors="coerce")
        m = dft.dropna(subset=["created_at"])
        mk = (m["created_at"].dt.month == NOW_IST.month) & (m["created_at"].dt.year == NOW_IST.year)
        im = safe_num(m[mk & (m["action_type"]=="ISSUE")]["quantity"].sum())
        rm = safe_num(m[mk & (m["action_type"]=="RETURN")]["quantity"].sum())

    s1, s2, s3, s4 = st.columns(4)
    with s1: st.markdown(f'<div class="stat-box"><p style="font-size:11px;font-weight:700;color:#64748B;text-transform:uppercase;margin:0;">Classes</p><h1 style="margin:4px 0 0 0;">{len(df_p)}</h1></div>', unsafe_allow_html=True)
    with s2: st.markdown(f'<div class="stat-box"><p style="font-size:11px;font-weight:700;color:#64748B;text-transform:uppercase;margin:0;">Stock</p><h1 style="margin:4px 0 0 0;">{ts:,.0f}</h1></div>', unsafe_allow_html=True)
    with s3: st.markdown(f'<div class="stat-box"><p style="font-size:11px;font-weight:700;color:#64748B;text-transform:uppercase;margin:0;">Issued (Month)</p><h1 style="margin:4px 0 0 0;">{im:,.0f}</h1></div>', unsafe_allow_html=True)
    with s4: st.markdown(f'<div class="stat-box"><p style="font-size:11px;font-weight:700;color:#64748B;text-transform:uppercase;margin:0;">Returned (Month)</p><h1 style="margin:4px 0 0 0;">{rm:,.0f}</h1></div>', unsafe_allow_html=True)
    
    st.markdown('<div style="margin-top:24px; border-bottom:2px solid #090D1A; padding-bottom:8px;"><h3 style="margin:0;">Live Inventory Status</h3></div>', unsafe_allow_html=True)
    cards = st.columns(5)
    sum_rows = []
    for idx, (_, r) in enumerate(df_p.iterrows()):
        stk = get_stock(df_t, r["id"])
        sum_rows.append({"Product Name": r["product_name"], "Item Code": r["item_code"], "In Stock": round(stk, 3), "Unit": r["default_unit"], "Total Added": int(r["total_added_to_system"])})
        with cards[idx % 5]:
            st.markdown(f'''<div class="p-card">
                <div class="p-name">{r["product_name"]}</div>
                <div style="display:flex; justify-content:space-between; align-items:flex-end;">
                    <div class="p-total">Cap: {int(r["total_added_to_system"])}</div>
                    <div class="p-stock">{stk:.0f}</div>
                </div>
            </div>''', unsafe_allow_html=True)

    df_sum = pd.DataFrame(sum_rows)
    st.markdown('<div style="margin-top:30px; border-bottom:2px solid #090D1A; padding-bottom:8px;"><h3 style="margin:0;">Data Extraction Hub</h3></div>', unsafe_allow_html=True)
    d1, d2, d3 = st.columns(3)
    with d1:
        st.markdown("<p style='font-size:13px;font-weight:700;margin-bottom:6px;'>Full Ledger Logs Dump</p>", unsafe_allow_html=True)
        if not df_t.empty:
            df_d = df_t.copy()
            df_d["created_at"] = df_d["created_at"].apply(ind_dt)
            df_d = explode_serials(df_d)
            st.download_button("Download Full Dump CSV", data=to_csv(df_d), file_name=f"AssetFlow_FullDump_{DT_STR}.csv", mime="text/csv", key="d1")
    with d2:
        st.markdown("<p style='font-size:13px;font-weight:700;margin-bottom:6px;'>System Balance Summary</p>", unsafe_allow_html=True)
        if not df_sum.empty:
            st.download_button("Download Summary CSV", data=to_csv(df_sum), file_name=f"AssetFlow_Summary_{DT_STR}.csv", mime="text/csv", key="d2")
    with d3:
        st.markdown("<p style='font-size:13px;font-weight:700;margin-bottom:6px;'>Targeted Asset Log Extraction</p>", unsafe_allow_html=True)
        sel = st.selectbox("Select Target Product", df_p["product_name"].tolist(), key="cs", label_visibility="collapsed")
        if sel:
            tid = df_p[df_p["product_name"]==sel]["id"].values[0]
            df_is = df_t[(df_t["product_id"]==tid) & (df_t["action_type"]=="ISSUE")].copy()
            if not df_is.empty:
                df_is["created_at"] = df_is["created_at"].apply(ind_dt)
                df_is["Product"] = sel
                df_is = explode_serials(df_is)
                ec = [c for c in ["created_at","Product","item_code","serial_number","quantity","unit","issued_to","invoice_no"] if c in df_is.columns]
                st.download_button(f"Export {sel} Sheets", data=to_csv(df_is[ec]), file_name=f"AssetFlow_{sel.lower().replace(' ','_')}_Issued_{DT_STR}.csv", mime="text/csv", key="d3")

elif page == "Transaction":
    cl, cr = st.columns(2, gap="large")
    with cl:
        st.markdown('<div class="form-sec">Asset Parameters</div>', unsafe_allow_html=True)
        sel_prod = st.selectbox("Target Catalog Product *", df_p["product_name"].tolist(), key="tp")
        item_code = st.text_input("Item Tracking Reference Code *", key="tc")
        serial = st.text_area("Hardware Unique Serials *", key="ts", placeholder="Split with comma")
        unit = st.selectbox("Standard Measurement Unit *", UNITS, key="tu")
        qty = st.number_input("Transaction Unit Quantity *", min_value=0.001, step=0.001, format="%.3f", key="tq")
    with cr:
        st.markdown('<div class="form-sec">Workflow Mapping</div>', unsafe_allow_html=True)
        action = st.selectbox("Ledger Action Trigger *", ["ISSUE","RETURN","UPLOAD"], key="ta")
        issued_to = st.text_input("Recipient Node / Operator Assignee" + (" *" if action != "UPLOAD" else ""), key="ti")
        invoice = st.text_input("Challan / Invoice Reference ID *", key="tn")
        st.text_input("System Logging Datetime (IST)", value=CLOCK_STR, disabled=True, key="td")
        
        st.markdown("<div style='margin-top:35px;'></div>", unsafe_allow_html=True)
        submitted = st.button("Commit Action Statement to Ledger", use_container_width=True, type="primary")

    if submitted:
        errs = []
        if not item_code.strip(): errs.append("Item code tracking link is required.")
        if not serial.strip(): errs.append("Hardware unique serial identification keys missing.")
        if qty <= 0: errs.append("Asset quantity metric dynamic fault.")
        if action != "UPLOAD" and not issued_to.strip(): errs.append("Recipient tracking parameter missing.")
        if not invoice.strip(): errs.append("Invoice mapping reference mandatory.")
        if errs:
            for e in errs: st.error(e)
            st.stop()
            
        pid = int(df_p[df_p["product_name"]==sel_prod]["id"].values[0])
        if action == "UPLOAD":
            codes = [c.strip() for c in item_code.split(",") if c.strip()]
            serials = [s.strip() for s in serial.split(",") if s.strip()]
            ok = 0
            for i, code in enumerate(codes):
                sn = serials[i] if i < len(serials) else ""
                payload = {"product_id": pid, "item_code": code, "serial_number": sn, "quantity": qty, "unit": unit, "issued_to": "", "invoice_no": invoice.strip(), "action_type": "UPLOAD", "created_at": datetime.now(IST).isoformat()}
                try:
                    res = supabase.table("tpl_inv_transactions").insert(payload).execute()
                    if res.data: ok += 1
                except Exception as ex: st.error(f"Fault on write tracing {code}: {ex}")
            if ok > 0:
                st.success(f"Synchronized {ok} blocks safely.")
                load_data.clear()
                st.rerun()
        else:
            ic, sn = item_code.strip(), serial.strip()
            if not df_t.empty:
                uploads = df_t[df_t["action_type"]=="UPLOAD"]
                if ic not in uploads["item_code"].values:
                    st.error(f"Trace tracking failed: Code '{ic}' not found inside UPLOAD system history.")
                    st.stop()
            if action == "ISSUE":
                cs = get_stock(df_t, pid)
                if qty > cs:
                    st.error(f"Shortfall Exception: stock shortfall. Available limit: {cs:.3f} {unit}")
                    st.stop()
            payload = {"product_id": pid, "item_code": ic, "serial_number": sn, "quantity": qty, "unit": unit, "issued_to": issued_to.strip(), "invoice_no": invoice.strip(), "action_type": action, "created_at": datetime.now(IST).isoformat()}
            try:
                res = supabase.table("tpl_inv_transactions").insert(payload).execute()
                if res.data:
                    st.success(f"Statement written into database ledger framework.")
                    load_data.clear()
                    st.rerun()
            except Exception as ex: st.error(f"Database sync pipeline error: {ex}")

elif page == "Reports":
    st.markdown('<div class="form-sec">Ledger Query Filter Engine</div>', unsafe_allow_html=True)
    f1, f2, f3, f4 = st.columns(4)
    with f1: im = st.selectbox("Query Asset Class", ["ALL"] + sorted(df_p["product_name"].tolist()), key="rm")
    with f2: st_ = st.selectbox("Query Flow State", ["ALL", "ISSUE", "RETURN", "UPLOAD"], key="rs")
    with f3: df_ = st.date_input("Query Start Date", value=pd.to_datetime(df_t["created_at"]).min().date() if not df_t.empty else NOW_IST.date())
    with f4: dt_ = st.date_input("Query End Date", value=NOW_IST.date())
    
    df_f = df_t.copy()
    if not df_f.empty and not df_p.empty:
        pmap = df_p.set_index("id")["product_name"].to_dict()
        df_f["product_name"] = df_f["product_id"].map(pmap).fillna("Unknown")
        df_f["created_at_dt"] = pd.to_datetime(df_f["created_at"]).dt.date
        
        if im != "ALL": df_f = df_f[df_f["product_name"] == im]
        if st_ != "ALL": df_f = df_f[df_f["action_type"] == st_]
        df_f = df_f[(df_f["created_at_dt"] >= df_) & (df_f["created_at_dt"] <= dt_)]

    r1, r2 = st.columns([2, 1])
    with r1: st.markdown(f'<p style="font-size:14px;color:#090D1A;margin-top:12px;font-weight:700;">Query matched <span style="color:#2563EB;">{len(df_f)}</span> log entries</p>', unsafe_allow_html=True)
    with r2:
        if not df_f.empty:
            df_ex = df_f.copy()
            df_ex["created_at"] = pd.to_datetime(df_ex["created_at"]).apply(ind_dt)
            df_ex = explode_serials(df_ex)
            ec = [c for c in ["created_at","product_name","item_code","serial_number","quantity","unit","issued_to","invoice_no","action_type"] if c in df_ex.columns]
            st.download_button("Export Compiled Data Sheet", data=to_csv(df_ex[ec]), file_name=f"AssetFlow_Report_{DT_STR}.csv", mime="text/csv", key="dr")

    if not df_f.empty:
        df_s = df_f.copy()
        df_s["created_at"] = pd.to_datetime(df_s["created_at"]).apply(ind_dt)
        df_s = explode_serials(df_s)
        ec = [c for c in ["created_at","product_name","item_code","serial_number","quantity","unit","issued_to","invoice_no","action_type"] if c in df_s.columns]
        df_s = df_s[ec].rename(columns={"created_at":"Date (IST)","product_name":"Product","item_code":"Code","serial_number":"Serial","quantity":"Qty","unit":"Unit","issued_to":"Issued To","invoice_no":"Invoice","action_type":"Action"})
        st.dataframe(df_s, use_container_width=True, hide_index=True, height=450)
    else: st.warning("No records matched the selected query boundaries.")
