```python
import streamlit as st
import pandas as pd
from supabase import create_client, Client
import os
from datetime import datetime

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="KCCL Bangla", layout="wide")

# ---------------- AUTH ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- LOGIN PAGE ----------------
if not st.session_state.logged_in:
    st.markdown("""
    <style>
    section[data-testid="stSidebar"]{display:none;}
    header{display:none;}
    .block-container{padding-top:30px;}
    .title{
        text-align:center;
        font-size:24px;
        font-weight:800;
        margin-bottom:50px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="title">KCCL Bangla</div>', unsafe_allow_html=True)

    with st.form("login"):
        username = st.text_input("Login")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Sign In")

        if submit:
            if username == "admin" and password == "kccl@2026":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid Login")

    st.stop()

# ---------------- MAIN CSS ----------------
st.markdown("""
<style>
section[data-testid="stSidebar"]{
    background:#0B0F19 !important;
}
section[data-testid="stSidebar"] *{
    color:white !important;
}
.stat-box{
    background:white;
    padding:20px;
    border-radius:10px;
    text-align:center;
    border:1px solid #ddd;
}
.stat-lbl{
    font-size:12px;
    color:gray;
}
.stat-val{
    font-size:26px;
    font-weight:700;
}
.p-card{
    background:white;
    border:1px solid #ddd;
    border-radius:10px;
    padding:12px;
    margin-bottom:10px;
}
.p-name{
    font-weight:700;
}
.p-stock{
    font-size:22px;
    font-weight:700;
}
.p-total{
    font-size:12px;
    color:gray;
}
.logout-btn{
    position:fixed;
    bottom:20px;
    width:220px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("### KCCL Bangla")
    page = st.radio("", ["Dashboard", "Transaction", "Reports"])

    st.markdown("<br><br><br><br><br><br><br><br>", unsafe_allow_html=True)

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# ---------------- DATA ----------------
COLS_P = ["id", "product_name", "default_unit", "total_added_to_system"]
COLS_T = ["id", "product_id", "quantity", "action_type", "created_at"]

@st.cache_data(ttl=60)
def load_data():
    try:
        p = supabase.table("tpl_inv_products").select(",".join(COLS_P)).execute()
        df_p = pd.DataFrame(p.data)
    except:
        df_p = pd.DataFrame(columns=COLS_P)

    try:
        t = supabase.table("tpl_inv_transactions").select(",".join(COLS_T)).execute()
        df_t = pd.DataFrame(t.data)
    except:
        df_t = pd.DataFrame(columns=COLS_T)

    return df_p, df_t

def get_stock(df_t, pid):
    if df_t.empty:
        return 0
    m = df_t[df_t["product_id"] == pid]
    up = m[m["action_type"] == "UPLOAD"]["quantity"].sum()
    rt = m[m["action_type"] == "RETURN"]["quantity"].sum()
    iss = m[m["action_type"] == "ISSUE"]["quantity"].sum()
    return (up + rt) - iss

df_p, df_t = load_data()

# ---------------- DASHBOARD ----------------
if page == "Dashboard":
    total_stock = 0
    issued_month = 0
    returned_month = 0

    for _, row in df_p.iterrows():
        total_stock += get_stock(df_t, row["id"])

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="stat-box">
        <div class="stat-lbl">Active Items</div>
        <div class="stat-val">{len(df_p)}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="stat-box">
        <div class="stat-lbl">Total Stock</div>
        <div class="stat-val">{total_stock}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="stat-box">
        <div class="stat-lbl">Issued</div>
        <div class="stat-val">{issued_month}</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="stat-box">
        <div class="stat-lbl">Returned</div>
        <div class="stat-val">{returned_month}</div>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("Live Inventory")

    cols = st.columns(4)

    for i, row in enumerate(df_p.iterrows()):
        row = row[1]
        stock = get_stock(df_t, row["id"])

        with cols[i % 4]:
            st.markdown(f"""
            <div class="p-card">
                <div class="p-name">{row["product_name"]}</div>
                <div class="p-total">Added: {row["total_added_to_system"]} {row["default_unit"]}</div>
                <div class="p-stock">{stock}</div>
            </div>
            """, unsafe_allow_html=True)

# ---------------- TRANSACTION ----------------
elif page == "Transaction":
    st.subheader("Transaction Entry")

    product = st.selectbox("Product", df_p["product_name"].tolist())
    qty = st.number_input("Quantity", min_value=1.0)
    action = st.selectbox("Action", ["UPLOAD", "ISSUE", "RETURN"])

    if st.button("Submit"):
        pid = df_p[df_p["product_name"] == product]["id"].values[0]

        payload = {
            "product_id": int(pid),
            "quantity": qty,
            "action_type": action,
            "created_at": datetime.now().isoformat()
        }

        supabase.table("tpl_inv_transactions").insert(payload).execute()

        if action == "UPLOAD":
            current = df_p[df_p["id"] == pid]["total_added_to_system"].values[0]
            supabase.table("tpl_inv_products").update({
                "total_added_to_system": current + qty
            }).eq("id", pid).execute()

        st.success("Transaction Added")
        load_data.clear()
        st.rerun()

# ---------------- REPORTS ----------------
elif page == "Reports":
    st.subheader("Transaction Reports")

    if not df_t.empty:
        st.dataframe(df_t, use_container_width=True)
    else:
        st.info("No records found.")
```
