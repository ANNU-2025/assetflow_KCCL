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
# PERSISTENT AUTH — 3-LAYER (JS Cookie + Streamlit Cookie + Query Param)
# ==========================================
_persistent = False
try:
    _av = st.query_params.get("auth", "")
    if isinstance(_av, list):
        _av = _av[0] if _av else ""
    if str(_av) == "1":
        _persistent = True
except Exception:
    pass
if not _persistent:
    try:
        if hasattr(st, "context") and hasattr(st.context, "cookies"):
            if str(st.context.cookies.get("kccl_auth", "")) == "1":
                _persistent = True
    except Exception:
        pass

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = _persistent

def _set_auth(val):
    st.session_state["logged_in"] = val
    if val:
        st.components.v1.html(
            '<script>document.cookie="kccl_auth=1;path=/;max-age=86400;SameSite=Lax";</script>',
            height=0, key="_sc"
        )
        try:
            st.query_params["auth"] = "1"
        except Exception:
            pass
    else:
        st.components.v1.html(
            '<script>document.cookie="kccl_auth=;path=/;max-age=0";</script>',
            height=0, key="_dc"
        )
        try:
            del st.query_params["auth"]
        except Exception:
            try:
                st.query_params.pop("auth", None)
            except Exception:
                pass

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(page_title="AssetFlow KCCL", page_icon="📦", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# LOGIN PAGE
# ==========================================
if not st.session_state["logged_in"]:
    st.components.v1.html("""<script>
    (function(){
        if(document.cookie.indexOf('kccl_auth=1')!==-1){
            var u=new URL(location.href);
            u.searchParams.set('auth','1');
            if(location.search!==u.search) location.replace(u.toString());
        }
    })();
    </script>""", height=0, key="_ac")

    st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    section[data-testid='stSidebar']{display:none!important}
    header[data-testid='stHeader']{display:none!important}
    footer{visibility:hidden!important}
    #MainMenu{visibility:hidden!important}
    .stApp{background:#F1F5F9!important}
    .block-container{display:flex!important;flex-direction:column!important;justify-content:center!important;align-items:center!important;min-height:100vh!important;max-width:100%!important;padding:20px!important}
    .block-container > div[data-testid="stVerticalBlock"]{width:100%!important;max-width:440px!important}
    .login-card{background:#FFFFFF!important;border-radius:20px!important;padding:45px 40px!important;width:100%!important;box-shadow:0 25px 60px rgba(0,0,0,0.06)!important;text-align:center!important}
    .login-brand{font-size:36px!important;font-weight:800!important;color:#0B0F19!important;margin-bottom:35px!important;font-family:'Inter',sans-serif!important;letter-spacing:-1px!important}
    .login-card label p{color:#334155!important;font-size:12px!important;font-weight:700!important;text-align:left!important}
    .login-card input{background:#F8FAFC!important;border:2px solid #E2E8F0!important;border-radius:10px!important;color:#0F172A!important}
    .login-card input:focus{border-color:#0EA5E9!important}
    .login-card button{background:#0B0F19!important;color:#FFFFFF!important;border:none!important;border-radius:10px!important;font-weight:700!important;padding:12px!important;margin-top:10px!important}
    .login-card button:hover{background:#1E293B!important}
    </style>""", unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 1.3, 1])
    with mid:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<div class="login-brand">KCCL Bangla</div>', unsafe_allow_html=True)
        with st.form("lf", clear_on_submit=False):
            u = st.text_input("Username", placeholder="Enter username")
            p = st.text_input("Password", type="password", placeholder="Enter password")
            if st.form_submit_button("Sign In", use_container_width=True):
                if u == "admin" and p == "kccl@2026":
                    _set_auth(True)
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please try again.")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ==========================================
# MAIN APP CSS
# ==========================================
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.stApp{background:#F1F5F9!important;color:#0F172A!important;font-family:'Inter',system-ui,sans-serif!important}
.block-container{padding:.8rem 2rem!important;max-width:1560px;margin:0 auto;position:relative;z-index:1}
header[data-testid="stHeader"]{visibility:hidden!important;height:0!important}
#MainMenu, footer{visibility:hidden!important}
section[data-testid="stSidebar"]{background:#0B0F19!important;border-right:1px solid #1E293B!important}
section[data-testid="stSidebar"] > div:first-child{display:flex!important;flex-direction:column!important;height:100vh!important}
.sb-header-title{font-size:16px!important;font-weight:700!important;color:#FFFFFF!important;text-align:center!important;padding:20px 10px 10px 10px!important;letter-spacing:.5px!important}
.sb-nav-label{font-size:11px!important;color:#94A3B8!important;text-transform:uppercase!important;letter-spacing:1.5px!important;font-weight:700!important;padding:15px 0 5px 0!important;text-align:center!important}
section[data-testid="stSidebar"] section[data-testid="stRadio"] div[role="radiogroup"] > div{padding:10px 20px!important;border-left:4px solid transparent!important;transition:none!important;margin:0!important}
section[data-testid="stSidebar"] section[data-testid="stRadio"] label p{color:#FFFFFF!important;font-size:14px!important;font-weight:600!important}
section[data-testid="stSidebar"] section[data-testid="stRadio"] div[role="radiogroup"] > div:hover{background:transparent!important}
section[data-testid="stSidebar"] section[data-testid="stRadio"] div[role="radiogroup"] > div[aria-checked="true"]{background:#111827!important;border-left:4px solid #FFFFFF!important}
section[data-testid="stSidebar"] section[data-testid="stRadio"] div[role="radiogroup"] > div[aria-checked="true"] label p{font-weight:700!important}
.sb-logout-box{margin-top:auto!important;padding:20px!important;border-top:1px solid #1E293B!important;background:#0B0F19!important}
.sb-logout-box button{background:transparent!important;color:#FFFFFF!important;border:1px solid #DC2626!important;border-radius:8px!important;padding:8px!important;font-weight:600!important;font-size:13px!important}
.sb-logout-box button:hover{background:#DC2626!important;color:#FFFFFF!important;box-shadow:0 4px 12px rgba(220,38,38,0.2)!important}
.p-card{background:#FFFFFF!important;border:1px solid #E2E8F0!important;border-radius:12px!important;padding:16px 18px!important;display:flex!important;flex-direction:column!important;justify-content:space-between!important;height:105px!important;box-shadow:0 1px 2px rgba(0,0,0,0.03)!important;transition:transform .15s ease,border-color .15s ease,background .15s ease!important}
.p-card:hover{border-color:#0EA5E9!important;background:#F0F9FF!important;transform:translateY(-2px)!important}
.p-top{display:flex!important;align-items:center!important;gap:8px!important}
.p-name{font-size:13px;font-weight:700;color:#0F172A!important;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.p-bottom{display:flex!important;flex-direction:column!important;gap:2px!important;margin-top:6px!important}
.p-stock{font-size:24px;font-weight:800;color:#059669!important;line-height:1.1}
.p-total{font-size:11px;color:#64748B!important;font-weight:600}
.dot{display:inline-block;width:8px;height:8px;border-radius:50%;flex-shrink:0}
.dot-g{background:#059669}.dot-y{background:#D97706}.dot-r{background:#DC2626}
.sec-h{font-size:15px!important;font-weight:800!important;color:#0B0F19!important;margin:22px 0 12px!important;padding-bottom:8px!important;border-bottom:2px solid #0B0F19!important}
label p,.stDateInput>label,.stTextArea>label,.stSelectbox>label,.stNumberInput>label{font-size:12px!important;font-weight:700!important;color:#334155!important}
.form-sec{font-size:11px!important;font-weight:800!important;color:#0B0F19!important;text-transform:uppercase!important;margin-bottom:12px!important;padding-bottom:6px!important;border-bottom:2px solid #0EA5E9!important;display:inline-block!important}
.hint{font-size:11px!important;color:#94A3B8!important;margin-top:-2px!important}
.stTextInput>div>div>input,.stSelectbox>div>div>select,.stTextArea>div>div>textarea,.stNumberInput>div>div>input,.stDateInput>div>div>input{background:#FFFFFF!important;border:2px solid #E2E8F0!important;border-radius:10px!important;color:#0F172A!important;font-size:14px!important}
.stButton>button[kind="primary"]{background:#0B0F19!important;color:#FFFFFF!important;border-radius:10px!important;font-weight:700!important;padding:12px 24px!important}
.stDownloadButton>button{background:#0EA5E9!important;color:#FFFFFF!important;border-radius:10px!important;font-weight:700!important;width:100%!important}
</style>""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================
st.sidebar.markdown('<div class="sb-header-title">KCCL Bangla</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sb-nav-label">Navigation</div>', unsafe_allow_html=True)
page = st.sidebar.radio("", ["Dashboard", "Transaction", "Reports"], label_visibility="collapsed")
with st.sidebar:
    st.markdown('<div class="sb-logout-box">', unsafe_allow_html=True)
    if st.button("Logout Session", key="sb_logout_btn", use_container_width=True):
        _set_auth(False)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# CONFIG & DATA
# ==========================================
UNITS = ["PCS", "LTR", "ML", "MTR", "DRUM", "BOX", "KG", "GM", "SET", "PAIR", "ROLL", "CAN", "BOTTLE", "PACK", "SHEET", "BUNDLE", "TUBE", "GAL", "NOS", "KIT"]
COLS_P = ["id", "product_name", "item_code", "default_unit", "total_added_to_system"]
COLS_T = ["id", "product_id", "item_code", "serial_number", "quantity", "unit", "issued_to", "invoice_no", "action_type", "created_at"]

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
    m = dt[dt["product_id"].eq(pid)]
    up = pd.to_numeric(m[m["action_type"].eq("UPLOAD")]["quantity"], errors="coerce").fillna(0).sum()
    rt = pd.to_numeric(m[m["action_type"].eq("RETURN")]["quantity"], errors="coerce").fillna(0).sum()
    is_ = pd.to_numeric(m[m["action_type"].eq("ISSUE")]["quantity"], errors="coerce").fillna(0).sum()
    return float((up + rt) - is_)

def get_serial_net_issue(dt, item_code, serial):
    """Per-serial net issue count: ISSUE - RETURN. >0 means currently issued out."""
    if dt.empty or not serial or not item_code:
        return 0
    m = dt[dt["item_code"].eq(item_code) & dt["serial_number"].eq(serial)]
    issues = pd.to_numeric(m[m["action_type"].eq("ISSUE")]["quantity"], errors="coerce").fillna(0).sum()
    returns = pd.to_numeric(m[m["action_type"].eq("RETURN")]["quantity"], errors="coerce").fillna(0).sum()
    return float(issues - returns)

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
# ROUTER
# ==========================================
NOW = datetime.now()
DT_STR = NOW.strftime("%d%b%Y")
df_p, df_t = load_data()

p_name_map = {}
if not df_p.empty:
    p_name_map = dict(zip(df_p["id"].tolist(), df_p["product_name"].tolist()))

# ==========================================
# DASHBOARD — No stat cards, straight to inventory + downloads
# ==========================================
if page == "Dashboard":
    if df_p.empty:
        st.info("No master entries found.")
        st.stop()

    st.markdown('<div class="sec-h">Live Inventory Distribution</div>', unsafe_allow_html=True)
    cards = st.columns(5)
    sum_rows = []

    idx = 0
    for _, row in df_p.iterrows():
        pid = row["id"]
        nm = row["product_name"]
        unit = row["default_unit"]

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

        sum_rows.append({"Product Name": nm, "In Stock": round(stk, 3), "Unit": unit, "Total Added": int(total_uploads)})

        card_html = (
            '<div class="p-card"><div class="p-top">'
            '<span class="dot ' + dc + '"></span>'
            '<div class="p-name">' + nm + '</div></div>'
            '<div class="p-bottom">'
            '<div class="p-stock">' + stk_str + ' <span style="font-size:13px;font-weight:500;color:#64748B;">In Stock</span></div>'
            '<div class="p-total">Added: ' + total_int + ' ' + unit + '</div>'
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
            ec = [c for c in ["created_at", "product_name", "item_code", "serial_number", "quantity", "unit", "issued_to", "invoice_no", "action_type"] if c in df_d.columns]
            st.download_button("Download Full Dump CSV", data=to_csv(df_d[ec]), file_name="AssetFlow_FullDump_" + DT_STR + ".csv", mime="text/csv", key="d1")

    with d2:
        st.markdown('<p style="font-size:12px;font-weight:700;color:#334155;margin-bottom:6px">System Balance Summary</p>', unsafe_allow_html=True)
        if not df_sum.empty:
            st.download_button("Download Summary CSV", data=to_csv(df_sum), file_name="AssetFlow_Summary_" + DT_STR + ".csv", mime="text/csv", key="d2")

    with d3:
        st.markdown('<p style="font-size:12px;font-weight:700;color:#334155;margin-bottom:6px">Targeted Asset Extraction</p>', unsafe_allow_html=True)
        sel = st.selectbox("Select Product", df_p["product_name"].tolist(), key="cs", label_visibility="collapsed")
        if sel:
            tid = df_p[df_p["product_name"].eq(sel)]["id"].values[0]
            df_is = df_t[(df_t["product_id"].eq(tid)) & (df_t["action_type"].eq("ISSUE"))].copy()
            if not df_is.empty:
                df_is["created_at"] = df_is["created_at"].apply(ind_dt)
                df_is["Product"] = sel
                df_is = explode_serials(df_is)
                ec = [c for c in ["created_at", "Product", "item_code", "serial_number", "quantity", "unit", "issued_to", "invoice_no"] if c in df_is.columns]
                st.download_button("Download " + sel + " Logs", data=to_csv(df_is[ec]), file_name="AssetFlow_" + sel.lower().replace(" ", "_") + "_Issued_" + DT_STR + ".csv", mime="text/csv", key="d3")
            else:
                st.markdown('<p style="font-size:11px;color:#EF4444;margin-top:4px;font-weight:600">No issue records found.</p>', unsafe_allow_html=True)

# ==========================================
# TRANSACTION — Serial-level ISSUE/RETURN guard
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
        serial = st.text_area("Serial Number(s) *", placeholder="Comma-separated: SN-001, SN-002, SN-003", height=60, key="ts")
        st.markdown('<div class="hint">UPLOAD: comma-separated serials = each gets its own row.<br>Quantity is auto-divided equally among serials.</div>', unsafe_allow_html=True)
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
            errs.append("Issued To is required for ISSUE / RETURN.")
        if not invoice.strip():
            errs.append("Invoice / DC No is required.")
        if errs:
            for e in errs:
                st.error(e)
            st.stop()

        pid = int(df_p[df_p["product_name"].eq(sel_prod)]["id"].values[0])

        # ---------- UPLOAD ----------
        if action == "UPLOAD":
            codes = [c.strip() for c in item_code.split(",") if c.strip()]
            serials = [s.strip() for s in serial.split(",") if s.strip()]
            if not codes:
                st.error("No valid Item Code provided.")
                st.stop()

            num_entries = max(len(codes), len(serials))
            per_qty = round(qty / num_entries, 3)
            distributed = per_qty * (num_entries - 1)
            last_qty = round(qty - distributed, 3)

            ok = 0
            for i in range(num_entries):
                code = codes[i] if i < len(codes) else (codes[-1] if codes else "")
                sn = serials[i] if i < len(serials) else ""
                entry_qty = last_qty if i == num_entries - 1 else per_qty
                payload = {
                    "product_id": pid, "item_code": code, "serial_number": sn,
                    "quantity": entry_qty, "unit": unit, "issued_to": "",
                    "invoice_no": invoice.strip(), "action_type": "UPLOAD",
                    "created_at": datetime.now().isoformat()
                }
                try:
                    res = supabase.table("tpl_inv_transactions").insert(payload).execute()
                    if res.data:
                        ok += 1
                except Exception as ex:
                    st.error("Failed for " + code + ": " + str(ex))
            if ok > 0:
                st.success("Uploaded " + str(ok) + " item(s) — " + "{:.3f}".format(per_qty) + " " + unit + " each (total " + "{:.3f}".format(qty) + ")")
                load_data.clear()
                st.rerun()

        # ---------- ISSUE ----------
        elif action == "ISSUE":
            ic = item_code.strip()
            sn = serial.strip()

            if not df_t.empty:
                uploads = df_t[df_t["action_type"].eq("UPLOAD")]
                # Check 1: item_code must exist in uploads
                if ic not in uploads["item_code"].values:
                    st.error("Item Code '" + ic + "' not found in uploads!")
                    st.stop()
                # Check 2: serial must exist in uploads for that item_code
                if sn:
                    match = uploads[(uploads["item_code"].eq(ic)) & (uploads["serial_number"].eq(sn))]
                    if match.empty:
                        st.error("Serial '" + sn + "' not found in uploads for '" + ic + "'!")
                        st.stop()
                    # Check 3: serial must NOT be currently issued out
                    net = get_serial_net_issue(df_t, ic, sn)
                    if net > 0:
                        st.error("Serial '" + sn + "' is already issued out! Return it first before re-issuing.")
                        st.stop()

            # Check 4: product-level stock
            cs = get_stock(df_t, pid)
            if qty > cs:
                st.error("Insufficient stock! Available: " + "{:.3f}".format(cs) + " " + unit)
                st.stop()

            payload = {
                "product_id": pid, "item_code": ic, "serial_number": sn,
                "quantity": qty, "unit": unit, "issued_to": issued_to.strip(),
                "invoice_no": invoice.strip(), "action_type": "ISSUE",
                "created_at": datetime.now().isoformat()
            }
            try:
                res = supabase.table("tpl_inv_transactions").insert(payload).execute()
                if res.data:
                    st.success("Issued: " + "{:.3f}".format(qty) + " " + unit + " — " + ic + " / " + sn)
                    load_data.clear()
                    st.rerun()
                else:
                    st.error("Insert failed. Check RLS.")
            except Exception as ex:
                st.error("DB Error: " + str(ex))

        # ---------- RETURN ----------
        elif action == "RETURN":
            ic = item_code.strip()
            sn = serial.strip()

            if not df_t.empty:
                # Check 1: item_code must exist
                all_codes = df_t["item_code"].values
                if ic not in all_codes:
                    st.error("Item Code '" + ic + "' not found in any transaction!")
                    st.stop()

                # Check 2: serial must have been ISSUED (net issue > 0)
                if sn:
                    net = get_serial_net_issue(df_t, ic, sn)
                    if net <= 0:
                        st.error("Serial '" + sn + "' has NOT been issued or already returned! Cannot return.")
                        st.stop()

            payload = {
                "product_id": pid, "item_code": ic, "serial_number": sn,
                "quantity": qty, "unit": unit, "issued_to": issued_to.strip(),
                "invoice_no": invoice.strip(), "action_type": "RETURN",
                "created_at": datetime.now().isoformat()
            }
            try:
                res = supabase.table("tpl_inv_transactions").insert(payload).execute()
                if res.data:
                    st.success("Returned: " + "{:.3f}".format(qty) + " " + unit + " — " + ic + " / " + sn)
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

    st.markdown('<div class="form-sec" style="margin-bottom:14px">Filter Criteria</div>', unsafe_allow_html=True)
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
        st.markdown('<p style="font-size:13px;margin-top:10px;font-weight:700;color:#334155">Showing <span style="color:#0EA5E9;font-weight:800">' + str(len(df_f)) + '</span> records</p>', unsafe_allow_html=True)
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
        st.dataframe(df_s, use_container_width=True, hide_index=True, height=440)
    else:
        st.warning("No records match this filter.")
