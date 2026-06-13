import streamlit as st
import pandas as pd
from supabase import create_client, Client
import os
from datetime import datetime

# ==========================================
# SUPABASE CONFIGURATION
# ==========================================
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://emdjnndnsdebhbzebrsg.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVtZGpubmRuc2RlYmhiemVicnNnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODExNzU4NDYsImV4cCI6MjA5Njc1MTg0Nn0.ypy3k30Nbp2caJaNXpwxbrnUzrOLrhwTJ1FZwW5L8Fc")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(page_title="AssetFlow KCCL", page_icon="📦", layout="wide", initial_sidebar_state="expanded")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# ==========================================
# LOGIN PAGE — CLEAN "KCCL BANGLA" CENTERED
# ==========================================
if not st.session_state["logged_in"]:

    st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    section[data-testid='stSidebar']{display:none!important}
    header[data-testid='stHeader']{display:none!important}
    footer{visibility:hidden!important}
    #MainMenu{visibility:hidden!important}
    .stApp{background:#F1F5F9!important}

    .block-container{
        max-width:100%!important;
        padding-top:0!important;
        padding-bottom:0!important;
    }
    .block-container > div > div > div > div[data-testid="stVerticalBlock"]{
        min-height:100vh;
        display:flex!important;
        flex-direction:column!important;
        justify-content:center!important;
        align-items:center!important;
    }
    .block-container > div > div > div > div[data-testid="stVerticalBlock"] > div[data-testid="stHorizontalBlock"]{
        width:100%;
        max-width:440px;
    }
    .lc{
        background:#fff!important;
        border-radius:24px!important;
        padding:50px 40px 40px!important;
        box-shadow:0 25px 60px rgba(0,0,0,0.06), 0 0 0 1px rgba(0,0,0,0.03)!important;
        text-align:center!important;
    }
    .lt{
        font-size:32px!important;
        font-weight:900!important;
        color:#0B0F19!important;
        letter-spacing:-1px!important;
        margin:0 0 6px 0!important;
        font-family:'Inter',sans-serif!important;
    }
    .ls{
        font-size:13px!important;
        color:#64748B!important;
        font-weight:500!important;
        margin:0 0 36px 0!important;
        font-family:'Inter',sans-serif!important;
    }
    .lc [data-testid="stTextInput"] label p{color:#334155!important;font-size:12px!important;font-weight:700!important;text-align:left!important}
    .lc [data-testid="stTextInput"] > div > div > input{background:#F8FAFC!important;border:2px solid #E2E8F0!important;border-radius:12px!important;color:#0F172A!important;font-size:14px!important}
    .lc [data-testid="stTextInput"] > div > div > input:focus{border-color:#0EA5E9!important;box-shadow:0 0 0 3px rgba(14,165,233,0.12)!important}
    .lc [data-testid="stFormSubmitButton"] button{background:#0B0F19!important;color:#fff!important;border:none!important;border-radius:12px!important;font-weight:700!important;font-size:14px!important;padding:14px!important;width:100%!important;margin-top:8px!important;font-family:'Inter',sans-serif!important;transition:all .2s!important}
    .lc [data-testid="stFormSubmitButton"] button:hover{background:#1E293B!important;transform:translateY(-1px);box-shadow:0 4px 12px rgba(0,0,0,0.15)!important}
    .lc [data-testid="stException"]{background:#FEF2F2!important;color:#DC2626!important;border:1px solid #FECACA!important;border-radius:12px!important;padding:12px 16px!important;font-size:13px!important;font-weight:600!important;text-align:left!important}
    </style>""", unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 1.2, 1])
    with mid:
        st.markdown('<div class="lc">', unsafe_allow_html=True)
        # শুধু টেক্সট, কোনো ইমেজ নেই
        st.markdown('<div class="lt">KCCL Bangla</div>', unsafe_allow_html=True)
        st.markdown('<div class="ls">Inventory Control Portal</div>', unsafe_allow_html=True)
        with st.form("lf", clear_on_submit=False):
            u = st.text_input("Username", placeholder="Enter username", label_visibility="visible")
            p = st.text_input("Password", type="password", placeholder="Enter password", label_visibility="visible")
            submitted = st.form_submit_button("Authenticate Sign In", use_container_width=True, type="primary")
            if submitted:
                if u == "admin" and p == "kccl@2026":
                    st.session_state["logged_in"] = True
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please try again.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.stop()

# ==========================================
# MAIN APP CSS — DARK NARROW SIDEBAR + SOLID MAIN
# ==========================================
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
.stApp{background:#F1F5F9!important;color:#0F172A!important;font-family:'Inter',system-ui,sans-serif!important}
.block-container{padding:1rem 2rem!important;max-width:1560px;margin:0 auto;position:relative;z-index:1}
header[data-testid="stHeader"]{visibility:hidden!important;height:0!important}
#MainMenu{visibility:hidden!important}
footer{visibility:hidden!important}

/* SIDEBAR — DARK & NARROW (220px) */
section[data-testid="stSidebar"]{
    background:#0B0F19!important;
    border-right:1px solid #1E293B!important;
    width:220px!important;
    min-width:220px!important;
    transition:all .2s!important;
}
section[data-testid="stSidebar"] > div{
    padding-top:12px!important;
    position:relative!important;
    min-height:100vh!important;
    display:flex!important;
    flex-direction:column!important;
}

/* SIDEBAR RADIO — BOLD & BROADER */
section[data-testid="stSidebar"] section[data-testid="stRadio"]{background:transparent!important}
section[data-testid="stSidebar"] section[data-testid="stRadio"] div[role="radiogroup"]{gap:4px!important;padding:0 12px!important}
section[data-testid="stSidebar"] section[data-testid="stRadio"] div[role="radiogroup"] > div{
    padding:11px 16px!important;
    border-left:4px solid transparent!important;
    border-radius:8px!important;
    transition:all .15s!important;
    margin:0!important;
}
section[data-testid="stSidebar"] section[data-testid="stRadio"] label p{
    color:#94A3B8!important;
    font-size:14px!important;
    font-weight:800!important;
    letter-spacing:.2px!important;
}
section[data-testid="stSidebar"] section[data-testid="stRadio"] div[role="radiogroup"] > div:hover{
    background:rgba(255,255,255,0.05)!important;
}
section[data-testid="stSidebar"] section[data-testid="stRadio"] div[role="radiogroup"] > div[aria-checked="true"]{
    background:#111827!important;
    border-left:4px solid #FFFFFF!important;
}
section[data-testid="stSidebar"] section[data-testid="stRadio"] div[role="radiogroup"] > div[aria-checked="true"] label p{
    color:#FFFFFF!important;
    font-weight:800!important;
}

/* LOGOUT BUTTON */
.sidebar-logout{
    position:absolute!important;
    bottom:0!important;
    left:0!important;
    width:100%!important;
    padding:16px!important;
    border-top:1px solid #1E293B!important;
    background:#0B0F19!important;
}
.sidebar-logout button{
    width:100%!important;
    background:transparent!important;
    color:#EF4444!important;
    border:1px solid #EF4444!important;
    border-radius:10px!important;
    font-weight:700!important;
    font-size:13px!important;
    padding:9px!important;
    transition:all .2s!important;
}
.sidebar-logout button:hover{
    background:#EF4444!important;
    color:#FFFFFF!important;
    box-shadow:0 4px 12px rgba(239,68,68,0.3)!important;
}

/* STAT BOXES — SOLID FEEL WITH LEFT ACCENT */
.stat-box{
    background:#fff!important;
    border:1px solid #E2E8F0!important;
    border-left:5px solid #0EA5E9!important;
    border-radius:14px!important;
    padding:22px 24px!important;
    min-height:105px!important;
    display:flex!important;
    flex-direction:column!important;
    justify-content:center!important;
    box-shadow:0 1px 3px rgba(0,0,0,0.03),0 8px 20px rgba(0,0,0,0.03)!important;
    color:#0F172A!important;
    transition:transform .2s,box-shadow .2s!important;
}
.stat-box:hover{transform:translateY(-3px)!important;box-shadow:0 12px 28px rgba(0,0,0,0.06)!important}
.stat-lbl{font-size:11px!important;color:#64748B!important;text-transform:uppercase!important;letter-spacing:1.2px!important;font-weight:700!important;white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important}
.stat-val{font-size:32px!important;font-weight:900!important;margin-top:6px!important;line-height:1!important;color:#0B0F19!important;letter-spacing:-.5px!important}

/* PRODUCT CARDS — SOLID & CLEAN */
.p-card{
    background:#fff!important;
    border:1px solid #E2E8F0!important;
    border-radius:14px!important;
    padding:16px 18px!important;
    display:flex!important;
    flex-direction:column!important;
    justify-content:space-between!important;
    height:88px!important;
    box-shadow:0 1px 2px rgba(0,0,0,0.02),0 4px 10px rgba(0,0,0,0.02)!important;
    transition:all .2s!important;
    color:#0F172A!important;
    position:relative!important;
    overflow:hidden!important;
}
.p-card:hover{border-color:#0EA5E9!important;background:#F0F9FF!important;transform:translateY(-3px)!important;box-shadow:0 12px 24px rgba(14,165,233,0.12)!important}
.p-top{display:flex;align-items:center;gap:8px;overflow:hidden}
.p-bottom{display:flex;align-items:flex-end;justify-content:space-between}
.p-name{font-size:13px;font-weight:800;color:#0F172A!important;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;letter-spacing:-.2px!important}
.p-stock{font-size:24px;font-weight:900;color:#059669!important;line-height:1;text-align:right;letter-spacing:-.5px!important}
.p-total{font-size:10px;color:#94A3B8!important;font-weight:700!important;text-transform:uppercase!important;letter-spacing:.5px!important}
.dot{display:inline-block;width:8px;height:8px;border-radius:50%;flex-shrink:0}
.dot-g{background:#059669;box-shadow:0 0 8px rgba(5,150,105,0.4)}
.dot-y{background:#D97706;box-shadow:0 0 8px rgba(217,119,6,0.4)}
.dot-r{background:#DC2626;box-shadow:0 0 8px rgba(220,38,38,0.4)}

/* SECTION HEADERS */
.sec-h{font-size:15px!important;font-weight:800!important;color:#0B0F19!important;margin:26px 0 14px!important;padding-bottom:8px!important;border-bottom:2px solid #0B0F19!important;letter-spacing:-.3px!important}

/* FORM */
label p,.stDateInput>label,.stTextArea>label,.stSelectbox>label,.stNumberInput>label{font-size:12px!important;font-weight:700!important;color:#334155!important}
.form-sec{font-size:11px!important;font-weight:800!important;color:#0B0F19!important;text-transform:uppercase!important;letter-spacing:1.2px!important;margin-bottom:14px!important;padding-bottom:8px!important;border-bottom:2px solid #0EA5E9!important;display:inline-block!important}
.hint{font-size:11px!important;color:#94A3B8!important;margin-top:-2px!important;margin-bottom:12px!important}

/* INPUTS */
.stTextInput>div>div>input,.stSelectbox>div>div>select,.stTextArea>div>div>textarea,.stNumberInput>div>div>input,.stDateInput>div>div>input{background:#fff!important;border:2px solid #E2E8F0!important;border-radius:12px!important;color:#0F172A!important;font-size:14px!important}
.stTextInput>div>div>input:focus,.stSelectbox>div>div>select:focus,.stTextArea>div>div>textarea:focus,.stNumberInput>div>div>input:focus{border-color:#0EA5E9!important;box-shadow:0 0 0 3px rgba(14,165,233,0.1)!important}

/* BUTTONS */
.stButton>button[kind="primary"]{background:#0B0F19!important;color:#fff!important;border:none!important;border-radius:12px!important;font-weight:800!important;font-size:14px!important;padding:14px 28px!important;transition:all .2s!important;letter-spacing:.2px!important}
.stButton>button[kind="primary"]:hover{background:#1E293B!important;box-shadow:0 8px 16px rgba(0,0,0,0.2)!important;transform:translateY(-1px)!important}
.stDownloadButton>button{background:#0EA5E9!important;color:#fff!important;border:none!important;border-radius:12px!important;font-weight:700!important;font-size:13px!important;padding:11px 20px!important;width:100%!important;box-shadow:0 2px 8px rgba(14,165,233,0.2)!important;transition:all .2s!important}
.stDownloadButton>button:hover{background:#0284C7!important;box-shadow:0 6px 20px rgba(14,165,233,0.3)!important;transform:translateY(-1px)!important}

/* DATAFRAME */
.stDataFrame{background:#fff!important;border-radius:14px!important;border:1px solid #E2E8F0!important;box-shadow:0 1px 3px rgba(0,0,0,0.04)!important}

/* ALERTS */
.stError{background-color:#FEF2F2!important;color:#DC2626!important;border:1px solid #FECACA!important;border-radius:12px!important}
.stWarning{background-color:#FFFBEB!important;color:#B45309!important;border:1px solid #FDE68A!important;border-radius:12px!important}
.stSuccess{background-color:#F0FDF4!important;color:#059669!important;border:1px solid #BBF7D0!important;border-radius:12px!important}
.stInfo{background-color:#F0F9FF!important;color:#0369A1!important;border:1px solid #BAE6FD!important;border-radius:12px!important}

/* MULTISELECT */
.stMultiSelect>div>div{background:#fff!important;border:2px solid #E2E8F0!important;border-radius:12px!important;color:#0F172A!important}
.stMultiSelect>div>div>div{color:#0F172A!important}
</style>""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR — STRIPPED DOWN & NARROW
# ==========================================
page = st.sidebar.radio("", ["Dashboard", "Transaction", "Reports"], label_visibility="collapsed")

# Logout Button at bottom
st.sidebar.markdown('<div class="sidebar-logout">', unsafe_allow_html=True)
if st.sidebar.button("🚪 Logout", key="logout_btn"):
    st.session_state["logged_in"] = False
    st.rerun()
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# CONFIG
# ==========================================
UNITS = ["PCS","LTR","ML","MTR","DRUM","BOX","KG","GM","SET","PAIR","ROLL","CAN","BOTTLE","PACK","SHEET","BUNDLE","TUBE","GAL","NOS","KIT"]
COLS_P = ["id","product_name","item_code","default_unit","total_added_to_system"]
COLS_T = ["id","product_id","item_code","serial_number","quantity","unit","issued_to","invoice_no","action_type","created_at"]

# ==========================================
# HELPERS
# ==========================================
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
    if dt.empty: return 0.0
    m = dt[dt["product_id"].eq(pid)]
    up = pd.to_numeric(m[m["action_type"].eq("UPLOAD")]["quantity"], errors="coerce").fillna(0).sum()
    rt = pd.to_numeric(m[m["action_type"].eq("RETURN")]["quantity"], errors="coerce").fillna(0).sum()
    is_ = pd.to_numeric(m[m["action_type"].eq("ISSUE")]["quantity"], errors="coerce").fillna(0).sum()
    return float((up + rt) - is_)

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

def safe_num(v, d=0.0):
    try: return float(v)
    except Exception: return d

def explode_serials(df):
    if df.empty: return df
    rows = []
    for _, r in df.iterrows():
        s = str(r.get("serial_number","")).strip()
        if s:
            parts = [x.strip() for x in s.split(",") if x.strip()]
            if len(parts) > 1:
                for p in parts:
                    nr = r.copy(); nr["serial_number"] = p; rows.append(nr)
                continue
        rows.append(r)
    return pd.DataFrame(rows)

# ==========================================
# DATA
# ==========================================
NOW = datetime.now()
DT_STR = NOW.strftime("%d%b%Y")
df_p, df_t = load_data()

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

    im = rm = 0.0
    if not df_t.empty:
        dft = df_t.copy()
        dft["created_at"] = pd.to_datetime(dft["created_at"], errors="coerce")
        m = dft.dropna(subset=["created_at"])
        mk = (m["created_at"].dt.month == NOW.month) & (m["created_at"].dt.year == NOW.year)
        im = safe_num(m[mk & (m["action_type"].eq("ISSUE"))]["quantity"].sum())
        rm = safe_num(m[mk & (m["action_type"].eq("RETURN"))]["quantity"].sum())

    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown('<div class="stat-box"><div class="stat-lbl">Active Items</div><div class="stat-val">'+str(len(df_p))+'</div></div>', unsafe_allow_html=True)
    with s2:
        st.markdown('<div class="stat-box"><div class="stat-lbl">Total Stock</div><div class="stat-val">'+"{:,.1f}".format(ts)+'</div></div>', unsafe_allow_html=True)
    with s3:
        st.markdown('<div class="stat-box"><div class="stat-lbl">Issued (Month)</div><div class="stat-val">'+"{:,.1f}".format(im)+'</div></div>', unsafe_allow_html=True)
    with s4:
        st.markdown('<div class="stat-box"><div class="stat-lbl">Returned (Month)</div><div class="stat-val">'+"{:,.1f}".format(rm)+'</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-h">Live Inventory Distribution</div>', unsafe_allow_html=True)
    cards = st.columns(5)
    sum_rows = []

    idx = 0
    for _, row in df_p.iterrows():
        pid = row["id"]; nm = row["product_name"]; unit = row["default_unit"]
        
        # TOTAL ADDED: শুধু UPLOAD এ বাড়বে, ISSUE/RETURN এ কমবে না (পয়েন্ট ৪)
        total = safe_num(row.get("total_added_to_system", 0), 0)
        
        # CURRENT STOCK: আসল ব্যালেন্স (Upload + Return - Issue)
        stk = get_stock(df_t, pid)
        dc = dot_cls(stk, total)
        stk_str = "{:.0f}".format(stk)
        total_int = str(int(total))
        
        sum_rows.append({"Product Name": nm, "In Stock": round(stk, 3), "Unit": unit, "Total Added": int(total)})
        
        card_html = (
            '<div class="p-card"><div class="p-top">'
            '<span class="dot '+dc+'"></span>'
            '<div class="p-name">'+nm+'</div></div>'
            '<div class="p-bottom">'
            '<div class="p-total">Added: '+total_int+' '+unit+'</div>'
            '<div class="p-stock">'+stk_str+'</div>'
            '</div></div>'
        )
        with cards[idx % 5]:
            st.markdown(card_html, unsafe_allow_html=True)
        idx += 1

    df_sum = pd.DataFrame(sum_rows)
    st.markdown('<div class="sec-h">Data Extraction Hub</div>', unsafe_allow_html=True)
    d1, d2, d3 = st.columns(3)

    with d1:
        st.markdown('<p style="font-size:12px;font-weight:700;color:#334155;margin-bottom:6px">Full Ledger Audit Log</p>', unsafe_allow_html=True)
        if not df_t.empty:
            df_d = df_t.copy()
            df_d["product_name"] = df_d["product_id"].map(p_name_map).fillna("Unknown")
            df_d["created_at"] = df_d["created_at"].apply(ind_dt)
            df_d = explode_serials(df_d)
            ec = [c for c in ["created_at","product_name","item_code","serial_number","quantity","unit","issued_to","invoice_no","action_type"] if c in df_d.columns]
            st.download_button("Download Full Dump CSV", data=to_csv(df_d[ec]), file_name="AssetFlow_FullDump_"+DT_STR+".csv", mime="text/csv", key="d1")

    with d2:
        st.markdown('<p style="font-size:12px;font-weight:700;color:#334155;margin-bottom:6px">System Balance Summary</p>', unsafe_allow_html=True)
        if not df_sum.empty:
            st.download_button("Download Summary CSV", data=to_csv(df_sum), file_name="AssetFlow_Summary_"+DT_STR+".csv", mime="text/csv", key="d2")

    with d3:
        st.markdown('<p style="font-size:12px;font-weight:700;color:#334155;margin-bottom:6px">Targeted Asset Extraction</p>', unsafe_allow_html=True)
        sel = st.selectbox("Select Product", df_p["product_name"].tolist(), key="cs", label_visibility="collapsed")
        if sel:
            tid = df_p[df_p["product_name"].eq(sel)]["id"].values[0]
            df_is = df_t[(df_t["product_id"].eq(tid)) & (df_t["action_type"].eq("ISSUE"))].copy()
            if not df_is.empty:
                df_is["created_at"] = df_is["created_at"].apply(ind_dt)
                df_is["Product"] = sel; df_is = explode_serials(df_is)
                ec = [c for c in ["created_at","Product","item_code","serial_number","quantity","unit","issued_to","invoice_no"] if c in df_is.columns]
                st.download_button("Download "+sel+" Logs", data=to_csv(df_is[ec]), file_name="AssetFlow_"+sel.lower().replace(" ","_")+"_Issued_"+DT_STR+".csv", mime="text/csv", key="d3")
            else:
                st.markdown('<p style="font-size:11px;color:#DC2626;margin-top:4px;font-weight:600">No issue records found.</p>', unsafe_allow_html=True)

# ==========================================
# TRANSACTION
# ==========================================
elif page == "Transaction":
    if df_p.empty:
        st.warning("Add products to master catalog first."); st.stop()

    cl, cr = st.columns(2)
    with cl:
        st.markdown('<div class="form-sec">Asset Parameters</div>', unsafe_allow_html=True)
        sel_prod = st.selectbox("Product *", df_p["product_name"].tolist(), key="tp")
        item_code = st.text_input("Item Code *", placeholder="Comma-separated for bulk: IC-001, IC-002", key="tc")
        serial = st.text_area("Serial Number(s) *", placeholder="Comma-separated: SN-001, SN-002", height=60, key="ts")
        st.markdown('<div class="hint">UPLOAD: comma = separate entries. ISSUE/RETURN: must match uploads.</div>', unsafe_allow_html=True)
        unit = st.selectbox("Unit *", UNITS, key="tu")
        qty = st.number_input("Quantity *", min_value=0.001, step=0.001, format="%.3f", key="tq")

    with cr:
        st.markdown('<div class="form-sec">Workflow Action</div>', unsafe_allow_html=True)
        action = st.selectbox("Action *", ["ISSUE","RETURN","UPLOAD"], key="ta")
        issued_to_label = "Issued To *" if action != "UPLOAD" else "Issued To"
        issued_to = st.text_input(issued_to_label, placeholder="Person or site name", key="ti")
        invoice = st.text_input("Invoice / DC No *", placeholder="e.g. DC-42", key="tn")
        st.text_input("DateTime (Auto)", value=NOW.strftime("%d-%b-%Y  %H:%M:%S"), disabled=True, key="td")
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.button("Commit Transaction", use_container_width=True, type="primary")

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

        pid = int(df_p[df_p["product_name"].eq(sel_prod)]["id"].values[0])

        if action == "UPLOAD":
            codes = [c.strip() for c in item_code.split(",") if c.strip()]
            serials = [s.strip() for s in serial.split(",") if s.strip()]
            if not codes:
                st.error("No valid Item Code."); st.stop()
            ok = 0
            for i, code in enumerate(codes):
                sn = serials[i] if i < len(serials) else ""
                payload = {
                    "product_id": pid, "item_code": code, "serial_number": sn,
                    "quantity": qty, "unit": unit, "issued_to": "",
                    "invoice_no": invoice.strip(), "action_type": "UPLOAD",
                    "created_at": datetime.now().isoformat()
                }
                try:
                    res = supabase.table("tpl_inv_transactions").insert(payload).execute()
                    if res.data: ok += 1
                except Exception as ex:
                    st.error("Failed for "+code+": "+str(ex))

            # TOTAL ADDED SYSTEM শুধু UPLOAD এ বাড়বে
            if ok > 0:
                try:
                    curr_res = supabase.table("tpl_inv_products").select("total_added_to_system").eq("id", pid).execute()
                    curr_val = safe_num(curr_res.data[0]["total_added_to_system"]) if curr_res.data else 0.0
                    new_val = curr_val + (qty * ok)
                    supabase.table("tpl_inv_products").update({"total_added_to_system": new_val}).eq("id", pid).execute()
                except Exception as ex:
                    st.warning("Saved but total counter update failed: "+str(ex))
                st.success("Uploaded "+str(ok)+" item(s)! Total counter updated.")
                load_data.clear()
                st.rerun()
        else:
            ic = item_code.strip(); sn = serial.strip()
            if not df_t.empty:
                uploads = df_t[df_t["action_type"].eq("UPLOAD")]
                if ic not in uploads["item_code"].values:
                    st.error("Item Code '"+ic+"' not found in uploads!"); st.stop()
                if sn:
                    match = uploads[(uploads["item_code"].eq(ic)) & (uploads["serial_number"].eq(sn))]
                    if match.empty:
                        st.error("Serial '"+sn+"' not found for '"+ic+"'!"); st.stop()
            if action == "ISSUE":
                cs = get_stock(df_t, pid)
                if qty > cs:
                    st.error("Insufficient stock! Available: "+"{:.3f}".format(cs)+" "+unit); st.stop()
            payload = {
                "product_id": pid, "item_code": ic, "serial_number": sn,
                "quantity": qty, "unit": unit, "issued_to": issued_to.strip(),
                "invoice_no": invoice.strip(), "action_type": action,
                "created_at": datetime.now().isoformat()
            }
            try:
                res = supabase.table("tpl_inv_transactions").insert(payload).execute()
                if res.data:
                    st.success("Committed: "+action+" "+"{:.3f}".format(qty)+" "+unit+" - "+ic)
                    load_data.clear(); st.rerun()
                else:
                    st.error("Insert failed. Check RLS.")
            except Exception as ex:
                st.error("DB Error: "+str(ex))

# ==========================================
# REPORTS
# ==========================================
elif page == "Reports":
    if df_t.empty:
        st.info("No transaction data available."); st.stop()

    df_r = df_t.copy()
    if not df_p.empty:
        pmap = df_p.set_index("id")["product_name"].to_dict()
        df_r["product_name"] = df_r["product_id"].map(pmap).fillna("Unknown")
    df_r["created_at"] = pd.to_datetime(df_r["created_at"], errors="coerce")
    df_r["_d"] = df_r["created_at"].dt.date
    mn = df_r["_d"].min() if df_r["_d"].notna().any() else NOW.date()
    mx = df_r["_d"].max() if df_r["_d"].notna().any() else NOW.date()

    st.markdown('<div class="form-sec" style="margin-bottom:14px">Filter Criteria</div>', unsafe_allow_html=True)
    f1, f2, f3, f4, f5 = st.columns(5)
    with f1: df_ = st.date_input("From", value=mn, key="rf")
    with f2: dt_ = st.date_input("To", value=mx, key="rt")
    with f3: it_ = st.multiselect("Issued To", sorted(df_r["issued_to"].dropna().unique()), key="ri")
    with f4: im_ = st.multiselect("Item", sorted(df_p["product_name"].tolist()), key="rm")
    with f5: st_ = st.multiselect("Type", ["ISSUE","RETURN","UPLOAD"], key="rs")

    iv_ = st.multiselect("Invoice No", sorted(df_r["invoice_no"].dropna().unique()), key="rv")

    df_f = df_r.copy()
    if df_ != mn: df_f = df_f[df_f["_d"] >= df_]
    if dt_ != mx: df_f = df_f[df_f["_d"] <= dt_]
    if it_: df_f = df_f[df_f["issued_to"].isin(it_)]
    if im_: df_f = df_f[df_f["product_name"].isin(im_)]
    if st_: df_f = df_f[df_f["action_type"].isin(st_)]
    if iv_: df_f = df_f[df_f["invoice_no"].isin(iv_)]

    r1, r2 = st.columns([2, 1])
    with r1:
        st.markdown('<p style="font-size:13px;margin-top:10px;font-weight:700;color:#334155">Showing <span style="color:#0EA5E9;font-weight:800">'+str(len(df_f))+'</span> records</p>', unsafe_allow_html=True)
    with r2:
        if not df_f.empty:
            df_ex = df_f.copy()
            df_ex["created_at"] = df_ex["created_at"].apply(ind_dt)
            df_ex = explode_serials(df_ex)
            ec = [c for c in ["created_at","product_name","item_code","serial_number","quantity","unit","issued_to","invoice_no","action_type"] if c in df_ex.columns]
            st.download_button("Export Filtered Logs", data=to_csv(df_ex[ec]), file_name="AssetFlow_Report_"+DT_STR+".csv", mime="text/csv", key="dr")

    if not df_f.empty:
        df_s = df_f.copy()
        df_s["created_at"] = df_s["created_at"].apply(ind_dt)
        df_s = explode_serials(df_s)
        ec = [c for c in ["created_at","product_name","item_code","serial_number","quantity","unit","issued_to","invoice_no","action_type"] if c in df_s.columns]
        df_s = df_s[ec].rename(columns={"created_at":"Date","product_name":"Product","item_code":"Code","serial_number":"Serial","quantity":"Qty","unit":"Unit","issued_to":"Issued To","invoice_no":"Invoice","action_type":"Action"})
        st.dataframe(df_s, use_container_width=True, hide_index=True, height=440)
    else:
        st.warning("No records match this filter.")
