import streamlit as st
import pandas as pd
from supabase import create_client, Client
import os
from datetime import datetime

# ==========================================
# 1. SUPABASE CONFIGURATION
# ==========================================
# রিয়াল deploy-এর সময় environment variable থেকে নিবে
# এখানে template হিসেবে hardcoded আছে
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://emdjnndnsdebhbzebrsg.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVtZGpubmRuc2RlYmhiemVicnNnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODExNzU4NDYsImV4cCI6MjA5Njc1MTg0Nn0.ypy3k30Nbp2caJaNXpwxbrnUzrOLrhwTJ1FZwW5L8Fc")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ==========================================
# 2. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="AssetFlow KCCL",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 3. CUSTOM CSS INJECTION
# ==========================================
CUSTOM_CSS = """
<style>
/* === Global Overrides === */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}
.stApp {
    background-color: #0A0F16;
    color: #E6EDF3;
}

/* === Sidebar Styling === */
section[data-testid="stSidebar"] {
    background-color: #111921;
    border-right: 1px solid #1B2636;
}
section[data-testid="stSidebar"] .stMarkdown {
    color: #E6EDF3;
}

/* === Card Containers === */
.inv-card {
    background: #141D28;
    border: 1px solid #1B2636;
    border-radius: 12px;
    padding: 18px;
    transition: all 0.25s ease;
    position: relative;
    overflow: hidden;
}
.inv-card:hover {
    border-color: rgba(0,229,160,0.3);
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(0,229,160,0.06);
}

/* === Stat Cards === */
.stat-card {
    background: #141D28;
    border: 1px solid #1B2636;
    border-radius: 12px;
    padding: 20px;
    position: relative;
    overflow: hidden;
}
.stat-card::after {
    content: '';
    position: absolute;
    top: -20px; right: -20px;
    width: 80px; height: 80px;
    border-radius: 50%;
    filter: blur(40px);
    opacity: 0.15;
    pointer-events: none;
}
.stat-green::after { background: #00E5A0; }
.stat-orange::after { background: #FF6B35; }
.stat-blue::after { background: #38BDF8; }
.stat-yellow::after { background: #F59E0B; }

/* === Stock Indicator Dots === */
.dot {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    margin-right: 6px;
}
.dot-good { background: #00E5A0; box-shadow: 0 0 8px #00E5A0; }
.dot-low { background: #F59E0B; box-shadow: 0 0 8px #F59E0B; }
.dot-critical { background: #EF4444; box-shadow: 0 0 8px #EF4444; }

/* === Badges === */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.3px;
}
.badge-issue { background: rgba(255,107,53,0.12); color: #FF6B35; }
.badge-return { background: rgba(0,229,160,0.1); color: #00E5A0; }
.badge-upload { background: rgba(56,189,248,0.1); color: #38BDF8; }

/* === Table Styling === */
.dataframe th {
    background-color: #111921 !important;
    color: #8B949E !important;
    font-size: 11px !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-weight: 700 !important;
    border-bottom: 1px solid #1B2636 !important;
}
.dataframe td {
    color: #E6EDF3 !important;
    font-size: 13px !important;
    border-bottom: 1px solid #1B2636 !important;
}
.dataframe tr:hover td {
    background-color: rgba(0,229,160,0.03) !important;
}

/* === Download Buttons === */
.stDownloadButton > button {
    background: #141D28;
    border: 1px solid #1B2636;
    color: #E6EDF3;
    border-radius: 8px;
    transition: all 0.2s ease;
}
.stDownloadButton > button:hover {
    border-color: #00E5A0;
    color: #00E5A0;
    background: rgba(0,229,160,0.05);
}

/* === Form Inputs === */
.stTextInput > div > div > input,
.stSelectbox > div > div > select,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea {
    background-color: #0E151E !important;
    color: #E6EDF3 !important;
    border-color: #1B2636 !important;
    border-radius: 8px !important;
}
.stTextInput > div > div > input:focus,
.stSelectbox > div > div > select:focus,
.stNumberInput > div > div > input:focus {
    border-color: #00E5A0 !important;
    box-shadow: 0 0 0 3px rgba(0,229,160,0.08) !important;
}

/* === Primary Button === */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #00E5A0, #00C98A);
    color: #060A10;
    border: none;
    border-radius: 8px;
    font-weight: 700;
    transition: all 0.2s ease;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 24px rgba(0,229,160,0.3);
}

/* === Section Headers === */
.section-head {
    font-size: 15px;
    font-weight: 700;
    color: #E6EDF3;
    margin-bottom: 14px;
    padding-bottom: 8px;
    border-bottom: 1px solid #1B2636;
}

/* === Hide Streamlit Default Elements === */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header[data-testid="stHeader"] { background-color: #0A0F16; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ==========================================
# 4. LOGO PROVISION (ALL PAGES)
# ==========================================
def render_logo():
    """সব পেজে থাকবে। assets/logo.png থাকলে সেটা দেখাবে, না থাকলে text logo।"""
    logo_path = "assets/logo.png"
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path, width=140)
    else:
        st.sidebar.markdown(
            '<div style="text-align:center;margin-bottom:8px;">'
            '<div style="width:48px;height:48px;margin:0 auto 8px;background:rgba(0,229,160,0.08);'
            'border:1.5px solid rgba(0,229,160,0.25);border-radius:12px;display:flex;'
            'align-items:center;justify-content:center;font-size:22px;">📦</div>'
            '<span style="font-size:18px;font-weight:800;color:#E6EDF3;letter-spacing:-0.5px;">AssetFlow</span><br>'
            '<span style="font-size:11px;color:#484F58;">KCCL Inventory System</span>'
            '</div>',
            unsafe_allow_html=True
        )
    st.sidebar.markdown("---")

render_logo()

# ==========================================
# 5. UNIT OPTIONS LIST (20+ UNITS)
# ==========================================
UNIT_OPTIONS = [
    "PCS", "LTR", "ML", "MTR", "DRUM", "BOX",
    "KG", "GM", "SET", "PAIR", "ROLL", "CAN",
    "BOTTLE", "PACK", "SHEET", "BUNDLE", "TUBE",
    "GAL", "NOS", "KIT"
]

# ==========================================
# 6. HELPER FUNCTIONS
# ==========================================

def fetch_products() -> pd.DataFrame:
    """Supabase থেকে product list আনা। Uncommon table name: tpl_inv_products"""
    try:
        res = supabase.table("tpl_inv_products").select("*").order("product_name").execute()
        return pd.DataFrame(res.data) if res.data else pd.DataFrame()
    except Exception as e:
        st.error(f"Product fetch failed: {e}")
        return pd.DataFrame()


def fetch_transactions() -> pd.DataFrame:
    """Supabase থেকে transaction list আনা। Uncommon table name: tpl_inv_transactions"""
    try:
        res = supabase.table("tpl_inv_transactions").select("*").order("created_at", desc=True).execute()
        return pd.DataFrame(res.data) if res.data else pd.DataFrame()
    except Exception as e:
        st.error(f"Transaction fetch failed: {e}")
        return pd.DataFrame()


def calculate_stock(df_tx: pd.DataFrame, product_id) -> float:
    """একটা product এর current in-stock বের করা।
    Formula: (UPLOAD + RETURN) - ISSUE
    Decimal সাপোর্ট — 0.5 LTR issue হলে 0.5 কাটবে।"""
    if df_tx.empty or "product_id" not in df_tx.columns:
        return 0.0
    p_tx = df_tx[df_tx["product_id"] == product_id]
    uploaded = pd.to_numeric(p_tx[p_tx["action_type"] == "UPLOAD"]["quantity"], errors="coerce").fillna(0).sum()
    returned = pd.to_numeric(p_tx[p_tx["action_type"] == "RETURN"]["quantity"], errors="coerce").fillna(0).sum()
    issued = pd.to_numeric(p_tx[p_tx["action_type"] == "ISSUE"]["quantity"], errors="coerce").fillna(0).sum()
    return float((uploaded + returned) - issued)


def get_stock_status(stock_val, total_added):
    """Stock status অনুযায়ী dot class return করা।"""
    if total_added <= 0:
        return "dot-critical"
    ratio = stock_val / total_added
    if ratio > 0.5:
        return "dot-good"
    elif ratio > 0.15:
        return "dot-low"
    else:
        return "dot-critical"


def action_badge(action_type: str) -> str:
    """Action type অনুযায়ী colored badge HTML return করা।"""
    cls_map = {"ISSUE": "badge-issue", "RETURN": "badge-return", "UPLOAD": "badge-upload"}
    cls = cls_map.get(action_type, "badge-issue")
    return f'<span class="badge {cls}">{action_type}</span>'


def df_to_csv_bytes(df: pd.DataFrame) -> bytes:
    """DataFrame কে CSV bytes-এ convert করা download-এর জন্য।"""
    return df.to_csv(index=False).encode("utf-8")


def safe_numeric(val, default=0.0):
    """সুরক্ষিত number conversion।"""
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


# ==========================================
# 7. LOGIN MECHANISM (SESSION-BASED)
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.subheader("🔑 System Secure Login")
    with st.form("login_form"):
        col_u, col_p = st.columns(2)
        with col_u:
            username = st.text_input("Username", placeholder="Enter username")
        with col_p:
            password = st.text_input("Password", type="password", placeholder="Enter password")
        submitted = st.form_submit_button("Sign In", use_container_width=True)

        if submitted:
            if username == "admin" and password == "kccl@2026":
                st.session_state["logged_in"] = True
                st.rerun()
            else:
                st.error("Invalid Username or Password!")

    st.caption("Template credentials — `admin` / `kccl@2026`")
    st.stop()

# Logout button
if st.sidebar.button("🔓 Logout", use_container_width=True):
    st.session_state["logged_in"] = False
    st.rerun()

st.sidebar.markdown("---")

# ==========================================
# 8. NAVIGATION
# ==========================================
page = st.sidebar.radio(
    "📌 Navigation Menu",
    ["Dashboard", "Transaction", "Reports"],
    label_visibility="collapsed"
)

# ==========================================
# 9. DATA LOADING (ALL PAGES NEED THIS)
# ==========================================
@st.cache_data(ttl=10)
def load_data():
    """প্রতি 10 সেকেন্ডে cache refresh — রিয়েলটাইমের কাছাকাছি।"""
    return fetch_products(), fetch_transactions()

df_products, df_transactions = load_data()

# ==========================================
# 10. DASHBOARD PAGE
# ==========================================
if page == "Dashboard":
    st.header("📈 Inventory Dashboard Summary")
    st.caption("Real-time product stock overview with download operations")

    if df_products.empty:
        st.info("No products found in `tpl_inv_products` table. Please add products via Supabase first.")
        st.stop()

    # ---- Summary Stats ----
    total_products = len(df_products)
    total_stock = 0.0
    issued_month = 0.0
    returned_month = 0.0
    now = datetime.now()

    for _, row in df_products.iterrows():
        total_stock += calculate_stock(df_transactions, row["id"])

    if not df_transactions.empty:
        df_tx_month = df_transactions.copy()
        df_tx_month["created_at"] = pd.to_datetime(df_tx_month["created_at"], errors="coerce")
        df_tx_month = df_tx_month.dropna(subset=["created_at"])
        mask = (df_tx_month["created_at"].dt.month == now.month) & (df_tx_month["created_at"].dt.year == now.year)
        issued_month = safe_numeric(df_tx_month[mask & (df_tx_month["action_type"] == "ISSUE")]["quantity"].sum())
        returned_month = safe_numeric(df_tx_month[mask & (df_tx_month["action_type"] == "RETURN")]["quantity"].sum())

    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    with stat_col1:
        st.markdown(
            f'<div class="stat-card stat-green">'
            f'<div style="font-size:11px;color:#8B949E;text-transform:uppercase;letter-spacing:0.5px;font-weight:600;">Total Products</div>'
            f'<div style="font-size:28px;font-weight:800;margin-top:4px;">{total_products}</div>'
            f'</div>', unsafe_allow_html=True
        )
    with stat_col2:
        st.markdown(
            f'<div class="stat-card stat-blue">'
            f'<div style="font-size:11px;color:#8B949E;text-transform:uppercase;letter-spacing:0.5px;font-weight:600;">Total In Stock</div>'
            f'<div style="font-size:28px;font-weight:800;margin-top:4px;">{total_stock:,.1f}</div>'
            f'</div>', unsafe_allow_html=True
        )
    with stat_col3:
        st.markdown(
            f'<div class="stat-card stat-orange">'
            f'<div style="font-size:11px;color:#8B949E;text-transform:uppercase;letter-spacing:0.5px;font-weight:600;">Issued This Month</div>'
            f'<div style="font-size:28px;font-weight:800;margin-top:4px;">{issued_month:,.1f}</div>'
            f'</div>', unsafe_allow_html=True
        )
    with stat_col4:
        st.markdown(
            f'<div class="stat-card stat-yellow">'
            f'<div style="font-size:11px;color:#8B949E;text-transform:uppercase;letter-spacing:0.5px;font-weight:600;">Returned This Month</div>'
            f'<div style="font-size:28px;font-weight:800;margin-top:4px;">{returned_month:,.1f}</div>'
            f'</div>', unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- Product Cards ----
    st.markdown('<div class="section-head">📦 Product Inventory Cards</div>', unsafe_allow_html=True)

    card_cols = st.columns(4)
    summary_rows = []

    for idx, row in df_products.iterrows():
        p_id = row["id"]
        p_name = row["product_name"]
        i_code = row["item_code"]
        u_type = row["default_unit"]
        total_added = safe_numeric(row.get("total_added_to_system", 0), default=0)

        stock = calculate_stock(df_transactions, p_id)
        dot_cls = get_stock_status(stock, total_added)

        summary_rows.append({
            "Product Name": p_name,
            "Item Code": i_code,
            "In Stock Quantity": f"{stock:.3f} {u_type}",
            "Unit": u_type,
            "Total Added to System": int(total_added)
        })

        with card_cols[idx % 4]:
            st.markdown(
                f'<div class="inv-card">'
                f'<div style="display:flex;align-items:center;gap:6px;margin-bottom:2px;">'
                f'<span class="dot {dot_cls}"></span>'
                f'<span style="font-size:13px;font-weight:600;color:#E6EDF3;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{p_name}</span>'
                f'</div>'
                f'<div style="font-size:11px;color:#484F58;font-family:monospace;margin-bottom:12px;">{i_code}</div>'
                f'<div style="font-size:24px;font-weight:800;color:#E6EDF3;font-family:monospace;">'
                f'{stock:.3f} <span style="font-size:13px;font-weight:500;color:#8B949E;">{u_type}</span></div>'
                f'<div style="height:1px;background:#1B2636;margin:10px 0;"></div>'
                f'<div style="font-size:11px;color:#484F58;">Total Added: <b style="color:#8B949E;">{int(total_added)}</b></div>'
                f'</div>',
                unsafe_allow_html=True
            )

    df_summary = pd.DataFrame(summary_rows)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- 3 Download Buttons ----
    st.markdown('<div class="section-head">📥 Master Download Operations</div>', unsafe_allow_html=True)

    dl_col1, dl_col2, dl_col3 = st.columns(3)

    with dl_col1:
        st.markdown("##### 1. Full Dump Log")
        st.caption("All transactions in one file")
        if not df_transactions.empty:
            st.download_button(
                label="📥 Download Full Dump CSV",
                data=df_to_csv_bytes(df_transactions),
                file_name=f"full_inventory_dump_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="dl_full_dump"
            )
        else:
            st.caption("No transactions to dump yet.")

    with dl_col2:
        st.markdown("##### 2. Product Summary")
        st.caption("In-stock + total count per product")
        if not df_summary.empty:
            st.download_button(
                label="📥 Download Product Summary",
                data=df_to_csv_bytes(df_summary),
                file_name="product_stock_summary.csv",
                mime="text/csv",
                key="dl_prod_summary"
            )

    with dl_col3:
        st.markdown("##### 3. Card-Issued Details")
        st.caption("Click a product to download its ISSUE records")
        if not df_products.empty:
            product_names = df_products["product_name"].tolist()
            selected_card_product = st.selectbox(
                "Choose Product",
                product_names,
                key="card_product_select",
                label_visibility="collapsed"
            )
            if selected_card_product:
                target_id = df_products[df_products["product_name"] == selected_card_product]["id"].values[0]
                df_issued = df_transactions[
                    (df_transactions["product_id"] == target_id) &
                    (df_transactions["action_type"] == "ISSUE")
                ].copy()

                if not df_issued.empty:
                    # Product name column যোগ করা
                    df_issued_export = df_issued.copy()
                    df_issued_export["Product Name"] = selected_card_product
                    export_cols = ["created_at", "Product Name", "item_code", "serial_number",
                                   "quantity", "unit", "issued_to", "invoice_no"]
                    existing_cols = [c for c in export_cols if c in df_issued_export.columns]
                    st.download_button(
                        label=f"📥 Download {selected_card_product} Issued Data",
                        data=df_to_csv_bytes(df_issued_export[existing_cols]),
                        file_name=f"{selected_card_product.lower().replace(' ', '_')}_issued_details.csv",
                        mime="text/csv",
                        key="dl_card_issued"
                    )
                else:
                    st.caption("No ISSUE records for this product.")


# ==========================================
# 11. TRANSACTION PAGE
# ==========================================
elif page == "Transaction":
    st.header("🔄 Stock Transaction Registry")
    st.caption("Issue, return, or upload inventory items with full traceability")

    if df_products.empty:
        st.warning("No products in `tpl_inv_products`. Add products via Supabase first.")
        st.stop()

    # Product map তৈরি
    product_map = {}
    for _, row in df_products.iterrows():
        product_map[row["product_name"]] = {
            "id": row["id"],
            "item_code": row["item_code"],
            "default_unit": row["default_unit"]
        }

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('<div class="section-head">Product & Quantity Details</div>', unsafe_allow_html=True)

        selected_product_name = st.selectbox(
            "Product List *",
            list(product_map.keys()),
            key="tx_product_select"
        )

        # Auto-fill item code (FIXED — disabled)
        target_product = product_map[selected_product_name]
        st.text_input(
            "Item Code (Auto)",
            value=target_product["item_code"],
            disabled=True,
            key="tx_item_code_display"
        )

        serial_number = st.text_area(
            "Serial Number(s)",
            placeholder="Comma-separated: SN-001, SN-002, SN-003",
            height=70,
            key="tx_serial"
        )
        st.caption("Optional. Leave blank if not applicable.", help="Separate multiple serial numbers with commas")

        # Unit dropdown (20 options)
        default_unit = target_product["default_unit"]
        unit_index = UNIT_OPTIONS.index(default_unit) if default_unit in UNIT_OPTIONS else 0
        selected_unit = st.selectbox(
            "Unit Classification *",
            UNIT_OPTIONS,
            index=unit_index,
            key="tx_unit_select"
        )
        st.caption(f"Default: {default_unit}. Override if needed.", help="EDFA = PCS, Alcohol = LTR, etc.")

        # Quantity (decimal support — 0.5 LTR issue possible)
        quantity = st.number_input(
            "Transaction Quantity *",
            min_value=0.001,
            step=0.001,
            format="%.3f",
            key="tx_qty",
            help="Supports decimal: 0.5 LTR issue = 0.5 stock deduction"
        )

    with col_right:
        st.markdown('<div class="section-head">Action & Destination</div>', unsafe_allow_html=True)

        issued_to = st.text_input(
            "Issued To *",
            placeholder="Person, site, or vendor name",
            key="tx_issued_to"
        )

        invoice_no = st.text_input(
            "Invoice / DC Number *",
            placeholder="e.g. INV-2025-042",
            key="tx_invoice"
        )

        action_type = st.selectbox(
            "Action Type *",
            ["ISSUE", "RETURN", "UPLOAD"],
            key="tx_action_select"
        )

        # Auto datetime (FIXED — disabled, always shows current time)
        current_datetime = datetime.now().strftime("%d-%b-%Y  %H:%M:%S")
        st.text_input(
            "Date & Time (Auto Captured)",
            value=current_datetime,
            disabled=True,
            key="tx_datetime_display"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Submit button
        submitted = st.button("⚡ Execute & Commit Transaction", use_container_width=True, type="primary")

    # ---- Submission Logic ----
    if submitted:
        errors = []
        if not selected_product_name:
            errors.append("Select a product.")
        if quantity <= 0:
            errors.append("Quantity must be greater than zero.")
        if action_type != "UPLOAD" and not issued_to.strip():
            errors.append("Issued To is required for ISSUE/RETURN.")
        if not invoice_no.strip():
            errors.append("Invoice / DC Number is required.")

        if errors:
            for err in errors:
                st.error(err)
        else:
            # ISSUE হলে stock validation চেক
            if action_type == "ISSUE":
                current_stock = calculate_stock(df_transactions, target_product["id"])
                if quantity > current_stock:
                    st.error(
                        f"Insufficient stock! Available: {current_stock:.3f} {selected_unit}. "
                        f"You tried to issue: {quantity:.3f} {selected_unit}"
                    )
                    st.stop()

            # Transaction payload তৈরি
            execution_time = datetime.now().isoformat()
            tx_payload = {
                "product_id": target_product["id"],
                "item_code": target_product["item_code"],
                "serial_number": serial_number.strip(),
                "quantity": quantity,
                "unit": selected_unit,
                "issued_to": issued_to.strip(),
                "invoice_no": invoice_no.strip(),
                "action_type": action_type,
                "created_at": execution_time
            }

            try:
                result = supabase.table("tpl_inv_transactions").insert(tx_payload).execute()
                if result.data:
                    st.success(
                        f"Transaction committed successfully!\n\n"
                        f"**{action_type}** — {quantity:.3f} {selected_unit} of **{selected_product_name}** "
                        f"({target_product['item_code']})\n"
                        f"Issued To: {issued_to.strip()} | Invoice: {invoice_no.strip()}\n"
                        f"Time: {execution_time}"
                    )
                    # Cache clear করে নতুন data load করা
                    load_data.clear()
                    st.rerun()
                else:
                    st.error("Insert returned no data. Check Supabase RLS policies.")
            except Exception as ex:
                st.error(f"Database insert failed: {ex}")

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- Recent Transactions Table ----
    st.markdown('<div class="section-head">🕐 Recent Transactions (Last 20)</div>', unsafe_allow_html=True)

    if not df_transactions.empty:
        # Product name যোগ করা
        df_recent = df_transactions.head(20).copy()
        df_recent = df_recent.merge(
            df_products[["id", "product_name"]].rename(columns={"id": "product_id"}),
            on="product_id",
            how="left"
        )

        # Display columns
        display_cols = ["created_at", "product_name", "item_code", "quantity", "unit",
                        "issued_to", "invoice_no", "action_type"]
        existing_display = [c for c in display_cols if c in df_recent.columns]
        df_display = df_recent[existing_display].copy()

        # Column rename for readability
        df_display = df_display.rename(columns={
            "created_at": "Date/Time",
            "product_name": "Product",
            "item_code": "Code",
            "quantity": "Qty",
            "unit": "Unit",
            "issued_to": "Issued To",
            "invoice_no": "Invoice",
            "action_type": "Action"
        })

        # Date format
        if "Date/Time" in df_display.columns:
            df_display["Date/Time"] = pd.to_datetime(df_display["Date/Time"], errors="coerce").dt.strftime("%d-%b-%Y %H:%M")

        st.dataframe(df_display, use_container_width=True, hide_index=True, height=420)
    else:
        st.info("No transactions recorded yet.")


# ==========================================
# 12. REPORTS PAGE (5-FILTER AUTO-FILTER)
# ==========================================
elif page == "Reports":
    st.header("📊 Advanced Analytics & Multi-Filter Reports")
    st.caption("Real-time auto-filtering with CSV export")

    if df_transactions.empty:
        st.info("No transaction data available. Add transactions first.")
        st.stop()

    # Product name merge
    df_report = df_transactions.copy()
    if not df_products.empty:
        df_report = df_report.merge(
            df_products[["id", "product_name"]].rename(columns={"id": "product_id"}),
            on="product_id",
            how="left"
        )

    # Date parse
    df_report["created_at"] = pd.to_datetime(df_report["created_at"], errors="coerce")
    df_report["_date_only"] = df_report["created_at"].dt.date

    # ---- Filter Options Prepare ----
    all_issued_to = sorted(df_report["issued_to"].dropna().unique().tolist()) if "issued_to" in df_report.columns else []
    all_items = sorted(df_products["product_name"].tolist()) if not df_products.empty else []
    all_invoices = sorted(df_report["invoice_no"].dropna().unique().tolist()) if "invoice_no" in df_report.columns else []

    min_date = df_report["_date_only"].min() if df_report["_date_only"].notna().any() else datetime.now().date()
    max_date = df_report["_date_only"].max() if df_report["_date_only"].notna().any() else datetime.now().date()

    # ---- Filter Bar ----
    st.markdown('<div class="section-head">🔍 Auto Filter Options</div>', unsafe_allow_html=True)

    f_col1, f_col2, f_col3, f_col4, f_col5 = st.columns(5)

    with f_col1:
        filter_date_from = st.date_input("Date From", value=min_date, key="rpt_from")
    with f_col2:
        filter_date_to = st.date_input("Date To", value=max_date, key="rpt_to")
    with f_col3:
        filter_issued_to = st.multiselect("Issued To", all_issued_to, key="rpt_issued")
    with f_col4:
        filter_item = st.multiselect("Item (Product)", all_items, key="rpt_item")
    with f_col5:
        filter_stock_type = st.multiselect(
            "Stock Type",
            ["ISSUE", "RETURN", "UPLOAD"],
            key="rpt_type"
        )

    # Invoice filter (আলাদা row-তে)
    f_inv_col, f_info_col = st.columns([3, 1])
    with f_inv_col:
        filter_invoice = st.multiselect("Invoice / DC No", all_invoices, key="rpt_invoice")
    with f_info_col:
        st.markdown("<br>", unsafe_allow_html=True)

    # ---- Apply Filters ----
    df_filtered = df_report.copy()

    if filter_date_from:
        df_filtered = df_filtered[df_filtered["_date_only"] >= filter_date_from]
    if filter_date_to:
        df_filtered = df_filtered[df_filtered["_date_only"] <= filter_date_to]
    if filter_issued_to:
        df_filtered = df_filtered[df_filtered["issued_to"].isin(filter_issued_to)]
    if filter_item:
        df_filtered = df_filtered[df_filtered["product_name"].isin(filter_item)]
    if filter_stock_type:
        df_filtered = df_filtered[df_filtered["action_type"].isin(filter_stock_type)]
    if filter_invoice:
        df_filtered = df_filtered[df_filtered["invoice_no"].isin(filter_invoice)]

    # Results info + download
    result_col1, result_col2 = st.columns([1, 1])
    with result_col1:
        st.markdown(
            f'Showing **<span style="color:#00E5A0;">{len(df_filtered)}</span>** records out of {len(df_report)} total',
            unsafe_allow_html=True
        )
    with result_col2:
        if not df_filtered.empty:
            st.download_button(
                label="📥 Export Filtered CSV",
                data=df_to_csv_bytes(df_filtered),
                file_name=f"filtered_report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                key="dl_filtered_report"
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- Results Table ----
    if not df_filtered.empty:
        display_cols = ["created_at", "product_name", "item_code", "serial_number",
                        "quantity", "unit", "issued_to", "invoice_no", "action_type"]
        existing_display = [c for c in display_cols if c in df_filtered.columns]
        df_show = df_filtered[existing_display].copy()

        df_show = df_show.rename(columns={
            "created_at": "Date/Time",
            "product_name": "Product",
            "item_code": "Code",
            "serial_number": "Serial",
            "quantity": "Qty",
            "unit": "Unit",
            "issued_to": "Issued To",
            "invoice_no": "Invoice",
            "action_type": "Action"
        })

        if "Date/Time" in df_show.columns:
            df_show["Date/Time"] = df_show["Date/Time"].dt.strftime("%d-%b-%Y %H:%M")

        st.dataframe(df_show, use_container_width=True, hide_index=True, height=480)
    else:
        st.warning("No records match the current filter combination. Try adjusting filters.")
